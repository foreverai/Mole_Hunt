'''
Added
-Changed mole size
-Altered gap between mole and wall
-Made mole reposition on center rather than bottom left
-Fixed some character selection issues
-time was running at double time? not sure why, something fishy
-Made button/characters translucent on press, opaque on touch up or touch moved off widget
-changed achievement scores

To Do
-Check scores arn't overwritten on update/removal on

Future features
-Make background grass, and have a little graphic of dug up dirt below each mole
-Change pop ups to modalviews
-Put changeable game mechanics, graphics, images, sounds, text in json files
-Put images in atlas
-Make a story, each medal earned adds to the story
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
-timesup      
  
'''

__version__ = '1.1.0'

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
    height_factor = NumericProperty(0.4)    
    
    'Change timesup_text'
    timesup_text = {
        "Lost": 'Game Over',
        "Win": 'Congratulations!'
    }    
    
    times_up = StringProperty()
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
        cond1 = self.app.game.databar.score_label < 36
        cond2 = self.app.game.databar.score_label >= 36
        if cond1:
            self.app.sounds["Lost"].play()
            self.times_up = self.timesup_text["Lost"]
        elif cond2:
            self.app.sounds["Win"].play()
            self.times_up = self.timesup_text["Win"]
      
    def sizing(self):
        self.x_size = self.app.game.width * self.width_factor
        self.y_size = self.app.game.height * self.height_factor
        
    def position(self, *args):
        self.x_center = self.app.game.width/2 
        self.y_center = self.app.game.height/100 * 56   #Slightly off center so the mole appears in the middle of the text without covering it
        
class Achievements(Widget):
    startpopup = ObjectProperty(None)
    bronze_medal = ObjectProperty(None)
    silver_medal = ObjectProperty(None)
    gold_medal = ObjectProperty(None)
    platinum_medal = ObjectProperty(None)
    
    'Set medal scores'
    bronze = NumericProperty(36)
    silver = NumericProperty(40)
    gold = NumericProperty(44)
    platinum = NumericProperty(48)
    
    start_game = BooleanProperty(True)
    top_score = NumericProperty(0)
    medal_1_full = BooleanProperty(False)
    medal_2_full = BooleanProperty(False)
    medal_3_full = BooleanProperty(False)
    medal_4_full = BooleanProperty(False)
    
    #Sets if which medals are displayed
    #Messy implementation...probably an easier way
    def fill_medals(self):
        self.top_score = self.startpopup.app.game.databar.high_score_label
        
        #Bronze medal
        cond1 = self.top_score >= self.bronze
        cond2 = self.medal_1_full == False
        if cond1 and cond2:
            self.bronze_medal.color = 1, 1, 1, 1    #Makes medal opaque
            self.medal_sound()
            self.medal_1_full = True
        
        #Silver medal
        cond1 = self.top_score >= self.silver
        cond2 = self.medal_2_full == False
        if cond1 and cond2:
            self.silver_medal.color = 1, 1, 1, 1
            self.medal_sound()
            self.medal_2_full = True
        
        #Gold medal
        cond1 = self.top_score >= self.gold
        cond2 = self.medal_3_full == False
        if cond1 and cond2:
            self.gold_medal.color = 1, 1, 1, 1
            self.medal_sound()
            self.medal_3_full = True
            
        #Platinum medal            
        cond1 = self.top_score >= self.platinum
        cond2 = self.medal_4_full == False
        if cond1 and cond2:
            self.platinum_medal.color = 1, 1, 1, 1
            self.medal_sound()
            self.medal_4_full = True
            
        self.start_game = False  #Now medal sounds will play when they are achieved
            
    def medal_sound(self):
        if self.start_game == False:
            self.startpopup.app.sounds["Medal"].play()

class CharSelect(Widget):
    startpopup = ObjectProperty(None)
    character1 = ObjectProperty(None)
    character2 = ObjectProperty(None)
    character3 = ObjectProperty(None) 
    
    'Number of columns to split character sprites over'
    char_columns = NumericProperty(3)
    'unselected transparency'
    unselected = ListProperty([0.5, 0.5, 0.5, 0.5])
    'character list'
    character_lst = {
        "mole_1": 'Images/mole_1.png',
        "mole_2": 'Images/mole_2.png',
        "mole_3": 'Images/mole_3.png'
    }              
    
    pressed_char = ObjectProperty(None)
    pressed_down = BooleanProperty(False)
    selected_mole = BooleanProperty(False)
    
    #Select center mole on start   
    def start(self, *args):
        self.character1.color = self.unselected
        self.character2.color = 1, 1, 1, 1
        self.character3.color = self.unselected
        self.startpopup.app.game.mole.current_char = self.character2.source
        
    def character_select(self, character):
        self.pressed_down = False       
        self.selected_mole = False
        if character == self.pressed_char:
            self.startpopup.app.sounds["Char_Select"].play()
            self.character1.color = self.unselected
            self.character2.color = self.unselected
            self.character3.color = self.unselected
            character.color = 1, 1, 1, 1
            self.startpopup.app.game.mole.current_char = character.source               
    
    def press_down(self, character):
        if character.color == [1, 1, 1, 1]:
            self.selected_mole = True
        self.pressed_down = True
        self.pressed_char = character
        character.color = 1, 1, 1, 1
        
    def touch_moved(self, character):
        if self.selected_mole:
            pass
        else:
            self.pressed_down = False
            self.pressed_char.color = self.unselected       

