"""Public API: register or unregister a PostgreSQL datasource (Engine) per tenant."""

from sqlalchemy import Engine, create_engine

from multi_tenant_postgres_sdk.router import MultiTenantRouter, _normalize_postgres_url


class TenantRegistry:
    """
    Register tenant datasources with the router.
    Accepts either a PostgreSQL URL (str) or an existing SQLAlchemy Engine.
    """

    def __init__(self, router: MultiTenantRouter) -> None:
        self._router = router

    def add_datasource(self, tenant_id: str, url_or_engine: str | Engine) -> None:
        if isinstance(url_or_engine, Engine):
            self._router.add_tenant(tenant_id, url_or_engine)
        else:
            url = _normalize_postgres_url(url_or_engine)
            engine = create_engine(url, pool_pre_ping=True)
            self._router.add_tenant(tenant_id, engine)

    def remove_datasource(self, tenant_id: str) -> None:
        self._router.remove_tenant(tenant_id)
