'''
Added
-Got all widgets working correctly
-Created links between all objects using app and kv file
-Fixed mole restart position
-Added kv variable type (layout variables declared in kv file)
-Made timer run better
-Made intital and random mole positioning better

To Do 
-Add multiple game types (based on game time)

'''

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty
from random import randrange
from kivy.uix.popup import Popup

'Popup screen declared in app class'
class StartPopUp(Popup):
    app = ObjectProperty(None)
           
    def start_click(self):
        self.app.game.start_game()  

'Child of MoleGame'            
class DataBar(Widget):
    app = ObjectProperty(None)
    
    game_time = NumericProperty(9.9)  #has to be one below whole number, why?
        
    high_score_label = NumericProperty(0)  
    time_label = NumericProperty(0)   
    score_label = NumericProperty(0)       
    
    def new_high_score(self):
        if self.score_label > self.high_score_label:    #Changes the high score if the current score is higher than the old high score 
            self.high_score_label = self.score_label  
    
    def time(self, dt):
        cond1 = self.app.game.playing_label
        cond2 = self.time_label < self.game_time
        if cond1 and cond2:
            self.time_label += 0.1
        elif cond1:
            self.app.game.end_game()            
           
    def score(self):  
        self.score_label += 1 
                     
'Child of MoleGame'                              
class Mole(Widget):
    app = ObjectProperty(None)
    
    wall_gap = NumericProperty(1.2)  #Needs to be a percentage to times the width/height of mole by
          
    #Detection of touch on mole
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.move()
            self.app.game.databar.score()        
    
    #New position of ball   
    #kv width and kv height are declared in kv file 
    #int methods are used to round all numbers as kv file doesn't accept lots of decimal places  
    def random(self):   
        rl_gap = int(self.kvwidth * self.wall_gap) #right-left side gap
        bt_gap = int(self.kvheight * self.wall_gap) #top-bottom gap
        right = int(self.app.game.gamebox.get_right() - bt_gap)
        top = int(self.app.game.gamebox.get_top() - rl_gap)
        x = randrange(rl_gap , right , 1)   
        y = randrange(bt_gap , top , 1)       
        return (x, y)    
        
    def move(self):
        self.pos = self.random()    
        
    def end(self):
        x = self.app.game.kvcenter_x
        y = self.app.game.kvcenter_y
        self.center = x, y           

'Game controller screen declared in app class'
class MoleGame(Widget):
    app = ObjectProperty(None)
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
    
    playing_label = BooleanProperty(False)
    
    def __init__(self, **kw):
        super(MoleGame, self).__init__(**kw)        
                
    def start_game(self):
        self.playing_label = True
        self.databar.score_label = 0
        self.databar.time_label = 0
    
    def end_game(self):
        self.mole.end()
        self.playing_label = False
        self.databar.new_high_score()
        self.app.start_popup_scrn()       

'app serves as the root of the widget tree.  All objects can call app'  
'app declares each screen in the app and handles screen management'  
'All objects present in a screen have an object property in that screens class' 

'Therefore through the process of every object having a reference to app.  App declaring all screen objects.  And each screen declaring all its children objects' 
'Every object can access every other object in the entire program'     
class MoleHuntApp(App):
    game = ObjectProperty(None)
    startpopup = ObjectProperty(None)

    def build(self):
        self.game = MoleGame()
        self.startpopup = StartPopUp()
        
        Clock.schedule_once(self.start_popup_scrn, 1)
        Clock.schedule_interval(self.game.databar.time, 0.1) #for counter label  
        
        return self.game
    
    def start_popup_scrn(self, *args):
        self.startpopup.open()
    

if __name__ == '__main__':
    MoleHuntApp().run()