# -*- coding: UTF-8 -*-
import pygame
import os
import random
import time

class Game:

    def __init__(self):
        self.current_open_image_number = []
        self.user_count = 2
        # to do: user info to class
        self.user_name = ["玩家 1", "玩家 2"]
        self.user_score = [0, 0]
        self.round_number = 0
        self.current_user_num = 0
        self.num = 6
        self.blue = (72,118,255)
        self.game_timeout = False
        
        self.game_window()
    
    def game_window(self):
        pygame.init()

        # base settings
        self.display_width = 800
        self.display_height = 800
        
        self.user_width = 100
        self.user_height = 400
        
        self.title_width = 800
        self.title_height = 40
        
        self.game_width = 600
        self.game_height = 760

        self.image_width = int(self.game_width / self.num)
        self.image_height = int(self.game_height / self.num)
        
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Anime Pairs')
        
        self.get_cards_info()
        self.run_game()
        
        pygame.quit()
        quit()
        
    def get_cards_info(self):     
        self.card_number = self.num * self.num
        card_type = int(self.card_number / 2)
        self.image_folder = os.path.join( os.path.abspath('.'), "img")
        self.back_image = os.path.join( os.path.abspath('.'), "special_img", "back.jpg")
        self.original_images = []
        for file in os.listdir(self.image_folder):
            file_path = os.path.join(self.image_folder, file)
            self.original_images.append(file_path)
        self.original_images = random.choices(self.original_images, k=card_type)
        self.original_images = self.original_images * 2
        random.shuffle(self.original_images)
        self.actuall_images = [self.back_image] * self.card_number
     
    def update_title(self):
        text = pygame.font.Font("zk.ttf", 30)
        self.current_user = text.render("当前回合: " + self.user_name[self.current_user_num], 1, self.blue)
        self.gameDisplay.blit(self.current_user, (150, 10))
        if self.count_down <= 0:
            self.count_down = 0
            self.game_timeout = True
        timer = text.render("时间: " + str(self.count_down) + "秒", 1, self.blue)
        self.gameDisplay.blit(timer, (450, 10))
        
    def update_game(self): 
        # add user
        text = pygame.font.Font("zk.ttf", 30)
        user1 = text.render(self.user_name[0], 1, self.blue)
        user1_rect = user1.get_rect()
        user1_rect.center = (self.user_width / 2, self.user_height / 2)
        self.gameDisplay.blit(user1, user1_rect)
        user1_score = text.render(str(self.user_score[0]), 1, self.blue)
        user1_score_rect = user1_score.get_rect()
        user1_score_rect.center = (self.user_width / 2, self.user_height / 2 + 30)
        self.gameDisplay.blit(user1_score, user1_score_rect)
        user2 = text.render(self.user_name[1], 1, self.blue)
        user2_rect = user2.get_rect()
        user2_rect.center = (self.display_width - self.user_width / 2, self.user_height / 2)
        self.gameDisplay.blit(user2, user2_rect)
        user2_score = text.render(str(self.user_score[1]), 1, self.blue)
        user2_score_rect = user1_score.get_rect()
        user2_score_rect.center = (self.display_width - self.user_width / 2, self.user_height / 2 + 30)
        self.gameDisplay.blit(user2_score, user2_score_rect)

        if self.game_timeout:
            if self.user_score[0] > self.user_score[1]:
                winner_text = (self.user_name[0] + "胜") 
            elif self.user_score[0] < self.user_score[1]:
                winner_text = (self.user_name[1] + "胜") 
            else:
                winner_text = "平局"
            winner_info = text.render(winner_text, 1, self.blue)
            winner_info_rect = winner_info.get_rect()
            winner_info_rect.center = (self.display_width / 2, display_height / 2)
            self.gameDisplay.blit(winner_info, winner_info_rect)
            
        else:
            # add self.original_images
            for c in self.current_open_image_number:
                self.actuall_images[c] = self.original_images[c]

            site_flag = 0
            for img in self.actuall_images:
                if img != "":            
                    carImg = pygame.image.load(img)
                    small_img = pygame.transform.scale(carImg,(self.image_width - 15, self.image_height - 15))
                    self.gameDisplay.blit(small_img, (self.user_width + self.image_width * (site_flag % self.num), self.title_height + self.image_height * int(site_flag / self.num)))
                
                text2 = pygame.font.Font("zk.ttf", 15)
                card_number = text2.render(str(site_flag), 1, self.blue)
                self.gameDisplay.blit(card_number, (self.user_width + self.image_width * (site_flag % self.num) + int(self.image_width / 2), self.title_height + self.image_height * (int(site_flag / self.num) + 1) - 15))
                site_flag += 1
                
            if len(self.current_open_image_number) == 2:
                
                if self.actuall_images[self.current_open_image_number[0]] == self.actuall_images[self.current_open_image_number[1]]:
                    self.user_score[self.current_user_num] += 1
                    self.actuall_images[self.current_open_image_number[0]] = ""
                    self.actuall_images[self.current_open_image_number[1]] = ""
                else:
                    self.actuall_images[self.current_open_image_number[0]] = self.back_image
                    self.actuall_images[self.current_open_image_number[1]] = self.back_image
                self.current_open_image_number = []
                self.round_number += 1
                self.current_user_num = self.round_number % self.user_count
        
        
    def run_game(self):

        clock = pygame.time.Clock()
        crashed = False
        while not crashed:
            self.count_down = 300 - int(pygame.time.get_ticks() / 1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos
                    if (not self.game_timeout) and len(self.current_open_image_number) != 2 and 100 < x < 700 and 40 < y < 800:                      
                        a = int((x - self.user_width) / self.image_width)
                        b = int((y - self.title_height) / self.image_height)
                        count = self.num * b + a
                        
                        if self.actuall_images[count] != "" and (not(len(self.current_open_image_number) == 1 and self.current_open_image_number[0] == count)):
                            self.current_open_image_number.append(count)
                  
            white = (255,255,255)
            self.gameDisplay.fill(white)
            self.update_title()
            self.update_game()

            pygame.display.update()
            clock.tick(60)
