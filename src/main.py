'''
Added
-Got all widgets working correctly
-Created links between all objects using app and kv file
-Fixed mole restart position
-Added kv variable type (layout variables declared in kv file)

To Do 
-Add multiple game types (based on game time)
-Make time run better
-Make initial mole positioning better


'''

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty
from random import randrange
from kivy.uix.popup import Popup

class StartPopUp(Popup):
    app = ObjectProperty(None)
    
    def __init__(self, **kw):
        super(StartPopUp, self).__init__(**kw)
           
    def start_click(self):
        self.app.game.start_game()  
            
class DataBar(Widget):
    app = ObjectProperty(None)
    
    high_score_label = NumericProperty(0)  
    time_label = NumericProperty(0)   
    score_label = NumericProperty(0)       
    
    def new_high_score(self):
        if self.score_label > self.high_score_label:    #Changes the high score if the current score is older than the old high score 
            self.high_score_label = self.score_label  
    
    def time(self):
        if (self.time_label < 9.9):   #when game is in on phase       
            self.time_label += 0.1  
        elif (self.time_label > 9.8):   #when the time limit is reached  
            self.app.game.end_game()     
            
    def score(self):  
        self.score_label += 1              
                              
class Mole(Widget):
    app = ObjectProperty(None)
    
    mole_start_x = NumericProperty(0)
    mole_start_y = NumericProperty(0)  
    
    def __init__(self, **kw):
        super(Mole, self).__init__(**kw)
          
    def initilise(self):
        self.mole_start_x = self.app.game.kvcenter_x
        self.mole_start_y = self.app.game.kvcenter_y  
        
    #touch on mole detection
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.move()
            self.app.game.databar.score()        
    
    #New position of ball      
    def random(self):   
        #Need a way to get to root widget
        x = randrange(self.kvwidth_size,round(self.app.game.gamebox.get_right(), 0)-self.kvwidth_size,1)   #50 from left and right
        y = randrange(self.kvheight_size,round(self.app.game.gamebox.get_top(), 0)-self.kvheight_size,1)     #50 from top and bottom  
        return (x, y)    
        
    def move(self):
        self.pos = self.random()    
        
    def end(self):
        x = self.mole_start_x
        y = self.mole_start_y
        self.center = x, y           

class MoleGame(Widget):
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
    
    playing_label = BooleanProperty(False)
    
    def __init__(self, **kw):
        super(MoleGame, self).__init__(**kw)        
    
    def start_popup(self, *args):
        self.mole.initilise()    
        sp = StartPopUp()
        sp.open() 
                
    def start_game(self):
        self.playing_label = True
        self.databar.score_label = 0
        self.databar.time_label = 0
    
    def end_game(self):
        self.mole.end()
        self.playing_label = False
        self.databar.new_high_score()
        self.start_popup()       
    
    def update(self, dt):
        if self.playing_label: 
            self.databar.time()
           
class MoleHuntApp(App):
    game = ObjectProperty(None)

    def build(self):
        self.game = MoleGame()
        Clock.schedule_once(self.game.start_popup, 1)
        Clock.schedule_interval(self.game.update, 0.1)  #schedule a function to run repeatedly
        return self.game

if __name__ == '__main__':
    MoleHuntApp().run()