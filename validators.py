"""Validation utilities powered by compositional rule chains."""

from typing import TypeVar, Generic, Callable, Any, List, Union

T = TypeVar("T")


class Rule(Generic[T]):
    """A composable validation rule wrapping a predicate function.

    Supports logical composition via bitwise operators (&, |, ~).
    """

    def __init__(self, predicate: Callable[[T], bool], message: str) -> None:
        self._predicate = predicate
        self.message = message

    def validate(self, target: T) -> bool:
        """Evaluate if the target satisfies the encapsulated rule."""
        return bool(self._predicate(target))

    def __and__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules using a logical AND operator."""
        return Rule(
            lambda x: self.validate(x) and other.validate(x),
            f"({self.message} AND {other.message})",
        )

    def __or__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules using a logical OR operator."""
        return Rule(
            lambda x: self.validate(x) or other.validate(x),
            f"({self.message} OR {other.message})",
        )

    def __invert__(self) -> "Rule[T]":
        """Negate the validation rule using a logical NOT operator."""
        return Rule(
            lambda x: not self.validate(x),
            f"NOT ({self.message})",
        )


def evaluate(target: T, *rules: Rule[T]) -> List[str]:
    """Validate target against a sequence of rules, returning failure messages."""
    failures: List[str] = []
    for rule in rules:
        if not rule.validate(target):
            failures.append(f"Validation error: {rule.message}")
    return failures


# Common reusable rule definitions
is_str: Rule[Any] = Rule(lambda v: isinstance(v, str), "must be a string")
is_positive: Rule[Union[int, float]] = Rule(
    lambda v: isinstance(v, (int, float)) and v > 0, "must be a positive number"
)
non_empty: Rule[Any] = Rule(
    lambda v: hasattr(v, "__len__") and len(v) > 0, "must not be empty"
)
