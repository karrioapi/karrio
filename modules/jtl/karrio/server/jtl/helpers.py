"""
JTL Onboarding Helper Functions

Provides reusable business logic for tenant onboarding operations.
"""

import logging
import typing
from django.db import transaction

logger = logging.getLogger(__name__)


def generate_full_name_from_email(email: str) -> str:
    """
    Generate a user-friendly full name from email address.

    Args:
        email: User email address

    Returns:
        str: Capitalized full name (e.g., "john.doe@example.com" → "John Doe")
    """
    username = email.split('@')[0]
    return username.replace('.', ' ').replace('_', ' ').title()


def generate_org_name_from_email(email: str) -> str:
    """
    Generate organization name from email domain.

    Args:
        email: User email address

    Returns:
        str: Organization name (e.g., "user@example.com" → "Example")
    """
    domain = email.split('@')[1] if '@' in email else 'organization'
    return domain.split('.')[0].title()


def get_or_create_user(email: str, password: str) -> typing.Tuple[typing.Any, bool]:
    """
    Get or create a user by email with password.

    Args:
        email: User email address
        password: User password

    Returns:
        Tuple[User, bool]: (User instance, created flag)
    """
    from karrio.server.user.models import User

    default_full_name = generate_full_name_from_email(email)

    user, user_created = User.objects.get_or_create(
        email=email,
        defaults={
            'is_active': True,
            'full_name': default_full_name,
        }
    )

    # Always update password for security
    user.set_password(password)
    user.save(update_fields=['password'])

    action = "Created" if user_created else "Updated password for"
    logger.info(f"{action} user: {email}")

    return user, user_created


def get_organization_by_tenant_id(tenant_id: str) -> typing.Optional[typing.Any]:
    """
    Retrieve organization by JTL tenantId in metadata.

    Args:
        tenant_id: JTL tenant UUID

    Returns:
        Organization instance or None
    """
    from karrio.server.orgs.models import Organization

    return Organization.objects.filter(
        metadata__tenantId=tenant_id
    ).first()


def get_user_organization(user) -> typing.Optional[typing.Any]:
    """
    Get the first organization associated with a user.

    Args:
        user: User instance

    Returns:
        Organization instance or None
    """
    from karrio.server.orgs.models import Organization

    return Organization.objects.filter(users__id=user.id).first()


def update_organization_metadata(org, tenant_id: str, email: str) -> None:
    """
    Update organization with tenantId and friendly name/slug.

    Args:
        org: Organization instance
        tenant_id: JTL tenant UUID
        email: User email for generating name
    """
    org.metadata['tenantId'] = tenant_id

    org_name = generate_org_name_from_email(email)
    org.name = f'{org_name} Organization'
    org.slug = f'{org_name.lower()}-{tenant_id[:8]}'

    org.save(update_fields=['metadata', 'name', 'slug'])

    logger.info(f"Updated existing organization {org.id} with tenantId: {tenant_id}")


def create_organization(tenant_id: str, email: str) -> typing.Any:
    """
    Create a new organization with tenantId in metadata.

    Args:
        tenant_id: JTL tenant UUID
        email: User email for generating org name

    Returns:
        Organization instance
    """
    from karrio.server.orgs.models import Organization

    org_name = generate_org_name_from_email(email)

    org = Organization.objects.create(
        name=f'{org_name} Organization',
        slug=f'{org_name.lower()}-{tenant_id[:8]}',
        is_active=True,
        metadata={'tenantId': tenant_id}
    )

    logger.info(f"Created new organization for tenantId: {tenant_id}")

    return org


def get_or_create_organization_for_tenant(
    tenant_id: str,
    user,
    email: str
) -> typing.Tuple[typing.Any, bool]:
    """
    Get or create organization for JTL tenant, reusing existing user org if available.

    Flow:
    1. Check if organization with tenantId exists
    2. If not, check if user has an existing organization
    3. If user has org, update it with tenantId
    4. Otherwise, create a new organization

    Args:
        tenant_id: JTL tenant UUID
        user: User instance
        email: User email for generating org name

    Returns:
        Tuple[Organization, bool]: (Organization instance, is_new flag)
    """
    # Check if organization with tenantId already exists
    org = get_organization_by_tenant_id(tenant_id)

    if org:
        return org, False

    # Check if user already has an organization
    existing_org = get_user_organization(user)

    if existing_org:
        # Reuse existing organization and update with tenantId
        update_organization_metadata(existing_org, tenant_id, email)
        return existing_org, False

    # Create new organization
    org = create_organization(tenant_id, email)
    return org, True


