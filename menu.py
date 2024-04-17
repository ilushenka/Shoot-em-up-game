import sys
from math import ceil
import pygame as pg
from constants import *
from sprite_utilities import player_one_features, \
                             player_two_features, \
                             mob_features, cursor_features
import menu_utilities as mu
from sprites import Player, Mob, Button, Cursor, all_sprites, mobs


class Game_process:
    def __init__(self, game_name='MyGame', width=WIDTH, height=HEIGHT, 
                 font_size=DEFAULT_FONT_SIZE):
        #Переменные, меняющиеся в процессе игры
        self.volume = 100
        
        self.is_new_game = True
        self.is_two_players = False
        self.is_new_wave = True
        self.wave_num = 0
        self.remain_mobs = 0
        
        self.score = 0
        self.scores_file = './high_scores.txt'
        self.new_record_str = None
        self.high_scores_is_open = False

        self.width = width
        self.height = height
        self.font_size = font_size
        self.font = pg.font.Font(None, self.font_size)
        self.buttons = mu.Buttons_placement(self.width, 
                                            self.height) 
        pg.display.set_caption(f"{game_name}")
        self.screen = pg.display.set_mode((self.width, self.height))

        self.cursor = Cursor(cursor_features['cursor_inactive'], 
                             cursor_features['cursor_active'],
                             cursor_features['cursor_click_sound'])
        self.dropdown = mu.DropDown([RED, LIGHT_RED], [RED, LIGHT_RED], 
                                    int(self.width*DROPDOWN_X_COEF), 
                                    int(self.height*DROPDOWN_Y_COEF), 
                                    int(DROPDOWN_WIDTH*self.width/WIDTH), 
                                    int(DROPDOWN_HEIGHT*self.height/HEIGHT), 
                                    self.font, 'screen resolution', 
                                    mu.screen_resolution.keys())
        self.slider = mu.Slider((SLIDER_X_COEF*self.width, 
                                 SLIDER_Y_COEF*self.height),
                                (int(SLIDER_WIDTH*self.width/WIDTH), 
                                 int(SLIDER_HEIGHT*self.height/HEIGHT)), 
                                pg.mixer.music.get_volume(), 0, 100, 
                                self.font)
        
        self.state = self.main_menu
        mu.check_music(main_menu=True)

    def main_menu(self):
        mu.set_background_image(self.screen, mu.menu_features['menu_background'], 
                             self.width, self.height)
        mu.print_text(self.screen, 'COSMO STAR', self.font, CREAM, 
                   self.width/2, self.height/4)        

        buttons = [self.buttons.dict['start'], self.buttons.dict['settings'],
                   self.buttons.dict['scores'], self.buttons.dict['quit']]
        
        for event in pg.event.get():
            mu.check_default_events(event, self.cursor, self.volume, buttons)
            if event.type == pg.USEREVENT:
                if event.button == self.buttons.dict['start']:
                    self.state = self.choose_player_num
                elif event.button == self.buttons.dict['quit']:
                    pg.quit()
                    sys.exit()
                elif event.button == self.buttons.dict['settings']:
                    self.state = self.settings_menu
                else:
                    self.state = self.scores_menu
        Button.list_check_hover(buttons, self.screen)
        self.cursor.update(self.screen)

    def settings_menu(self):
        self.controls_button_list = [self.buttons.dict['shoot_p1'], 
                                     self.buttons.dict['up_p1'], 
                                     self.buttons.dict['down_p1'], 
                                     self.buttons.dict['right_p1'], 
                                     self.buttons.dict['left_p1'], 
                                     self.buttons.dict['shoot_p2'], 
                                     self.buttons.dict['up_p2'], 
                                     self.buttons.dict['down_p2'], 
                                     self.buttons.dict['right_p2'], 
                                     self.buttons.dict['left_p2']]
        buttons = [self.buttons.dict['back'],
                    *self.controls_button_list]
        
        mu.set_background_image(self.screen, 
                             mu.menu_features['settings_background'], 
                             self.width, self.height)
        mu.print_text(self.screen, 'Player 1', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   - self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Player 2', self.font, CREAM, 
                   self.buttons.dict['shoot_p2'].x 
                   + self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p2'].y 
                   - self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Shoot', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + 3*self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   + self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Up', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + 3*self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   + 3*self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Down', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + 3*self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   + 5*self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Right', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + 3*self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   + 7*self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        mu.print_text(self.screen, 'Left', self.font, CREAM, 
                   self.buttons.dict['shoot_p1'].x 
                   + 3*self.width/(2*SCREEN_PART_FOR_SETTINGS_BUTTON), 
                   self.buttons.dict['shoot_p1'].y 
                   + 9*self.height/(2*SCREEN_PART_FOR_SETTINGS_BUTTON))
        events = pg.event.get()
        for event in events:
            mu.check_default_events(event, self.cursor, self.volume, buttons)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.state = self.main_menu            
            if event.type == pg.USEREVENT:
                if event.button == self.buttons.dict['back']:
                    self.state = self.main_menu
                else:
                    self.rewrite_button = event.button
                    self.rewrite = False
                    self.state = self.change_button

        self.volume = self.slider.check(self.screen)
        pg.mixer.music.set_volume(self.volume/100)

        selected_option = self.dropdown.update(events)
        self.dropdown.draw(self.screen)

        for key, value in mu.screen_resolution.items():
            if(key == selected_option 
               and (value[0] != self.width or value[1] != self.height)):
                self.font_size = int((value[0]*value[1])/ \
                                     (self.width*self.height)*self.font_size)
                self.font = pg.font.Font(None, self.font_size)
                self.width = value[0] 
                self.height = value[1]
                self.screen = pg.display.set_mode((self.width, self.height))

                self.buttons = mu.Buttons_placement(self.width, self.height, 
                                                    self.font_size)
                
                self.dropdown.font = self.font
                self.dropdown.rect.width \
                    = int(DROPDOWN_WIDTH*self.width/WIDTH) 
                self.dropdown.rect.height \
                    = int(DROPDOWN_HEIGHT*self.height/HEIGHT)
                self.dropdown.rect.center = (int(self.width*DROPDOWN_X_COEF), 
                                             int(self.height*DROPDOWN_Y_COEF))
                 
                self.slider \
                    = mu.Slider((self.width*SLIDER_X_COEF, 
                                 self.height*SLIDER_Y_COEF),
                                (int(SLIDER_WIDTH*self.width/WIDTH), 
                                 int(SLIDER_HEIGHT*self.height/HEIGHT)), 
                                pg.mixer.music.get_volume(), 
                                0, 100, self.font)
        Button.list_check_hover(buttons, self.screen)
        self.cursor.update(self.screen)

    def change_button(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['settings_background'], 
                             self.width, self.height)
        if not self.rewrite: 
            for event in pg.event.get():
                mu.check_default_events(event, self.cursor, self.volume)
                if event.type == pg.KEYDOWN:
                    self.rewrite_control_key = event.key
                    self.rewrite_control_str = event.unicode
                    for item in self.controls_button_list:
                        if item.control_button == event.key:
                            self.rewrite = True
                            self.rewrite_from = item
                            self.rewrite = True if \
                                item.control_button == event.key else False
                    if not self.rewrite:
                        self.rewrite_button.change_controls( \
                            self.rewrite_control_key, 
                            self.rewrite_control_str)
                        self.state = self.settings_menu
        else:
            buttons = [self.buttons.dict['Yes'], self.buttons.dict['No']]      
            for event in pg.event.get():
                mu.check_default_events(event, self.cursor, self.volume, buttons)
                if event.type == pg.USEREVENT:
                    if event.button == self.buttons.dict['quit']:
                        pg.quit()
                        sys.exit()
                    elif event.button == self.buttons.dict['Yes']:
                        self.rewrite_from.change_controls( \
                            self.rewrite_button.control_button,
                            self.rewrite_button.text)
                        self.rewrite_button.change_controls( \
                            self.rewrite_control_key, 
                            self.rewrite_control_str)
                        self.state = self.settings_menu
                        self.rewrite = False
                    elif event.button == self.buttons.dict['No']:
                        self.state = self.settings_menu
                        self.rewrite = False
            Button.list_check_hover(buttons, self.screen)
        self.cursor.update(self.screen)

    def scores_menu(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['settings_background'], 
                             self.width, self.height)
        
        if not self.high_scores_is_open:
            self.scores = mu.get_high_scores_data(self.scores_file)
            self.high_scores_is_open = True
        else:
            for item, i in zip(self.scores, range(10)):
                mu.print_text(self.screen, item[:-1], self.font, CREAM, 
                           self.width/2, 
                           self.height/4 \
                           + i*self.height/((2*SCREEN_PART_FOR_BUTTON)))
                
            buttons = [self.buttons.dict['back']]
        
            for event in pg.event.get():
                mu.check_default_events(event, self.cursor, self.volume, buttons)
                if event.type == pg.USEREVENT:
                    if event.button == self.buttons.dict['back']:
                        self.state = self.main_menu
                        self.high_scores_is_open = False
            Button.list_check_hover(buttons, self.screen)
            self.cursor.update(self.screen)

    def pause_menu(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['pause_background'], 
                             self.width, self.height)
        mu.print_text(self.screen, 'Pause', self.font, CREAM, WIDTH/2, HEIGHT/4)

        buttons = [self.buttons.dict['resume'], 
                   self.buttons.dict['main_menu']]

        for event in pg.event.get():
            mu.check_default_events(event, self.cursor, self.volume, buttons)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.state = self.start_the_game
                mu.check_music()
            if event.type == pg.USEREVENT:
                if event.button == self.buttons.dict['resume']:
                    self.state = self.start_the_game
                    mu.check_music()
                elif event.button == self.buttons.dict['main_menu']:
                    self.state = self.main_menu
                    mu.check_music(main_menu=True)
        
        Button.list_check_hover(buttons, self.screen)
        self.cursor.update(self.screen)

    def game_over(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['game_over_background'], 
                             self.width, self.height)

        mu.print_text(self.screen, 'GAME OVER', self.font, RED, 
                   self.width/2, self.height/5)
        mu.print_text(self.screen, f'Your score {self.score}', self.font, RED, 
                   self.width/2, self.height*4/15)
        if not self.high_scores_is_open:
            self.scores = mu.get_high_scores_data(self.scores_file)
            self.record_pos = -1
            for num,score in zip(range(10),
                                 list(self.scores[j].rsplit(' ', 1)[1] \
                                      for j in range(len(self.scores)-1))):
                if self.score > int(score):
                    self.record_pos = num
                    break
            if self.record_pos == -1 and len(self.scores) < 11:
                self.record_pos = len(self.scores) - 1

            self.textbox = mu.TextBox(self.width*TEXTBOX_X_COEF, 
                                      self.height*TEXTBOX_Y_COEF, 
                                      self.width/WIDTH*TEXTBOX_WIDTH, 
                                      self.height/HEIGHT*TEXTBOX_HEIGHT, 
                                      RED, LIGHT_RED, self.font, 'Nickname')        
            self.high_scores_is_open = True

        buttons = [self.buttons.dict['retry'], 
                   self.buttons.dict['quit_from_game_over']]

        mu.check_music(stop=True)

        for event in pg.event.get():
            mu.check_default_events(event, self.cursor, self.volume, buttons)
            if self.record_pos != -1 and not self.new_record_str:
                self.new_record_str = self.textbox.handle_event(event)
            if event.type == pg.USEREVENT:
                if event.button == self.buttons.dict['quit_from_game_over']:
                    self.state = self.main_menu
                elif event.button == self.buttons.dict['retry']:
                    self.state = self.start_the_game
                    self.is_new_game = True

        if self.record_pos != -1 and not self.new_record_str:
            mu.print_text(self.screen, 'You are in the top ten on the scorecard', 
                       self.font, RED, self.width/2, self.height/3)
            self.textbox.update()
            self.textbox.draw(self.screen)

        Button.list_check_hover(buttons, self.screen)  
        self.cursor.update(self.screen) 

        if self.state != self.game_over:
            if self.record_pos != -1:
                mu.set_high_scores_data(self.scores_file, self.score, 
                                     self.scores, self.record_pos, 
                                     self.new_record_str)
            self.new_record_str = None
            self.high_scores_is_open = False

    def choose_player_num(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['menu_background'], 
                             self.width, self.height)


        mu.print_text(self.screen, 'Choose game mode', self.font, CREAM, 
                   self.width/2, self.height/4)    

        buttons = [self.buttons.dict['1 player'], 
                   self.buttons.dict['2 players'], 
                   self.buttons.dict['back']]
        
        for event in pg.event.get():
            mu.check_default_events(event, self.cursor, self.volume, buttons)
            if event.type == pg.USEREVENT:
                if event.button == self.buttons.dict['1 player']:
                    self.is_new_game = True
                    self.is_two_players = False
                    self.state = self.start_the_game
                elif event.button == self.buttons.dict['2 players']:
                    self.is_new_game = True
                    self.is_two_players = True
                    self.state = self.start_the_game
                elif event.button == self.buttons.dict['back']:
                    self.state = self.main_menu
        
        Button.list_check_hover(buttons, self.screen)
        self.cursor.update(self.screen)

    def game_interface(self):
        mu.set_background_image(self.screen, 
                             mu.menu_features['menu_background'], 
                             self.width, self.height)
        mu.print_text(self.screen, f'Score:{self.score} Wave:{self.wave_num}', 
                   self.font, CREAM, self.width/8, self.height/7)
        
        all_sprites.draw(self.screen)

        player_one_health_image = pg.image.load(
            mu.health_bar[ceil(self.player_one.features.health \
                            /(DEFAULT_PLAYER_HEALTH/10))])
        player_one_health_image = \
            pg.transform.scale(player_one_health_image, 
                               tuple(i*j for i,j in zip( \
                                   player_one_health_image.get_size(), 
                                   (self.width/WIDTH, self.height/HEIGHT))))
        self.screen.blit(player_one_health_image, 
                         (self.width*HEALTH_BAR_COEF, 
                          self.height*HEALTH_BAR_COEF))
        if self.is_two_players:
            player_two_health_image = \
                  pg.transform.scale(pg.image.load(mu.health_bar[ceil( \
                      self.player_two.features.health \
                      /(DEFAULT_PLAYER_HEALTH/10))]), 
                      player_one_health_image.get_size())
            self.screen.blit(player_two_health_image, 
                             (self.width*(1-5*HEALTH_BAR_COEF), 
                              self.height*HEALTH_BAR_COEF))       

    def new_wave(self):
        if self.is_new_wave:
            self.is_new_wave = False
            self.wave_num += 1
            self.remain_mobs = self.wave_num*2

        mobs_num = self.remain_mobs \
            if self.remain_mobs < DEFAULT_MAX_MOB_NUM else DEFAULT_MAX_MOB_NUM
        
        Mob.spawnMobs(mobs_num, mob_features, self.width, 
                      self.height, self.volume)
        
        self.remain_mobs -= mobs_num
        self.is_new_wave = True \
            if self.remain_mobs == 0 and len(mobs) == 0 else self.is_new_wave

    def start_the_game(self):
        # Цикл игры
        if self.is_new_game:
            self.is_new_wave = True
            self.is_new_game = False
            self.wave_num = 0
            self.remain_mobs = 0
            self.score = 0
            mu.check_music(start_game=True)
            for sprite in all_sprites:
                sprite.kill()
            
            self.player_one = Player(player_one_features, self.width, 
                                     self.height, self.volume)
            if self.is_two_players:
                self.player_two = Player(player_two_features, self.width, 
                                         self.height, self.volume)
                self.player_two.rect.x = self.width/2 - 20 \
                                         + self.player_two.rect.width
                self.player_two.rect.y = self.height - 80
                self.player_one.rect.x = self.width/2 - 20 \
                                         - self.player_one.rect.width
                self.player_one.rect.y = self.height - 80
            else:
                self.player_one.rect.x = self.width/2 - 20
                self.player_one.rect.y = self.height - 80        
        self.new_wave()
        mobs_num = len(mobs)
        all_sprites.update()
        if mobs_num > len(mobs):
            self.score += (mobs_num - len(mobs))*DEFAULT_KILL_POINTS
        
        self.game_interface()

        for event in pg.event.get():
            mu.check_default_events(event, self.cursor, self.volume)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                mu.check_music(pause=True)
                self.state = self.pause_menu
        if(self.is_two_players and self.player_one.features.health == 0 \
           and self.player_two.features.health == 0) \
          or (not self.is_two_players \
              and self.player_one.features.health == 0):
            self.state = self.game_over
        self.cursor.update(self.screen, True)
