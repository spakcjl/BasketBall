"""Run a demonstration of the magnetically assisted smart ball."""

from __future__ import annotations

import matplotlib.pyplot as plt

from smart_ball import Ball, Hoop, simulate


def main() -> None:
    # initial state
    initial_pos = (0.0, 2.0)
    initial_vel = (8.0, 8.0)

    # hoop definition
    hoop = Hoop(center=(5.0, 3.0), current=400.0)

    dt = 0.01
    t_max = 3.0

    # normal shot
    normal_ball = Ball(initial_pos, initial_vel, susceptibility=0.05)
    traj_normal, score_normal = simulate(normal_ball, hoop, dt, t_max, magnet=False)

    # magnet assisted
    magnet_ball = Ball(initial_pos, initial_vel, susceptibility=0.05)
    traj_magnet, score_magnet = simulate(magnet_ball, hoop, dt, t_max, magnet=True)

    # Plotting
    plt.plot(traj_normal[:, 0], traj_normal[:, 1], label="normal shot")
    plt.plot(traj_magnet[:, 0], traj_magnet[:, 1], label="magnet assisted")
    plt.scatter([hoop.center[0]], [hoop.center[1]], color="black", zorder=5)
    plt.legend()
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Smart ball trajectories")
    plt.ylim(0, 5)
    plt.grid(True)
    plt.show()

    print(f"Scored without magnet: {score_normal}")
    print(f"Scored with magnet: {score_magnet}")


if __name__ == "__main__":
    main()
