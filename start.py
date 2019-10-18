import pygame
import os
import random
import time

pygame.init()

display_width = 600
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('anime_pairs')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False

image_folder = os.path.join( os.path.abspath('.'), "img")
back_image = os.path.join( os.path.abspath('.'), "special_img", "back.jpg")
num = 6
card_number = num * num
card_type = card_number / 2

open_image_count = []
open_image_name = []
images = []
for file in os.listdir(image_folder):
    file_path = os.path.join(image_folder, file)
    images.append(file_path)

if len(images) > card_type:
  images = random.sample(images, card_type)
images = images * 2
random.shuffle(images)
cards = [back_image] * card_number

image_width = int(display_width / num)
image_height = int(display_height / num)


def set_card(): 
    global open_image_count
    global open_image_name
    x = display_width / num / 2
    y = display_height / num / 2
    i = 0
    for c in open_image_count:
        cards[c] = images[c]

    for img in cards:
        if img != "":            
            carImg = pygame.image.load(img)
            small_img = pygame.transform.scale(carImg,(image_width - 5, image_height - 5))
            gameDisplay.blit(small_img, (image_width * (i % num), image_height * int(i / num)))
        i = i + 1
        
    if len(open_image_count) == 2:
        if open_image_name[0] == open_image_name[1]:
            cards[open_image_count[0]] = ""
            cards[open_image_count[1]] = ""
        else:
            cards[open_image_count[0]] = back_image
            cards[open_image_count[1]] = back_image
        open_image_count = []
        open_image_name = []
        

x =  (display_width * 0.45)
y = (display_height * 0.8)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            if len(open_image_count) != 2:
                x, y = event.pos
                a = int(x / image_width)
                b = int(y / image_height)
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