def link_user_to_organization(
    org,
    user,
    user_id: str
) -> typing.Tuple[typing.Any, bool]:
    """
    Get or create organization user link with userId in metadata.

    Args:
        org: Organization instance
        user: User instance
        user_id: JTL user UUID

    Returns:
        Tuple[OrganizationUser, bool]: (OrganizationUser instance, created flag)
    """
    from karrio.server.orgs.models import OrganizationUser

    org_user = OrganizationUser.objects.filter(
        organization=org,
        user=user
    ).first()

    if org_user:
        # Update userId in metadata if changed
        if org_user.metadata.get('userId') != user_id:
            org_user.metadata['userId'] = user_id
            org_user.save(update_fields=['metadata'])
            logger.info(f"Updated userId for organization user: {user_id}")
        return org_user, False

    # Create new organization user link
    org_user = OrganizationUser.objects.create(
        organization=org,
        user=user,
        metadata={'userId': user_id}
    )

    logger.info(f"Linked user {user.email} to organization {org.id}")

    return org_user, True


def ensure_organization_ownership(org, org_user, org_is_new: bool) -> bool:
    """
    Ensure ownership is set for new organizations.

    Args:
        org: Organization instance
        org_user: OrganizationUser instance
        org_is_new: Whether the organization was just created

    Returns:
        bool: True if user is owner, False otherwise
    """
    from karrio.server.orgs.models import OrganizationOwner

    is_owner = OrganizationOwner.objects.filter(
        organization=org,
        organization_user=org_user
    ).exists()

    if not is_owner and org_is_new:
        # Make the first user the owner of a new organization
        OrganizationOwner.objects.create(
            organization=org,
            organization_user=org_user
        )
        is_owner = True
        logger.info(f"Set {org_user.user.email} as owner of organization {org.id}")

    return is_owner


@transaction.atomic
def onboard_jtl_tenant(
    tenant_id: str,
    user_id: str,
    email: str,
    password: str
) -> typing.Tuple[typing.Any, typing.Any, typing.Any, bool]:
    """
    Onboard JTL tenant with user, organization, and ownership setup.

    This is the main orchestration function that coordinates all onboarding steps.

    Flow:
    1. Check if tenant and user already exist - if so, short-circuit (no updates)
    2. Get or create user by email
    3. Get or create organization (reusing user's existing org if available)
    4. Link user to organization with userId metadata
    5. Ensure ownership is properly set

    Args:
        tenant_id: JTL tenant UUID
        user_id: JTL user UUID
        email: User email address
        password: User password

    Returns:
        Tuple[User, Organization, OrganizationUser, bool]:
            (user, org, org_user, is_owner)

    Raises:
        Exception: If onboarding fails at any step
    """
    from karrio.server.user.models import User
    from karrio.server.orgs.models import OrganizationUser, OrganizationOwner

    # Short-circuit: Check if tenant and user already exist
    org = get_organization_by_tenant_id(tenant_id)

    if org:
        user = User.objects.filter(email=email).first()

        if user:
            org_user = OrganizationUser.objects.filter(
                organization=org,
                user=user,
                metadata__userId=user_id
            ).first()

            if org_user:
                # Everything already exists - return without modifications
                is_owner = OrganizationOwner.objects.filter(
                    organization=org,
                    organization_user=org_user
                ).exists()

                logger.info(
                    f"Tenant {tenant_id} and user {email} already onboarded. "
                    f"Returning existing data without modifications."
                )

                return user, org, org_user, is_owner

    # Tenant/user doesn't exist or not linked - proceed with onboarding

    # Step 1: Get or create user
    user, _ = get_or_create_user(email, password)

    # Step 2: Get or create organization
    org, org_is_new = get_or_create_organization_for_tenant(
        tenant_id, user, email
    )

    # Step 3: Link user to organization
    org_user, _ = link_user_to_organization(org, user, user_id)

    # Step 4: Ensure ownership
    is_owner = ensure_organization_ownership(org, org_user, org_is_new)

    return user, org, org_user, is_owner
