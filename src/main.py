'''
Added
-Moved sounds to a matrix in the app class
-Added high score read/writing to text file (to save high score after game is closed)
-Character1 is always the selected character sprite when game ends
-Text scales between screen densities
-Mole scales between screens
-Added 4 achievement levels

To Do Before Production Release
-General tidy up
-Check scores arn't overwritten on update/removal
-Mole restart position is wrong

Future features
-Make character select keep currently selected character rather than reverting to character1
-Phone vibration on tap (using plyer to access android vibration api)
-Display top 5 friends scores on game HUD, or on between game screen
-Display ads
-Ability to take pictures of people and have them as characters

Widget tree
-app
-game
    -gamebox
    -mole
    -databar
-startpopup
    -achievements
    -charselect
        -character1
        -selectbox
-timesup      
  
'''

__version__ = '1.0.4'

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
        cond1 = self.app.game.databar.score_label < 10
        cond2 = self.app.game.databar.score_label > 20
        if cond1:
            self.app.sounds["Lost"].play()
        elif cond2:
            self.app.sounds["Win"].play()
        else:
            self.app.sounds["Draw"].play()        
    
    def sizing(self):
        self.x_size = self.app.game.width * self.width_factor
        self.y_size = self.app.game.height * self.height_factor
        
    def position(self, *args):
        self.x_center = self.app.game.width/2 
        self.y_center = self.app.game.height/2

class Achievements(Widget):
    startpopup = ObjectProperty(None)
    
    'Set medal scores'
    bronze = NumericProperty(15)
    silver = NumericProperty(20)
    gold = NumericProperty(22)
    platinum = NumericProperty(25)
    
    'Medal images'
    medal_images = {
        "No_Medal": 'Images/No_Medal.png',
        "Bronze": 'Images/Bronze.png',
        "Silver": 'Images/Silver.png',
        "Gold": 'Images/Gold.png',
        "Platinum": 'Images/Platinum.png'
        }
    
    top_score = NumericProperty(0)
    medal_1 = StringProperty()
    medal_2 = StringProperty()
    medal_3 = StringProperty()
    medal_4 = StringProperty()
    
    def fill_medals(self):
        self.top_score = self.startpopup.app.game.databar.high_score_label
        if self.top_score >= self.platinum:
            self.medal_4 = self.medal_images["Platinum"]
        else: 
            self.medal_4 = self.medal_images["No_Medal"]
                
        if self.top_score >= self.gold:
            self.medal_3 = self.medal_images["Gold"]
        else: 
            self.medal_3 = self.medal_images["No_Medal"]
                
        if self.top_score >= self.silver:
            self.medal_2 = self.medal_images["Silver"]
        else: 
            self.medal_2 = self.medal_images["No_Medal"]
                
        if self.top_score >= self.bronze:
            self.medal_1 = self.medal_images["Bronze"]
        else: 
            self.medal_1 = self.medal_images["No_Medal"]
        
class SelectBox(Widget):
    startpopup = ObjectProperty(None)   
    
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
        self.startpopup.app.game.mole.current_char = self.character1.source        
    
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
    startpopup_size = ListProperty([.6, .6]) 
    
    #on button click start game           
    def start_click(self):
        self.app.game.start_game()  
         
class DataBar(Widget):
    game = ObjectProperty(None)
    
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
    
    'Mole width'
    mole_width = NumericProperty(55)
    'Mole height'
    mole_height = NumericProperty(75)
    'Min gap between mole center and screen edges'
    wall_gap = NumericProperty(1.2)  #Needs to be a percentage to times the width/height of mole by    
    
    #Detection of touch on mole
    def on_touch_down(self, touch):
        cond1 = self.collide_point(*touch.pos)
        cond2 = self.game.playing_label
        if cond1 and cond2:
            self.sound()
            self.move()
            self.game.databar.score()  
    
    #Sound to play when mole is tapped
    def sound(self):
        # stop the sound if it's currently playing
        if self.game.app.sounds["Mole_Tap"].status != 'stop':
            self.game.app.sounds["Mole_Tap"].stop()
        self.game.app.sounds["Mole_Tap"].play()
    
    #New position of mole              
    def move(self):
        self.pos = self.random()
    
    #Wall gaps based on mole size     
    #int methods are used to round all numbers as randrange doesn't accept float numbers  
    def random(self):   
        left = int(self.mole_width * self.wall_gap) #left side gap
        right = int(self.game.gamebox.get_right() - left) #right side gap
        x = randrange(left , right , 1)  
        bottom = int(self.mole_height * self.wall_gap) #bottom gap
        top = int(self.game.gamebox.get_top() - bottom) #top gap 
        y = randrange(bottom , top , 1)       
        return (x, y)        
    
    #Return mole to center of screen    
    def end(self):
        x = self.game.width/2
        y = self.game.height/2
        print x, y
        self.center = x, y           

class MoleGame(Widget):
    app = ObjectProperty(None)
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
      
    'Seconds times_up pop up is visible for'  
    timesup_time = NumericProperty(2)
    
    playing_label = BooleanProperty(False)  
    
    def start_game(self):
        self.playing_label = True
        self.databar.start()
        Clock.schedule_interval(self.databar.time, 0.1) #to add to counter every 0.1 seconds
        
    def end_game(self):
        self.mole.end()
        Clock.unschedule(self.databar.time)
        self.playing_label = False
        self.databar.new_high_score()
        self.app.times_up()
        Clock.schedule_once(self.app.start_popup_scrn, self.timesup_time)      
   
class MoleHuntApp(App):
    game = ObjectProperty(None)
    startpopup = ObjectProperty(None)
    timesup = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(MoleHuntApp, self).__init__(**kwargs)
        #Hash out sound lines to allow running in kivy launcher
        # setup all sounds
        self.sounds = {
            "Mole_Tap": SoundLoader.load('Sounds/mole_tap.wav'),
            "Lost": SoundLoader.load('Sounds/Lost.wav'),
            "Draw": SoundLoader.load('Sounds/Drawl.wav'),
            "Win": SoundLoader.load('Sounds/Win.wav')
        }
    
    def build(self):
        self.game = MoleGame()
        self.startpopup = StartPopUp()
        #Hash out Read line to allow running in kivy launcher
        self.read_save()
        Clock.schedule_once(self.start_popup_scrn, 0.5) #So it runs after game widget is created
        return self.game
    
    #Reads high score data
    def read_save(self):
        save_dir = self.user_data_dir
        f = open (save_dir + '\high_score.txt', 'r')
        self.game.databar.high_score_label = int(f.read())
    
    #Writes high score data to file
    def on_stop(self):
        save_dir = self.user_data_dir
        f = open(save_dir + '\high_score.txt', 'w')
        f.write(str(self.game.databar.high_score_label))
        f.close()
    
    #Displays times up popup
    def times_up(self):
        self.timesup = TimesUp()   #Needs declared here rather than in build otherwise initilised wrongly
        self.game.add_widget(self.timesup)  
    
    #Displays out of game popup
    def start_popup_scrn(self, *args):
        self.game.remove_widget(self.timesup) 
        self.startpopup.open() 
        self.startpopup.achievements.fill_medals()  
        Clock.schedule_once(self.startpopup.charselect.start, 0.5)   # select box can only be initilised after the pop up is created 
         
if __name__ == '__main__':
    MoleHuntApp().run()