import pygame

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 165, 0)  # Orange
HOOP_COLOR = (255, 0, 0)     # Red

BALL_RADIUS = 15
HOOP_WIDTH = 10
HOOP_HEIGHT = 100
HOOP_X = WIDTH - 100
HOOP_Y = HEIGHT // 2 - HOOP_HEIGHT // 2


class BasketballGame:
    """Simple wireframe for a ball and hoop simulation using pygame."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Basketball Simulation")
        self.clock = pygame.time.Clock()
        self.ball_pos = [100, HEIGHT // 2]

    def draw_ball(self):
        pygame.draw.circle(self.screen, BALL_COLOR, self.ball_pos, BALL_RADIUS)

    def draw_hoop(self):
        # Represent hoop as a vertical rectangle for now
        pygame.draw.rect(
            self.screen,
            HOOP_COLOR,
            pygame.Rect(HOOP_X, HOOP_Y, HOOP_WIDTH, HOOP_HEIGHT),
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)
            self.draw_ball()
            self.draw_hoop()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = BasketballGame()
    game.run()
