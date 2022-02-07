from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


class _Criteria:
    """Criteria interface"""

    def build_criteria(self) -> str:
        pass


class _AndCriteria(_Criteria):
    """Add criteria to the AND clause"""

    def __init__(self, *criteria: Union[str, _Criteria]) -> None:
        self.criteria = criteria

    def build_criteria(self) -> str:
        return " AND ".join(build_criteria(criteria) for criteria in self.criteria)


class _OrCriteria(_Criteria):
    """Add criteria to the OR clause"""

    def __init__(self, *criteria: Union[str, _Criteria]) -> None:
        self.criteria = criteria

    def build_criteria(self) -> str:
        return " OR ".join(build_criteria(criteria) for criteria in self.criteria)


class _NotCriteria(_Criteria):
    """Add criteria to the NOT clause"""

    def __init__(self, criteria: Union[str, _Criteria]) -> None:
        self.criteria = criteria

    def build_criteria(self) -> str:
        return f"NOT {build_criteria(self.criteria)}"


def build_criteria(criteria: Union[str, _Criteria]) -> str:
    """Build a criteria"""
    if isinstance(criteria, str):
        return criteria
    return f"({criteria.build_criteria()})"


def and_(*criteria: Union[str, _Criteria]) -> _AndCriteria:
    """Add criteria to the AND clause"""
    return _AndCriteria(*criteria)


def or_(*criteria: Union[str, _Criteria]) -> _OrCriteria:
    """Add criteria to the OR clause"""
    return _OrCriteria(*criteria)


def not_(criteria: Union[str, _Criteria]) -> _NotCriteria:
    """Add criteria to the NOT clause"""
    return _NotCriteria(criteria)


@dataclass(frozen=True)
class Query:
    """SQL Query."""

    table: str
    columns: List[str]
    joins: List[Tuple[Union[str, "Query"], str]]
    criteria: Optional[Union[str, _Criteria]] = None
    alias: Optional[str] = None

    def __str__(self) -> str:
        return self.build()

    def build(self) -> str:
        """Build query string."""
        query = f"SELECT {f', '.join(self.columns)}"
        query += f" FROM {self.table}"
        if self.joins:
            for join in self.joins:
                query += f" JOIN {join[0].subquery() if isinstance(join[0], Query) else join[0]}"
                query += f" ON {join[1]}"
        if self.criteria:
            query += f" WHERE {self.criteria.build_criteria() if isinstance(self.criteria, _Criteria) else self.criteria}"
        return query

    def subquery(self) -> str:
        """Build subquery string."""
        query = f"({self.build()})"
        if self.alias:
            query += f" AS {self.alias}"
        return query


class QueryBuilder:
    """Query builder."""

    def __init__(self, table: str) -> None:
        self.table = table
        self.columns: List[str] = []
        self.joins: List[Tuple[Union[str, Query], str]] = []
        self.criteria: Optional[Union[str, _Criteria]] = None
        self.alias: Optional[str] = None

    def select(self, *columns: str) -> "QueryBuilder":
        """Select columns."""
        self.columns = list(columns)
        return self

    def where(self, criteria: Union[str, _Criteria]) -> "QueryBuilder":
        """Add criteria."""
        self.criteria = criteria
        return self

    def join(self, condition: Tuple[Union[str, Query], str]) -> "QueryBuilder":
        """Add join."""
        self.joins.append(condition)
        return self

    def subquery(self, alias: str) -> "QueryBuilder":
        """Build subquery."""
        self.alias = alias
        return self

    def build(self) -> Query:
        """Build query."""
        return Query(self.table, self.columns, self.joins, self.criteria, self.alias)
