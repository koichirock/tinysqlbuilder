from typing import List, Optional, Tuple, Union

all = ["Operator", "and_", "or_", "not_", "Query", "QueryBuilder"]


class Condition:
    """Condition interface"""

    def build_condition(self) -> str:
        pass


class _AndCondition(Condition):
    """Add condition to the AND clause"""

    def __init__(self, *condition: Union[str, Condition]) -> None:
        self.condition = condition

    def build_condition(self) -> str:
        return " AND ".join(_build_condition(condition, inner=True) for condition in self.condition)


class _OrCondition(Condition):
    """Add condition to the OR clause"""

    def __init__(self, *condition: Union[str, Condition]) -> None:
        self.condition = condition

    def build_condition(self) -> str:
        return " OR ".join(_build_condition(condition, inner=True) for condition in self.condition)


class _NotCondition(Condition):
    """Add condition to the NOT clause"""

    def __init__(self, condition: Union[str, Condition]) -> None:
        self.condition = condition

    def build_condition(self) -> str:
        return f"NOT {_build_condition(self.condition, inner=True)}"


def _build_condition(condition: Union[str, Condition], inner: bool = False) -> str:
    """Build a operator"""
    if isinstance(condition, str):
        return condition
    return f"({condition.build_condition()})" if inner else condition.build_condition()


def and_(*conditions: Union[str, Condition]) -> _AndCondition:
    """Add condition to the AND clause"""
    return _AndCondition(*conditions)


def or_(*conditions: Union[str, Condition]) -> _OrCondition:
    """Add condition to the OR clause"""
    return _OrCondition(*conditions)


def not_(condition: Union[str, Condition]) -> _NotCondition:
    """Add condition to the NOT clause"""
    return _NotCondition(condition)


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
                query += f" ON {_build_condition(join[1])}"
        if self.condition:
            query += f" WHERE {_build_condition(self.condition)}"
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