class StartPopUp(Popup):
    app = ObjectProperty(None)
    charselect = ObjectProperty(None)
    
    'Size of startpopup'
    startpopup_size = ListProperty([.78, .8])
    'Normal text color'
    text_col_norm = 1, 0.5, 0.5, 1
    'Pressed down text color'
    text_col_pres = 1, 0.5, 0.5, 0.4 
    
    pressed_down = BooleanProperty(False)
    
    #on button click start game           
    def start_click(self):
        self.app.game.start_game()  
        if self.app.sounds["Open"].status != 'stop':       #stops start game sound if its currently playing
            self.app.sounds["Open"].stop()
    
    #when button is clicked text becomes translucent        
    def press_down(self, play_text):
        self.pressed_down = True
        play_text.color = self.text_col_pres
    
    #when touch moves off text text returns to normal color    
    def press_release(self, play_text):
        if self.pressed_down:               #only runs if button was pressed in the first place
            self.pressed_down = False
            play_text.color = self.text_col_norm   
                        
class DataBar(Widget):
    game = ObjectProperty(None)
    
    'Game length'
    game_time = NumericProperty(20)  #has to be one below whole number, why?
    
    score_label = NumericProperty(0)     
    high_score_label = NumericProperty(0)  
    time_label = NumericProperty(0)        
               
    def score(self):  
        self.score_label += 1  
    
    def time(self, dt):
        cond1 = self.game.playing_label
        cond2 = self.time_label < self.game_time
        if cond1 and cond2:
            self.time_label += 0.05    #something fishy going on with timing....this is a slap up fix
        elif cond1:
            self.game.end_game()  
            
    #Changes the high score if the current score is higher than the old high score    
    def new_high_score(self):
        if self.score_label > self.high_score_label: 
            self.high_score_label = self.score_label    
    
    #Runs when startpopup comes up        
    def end(self):
        self.score_label = 0
        self.time_label = 0                       
                                                   
class Mole(Widget):
    game = ObjectProperty(None)
    
    'Mole width'
    mole_width = NumericProperty(50)
    'Mole height'
    mole_height = NumericProperty(60)
    'Min gap between mole center and screen edges'
    wall_gap = NumericProperty(1.2)  #Needs to be a percentage to times the width/height of mole by    
    
    current_char = StringProperty()
    
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
        if self.game.app.sounds["Mole_Tap"].status != 'stop':     # stop the sound if it's currently playing
            self.game.app.sounds["Mole_Tap"].stop()
        self.game.app.sounds["Mole_Tap"].play()
    
    #New position of mole              
    def move(self):
        self.center = self.random()
    
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
        self.center = x, y           

class MoleGame(Widget):
    app = ObjectProperty(None)
    databar = ObjectProperty(None) 
    mole = ObjectProperty(None) 
    gamebox = ObjectProperty(None)
    
    'Seconds times_up pop up is visible for'  
    timesup_time = NumericProperty(2.5)
    
    playing_label = BooleanProperty(False)  
    
    def start_game(self):
        self.playing_label = True
        self.app.sounds["Play"].play()
        Clock.schedule_interval(self.databar.time, 0.1) 
        
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
            "Mole_Tap": SoundLoader.load('Sounds/Mole_Tap.wav'),
            "Lost": SoundLoader.load('Sounds/Lost.wav'),
            "Win": SoundLoader.load('Sounds/Win.wav'),
            "Char_Select": SoundLoader.load('Sounds/Char_Select.wav'),
            "Play": SoundLoader.load('Sounds/Play.wav'),
            "Open": SoundLoader.load('Sounds/Open.wav'),
            "Medal": SoundLoader.load('Sounds/Medal.wav')
        }
    
    def build(self):
        self.game = MoleGame()
        self.startpopup = StartPopUp()
        #Hash out Read line to allow running in kivy launcher
        self.read_save()
        return self.game
    
    #Runs after the build has been made 
    def on_start(self):
        self.start_popup_scrn()
    
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
        open_sound = self.sounds["Open"]
        open_sound.play()
        open_sound.loop = True
        self.game.databar.end()  #resets scores and time to 0 
        self.game.remove_widget(self.timesup) 
        self.startpopup.open() 
        self.startpopup.achievements.fill_medals()  
        Clock.schedule_once(self.startpopup.charselect.start, 0.5)   # select box can only be initilised after the pop up is created 
         
if __name__ == '__main__':
    MoleHuntApp().run()