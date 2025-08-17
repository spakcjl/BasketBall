"""Basic physics engine for the magnetically assisted smart ball."""

from __future__ import annotations

import numpy as np

MU0 = 4e-7 * np.pi  # vacuum permeability


class Ball:
    """State of the basketball."""

    def __init__(
        self,
        position: tuple[float, float],
        velocity: tuple[float, float],
        radius: float = 0.12,
        mass: float = 0.62,
        susceptibility: float = 0.01,
    ) -> None:
        self.pos = np.array(position, dtype=float)
        self.vel = np.array(velocity, dtype=float)
        self.radius = radius
        self.mass = mass
        self.susceptibility = susceptibility
        self.volume = 4 / 3 * np.pi * radius ** 3


class Hoop:
    """Hoop with an electromagnetic coil."""

    def __init__(
        self,
        center: tuple[float, float],
        radius: float = 0.23,
        turns: int = 200,
        current: float = 0.0,
    ) -> None:
        self.center = np.array(center, dtype=float)
        self.radius = radius
        self.turns = turns
        self.current = current

    def magnetic_field(self, pos: np.ndarray) -> float:
        """Approximate magnetic field at a given position.

        Uses the on-axis field of a current loop with radius ``self.radius``.
        The distance ``r`` is measured from the centre of the hoop.
        """

        r = np.linalg.norm(pos - self.center)
        return MU0 * self.turns * self.current * self.radius ** 2 / (
            2 * (self.radius ** 2 + r ** 2) ** 1.5
        )

    def magnetic_force(self, ball: Ball) -> np.ndarray:
        """Return the magnetic force on ``ball``."""

        B = self.magnetic_field(ball.pos)
        magnitude = (B ** 2 * ball.volume * ball.susceptibility) / (2 * MU0)
        r_vec = self.center - ball.pos
        r = np.linalg.norm(r_vec)
        if r == 0:
            return np.zeros(2)
        return magnitude * r_vec / r

    def check_score(self, prev_pos: np.ndarray, curr_pos: np.ndarray, ball_radius: float) -> bool:
        """Check if the ball passed through the hoop between two positions."""

        if prev_pos[1] >= self.center[1] and curr_pos[1] < self.center[1]:
            if abs(curr_pos[0] - self.center[0]) < (self.radius - ball_radius):
                return True
        return False


def simulate(
    ball: Ball,
    hoop: Hoop,
    dt: float = 0.01,
    t_max: float = 5.0,
    magnet: bool = True,
):
    """Simulate ``ball`` in the presence of ``hoop``.

    Returns the trajectory (``N``\ x\ ``2`` array) and a boolean indicating
    whether the shot scored.
    """

    positions = [ball.pos.copy()]
    prev_pos = ball.pos.copy()
    scored = False
    steps = int(t_max / dt)
    for _ in range(steps):
        force = np.array([0.0, -9.81 * ball.mass])
        if magnet and hoop.current != 0:
            force += hoop.magnetic_force(ball)
        ball.vel += force / ball.mass * dt
        ball.pos += ball.vel * dt
        positions.append(ball.pos.copy())
        if hoop.check_score(prev_pos, ball.pos, ball.radius):
            scored = True
            break
        prev_pos = ball.pos.copy()
        if ball.pos[1] < -1.0:  # hit the ground
            break
    return np.array(positions), scored
