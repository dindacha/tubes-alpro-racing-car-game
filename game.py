
import sys
from tkinter import *

from button import Button
import pygame
import time 
import math
from utils import blit_text_center
from utils import blit_rotate_center
from utils import scale_image



pygame.font.init()

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface (TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface (FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.5)
WHITE_CAR = scale_image(pygame.image.load("imgs/white-car.png"), 0.5)
GREY_CAR = scale_image(pygame.image.load("imgs/grey-car.png"), 0.5)
GREEN_CAR = scale_image(pygame.image.load ("imgs/green-car.png"), 0.5)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.Font("assets/orangedays.ttf", 33)

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/orangedays.ttf", size)



FPS = 60
PATH = [(175, 141), (120, 72), (57, 131), (57, 409), (104, 513), (278, 696), (349, 726), (401, 656), 
(414, 539), (502, 476), (598, 570), (615, 712), (680, 734), (738, 679), (749, 444), (681, 368), (459, 357), (460, 262), 
(697, 256), (736, 123), (638, 72), (345, 75), (284, 173), (272, 356), (176, 380), (178, 260)]

class GameInfo :
    LEVELS = 2

    def __init__(self, level=1):
        self.level = level 
        self.started = False 
        self.level_start_time = 0

    def next_level (self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
    
    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time (self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

class AbstractCar : 
    IMG = RED_CAR

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 

    def rotate (self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right :
            self.angle -= self.rotation_vel

    def draw (self, win): 
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move (self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide (self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset (self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0 

class PlayerCarRed (AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration /2, 0)
        self.move()

    def bounce (self):
        self.vel = -self.vel
        self.move()

class PlayerCarWhite (AbstractCar):
    IMG = WHITE_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration /2, 0)
        self.move()

    def bounce (self):
        self.vel = -self.vel
        self.move()
    
class PlayerCarGrey (AbstractCar):
    IMG = GREY_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration /2, 0)
        self.move()

    def bounce (self):
        self.vel = -self.vel
        self.move()

class PlayerCarGreen (AbstractCar):
    IMG = GREEN_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration /2, 0)
        self.move()

    def bounce (self):
        self.vel = -self.vel
        self.move()

class ComputerCar (AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path= []):
        super().__init__(max_vel, rotation_vel)
        self.path = path 
        self.current_point = 0
        self.vel = max_vel
    
    def draw_points (self, win):
        for point in self.path :
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw (self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0 :
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y :
            desired_radian_angle += math.pi 

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180 :
            difference_in_angle -= 360 
        
        if difference_in_angle > 0 :
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else :
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point (self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len (self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level (self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1)*0.2
        self.current_point = 0 



def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height()-95))

    time_text = MAIN_FONT.render(
        f"Time : {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel : {round (player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    score = (round (player_car.vel, 1))*(game_info.level)+(game_info.get_level_time())
    score_text = MAIN_FONT.render(
        f"score : {score} xp", 1, (255, 255, 255))
    win.blit(score_text, (10, HEIGHT - vel_text.get_height() - 70))
    

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player (player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left = True)
    if keys[pygame.K_d]:
        player_car.rotate(right = True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved :
        player_car.reduce_speed()

def handle_collision (player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None :
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None :
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()


    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You won!")
        if player_finish_poi_collide [1] == 0:
            player_car.bounce()
        else : 
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)



run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0 )), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
player_carred =  PlayerCarRed(4,4)
player_carwhite = PlayerCarWhite(4,4)
player_cargrey = PlayerCarGrey(4,4)
player_cargreen = PlayerCarGreen(4,4)
computer_car = ComputerCar( 2, 4, PATH)
game_info = GameInfo()

def playred():
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        clock.tick(FPS)

        draw(WIN, images, player_carred, computer_car, game_info)

        PLAY_BACK = Button(image=None, pos=(70, 660), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Black")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        move_player(player_carred)
        computer_car.move()

        handle_collision(player_carred, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            game_info.reset()
            player_carred.reset()
            computer_car.reset()
            main_menudua()
            
            
        pygame.display.update()

def playwhite():
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        clock.tick(FPS)

        draw(WIN, images, player_carwhite, computer_car, game_info)

        PLAY_BACK = Button(image=None, pos=(70, 660), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Black")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        move_player(player_carwhite)
        computer_car.move()

        handle_collision(player_carwhite, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            game_info.reset()
            player_carwhite.reset()
            computer_car.reset()
            
            
        pygame.display.update()

def playgrey():
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        clock.tick(FPS)

        draw(WIN, images, player_cargrey, computer_car, game_info)

        PLAY_BACK = Button(image=None, pos=(70, 660), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Black")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        move_player(player_cargrey)
        computer_car.move()

        handle_collision(player_cargrey, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            game_info.reset()
            player_cargrey.reset()
            computer_car.reset()
            
            
        pygame.display.update()

def playgreen():
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        clock.tick(FPS)

        draw(WIN, images, player_cargreen, computer_car, game_info)

        PLAY_BACK = Button(image=None, pos=(70, 660), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Black")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        move_player(player_cargreen)
        computer_car.move()

        handle_collision(player_cargreen, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            game_info.reset()
            player_cargreen.reset()
            computer_car.reset()
            
            
        pygame.display.update()



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(90).render("CHOOSE CAR", True, "#F7F42D")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 170))

        RED_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 360), 
                            text_input="RED", font=get_font(60), base_color="#d7fcd4", hovering_color="Red")
        WHITE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 470), 
                            text_input="WHITE", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        GREY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 580), 
                            text_input="GREY", font=get_font(60), base_color="#d7fcd4", hovering_color="Grey")
        GREEN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 690), 
                            text_input="GREEN", font=get_font(60), base_color="#d7fcd4", hovering_color="Green")

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        for button in [RED_BUTTON, WHITE_BUTTON, GREY_BUTTON, GREEN_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RED_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    playred()
                if WHITE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    playwhite()
                if GREY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    playgrey()
                if GREEN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    playgreen()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(GRASS, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("RACING CAR", True, "#F7F42D")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 170))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 360), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 500), 
                            text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 660), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playred()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menudua():
    while True:
        SCREEN.blit(GRASS, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("You Won! Score : 108 xp", True, "#F7F42D")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 170))


        PLAY_BUTTON = Button(image=pygame.image.load("/Users/Dinda Chairunisa/Desktop/python/alpro copy/assets/Play Rect.png"), pos=(400, 360), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("/Users/Dinda Chairunisa/Desktop/python/alpro copy/assets/Play Rect.png"), pos=(400, 500), 
                            text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("/Users/Dinda Chairunisa/Desktop/python/alpro copy/assets/Quit Rect.png"), pos=(400, 660), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playred()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    