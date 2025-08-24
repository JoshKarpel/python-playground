from __future__ import annotations
from dataclasses import dataclass
from math import sin, cos, pi
from more_itertools import windowed
import matplotlib.pyplot as plt


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

    def __rmul__(self, scaler: float) -> Vector2D:
        return self * scaler

    def __truediv__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x / scalar, self.y / scalar)

    def rotate(self, theta: float) -> Vector2D:
        cos_theta = cos(theta)
        sin_theta = sin(theta)
        return Vector2D(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta,
        )

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


def points_to_arrays(points: list[Vector2D]) -> tuple[list[float], list[float]]:
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return xs, ys


ROOT_3_OVER_2 = (3**0.5) / 2


def expand_koch_segment(start: Vector2D, end: Vector2D) -> list[Vector2D]:
    direction = end - start
    midpoint = start + (direction / 2)
    segment = direction / 3

    one_third = start + segment
    two_third = start + (2 * segment)

    h = ROOT_3_OVER_2 * segment
    peak = midpoint + h.rotate(pi / 2)

    return [one_third, peak, two_third]


def koch_layer(points: list[Vector2D]) -> list[Vector2D]:
    new_points = []
    for start, end in windowed(points, 2):
        new_points.append(start)
        segment = expand_koch_segment(start, end)
        new_points.extend(segment)
    new_points.append(points[-1])
    return new_points

def draw(points: list[Vector2D], filename: str) -> None:
    fig, ax = plt.subplots(figsize=(20, 20))
    x, y = points_to_arrays(points)
    ax.plot(x, y)
    ax.set_aspect("equal", "box")
    ax.axis("off")
    plt.savefig(filename, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

def unit_polygon(sides: int) -> list[Vector2D]:
    angle_step = 2 * pi / sides
    points = [
        Vector2D(cos(i * angle_step), sin(i * angle_step))
        for i in range(sides)
    ]
    points.append(points[0])  # Close the polygon
    return points

def main():
    kochs = {
        "triangle": unit_polygon(3),
        "square": unit_polygon(4),
        "pentagon": unit_polygon(5),
        "hexagon": unit_polygon(6),
        "heptagon": unit_polygon(7),
        "octagon": unit_polygon(8),
    }

    for direction in ["normal", "reversed"]:
        for name, points in kochs.items():
            if direction == "reversed":
                points = list(reversed(points))

            print(f"Drawing {name} in {direction} direction")
            for idx in range(5):
                draw(points, f"koch-{name}-{direction}-{idx}.png")
                points = koch_layer(points)

    print("Done!")


if __name__ == "__main__":
    main()
