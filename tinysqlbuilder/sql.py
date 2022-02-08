from typing import List, Optional, TypeVar, Union

all = [
    "Query",
    "Condition",
    "Join",
    "and_",
    "or_",
    "not_",
    "eq",
    "not_eq",
    "gt",
    "lt",
    "ge",
    "le",
    "between",
    "like",
    "in_",
    "inner_join",
    "left_outer_join",
    "right_outer_join",
    "full_outer_join",
]


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


def and_(*conditions: Union[str, Condition]) -> Condition:
    """Add condition to the AND clause"""
    return _AndCondition(*conditions)


def or_(*conditions: Union[str, Condition]) -> Condition:
    """Add condition to the OR clause"""
    return _OrCondition(*conditions)


def not_(condition: Union[str, Condition]) -> Condition:
    """Add condition to the NOT clause"""
    return _NotCondition(condition)


OpT = TypeVar("OpT")


def eq(column: str, value: OpT) -> str:
    """Equal"""
    return f"{column} = {value}"


def not_eq(column: str, value: OpT) -> str:
    """Not equal"""
    return f"{column} != {value}"


def gt(column: str, value: OpT) -> str:
    """Greater than"""
    return f"{column} > {value}"


def lt(column: str, value: OpT) -> str:
    """Less than"""
    return f"{column} < {value}"


def ge(column: str, value: OpT) -> str:
    """Greater or equal"""
    return f"{column} >= {value}"


def le(column: str, value: OpT) -> str:
    """Less or equal"""
    return f"{column} <= {value}"


def between(column: str, value1: OpT, value2: OpT) -> str:
    """Between"""
    return f"{column} BETWEEN {value1} AND {value2}"


def like(column: str, value: OpT) -> str:
    """Like"""
    return f"{column} LIKE '{value}'"


def in_(column: str, values: List[OpT]) -> str:
    """In"""
    return f"{column} IN ({', '.join(map(lambda v: str(v), values))})"


class Join:
    """Join interface"""

    def build_join(self) -> str:
        pass


class _InnerJoin(Join):
    """Add join to the INNER clause"""

    def __init__(self, table: Union[str, "Query"], condition: Union[str, Condition]) -> None:
        self.table = table
        self.condition = condition

    def build_join(self) -> str:
        return f" JOIN {_build_joined_table(self.table)} ON {_build_condition(self.condition)}"


class _LeftOuterJoin(Join):
    """Add join to the LEFT OUTER clause"""

    def __init__(self, table: Union[str, "Query"], condition: Union[str, Condition]) -> None:
        self.table = table
        self.condition = condition

    def build_join(self) -> str:
        return f" LEFT OUTER JOIN {_build_joined_table(self.table)} ON {_build_condition(self.condition)}"


class _RightOuterJoin(Join):
    """Add join to the RIGHT OUTER clause"""

    def __init__(self, table: Union[str, "Query"], condition: Union[str, Condition]) -> None:
        self.table = table
        self.condition = condition

    def build_join(self) -> str:
        return f" RIGHT OUTER JOIN {_build_joined_table(self.table)} ON {_build_condition(self.condition)}"


class _FullOuterJoin(Join):
    """Add join to the FULL OUTER clause"""

    def __init__(self, table: Union[str, "Query"], condition: Union[str, Condition]) -> None:
        self.table = table
        self.condition = condition

    def build_join(self) -> str:
        return f" FULL OUTER JOIN {_build_joined_table(self.table)} ON {_build_condition(self.condition)}"


def inner_join(table: Union[str, "Query"], condition: Union[str, Condition]) -> Join:
    """Add join to the INNER clause"""
    return _InnerJoin(table, condition)


def left_outer_join(table: Union[str, "Query"], condition: Union[str, Condition]) -> Join:
    """Add join to the LEFT OUTER clause"""
    return _LeftOuterJoin(table, condition)


def right_outer_join(table: Union[str, "Query"], condition: Union[str, Condition]) -> Join:
    """Add join to the RIGHT OUTER clause"""
    return _RightOuterJoin(table, condition)


def full_outer_join(table: Union[str, "Query"], condition: Union[str, Condition]) -> Join:
    """Add join to the FULL OUTER clause"""
    return _FullOuterJoin(table, condition)


def _build_joined_table(table: Union[str, "Query"]) -> str:
    """Build joined table"""
    if isinstance(table, str):
        return table
    return table.subquery()


class Query:
    """SQL Query."""

    def __init__(self, table: str):
        self.table = table
        self.columns: List[str] = []
        self.joins: List[Join] = []
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
                query += join.build_join()
        if self.condition:
            query += f" WHERE {_build_condition(self.condition)}"
        return query

    def subquery(self) -> str:
        """Build subquery string."""
        query = f"({self.to_sql()})"
        if self.alias:
            query += f" AS {self.alias}"
        return query


def union(*queries: Query) -> str:
    """Build UNION query."""
    return " UNION ".join(query.to_sql() for query in queries)


def union_all(*queries: Query) -> str:
    """Build UNION ALL query."""
    return " UNION ALL ".join(query.to_sql() for query in queries)
