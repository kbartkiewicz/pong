import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60

pygame.font.init()
FONT_BIG = pygame.font.SysFont('', 100)
FONT_SMALL = pygame.font.SysFont('', 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCORE_TO_WIN = 10
MIDDLE_LINE_WIDTH = 4


class Paddle:
    VEL = 5
    WIDTH = 20
    HEIGHT = 80

    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points
        self.start_position_x = x
        self.start_position_y = y

    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def draw_score(self, window, position):
        score = FONT_BIG.render(f"{self.points}", True, WHITE)
        window.blit(score, position)

    def get_score_width(self):
        return FONT_BIG.render(f"{self.points}", True, WHITE).get_width()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def reset_position(self):
        self.x = self.start_position_x
        self.y = self.start_position_y


class Ball:
    WIDTH = 16
    HEIGHT = 16
    vel_x = 5
    vel_y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_position_x = x
        self.start_position_y = y

    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def move(self, paddle_left, paddle_right):
        self.x += self.vel_x
        self.y -= self.vel_y
        # bouncing the ball after hitting the bound
        if self.y < 0:
            self.vel_y = - self.vel_y
        elif self.y > HEIGHT - self.HEIGHT:
            self.vel_y = - self.vel_y
        # bouncing the ball after hitting the paddle
        if self.vel_x > 0:
            if self.get_rect().colliderect(paddle_right.get_rect()):
                self.vel_x = - self.vel_x
                self.vel_y = ((paddle_right.y + Paddle.HEIGHT / 2) - (self.y + Ball.HEIGHT / 2)) / 10
        else:
            if self.get_rect().colliderect(paddle_left.get_rect()):
                self.vel_x = - self.vel_x
                self.vel_y = ((paddle_left.y + Paddle.HEIGHT / 2) - (self.y + Ball.HEIGHT / 2)) / 10

    def reset_position(self):
        self.x = self.start_position_x
        self.y = self.start_position_y
        self.vel_y = 0


def game_finished_menu(window, position_x):
    win = FONT_BIG.render("WIN", True, WHITE)
    play_again = FONT_SMALL.render("(R) PLAY AGAIN", True, WHITE)
    exit_game = FONT_SMALL.render("(ESC) EXIT", True, WHITE)
    window.blit(win, (position_x - win.get_width() / 2, 100))
    window.blit(play_again, (position_x - play_again.get_width() / 2, 100 + win.get_height() + 50))
    window.blit(exit_game, (position_x - exit_game.get_width() / 2, 100 + win.get_height() + play_again.get_height() + 100))


def main():
    run = True
    game_finished = False
    clock = pygame.time.Clock()

    paddle_left = Paddle(20, HEIGHT / 2 - Paddle.HEIGHT / 2, 0)
    paddle_right = Paddle(WIDTH - Paddle.WIDTH - 20, HEIGHT / 2 - Paddle.HEIGHT / 2, 0)
    ball = Ball(WIDTH / 2 - Ball.WIDTH / 2, HEIGHT / 2)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and game_finished:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        if not game_finished:
            # moving the paddles on the screen
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_left.y > 0:
                paddle_left.y -= Paddle.VEL
            if keys[pygame.K_s] and paddle_left.y < HEIGHT - Paddle.HEIGHT:
                paddle_left.y += Paddle.VEL
            if keys[pygame.K_UP] and paddle_right.y > 0:
                paddle_right.y -= Paddle.VEL
            if keys[pygame.K_DOWN] and paddle_right.y < HEIGHT - Paddle.HEIGHT:
                paddle_right.y += Paddle.VEL

            # moving the ball
            ball.move(paddle_left, paddle_right)

            # updating the score, resetting the paddles and ball positions after getting a point
            if ball.x < 0 or ball.x > WIDTH:
                if ball.x < 0:
                    paddle_right.points += 1
                else:
                    paddle_left.points += 1
                ball.reset_position()
                paddle_left.reset_position()
                paddle_right.reset_position()

            if paddle_right.points == SCORE_TO_WIN or paddle_left.points == SCORE_TO_WIN:
                game_finished = True

            # drawing on the screen
            WIN.fill(BLACK)
            pygame.draw.line(WIN, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), MIDDLE_LINE_WIDTH)
            paddle_left.draw(WIN)
            paddle_right.draw(WIN)
            ball.draw(WIN)
            paddle_right.draw_score(WIN, (WIDTH / 2 + 24, 20))
            paddle_left.draw_score(WIN, (WIDTH / 2 - 24 - paddle_left.get_score_width(), 20))
        else:
            # drawing the menu after finishing match
            if paddle_left.points == SCORE_TO_WIN:
                game_finished_menu(WIN, WIDTH / 4)
            else:
                game_finished_menu(WIN, WIDTH / 4 + WIDTH / 2)

        pygame.display.update()


if __name__ == '__main__':
    main()
