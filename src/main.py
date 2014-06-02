'''
Added
-Mole only moves if game is active
-Button background when clicked has been changed

'''

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from random import randrange
from kivy.uix.popup import Popup


class StartPopUp(Popup):
    
    def __init__(self, controller, **kw):
        super(StartPopUp, self).__init__(**kw)
        self.controller = controller
           
    def start_click(self):
        self.controller.start_game()                    

class Mole(Widget):
    mole_center = ListProperty([0, 0])  #Start position of ball
    
    #New position of ball      
    def random(self):   
        x = randrange(50,round(self.get_right(), 0)-50,1)   #50 from left and bottom and right and top
        y = randrange(50,round(self.get_top(), 0)-50,1)     #50 from left and bottom and right and top    
        return (x, y)    
        
    def move(self):
        if self.parent.parent.parent.playing_label == 1:
            self.mole_center = self.random()
            Controller.score(self.parent.parent.parent)

class Controller(Widget):
    score_label = NumericProperty(0)
    time_label = NumericProperty(0)
    playing_label = NumericProperty(0)          #Intitial phase of game is off
    high_score_label = NumericProperty(0)
    
    
    def __init__(self, **kw):
        super(Controller, self).__init__(**kw)        
    
    def start_popup(self, *args):    
        sp = StartPopUp(self)
        sp.open() 
            
    def start_game(self):
        self.score_label = 0
        self.playing_label = 1
        self.time_label = 0
    
    def end_game(self):
        self.playing_label = 0 
        self.start_popup()
        if self.score_label > self.high_score_label:    #Changes the high score if the current score is older than the old high score 
            self.high_score_label = self.score_label
    
    def score(self):  
        if (self.playing_label == 1):   #Only update label during game phase
            self.score_label += 1 
            
    def time(self):
        if (self.playing_label == 0):   #when game is in off phase
            self.time_label = 0 
        elif (self.playing_label == 1 and self.time_label < 9.9):   #when game is in on phase       
            self.time_label += 0.1  
        elif (self.playing_label == 1 and self.time_label > 9.8):   #when the time limit is reached  
            self.end_game()               

    def update(self, dt): 
        self.time() 
           
class MoleHuntApp(App):

    def build(self):
        game = Controller()
        Clock.schedule_once(game.start_popup, 1)
        Clock.schedule_interval(game.update, 0.1)  #schedule a function to run repeatedly
        return game

if __name__ == '__main__':
    MoleHuntApp().run()