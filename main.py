from __future__ import annotations
from dataclasses import dataclass


def main():
    print("Hello from python-playground!")


@dataclass(frozen=True, slots=True)
class Vector2D:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


if __name__ == "__main__":
    main()
