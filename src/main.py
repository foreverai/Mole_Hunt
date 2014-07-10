'''
Added
-Added character selection functionality
-Added Times up popup
-Added preliminary graphics
-Added fonts

To Do 
-Fix how charselect is done
-Refactor code
-Organise changeable elements of game
-Start creating game graphics

Widget tree
-app
-game
    -gamebox
    -mole
    -databar
-startpopup
    -charselect
        -character1
        -selectbox
-timesup      
  
'''

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from random import randrange
from kivy.uix.popup import Popup

class TimesUp(Widget):
    app = ObjectProperty(None)
    
    'Change pop up size'
    width_factor = NumericProperty(0.5)
    height_factor = NumericProperty(0.3)    
    
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_center = NumericProperty(0)
    y_center = NumericProperty(0)
    
    def __init__(self, *args, **kwargs):
        super(TimesUp, self).__init__(*args, **kwargs)
        self.sizing()    #sizing has to be before positioning.  otherwise the center of widget is unknown
        self.position()
    
    def sizing(self):
        self.x_size = self.app.game.width * self.width_factor
        self.y_size = self.app.game.height * self.height_factor
        
    def position(self, *args):
        self.x_center = self.app.game.kvcenter_x 
        self.y_center = self.app.game.kvcenter_y 
        
class SelectBox(Widget):
    startpopup = ObjectProperty(None)   
    
    'Selectbox Image'
    img_selectbox = StringProperty('Images/selectbox.png')  

class CharSelect(Widget):
    startpopup = ObjectProperty(None)
    selectbox = ObjectProperty(None)
    character1 = ObjectProperty(None)
    
    character_lst = ListProperty([])
     
    def __init__(self, *args, **kwargs):
        super(CharSelect, self).__init__(*args, **kwargs)
        'Put selectable characters here, also add a character widget in kv file'
        self.character_lst.append('Images/mole.png') 
        self.character_lst.append('Images/bird.png') 
    
    def image_select(self, character):
        #To do with relativelayout
        #will it work for muore characters?
        if character.x < 0:
            x = 0
        else:    
            x = character.x - self.character1.x
            
        if  character.y < 0:
            y = 0
        else:
            y = character.y - self.character1.y  
            
        self.selectbox.pos = x, y
        self.startpopup.app.game.mole.current_char = character.source  

class StartPopUp(Popup):
    app = ObjectProperty(None)
    charselect = ObjectProperty(None)
    
    'Size of startpopup'
    startpopup_size = ListProperty([.4, .4])
    'Image of startpopup'
    img_startpopup = StringProperty('Images/gamebox.png') 
               
    def start_click(self):
        self.app.game.start_game()  
         
class DataBar(Widget):
    game = ObjectProperty(None)
    
    'Game length'
    game_time = NumericProperty(0.9)  #has to be one below whole number, why?
        
    high_score_label = NumericProperty(0)  
    time_label = NumericProperty(0)   
    score_label = NumericProperty(0)       
    
    def new_high_score(self):
        if self.score_label > self.high_score_label:    #Changes the high score if the current score is higher than the old high score 
            self.high_score_label = self.score_label  
    
    def time(self, dt):
        cond1 = self.game.playing_label
        cond2 = self.time_label < self.game_time
        if cond1 and cond2:
            self.time_label += 0.1
        elif cond1:
            self.game.end_game()            
           
    def score(self):  
        self.score_label += 1 
                                                   
class Mole(Widget):
    game = ObjectProperty(None)
    
    'Starting character selection'
    current_char = StringProperty('Images/mole.png')
    'Distance from wall moles center cant be'
    wall_gap = NumericProperty(1.2)  #Needs to be a percentage to times the width/height of mole by 
          
    #Detection of touch on mole
    def on_touch_down(self, touch):
        cond1 = self.collide_point(*touch.pos)
        cond2 = self.game.playing_label
        if cond1 and cond2:
            self.move()
            self.game.databar.score()        
    
    #New position of ball   
    #kv width and kv height are declared in kv file 
    #int methods are used to round all numbers as kv file doesn't accept lots of decimal places  
    def random(self):   
        rl_gap = int(self.kvwidth * self.wall_gap) #right-left side gap
        bt_gap = int(self.kvheight * self.wall_gap) #top-bottom gap
        right = int(self.game.gamebox.get_right() - bt_gap)
        top = int(self.game.gamebox.get_top() - rl_gap)
        x = randrange(rl_gap , right , 1)   
        y = randrange(bt_gap , top , 1)       
        return (x, y)    
        
    def move(self):
        self.pos = self.random()    
        
    def end(self):
        x = self.game.kvcenter_x
        y = self.game.kvcenter_y
        self.center = x, y           

class MoleGame(Widget):
    app = ObjectProperty(None)
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
    
    'Gamebox Image'
    img_gamebox = StringProperty('Images/gamebox.png')  
    'Seconds times_up pop up is visible for'  
    timesup_time = NumericProperty(1.5)
    
    playing_label = BooleanProperty(False)      
                
    def start_game(self):
        self.playing_label = True
        self.databar.score_label = 0
        self.databar.time_label = 0
        
    def end_game(self):
        self.mole.end()
        self.playing_label = False
        self.databar.new_high_score()
        self.app.times_up()
        Clock.schedule_once(self.app.start_popup_scrn, self.timesup_time)      
   
class MoleHuntApp(App):
    game = ObjectProperty(None)
    startpopup = ObjectProperty(None)
    times_up = ObjectProperty(None)

    def build(self):
        self.game = MoleGame()
        self.startpopup = StartPopUp()
        
        Clock.schedule_once(self.start_popup_scrn, 1)
        Clock.schedule_interval(self.game.databar.time, 0.1) #for counter label 
        
        return self.game
    
    def times_up(self):
        self.times_up = TimesUp()
        self.game.add_widget(self.times_up)  
    
    def start_popup_scrn(self, *args):
        self.game.remove_widget(self.times_up) 
        self.startpopup.open()   

if __name__ == '__main__':
    MoleHuntApp().run()