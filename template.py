"""Runs a callback in a tenant context inside a transaction, then clears context."""

from typing import Callable, TypeVar

from sqlalchemy.orm import Session, sessionmaker

from multi_tenant_postgres_sdk.context import TenantContext
from multi_tenant_postgres_sdk.router import MultiTenantRouter

T = TypeVar("T")


class TenantExecutionTemplate:
    """
    Sets tenant context, opens a Session for that tenant's Engine,
    runs the callback in a transaction, then closes the session and clears context.
    """

    def __init__(self, router: MultiTenantRouter) -> None:
        self._router = router

    def execute(self, tenant_id: str, work: Callable[[Session], T]) -> T:
        try:
            TenantContext.set_current_tenant(tenant_id)
            engine = self._router.get_engine()
            session_factory = sessionmaker(engine, autoflush=False, expire_on_commit=False)
            session = session_factory()
            try:
                with session.begin():
                    return work(session)
            finally:
                session.close()
        finally:
            TenantContext.clear()
