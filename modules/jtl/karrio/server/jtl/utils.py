"""
Utility functions for JTL Hub integration.
"""

import logging

logger = logging.getLogger(__name__)


def get_user_email(user_id: str, tenant_id: str) -> str:
    """
    Get user email from JTL Hub or generate placeholder.

    JTL Hub tokens don't include email in the JWT payload.
    Options:
    1. Fetch from JTL Hub API (if available) - TODO
    2. Use placeholder: {userId}@jtl.local

    Args:
        user_id: JTL Hub user ID (UUID)
        tenant_id: JTL Hub tenant ID (UUID)

    Returns:
        str: User email address
    """
    # TODO: Implement JTL Hub API call if user details endpoint is available
    # Example:
    # try:
    #     response = requests.get(
    #         f"{settings.JTL_HUB_API_BASE_URL}/users/{user_id}",
    #         headers={"X-Tenant-Id": tenant_id},
    #         timeout=5
    #     )
    #     if response.ok:
    #         user_data = response.json()
    #         return user_data.get('email', f'{user_id}@jtl.local')
    # except Exception as e:
    #     logger.warning(f"Failed to fetch email from JTL API: {e}")

    # For now, use placeholder email
    email = f'{user_id}@jtl.local'
    logger.debug(f"Generated placeholder email for user {user_id}: {email}")
    return email
