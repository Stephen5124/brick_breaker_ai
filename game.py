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
                game.score += 10  # Increment score for breaking a brick

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
        self.level = 1  # Initialize level
        self.initialize_level()  # Initialize the first level
        self.ai = SimpleAI(self.paddle, self.ball)  # Initialize the AI
        self.paddle_hits = 0  # Counter for paddle hits
        self.font = pygame.font.SysFont('Arial', 24)  # Initialize font
        self.win_font = pygame.font.SysFont('Arial', 48)  # Font for win message
        self.game_won = False  # Flag to check if the game is won

        # Slider properties
        self.slider_rect = pygame.Rect(200, HEIGHT - 60, 400, 10)
        self.slider_handle_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y - 5, 10, 20)
        self.dragging = False

        # Lives
        self.lives = 3  # Number of lives

        # Score
        self.score = 0  # Player's score

        print("Initialized game components")

    def initialize_level(self):
        if self.level == 1:
            self.bricks = [Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 30) for y in range(ROWS) for x in range(COLS)]
            self.ball = Ball(WIDTH // 2, HEIGHT // 2, 5, -5)
        elif self.level == 2:
            self.bricks = []
            for y in range(ROWS + 1):
                for x in range(COLS + 1):
                    if (x + y) % 2 == 0:
                        self.bricks.append(Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 30))
            self.ball = Ball(WIDTH // 2, 100, 5, 5)
        elif self.level == 3:
            self.bricks = []
            for y in range(ROWS + 2):
                for x in range(COLS + 2):
                    if (x + y) % 3 != 0:
                        self.bricks.append(Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 30))
            self.ball = Ball(WIDTH // 2, HEIGHT // 2, -5, 5)
        self.ai = SimpleAI(self.paddle, self.ball)  # Reinitialize the AI for each level
        self.game_won = False

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

    def get_speed_display_value(self):
        slider_range = self.slider_rect.width
        handle_position = self.slider_handle_rect.x - self.slider_rect.x
        return int((handle_position / slider_range) * 9) + 1  # Speed value from 1 to 10

    def show_level_transition(self):
        self.screen.fill(BLACK)
        level_text = self.win_font.render(f"Level {self.level}", True, GREEN)
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - level_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds

    def show_win_screen(self):
        self.screen.fill(BLACK)
        win_text = self.win_font.render("Congratulations! You Win!", True, GREEN)
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds

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
                    self.lives -= 1  # Deduct a life
                    if self.lives <= 0:
                        print("Game Over")
                        running = False
                    else:
                        # Reset ball and paddle positions
                        self.ball.rect.x, self.ball.rect.y = WIDTH // 2, HEIGHT // 2
                        self.ball.dx, self.ball.dy = 5, -5
                        self.paddle.rect.x = WIDTH // 2 - PADDLE_WIDTH // 2

                # Check if all bricks are destroyed
                if not self.bricks:
                    self.game_won = True
                    if self.level == 3:
                        self.show_win_screen()
                        running = False
                    else:
                        self.level += 1
                        self.show_level_transition()
                        self.initialize_level()

            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, self.paddle.rect)
            pygame.draw.ellipse(self.screen, RED, self.ball.rect)
            for brick in self.bricks:
                pygame.draw.rect(self.screen, BLUE, brick.rect)

            # Render the paddle hits counter
            hits_text = self.font.render(f'Paddle Hits: {self.paddle_hits}', True, WHITE)
            self.screen.blit(hits_text, (10, HEIGHT - 40))  # Positioned at the bottom in the new space

            # Render the lives counter
            lives_text = self.font.render(f'Lives: {self.lives}', True, WHITE)
            self.screen.blit(lives_text, (WIDTH - 100, HEIGHT - 40))

            # Render the score counter
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT - 40))

            # Display win message if game is won
            if self.game_won and self.level < 3:
                win_text = self.win_font.render("You Win!", True, GREEN)
                self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

            # Draw the slider
            self.draw_slider()

            # Display the speed value
            speed_value = self.get_speed_display_value()
            speed_text = self.font.render(f'Speed: {speed_value}', True, WHITE)
            self.screen.blit(speed_text, (self.slider_rect.x, self.slider_rect.y + 20))

            pygame.display.flip()
            self.clock.tick(60)

            # Simple win animation (flashing text)
            if self.game_won and self.level < 3:
                pygame.time.wait(500)

        print("Game loop ended")

if __name__ == "__main__":
    game = BrickBreaker()
    game.run()
    pygame.quit()
    print("Pygame quit")
