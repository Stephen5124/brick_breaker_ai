import pygame
import random
from ai import SimpleAI  # Import the AI

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize the font module

# Screen dimensions
WIDTH, HEIGHT = 800, 650  # Increased height by 50 pixels
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
ROWS, COLS = 5, 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, WIDTH - PADDLE_WIDTH))

# Ball class
class Ball:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

# Game class
class BrickBreaker:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 80)  # Adjusted paddle position
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 5, -5)
        self.bricks = [Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 30) for y in range(ROWS) for x in range(COLS)]
        self.ai = SimpleAI(self.paddle, self.ball)  # Initialize the AI
        self.paddle_hits = 0  # Counter for paddle hits
        self.font = pygame.font.SysFont('Arial', 24)  # Initialize font
        self.win_font = pygame.font.SysFont('Arial', 48)  # Font for win message
        self.game_won = False  # Flag to check if the game is won

        print("Initialized game components")

    def run(self):
        running = True
        print("Starting game loop")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Exiting game loop")

            if not self.game_won:
                self.ai.update()  # Update AI
                self.ball.move()

                # Check for collisions
                if self.ball.rect.colliderect(self.paddle.rect):
                    self.ball.dy = -self.ball.dy
                    self.paddle_hits += 1  # Increment paddle hits

                for brick in self.bricks[:]:
                    if self.ball.rect.colliderect(brick.rect):
                        self.bricks.remove(brick)
                        self.ball.dy = -self.ball.dy

                # Check if ball is lost
                if self.ball.rect.bottom >= HEIGHT - 50:  # Adjusted for new height
                    print("Game Over")
                    running = False

                # Check if all bricks are destroyed
                if not self.bricks:
                    self.game_won = True

            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, self.paddle.rect)
            pygame.draw.ellipse(self.screen, RED, self.ball.rect)
            for brick in self.bricks:
                pygame.draw.rect(self.screen, BLUE, brick.rect)

            # Render the paddle hits counter
            hits_text = self.font.render(f'Paddle Hits: {self.paddle_hits}', True, WHITE)
            self.screen.blit(hits_text, (10, HEIGHT - 40))  # Positioned at the bottom in the new space

            # Display win message if game is won
            if self.game_won:
                win_text = self.win_font.render("You Win!", True, GREEN)
                self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(60)

            # Simple win animation (flashing text)
            if self.game_won:
                pygame.time.wait(500)

        print("Game loop ended")

if __name__ == "__main__":
    game = BrickBreaker()
    game.run()
    pygame.quit()
    print("Pygame quit")
