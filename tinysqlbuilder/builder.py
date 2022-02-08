from typing import List, Optional, Tuple, Union

from tinysqlbuilder.sql import Condition, build_condition

all = ["Query", "QueryBuilder"]


class Query:
    """SQL Query."""

    def __init__(self, table: str):
        self.table = table
        self.columns: List[str] = []
        self.joins: List[Tuple[Union[str, "Query"], Union[str, Condition]]] = []
        self.condition: Optional[Union[str, Condition]] = None
        self.alias: Optional[str] = None

    def __str__(self) -> str:
        return self.to_sql()

    def to_sql(self) -> str:
        """Build query string."""
        query = f"SELECT {f', '.join(self.columns)}"
        query += f" FROM {self.table}"
        if self.joins:
            for join in self.joins:
                query += f" JOIN {join[0].subquery() if isinstance(join[0], Query) else join[0]}"
                query += f" ON {build_condition(join[1])}"
        if self.condition:
            query += f" WHERE {build_condition(self.condition)}"
        return query

    def subquery(self) -> str:
        """Build subquery string."""
        query = f"({self.to_sql()})"
        if self.alias:
            query += f" AS {self.alias}"
        return query


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

    def join(self, condition: Tuple[Union[str, Query], Union[str, Condition]]) -> "QueryBuilder":
        """Add join."""
        self._query.joins.append(condition)
        return self

    def subquery(self, alias: str) -> "QueryBuilder":
        """Build subquery."""
        self._query.alias = alias
        return self

    def build(self) -> Query:
        """Build query."""
        return self._query
