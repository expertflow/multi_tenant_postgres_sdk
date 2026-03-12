"""Thread-local holder for the current tenant ID. Used by the router to pick the correct datasource."""

import threading

_tenant_local = threading.local()


class TenantContext:
    """Thread-local current tenant. Set before DB work, cleared after."""

    @staticmethod
    def set_current_tenant(tenant_id: str | None) -> None:
        _tenant_local.current_tenant = tenant_id

    @staticmethod
    def get_current_tenant() -> str | None:
        return getattr(_tenant_local, "current_tenant", None)

    @staticmethod
    def clear() -> None:
        _tenant_local.current_tenant = None
