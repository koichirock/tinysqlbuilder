from .sql import Query


def create_or_replace_table_from_query(table: str, query: Query) -> str:
    """Create or replace table."""
    return f"CREATE OR REPLACE TABLE {table} AS {query.subquery()}"


def create_table_from_query(table: str, query: Query) -> str:
    """Create table."""
    return f"CREATE TABLE {table} AS {query.subquery()}"
