# -*- coding: UTF-8 -*-
import pygame
import os
import random
import time

pygame.init()

# base settings
display_width = 800
display_height = 800
user_width = int(display_width / 4 / 2)
user_height = display_height / 2
title_width = display_width
title_height = 40
game_width = display_width - user_width * 2
game_height = display_height - title_height
num = 6
card_number = num * num
card_type = int(card_number / 2)
image_width = int(game_width / num)
image_height = int(game_height / num)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('anime_pairs')

black = (0,0,0)
white = (255,255,255)
blue = (72,118,255)

clock = pygame.time.Clock()
crashed = False

image_folder = os.path.join( os.path.abspath('.'), "img")
back_image = os.path.join( os.path.abspath('.'), "special_img", "back.jpg")

images = []
for file in os.listdir(image_folder):
    file_path = os.path.join(image_folder, file)
    images.append(file_path)


images = random.choices(images, k=card_type)
images = images * 2
random.shuffle(images)
cards = [back_image] * card_number

open_image_count = []
open_image_name = []
user_count = 2
user_name = ["玩家 1", "玩家 2"]
user_score = [0, 0]
user_flag = 0
current_user_num = 0

def set_card(): 
    global open_image_count
    global open_image_name
    global user_count
    global user_name
    global user_score
    global user_flag
    global current_user_num
    
    # add user
    text = pygame.font.Font("zk.ttf", 30)
    current_user = text.render("当前回合: " + user_name[current_user_num], 1, blue)

    gameDisplay.blit(current_user, (260, 10))
    user1 = text.render(user_name[0], 1, blue)
    user1_rect = user1.get_rect()
    user1_rect.center = (user_width / 2, user_height / 2)
    gameDisplay.blit(user1, user1_rect)
    user1_score = text.render(str(user_score[0]), 1, blue)
    user1_score_rect = user1_score.get_rect()
    user1_score_rect.center = (user_width / 2, user_height / 2 + 30)
    gameDisplay.blit(user1_score, user1_score_rect)
    user2 = text.render(user_name[1], 1, blue)
    user2_rect = user2.get_rect()
    user2_rect.center = (display_width - user_width / 2, user_height / 2)
    gameDisplay.blit(user2, user2_rect)
    user2_score = text.render(str(user_score[1]), 1, blue)
    user2_score_rect = user1_score.get_rect()
    user2_score_rect.center = (display_width - user_width / 2, user_height / 2 + 30)
    gameDisplay.blit(user2_score, user2_score_rect)


    # add images
    for c in open_image_count:
        cards[c] = images[c]

    site_flag = 0
    for img in cards:
        if img != "":            
            carImg = pygame.image.load(img)
            small_img = pygame.transform.scale(carImg,(image_width - 5, image_height - 5))
            gameDisplay.blit(small_img, (user_width + image_width * (site_flag % num), title_height + image_height * int(site_flag / num)))
        site_flag += 1
        
    if len(open_image_count) == 2:
        
        if open_image_name[0] == open_image_name[1]:
            user_score[current_user_num] += 1
            cards[open_image_count[0]] = ""
            cards[open_image_count[1]] = ""
        else:
            cards[open_image_count[0]] = back_image
            cards[open_image_count[1]] = back_image
        open_image_count = []
        open_image_name = []
        user_flag += 1
        current_user_num = user_flag % user_count

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            if len(open_image_count) != 2:
                x, y = event.pos
                a = int((x - user_width) / image_width)
                b = int((y - title_height) / image_height)
                count = num * b + a
                
                if cards[count] != "" and (not(len(open_image_count) == 1 and open_image_count[0] == count)):
                    open_image_name.append(images[count])
                    open_image_count.append(count)
          

    gameDisplay.fill(white)
    set_card()


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
