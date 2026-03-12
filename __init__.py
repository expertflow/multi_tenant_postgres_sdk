"""
Multi-tenant PostgreSQL SDK.

Dynamic tenant datasource registration and routing:
- TenantContext: thread-local current tenant
- TenantRegistry: add/remove PostgreSQL datasources per tenant
- TenantExecutionTemplate: run code in a tenant context with a transaction
"""

from multi_tenant_postgres_sdk.context import TenantContext
from multi_tenant_postgres_sdk.exceptions import (
    NoTenantException,
    TenantNotFoundException,
)
from multi_tenant_postgres_sdk.registry import TenantRegistry
from multi_tenant_postgres_sdk.router import MultiTenantRouter
from multi_tenant_postgres_sdk.template import TenantExecutionTemplate

__all__ = [
    "TenantContext",
    "TenantRegistry",
    "TenantExecutionTemplate",
    "MultiTenantRouter",
    "NoTenantException",
    "TenantNotFoundException",
]
__version__ = "1.0.0"
