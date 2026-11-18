import threading
import unittest
import karrio.lib as lib


def _within(seconds: float, fn, *args, **kwargs):
    """Run `fn` in a daemon thread; (finished, result)."""
    result = {}
    thread = threading.Thread(
        target=lambda: result.update(value=fn(*args, **kwargs)), daemon=True
    )
    thread.start()
    thread.join(seconds)
    return not thread.is_alive(), result.get("value")


class TestToSlug(unittest.TestCase):
    def test_an_empty_separator_returns(self):
        """Document templates can call lib.to_slug; an empty separator used to
        loop forever and hold a worker."""
        finished, value = _within(2, lib.to_slug, "Hello World", "a b", separator="")

        self.assertTrue(finished, "lib.to_slug(separator='') did not return")
        self.assertEqual(value, "helloworldab")

    def test_the_default_separator_is_unchanged(self):
        self.assertEqual(lib.to_slug("Hello  World!", "Foo-Bar"), "hello_world_foo_bar")
        self.assertEqual(lib.to_slug("a b", separator="-"), "a-b")


if __name__ == "__main__":
    unittest.main()
