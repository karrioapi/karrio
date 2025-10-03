import typing
import threading
import datetime
import concurrent.futures as futures


class AbstractCache:
    def get(self, key: str):
        pass

    def set(self, key: str, value: typing.Any, **kwargs):
        pass


class Cache(AbstractCache):
    def __init__(self, cache: typing.Optional[AbstractCache] = None, **kwargs) -> None:
        self._cache = cache  # system cache
        self._values: typing.Dict[str, futures.Future] = {}  # shallow cache

        for key, value in kwargs.items():
            self.set(key, value)

    def get(self, key: str):
        _value = self._values.get(key)
        _cache_value = None if self._cache is None else self._cache.get(key)
        _result = None

        if _value is not None:
            _result = _value.result()

        if self._cache is not None and _cache_value is not None:
            _result = _cache_value

        # sync value in shallow cache if it only exist in the cache
        if _value is None and _cache_value is not None:
            self.set(key, _cache_value)

        # sync value in cache if it only exist shallow cache
        if _cache_value is None and _value is not None and self._cache is not None:
            self._cache.set(key, _cache_value)

        return _result

    def set(self, key: str, value: typing.Any, timeout: int = 86400, **kwargs):
        def _save():
            if isinstance(value, typing.Callable):
                return value()

            return value

        executor = futures.ThreadPoolExecutor(max_workers=1)
        promise = executor.submit(_save)
        self._values.update({key: promise})

        # set value in cache if it exist
        if self._cache is not None:
            promise.add_done_callback(
                lambda _: self._cache.set(key, _.result(), timeout=timeout)
            )

    def thread_safe(
        self,
        refresh_func: typing.Callable[[], dict],
        cache_key: str,
        buffer_minutes: int = 30,
        token_field: str = "access_token",
        expiry_field: str = "expiry",
        expiry_format: str = "%Y-%m-%d %H:%M:%S",
    ) -> "ThreadSafeTokenManager":
        """Create a thread-safe token manager for OAuth token management.

        This method provides a convenient way to create a ThreadSafeTokenManager
        that handles token refresh with thread safety and automatic expiry management.

        Args:
            refresh_func: Function to call when token needs refresh
            cache_key: Unique key for caching the token
            buffer_minutes: Minutes before expiry to consider token as expired
            token_field: Field name containing the token in cached data
            expiry_field: Field name containing the expiry timestamp
            expiry_format: Format string for parsing expiry timestamp

        Returns:
            ThreadSafeTokenManager instance configured with the provided parameters

        Example:
            token_manager = self.connection_cache.thread_safe(
                refresh_func=lambda: login(self),
                cache_key=f"{self.carrier_name}|{self.client_id}|{self.client_secret}",
                buffer_minutes=30
            )
            token = token_manager.get_token()
        """
        return ThreadSafeTokenManager(
            cache=self,
            refresh_func=refresh_func,
            cache_key=cache_key,
            buffer_minutes=buffer_minutes,
            token_field=token_field,
            expiry_field=expiry_field,
            expiry_format=expiry_format,
        )


