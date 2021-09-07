import pygame,sys
from pygame.locals import *
from tkinter import *
import time
import random
from pygame import mixer

root = Tk()
class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.x = 120
        self.y = 120

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move_random_place(self):
        self.x = random.randint(1, 19) * Size
        self.y = random.randint(1, 14) * Size

Size = 40
BACKGROUND_COLOR = (110, 110, 5)

class Snake:
    def __init__(self, screen, body):
        self.background = pygame.image.load("aw0e_19ni_180801.jpg").convert_alpha()
        self.body = body
        self.screen = screen
        self.block = pygame.image.load("Screenshot 2021-08-25 191911_35.png").convert_alpha()
        self.x = [Size] * body
        self.y = [Size] * body
        self.direction = 'right'

    def draw(self):
        # pygame.transform.scale(self.background, (600, 600))
        self.screen.blit(self.background, (0, 0))
        for i in range(self.body):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def increase_length(self):
        self.body += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move(self):
        for i in range(self.body-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == "left":
            self.x[0] -= Size
        if self.direction == "right":
            self.x[0] += Size
        if self.direction == "up":
            self.y[0] -= Size
        if self.direction == "down":
            self.y[0] += Size
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        icon = pygame.image.load("snake.png")
        pygame.display.set_icon(icon)
        # self.background = pygame.image.load("Grass_7.png")
        # pygame.transform.scale(self.background, (600, 600 ))
        pygame.display.set_caption("Snake Game (Work in progress)")
        # self.screen.blit(self.background, (0, 0))
        background_music = pygame.mixer.Sound("background_music.wav")
        pygame.mixer.Sound.play(background_music, (-1))
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont("Poetsen One", 50)
        score = font.render(f"Score: {self.snake.body}", True, (255, 255, 255))
        self.screen.blit(score, (20, 10))

    def reset(self):
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)

    def show_game_over(self):
        self.screen.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 40)
        text = font.render(f"Game over !"
                           f"  Your score is {self.snake.body}", True, (225, 225, 225))
        self.screen.blit(text, (190, 250))
        pygame.display.update()
        pygame.mixer.music.pause()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Size:
            if y1 >= y2 and y1 < y2 + Size:
                return True
            return False

    def play(self):
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # for i in range(self.snake.length):
        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            music = pygame.mixer.Sound("pause_sound.wav")
            pygame.mixer.Sound.play(music)
            self.snake.increase_length()
            self.apple.move_random_place()

        # snake colliding with itself
        for i in range(2, self.snake.body):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                music = pygame.mixer.Sound("crash.mp3")
                pygame.mixer.Sound.play(music)
                # pygame.mixer.music.pause()
                raise "collision occured"

        if not (0 <= self.snake.x[0] <= 790 and 0 <= self.snake.y[0] <= 590):
            music = pygame.mixer.Sound("crash.mp3")
            pygame.mixer.Sound.play(music)
            raise "Hit the boundry error"


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

game = Game()
game.run()


