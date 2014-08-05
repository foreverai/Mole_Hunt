'''
Added
-Fixed databar layout
-Changed both characters to moles
-Added sounds 

To Do 
-Check timer will work even if game is running slowly
-Organise kv file into changeable elements
-Create more advanced graphics
-Add phone vibration through plyer (platform independent way to access API)
-Make mole proportionally sized correctly
-Sort text sizing

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
from kivy.core.audio import SoundLoader
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from random import randrange
from kivy.uix.popup import Popup

class TimesUp(Widget):
    app = ObjectProperty(None)
    
    'Change pop up size'
    width_factor = NumericProperty(0.5)
    height_factor = NumericProperty(0.3)    
    'Sound at game end'
    sound_bad = SoundLoader.load('Sounds/sound_bad.wav')
    sound_neutral = SoundLoader.load('Sounds/sound_neutral.wav')
    sound_good = SoundLoader.load('Sounds/sound_good.wav')    
    
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_center = NumericProperty(0)
    y_center = NumericProperty(0)
    
    def __init__(self, *args, **kwargs):
        super(TimesUp, self).__init__(*args, **kwargs)
        self.sound()
        self.sizing()    #sizing has to be before positioning.  otherwise the center of widget is unknown
        self.position()
    
    #plays end game sonds based on score
    def sound(self):
        print self.app.game.databar.score
        cond1 = self.app.game.databar.score_label < 10
        cond2 = self.app.game.databar.score_label > 20
        if cond1:
            self.sound_bad.play()
        elif cond2:
            self.sound_good.play()
        else:
            self.sound_neutral.play()        
    
    def sizing(self):
        self.x_size = self.app.game.width * self.width_factor
        self.y_size = self.app.game.height * self.height_factor
        
    def position(self, *args):
        self.x_center = self.app.game.width/2 
        self.y_center = self.app.game.height/2
        
class SelectBox(Widget):
    startpopup = ObjectProperty(None)   
    
    'Selectbox Image'
    img_selectbox = StringProperty('Images/selectbox.png') 
    
    x_center = NumericProperty(0)
    y_center = NumericProperty(0) 
    x_width = NumericProperty(0)
    y_height = NumericProperty(0) 
    
    #Sizing and positioning in charselect.  
    #Issues selecting through the widget tree prevent putting them in SelectBox 

class CharSelect(Widget):
    startpopup = ObjectProperty(None)
    selectbox = ObjectProperty(None)
    character1 = ObjectProperty(None)
    
    'Number of columns to split character sprites over'
    char_columns = NumericProperty(2)
    
    character_lst = ListProperty([])
     
    def __init__(self, *args, **kwargs):
        super(CharSelect, self).__init__(*args, **kwargs)
        'Put selectable characters here, also add a character widget in kv file'
        self.character_lst.append('Images/mole.png') 
        self.character_lst.append('Images/bird.png')   
    
    #Position selectbox on start    
    def start(self, *args):
        #if these are in select box widget charselect cant be accessed from selectbox, why?
        self.selectbox.x_width = self.character1.width
        self.selectbox.y_height = self.character1.height 
        self.selectbox.x_center = self.character1.center_x
        self.selectbox.y_center = self.character1.center_y       
    
    #Position selectbox on character click
    def image_select(self, character):
        self.selectbox.x_width = character.width
        self.selectbox.y_height = character.height
        self.selectbox.x_center = character.center_x
        self.selectbox.y_center = character.center_y
        self.startpopup.app.game.mole.current_char = character.source  

class StartPopUp(Popup):
    app = ObjectProperty(None)
    charselect = ObjectProperty(None)
    
    'Size of startpopup'
    startpopup_size = ListProperty([.4, .4])
    'Image of startpopup'
    img_startpopup = StringProperty('Images/popup.png') 
    
    #on button click start game           
    def start_click(self):
        self.app.game.start_game()  
         
class DataBar(Widget):
    game = ObjectProperty(None)
    
    'Image of startpopup'
    img_databar = StringProperty('Images/databar.png') 
    'Game length'
    game_time = NumericProperty(9.9)  #has to be one below whole number, why?
    
    score_label = NumericProperty(0)     
    high_score_label = NumericProperty(0)  
    time_label = NumericProperty(0)        
    
    def start(self):
        self.score_label = 0
        self.time_label = 0
               
    def score(self):  
        self.score_label += 1  
    
    def time(self, dt):
        cond1 = self.game.playing_label
        cond2 = self.time_label < self.game_time
        if cond1 and cond2:
            self.time_label += 0.1
        elif cond1:
            self.game.end_game()  
            
    #Changes the high score if the current score is higher than the old high score    
    def new_high_score(self):
        if self.score_label > self.high_score_label: 
            self.high_score_label = self.score_label                   
                                                   
class Mole(Widget):
    game = ObjectProperty(None)
    
    'Starting character selection'
    current_char = StringProperty('Images/mole.png')
    'Size of mole as percentage of screen (height , width)'
    mole_size = ListProperty([0.1, 0.15])
    'Min gap between mole center and screen edges'
    wall_gap = NumericProperty(1.2)  #Needs to be a percentage to times the width/height of mole by    
    'Sound when mole is tapped'
    sound_mole = SoundLoader.load('Sounds/sound_mole.wav')
    
    #Detection of touch on mole
    def on_touch_down(self, touch):
        cond1 = self.collide_point(*touch.pos)
        cond2 = self.game.playing_label
        if cond1 and cond2:
            self.sound()
            self.move()
            self.game.databar.score()  

    def sound(self):
        # stop the sound if it's currently playing
        if self.sound_mole.status != 'stop':
            self.sound_mole.stop()
        self.sound_mole.play()
                  
    def move(self):
        self.pos = self.random()
    
    #Wall gaps based on mole size     
    #int methods are used to round all numbers as randrange doesn't accept float numbers  
    def random(self):   
        left = int(self.width * self.wall_gap) #left side gap
        right = int(self.game.gamebox.get_right() - left) #right side gap
        x = randrange(left , right , 1)  
        bottom = int(self.height * self.wall_gap) #bottom gap
        top = int(self.game.gamebox.get_top() - bottom) #top gap 
        y = randrange(bottom , top , 1)       
        return (x, y)        
    
    #Return mole to center of screen    
    def end(self):
        x = self.game.width/2
        y = self.game.height/2
        self.center = x, y           

class MoleGame(Widget):
    app = ObjectProperty(None)
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
    
    'Gamebox Image'
    img_gamebox = StringProperty('Images/gamebox.png')  
    'Seconds times_up pop up is visible for'  
    timesup_time = NumericProperty(2)
    
    playing_label = BooleanProperty(False)  
    
    def start_game(self):
        self.playing_label = True
        self.databar.start()
        
    def end_game(self):
        self.mole.end()
        self.playing_label = False
        self.databar.new_high_score()
        self.app.times_up()
        Clock.schedule_once(self.app.start_popup_scrn, self.timesup_time)      
   
class MoleHuntApp(App):
    game = ObjectProperty(None)
    startpopup = ObjectProperty(None)
    timesup = ObjectProperty(None)

    def build(self):
        self.game = MoleGame()
        self.startpopup = StartPopUp()
        Clock.schedule_once(self.start_popup_scrn, 0.5) #So it runs after game widget is created
        Clock.schedule_interval(self.game.databar.time, 0.1) #to add to counter every 0.1 seconds 
        return self.game
    
    def times_up(self):
        self.timesup = TimesUp()   #Needs declared here rather than in build otherwise initilised wrongly
        self.game.add_widget(self.timesup)  
    
    def start_popup_scrn(self, *args):
        self.game.remove_widget(self.timesup) 
        self.startpopup.open()   
        Clock.schedule_once(self.startpopup.charselect.start, 0.5)   # select box can only be initilised after the pop up is created

if __name__ == '__main__':
    MoleHuntApp().run()