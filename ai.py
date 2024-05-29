class SimpleAI:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

    def update(self):
        if self.ball.rect.centerx > self.paddle.rect.centerx:
            self.paddle.move(10)  # Move right
        elif self.ball.rect.centerx < self.paddle.rect.centerx:
            self.paddle.move(-10)  # Move left
