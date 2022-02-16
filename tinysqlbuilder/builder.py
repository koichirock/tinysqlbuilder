from typing import Union

from .sql import Condition, Query, full_outer_join, inner_join, left_outer_join, right_outer_join

all = ["Query", "QueryBuilder"]


class QueryBuilder:
    """Query builder."""

    def __init__(self, table: str) -> None:
        self._query = Query(table)

    def select(self, *columns: str) -> "QueryBuilder":
        """Select columns."""
        self._query.columns = list(columns)
        return self

    def where(self, condition: Union[str, Condition]) -> "QueryBuilder":
        """Add condition."""
        self._query.condition = condition
        return self

    def join(self, table: Union[str, Query], condition: Union[str, Condition]) -> "QueryBuilder":
        """Add join."""
        self._query.joins.append(inner_join(table, condition))
        return self

    def left_outer_join(
        self, table: Union[str, Query], condition: Union[str, Condition]
    ) -> "QueryBuilder":
        """Add left outer join."""
        self._query.joins.append(left_outer_join(table, condition))
        return self

    def right_outer_join(
        self, table: Union[str, Query], condition: Union[str, Condition]
    ) -> "QueryBuilder":
        """Add right outer join."""
        self._query.joins.append(right_outer_join(table, condition))
        return self

    def full_outer_join(
        self, table: Union[str, Query], condition: Union[str, Condition]
    ) -> "QueryBuilder":
        """Add full outer join."""
        self._query.joins.append(full_outer_join(table, condition))
        return self

    def subquery(self, alias: str) -> "QueryBuilder":
        """Build subquery."""
        self._query.alias = alias
        return self

    def build(self) -> Query:
        """Build query."""
        return self._query
