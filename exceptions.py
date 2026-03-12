"""Exceptions raised when tenant context or registration is invalid."""


class NoTenantException(Exception):
    """Raised when tenant context is required but not set."""

    def __init__(self) -> None:
        super().__init__("Tenant not set!")


class TenantNotFoundException(Exception):
    """Raised when a requested tenant is not registered."""

    def __init__(self, tenant_id: str) -> None:
        super().__init__(f"Tenant '{tenant_id}' is not registered.")
