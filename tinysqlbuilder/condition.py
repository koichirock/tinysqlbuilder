from typing import List, TypeVar, Union

all = [
    "Condition",
    "build_condition",
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
        return " AND ".join(build_condition(condition, inner=True) for condition in self.condition)


class _OrCondition(Condition):
    """Add condition to the OR clause"""

    def __init__(self, *condition: Union[str, Condition]) -> None:
        self.condition = condition

    def build_condition(self) -> str:
        return " OR ".join(build_condition(condition, inner=True) for condition in self.condition)


class _NotCondition(Condition):
    """Add condition to the NOT clause"""

    def __init__(self, condition: Union[str, Condition]) -> None:
        self.condition = condition

    def build_condition(self) -> str:
        return f"NOT {build_condition(self.condition, inner=True)}"


def build_condition(condition: Union[str, Condition], inner: bool = False) -> str:
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
