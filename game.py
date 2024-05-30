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
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

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

    def move(self, speed_multiplier):
        steps = int(max(abs(self.dx * speed_multiplier), abs(self.dy * speed_multiplier)))
        for _ in range(steps):
            self.rect.x += self.dx * speed_multiplier / steps
            self.rect.y += self.dy * speed_multiplier / steps

            # Bounce off walls
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.dx = -self.dx
            if self.rect.top <= 0:
                self.dy = -self.dy

    def update_position(self, paddle, bricks, game):
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy
            game.paddle_hits += 1  # Increment paddle hits counter

        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                bricks.remove(brick)
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

        # Slider properties
        self.slider_rect = pygame.Rect(200, HEIGHT - 40, 400, 10)
        self.slider_handle_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y - 5, 10, 20)
        self.dragging = False

        print("Initialized game components")

    def draw_slider(self):
        pygame.draw.rect(self.screen, GRAY, self.slider_rect)
        pygame.draw.rect(self.screen, DARK_GRAY, self.slider_handle_rect)

    def handle_slider_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = max(self.slider_rect.x, min(event.pos[0], self.slider_rect.right))
                self.slider_handle_rect.x = new_x

    def get_slider_value(self):
        slider_range = self.slider_rect.width
        handle_position = self.slider_handle_rect.x - self.slider_rect.x
        return 0.5 + (handle_position / slider_range) * 1.5  # Speed multiplier from 0.5x to 2.0x

    def run(self):
        running = True
        print("Starting game loop")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Exiting game loop")
                self.handle_slider_event(event)

            if not self.game_won:
                self.ai.update()  # Update AI
                speed_multiplier = self.get_slider_value()
                self.ball.move(speed_multiplier)  # Move ball with speed multiplier

                # Check for collisions
                self.ball.update_position(self.paddle, self.bricks, self)

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

            # Draw the slider
            self.draw_slider()

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