class ThreadSafeTokenManager:
    """Thread-safe token manager that prevents race conditions during token refresh.

    This class provides a clean abstraction for managing OAuth tokens with automatic
    refresh capabilities. It ensures that only one thread can refresh a token at a time,
    preventing race conditions that can cause authentication failures.

    Supports multiple carriers with different token field names, expiry formats,
    and cache key patterns.

    Usage:
        # UPS example
        token_manager = ThreadSafeTokenManager(
            cache=connection_cache,
            refresh_func=lambda: login(self),
            cache_key=f"{self.carrier_name}|{self.client_id}|{self.client_secret}",
            buffer_minutes=30
        )

        # USPS example with different token field
        payment_token_manager = ThreadSafeTokenManager(
            cache=connection_cache,
            refresh_func=lambda: payment_auth(self),
            cache_key=f"payment|{self.carrier_name}|{self.client_id}|{self.client_secret}",
            buffer_minutes=45,
            token_field="paymentAuthorizationToken"
        )

        # FedEx example with different cache key pattern
        track_token_manager = ThreadSafeTokenManager(
            cache=connection_cache,
            refresh_func=lambda: login(self, client_id=self.track_api_key, client_secret=self.track_secret_key),
            cache_key=f"{self.carrier_name}|{self.track_api_key}|{self.track_secret_key}",
            buffer_minutes=30
        )

        token = token_manager.get_token()
    """

    def __init__(
        self,
        cache: AbstractCache,
        refresh_func: typing.Callable[[], dict],
        cache_key: str,
        buffer_minutes: int = 30,
        token_field: str = "access_token",
        expiry_field: str = "expiry",
        expiry_format: str = "%Y-%m-%d %H:%M:%S",
    ):
        """Initialize the thread-safe token manager.

        Args:
            cache: The cache instance to store tokens
            refresh_func: Function to call when token needs refresh
            cache_key: Unique key for caching the token
            buffer_minutes: Minutes before expiry to consider token as expired
            token_field: Field name containing the token in cached data
            expiry_field: Field name containing the expiry timestamp
            expiry_format: Format string for parsing expiry timestamp
        """
        self.cache = cache
        self.refresh_func = refresh_func
        self.cache_key = cache_key
        self.buffer_minutes = buffer_minutes
        self.token_field = token_field
        self.expiry_field = expiry_field
        self.expiry_format = expiry_format
        self._lock = threading.Lock()

    def get_token(self) -> str:
        """Get a valid token, refreshing if necessary.

        This method implements the double-check pattern to ensure thread safety:
        1. Check if token exists and is valid (no lock)
        2. If expired, acquire lock and check again
        3. If still expired, refresh token
        4. Return the token

        Returns:
            Valid access token string

        Raises:
            Exception: If token refresh fails
        """
        # First check without lock for performance
        token_data = self.cache.get(self.cache_key) or {}
        token = token_data.get(self.token_field)
        expiry = self._parse_expiry(token_data.get(self.expiry_field))

        if self._is_token_valid(token, expiry):
            return token

        # Token is expired or doesn't exist - need to refresh
        with self._lock:
            # Double-check pattern: another thread might have refreshed
            token_data = self.cache.get(self.cache_key) or {}
            token = token_data.get(self.token_field)
            expiry = self._parse_expiry(token_data.get(self.expiry_field))

            if self._is_token_valid(token, expiry):
                return token

            # Still need to refresh - this thread will do it
            try:
                new_token_data = self.refresh_func()
                self.cache.set(self.cache_key, new_token_data)

                new_token = new_token_data.get(self.token_field)
                if not new_token:
                    raise ValueError("Token refresh function returned no token")

                return new_token

            except Exception as e:
                raise Exception(f"Token refresh failed: {str(e)}")

    def get_state(self) -> str:
        """Get the current token state (valid token or refresh if needed).

        This is a convenience method that calls get_token() for a cleaner API.

        Returns:
            Valid access token string

        Raises:
            Exception: If token refresh fails
        """
        return self.get_token()

    def _is_token_valid(self, token: str, expiry: datetime.datetime) -> bool:
        """Check if token is valid and not expired.

        Args:
            token: The token string
            expiry: The expiry datetime

        Returns:
            True if token is valid and not expired
        """
        if not token or not expiry:
            return False

        buffer_time = datetime.datetime.now() + datetime.timedelta(
            minutes=self.buffer_minutes
        )
        return expiry > buffer_time

    def _parse_expiry(self, expiry_str: str) -> typing.Optional[datetime.datetime]:
        """Parse expiry string to datetime object.

        Args:
            expiry_str: Expiry timestamp string

        Returns:
            Parsed datetime object or None if parsing fails
        """
        if not expiry_str:
            return None

        try:
            return datetime.datetime.strptime(expiry_str, self.expiry_format)
        except (ValueError, TypeError):
            return None
