'''
Created on 12 Nov 2013

@author: Mr Lahey

Function
-A button moves around the screen as you click it.  Get as many clicks in a set time as possible

Uses: 
-Adding and removing widgets in kv file using kv file
-Adding/removing widgets in kv file using py file
-Game phase logic, i.e starting, ending and during
-Moving a widget around a float layout
-Creating random numbers
-Calling functions from widget outside root widget

'''

import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from random import randrange

class Ball(Widget):
    ball_center = ListProperty([200, 200])  #Start position of ball
    
    #New position of ball      
    def random(self):   
        x = randrange(50,round(self.get_right(), 0)-50,1)   #50 from left and bottom and right and top
        y = randrange(50,round(self.get_top(), 0)-50,1)     #50 from left and bottom and right and top    
        return (x, y)    
        
    def move(self):
        self.ball_center = self.random()
        #The reason for so many parents
        #needs to be called with the controller widget, 
        #not sure why, should probably be a better way
        Controller.update_score(self.parent.parent.parent)

class Controller(Widget):
    score_label = NumericProperty(0)
    time_label = NumericProperty(0)
    playing_label = NumericProperty(0)          #Intitial phase of game is off
    high_score_label = NumericProperty(0)
    
    def restart_game(self):
        self.score_label = 0
        self.playing_label = 1
        self.time_label = 0
    
    def end_game(self):
        self.playing_label = 0 
        self.add_widget(self.ids.Begin)     #Adding a widget in kv file from py file
        if self.score_label > self.high_score_label:    #Changes the high score if the current score is older than the old high score 
            self.high_score_label = self.score_label
    
    def update_score(self):  
        if (self.playing_label == 1):   #Only update label during game phase
            self.score_label += 1 
            
    def update_time(self, dt):
        if (self.playing_label == 0):   #when game is in off phase
            self.time_label = 0 
        elif (self.playing_label == 1 and self.time_label < 9.9):   #when game is in on phase       
            self.time_label += 0.1  
        elif (self.playing_label == 1 and self.time_label > 9.8):   #when the time limit is reached  
            self.end_game()
        else:
            print "update_time function error"                 

class MoleHuntApp(App):

    def build(self):
        game = Controller()
        Clock.schedule_interval(game.update_time, 0.1)  #schedule a function to run repeatedly
        return game

if __name__ == '__main__':
    MoleHuntApp().run()