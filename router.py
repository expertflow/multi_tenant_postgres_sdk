"""Routing layer: selects the PostgreSQL Engine for the current tenant from thread-local context."""

from threading import Lock

from sqlalchemy import Engine, create_engine

from multi_tenant_postgres_sdk.context import TenantContext
from multi_tenant_postgres_sdk.exceptions import TenantNotFoundException


DEFAULT_KEY = "__default__"


def _normalize_postgres_url(url: str) -> str:
    """Ensure URL uses PostgreSQL driver. Accepts postgresql:// or postgres://."""
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    if not (url.startswith("postgresql://") or url.startswith("postgresql+psycopg2://")):
        raise ValueError("Only PostgreSQL URLs are supported (postgresql:// or postgres://).")
    return url


class MultiTenantRouter:
    """
    Holds one Engine per tenant plus a default Engine.
    get_engine() returns the Engine for the current tenant from TenantContext, or the default.
    """

    def __init__(self, default_engine: Engine) -> None:
        self._targets: dict[str, Engine] = {DEFAULT_KEY: default_engine}
        self._lock = Lock()

    def add_tenant(self, tenant_id: str, engine: Engine) -> None:
        with self._lock:
            self._targets[tenant_id] = engine

    def remove_tenant(self, tenant_id: str) -> None:
        with self._lock:
            self._targets.pop(tenant_id, None)

    def get_engine(self) -> Engine:
        tenant = TenantContext.get_current_tenant()
        key = tenant if tenant is not None else DEFAULT_KEY
        with self._lock:
            engine = self._targets.get(key)
        if engine is None:
            raise TenantNotFoundException(key)
        return engine
