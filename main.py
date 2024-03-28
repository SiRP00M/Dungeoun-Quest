from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen , FadeTransition
import random


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.image = Image(source='Sprites/background/Dunmenu.png')
        self.image.size_hint = (1, 1)  
        self.image.pos_hint = {'center_x': 0.5, 'center_y': 0.5} 
        self.layout.add_widget(self.image)
        self.start_button = Button(text='Start Game', size_hint=(0.2, 0.1), pos_hint={"x": 0.4, "y": 0.1},background_color=(0,0,0,1))
        self.start_button.bind(on_press=self.start_game)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def start_game(self, instance):
    
        pass
    
    def on_enter(self):
        self.sound = SoundLoader.load("Sprites/OST/OST.mp3") 
        if self.sound:
            self.sound.volume = 0.7
            self.sound.play()
    def start_game(self, instance):
        self.manager.current = 'Portal1'
        if self.sound:
            self.sound.stop() 

class IntroOne(Widget):
    def __init__(self, **kwargs):
        super(IntroOne, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/1.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class Intro2(Widget):
    def __init__(self, **kwargs):
        super(Intro2, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/2.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class Intro3(Widget):
    def __init__(self, **kwargs):
        super(Intro3, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/3.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class Intro4(Widget):
    def __init__(self, **kwargs):
        super(Intro4, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/4.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class IntroLast(Widget):
    def __init__(self, **kwargs):
        super(IntroLast, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/5.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super(BackgroundWidget, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/background1.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class BackgroundWidget2(Widget):
    def __init__(self, **kwargs):
        super(BackgroundWidget2, self).__init__(**kwargs)
        self.background_img = Image(source='Sprites/Background/background2.png', size_hint=(None, None),
                                    allow_stretch=True, keep_ratio=False)
        self.background_img.size = (1920, 1080) 
        self.add_widget(self.background_img)

class Fighter(Widget):
    def __init__(self, x, y, name, max_hp,hp, strength, potions, game_instance, **kwargs):
        super(Fighter, self).__init__(**kwargs)
        self.original_position = (x, y) 
        self.image = Image(source=f'Sprites/{name}/Idle/0.png',allow_stretch=True)
        self.add_widget(self.image)
        self.image.pos = self.original_position
        self.image.size =(380, 600)
        self.game_instance = game_instance
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead , 4:dash , 5:Run
        self.update_time = 0  

        self.load_images()

    def load_images(self):
        # This is For Load images for each animation state
        for state in ["Idle", "Attack", "Hurt", "Death","Dash","Run"]:
            temp_list = []
            for i in range(7 if state == "Idle" else(8 if state == "Run" else (11 if state == "Death" else (12 if state == "Attack" else (7 if state == "Dash" else (4 if state == "Hurt" else 0)))))):
                img = f'Sprites/{self.name}/{state}/{i}.png'
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self, dt):
        animation_cooldown = 0.1  

        # Update image
        self.image.source = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if Clock.get_time() - self.update_time > animation_cooldown:
            self.update_time = Clock.get_time()
            self.frame_index += 1

        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = Clock.get_time()

    def attack(self, Bandit):
        if Bandit.alive:
            rand = random.randint(15, 25)
            damage = self.strength + rand
            Bandit.hp -= damage

            # Check if Bandit has died
            if Bandit.hp < 1:
                Bandit.hp = 0
                Bandit.alive = False
                Bandit.death()
                
            else:
                Clock.schedule_once(lambda dt: self.delay_hurt_animation(Bandit), 3.5)
                Clock.schedule_once(lambda dt: self.run_back(), 1.5)
                self.dash()

            self.action = 1
            self.frame_index = 0
            self.update_time = Clock.get_time()
            self.game_instance.show_damage_text(Bandit, damage)
            
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = Clock.get_time()
        self.game_instance.play_random_Knight_sound()
       
    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = Clock.get_time()
    
    def delay_hurt_animation(self, Bandit):
        Bandit.hurt()
        
    def dash(self):
        self.action = 4 
        self.frame_index = 0
        self.update_time = Clock.get_time()

        dash_animation =  Animation(pos=(self.original_position[0] + 1420, self.original_position[1]), duration=0.5)
        dash_animation.start(self.image)
    
    def run_back(self):
        self.attack_animation = Animation(pos=(self.original_position[0] , self.original_position[1]), duration=0.8)
        self.attack_animation.start(self.image)
        self.Run()
    
    def Run(self):
        self.action = 5  
        self.frame_index = 0
        self.update_time = Clock.get_time()
    
    def RunPortal(self):
        self.attack_animation = Animation(pos=(self.original_position[0]+100 , self.original_position[1]), duration=1.0)
        self.attack_animation.start(self.image)
        self.Run()

class Bandit(Widget):
    def __init__(self, x, y, name, hp, max_hp, strength, potions, game_instance, **kwargs):
        super(Bandit, self).__init__(**kwargs)
        self.original_position = (x, y)
        self.image = Image(source=f'Sprites/{name}/Idle/0.png', allow_stretch=True)
        self.add_widget(self.image)
        self.image.pos = self.original_position
        self.image.size = (800, 800)
        self.game_instance = game_instance
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead, 4:dash , 5:Run
        self.update_time = 0  
        self.potion_cooldown = 10  
        self.last_potion_time = 0 

        self.load_images()

    def load_images(self):
        # This is For Load images for each animation state
        for state in ["Idle", "Attack", "Hurt", "Death", "Dash", "Run"]:
            temp_list = []
            for i in range(8 if state == "Idle" else (8 if state == "Run" else(11 if state == "Death" else (10 if state == "Attack" else (8 if state == "Dash" else (3 if state == "Hurt" else 0)))))):
                img = f'Sprites/{self.name}/{state}/{i}.png'
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self, dt):
        animation_cooldown = 0.1  

        # Update image
        self.image.source = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if Clock.get_time() - self.update_time > animation_cooldown:
            self.update_time = Clock.get_time()
            self.frame_index += 1

        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = Clock.get_time()

    def attack(self, Knight):
        if Knight.alive:
            rand = random.randint(4, 20)
            damage = self.strength + rand
            Knight.hp -= damage

            if Knight.hp < 1:
                Knight.hp = 0
                Knight.alive = False
                Knight.death()
            else:
                Clock.schedule_once(lambda dt: self.delay_hurt_animation(Knight), 3.5)
                Clock.schedule_once(lambda dt: self.run_back(), 1.5)
                self.dash()

            self.action = 1
            self.frame_index = 0
            self.update_time = Clock.get_time()
            self.game_instance.show_damage_text(Knight, damage)
            
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = Clock.get_time()
        self.game_instance.play_random_Bandit_sound()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = Clock.get_time()

    def delay_hurt_animation(self, Knight):
        Knight.hurt()
       
    def dash(self):
        self.action = 4 
        self.frame_index = 0
        self.update_time = Clock.get_time()

        dash_animation =  Animation(pos=(self.original_position[0] -1300, self.original_position[1]), duration=0.8)
        dash_animation.start(self.image)
    
    def run_back(self):
        self.run_back_animation = Animation(pos=self.original_position, duration= 0.8)
        self.run_back_animation.start(self.image)
        self.Run()
    
    def Run(self):
        self.action = 5  
        self.frame_index = 0
        self.update_time = Clock.get_time()
        
    def use_potion(self):
        current_time = Clock.get_time()
        if current_time - self.last_potion_time > self.potion_cooldown and self.potions > 0:
            self.hp += 20 
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.potions -= 1
            self.last_potion_time = current_time
            self.game_instance.update_health_bars()  
        
            # Display healing text
            heal_text = Label(text="Opponent  Healed +20 HP!", color=(0, 1, 0, 1))  
            heal_text.pos = (140, -330)  
            self.game_instance.add_widget(heal_text) 
          
            Clock.schedule_once(lambda dt: self.game_instance.remove_widget(heal_text), 2.0)

class Boss(Widget):
    def __init__(self, x, y, name, hp, max_hp, strength, potions, game_instance, **kwargs):
        super(Boss, self).__init__(**kwargs)
        self.original_position = (x, y)
        self.image = Image(source=f'Sprites/{name}/Idle/0.png', allow_stretch=True)
        self.add_widget(self.image)
        self.image.pos = self.original_position
        self.image.size = (1000, 1000)
        self.game_instance = game_instance
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead , 4:dash , 5:Run
        self.update_time = 0  
        self.potion_cooldown = 10  
        self.last_potion_time = 0 

        self.load_images()

    def load_images(self):
        # This is For Load images for each animation state
        for state in ["Idle", "Attack", "Hurt", "Death", "Dash", "Run"]:
            temp_list = []
            for i in range(8 if state == "Idle" else (8 if state == "Run" else(6 if state == "Death" else (6 if state == "Attack" else (8 if state == "Dash" else (4 if state == "Hurt" else 0)))))):
                img = f'Sprites/{self.name}/{state}/{i}.png'
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self, dt):
        animation_cooldown = 0.1  

        # Update image
        self.image.source = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if Clock.get_time() - self.update_time > animation_cooldown:
            self.update_time = Clock.get_time()
            self.frame_index += 1

        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = Clock.get_time()

    def attack(self, Knight):
        if Knight.alive:
            rand = random.randint(4, 20)
            damage = self.strength + rand
            Knight.hp -= damage

            if Knight.hp < 1:
                Knight.hp = 0
                Knight.alive = False
                Knight.death()
            else:
                Clock.schedule_once(lambda dt: self.delay_hurt_animation(Knight), 3.5)
                Clock.schedule_once(lambda dt: self.run_back(), 1.5)
                self.dash()

            self.action = 1
            self.frame_index = 0
            self.update_time = Clock.get_time()
            self.game_instance.show_damage_text(Knight, damage)
            
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = Clock.get_time()
        self.game_instance.play_random_Bandit_sound()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = Clock.get_time()

    def delay_hurt_animation(self, Knight):
        Knight.hurt()
       
    def dash(self):
        self.action = 4 
        self.frame_index = 0
        self.update_time = Clock.get_time()

        dash_animation =  Animation(pos=(self.original_position[0] -1300, self.original_position[1]), duration=0.8)
        dash_animation.start(self.image)
    
    def run_back(self):
        self.run_back_animation = Animation(pos=self.original_position, duration= 0.8)
        self.run_back_animation.start(self.image)
        self.Run()
    
    def Run(self):
        self.action = 5  
        self.frame_index = 0
        self.update_time = Clock.get_time()
        
    def use_potion(self):
        current_time = Clock.get_time()
        if current_time - self.last_potion_time > self.potion_cooldown and self.potions > 0:
            self.hp += 20 
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.potions -= 1
            self.last_potion_time = current_time
            self.game_instance.update_health_bars()  
        
            # Display healing text
            heal_text = Label(text="Bandit healed by 20 HP!", color=(0, 1, 0, 1))  
            heal_text.pos = (140, -330)  
            self.game_instance.add_widget(heal_text) 
              
            Clock.schedule_once(lambda dt: self.game_instance.remove_widget(heal_text), 2.0)

class Potion(Button):
    def __init__(self,cooldown_duration=10, **kwargs):
        super(Potion, self).__init__(**kwargs)
        self.background_normal = 'Sprites/Icons/potion.png'
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.bind(on_press=self.use_potion)
        self.potion_count = 3  
        self.potion_count_label = Label(text=str(self.potion_count))
        self.update_potion_count_label_position()
        self.add_widget(self.potion_count_label)
        self.cooldown_duration = cooldown_duration
        self.cooldown_active = False 
        self.last_used_time = 0 
        self.bind(pos=self.update_potion_count_label_position)

    def update_potion_count_label_position(self, *args):
        # Update position of potion count label relative to Potion button
        offset = 35
        self.potion_count_label.pos = (self.pos[0] + self.width - self.potion_count_label.width - offset,self.pos[1] + 30)

    def use_potion(self, *args):
        if not self.cooldown_active:
            if self.potion_count > 0:
                self.potion_count -= 1
                self.potion_count_label.text = str(self.potion_count)
                heal_text = Label(text="Knight healed HP!", color=(0, 1, 0, 1))  
                heal_text.pos = (-140,-330)  
                self.parent.add_widget(heal_text) 
            self.cooldown_active = True 
            self.last_used_time = Clock.get_time() 
            Clock.schedule_once(self.end_cooldown, self.cooldown_duration)
            Clock.schedule_once(lambda dt: self.parent.remove_widget(heal_text), 2.0)
            self.heal_knight()  
        else:
            pass
    def end_cooldown(self, dt):
        self.cooldown_active = False

    def heal_knight(self):
        # Heal the Knight
        if self.parent and isinstance(self.parent, MyGame): 
            game_instance = self.parent
            game_instance.heal_knight()  
        elif isinstance(self.parent, MyGame3):
            game_instance = self.parent
            game_instance.heal_knight3()
        elif isinstance(self.parent, BossFight):
            game_instance = self.parent
            game_instance.heal_knight4()
  
class HealthBar(Widget):
    def __init__(self, x, y, hp, max_hp, **kwargs):
        super(HealthBar, self).__init__(**kwargs)
        self.height = 40
        self.size_hint = (None, None)
        self.original_x = x 
        self.original_y = y 
        self.pos = (x, y)
        self.hp = hp
        self.max_hp = max_hp
        self.draw()

        self.hp_label = Label(text=f"{self.hp}%", pos=(x + 100, y - 20), size=(360, 80))
        self.add_widget(self.hp_label)

    def draw(self):
        with self.canvas:
            Color(1, 0, 0, 1) 
            self.background = Rectangle(pos=self.pos, size=(300, self.height))
            Color(0, 1, 0, 1) 
            health_width = (self.hp / self.max_hp) * 300
            self.health = Rectangle(pos=self.pos, size=(health_width, self.height))

    def update_health(self, hp, max_hp):
        self.hp = hp
        self.max_hp = max_hp
        self.hp_label.text = f"{self.hp}%"  
        health_width = (self.hp / self.max_hp) * 300
        self.health.size = (health_width, self.height)
        
class DamageText(Label):
    def __init__(self, x, y, damage, colour, **kwargs):
        super().__init__(**kwargs)
        self.text = str(damage)
        self.font_size = '50sp'
        self.color = colour
        self.counter = 0
        self.pos = (0, -300)
        self.parent_widget = None  
        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        if self.parent_widget: 
            self.y += 1 
            self.counter += 1
            if self.counter > 180:
                self.parent_widget.remove_widget(self)

class Portal(Widget):
    def __init__(self, x, y, name, game_instance, **kwargs):
        super(Portal, self).__init__(**kwargs)
        self.original_position = (x, y)
        self.image = Image(source=f'Sprites/{name}/Idle/0.png', allow_stretch=True)
        self.add_widget(self.image)
        self.image.pos = self.original_position
        self.image.size = (400, 400)
        self.game_instance = game_instance
        self.name = name
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:open 2:close
        self.update_time = 0  
        self.load_images()

    def load_images(self):
        # This is For Load images for each animation state
        for state in ["idle", "Open", "Close"]:
            temp_list = []
            for i in range(8 if state == "idle" else  (7 if state == "Open" else (8 if state == "Close" else 0))):
                img = f'Sprites/{self.name}/{state}/{i}.png'
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self, dt):
        animation_cooldown = 0.1  

        # Update image
        self.image.source = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since the last update
        if Clock.get_time() - self.update_time > animation_cooldown:
            self.update_time = Clock.get_time()
            self.frame_index += 1

        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = Clock.get_time()
   
    def Open(self):
        self.action = 1
        self.frame_index = 0
        self.update_time = Clock.get_time() 
    
    def Closed(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = Clock.get_time() 

    def open_portal(self):
        self.Open()

class AttackButton(ButtonBehavior, Image):
    def __init__(self, knight_attack_callback, allow_stretch=True, **kwargs):
        super().__init__(**kwargs)
        self.original_source  ='Sprites/Icons/Attack.png'
        self.source = self.original_source
        self.size_hint = (None, None)
        self.size = (110, 110)
        self.pos = (120, 150)
        self.knight_attack_callback = knight_attack_callback
        self.allow_stretch = allow_stretch
        self.enabled = True
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.enabled:
            self.knight_attack_callback(self)  
            self.enabled = False 
            self.source = 'Sprites/Icons/NoAttack1.png'
            Clock.schedule_once(self.enable_button, 12.7) 
            return True
        return super().on_touch_down(touch)
    
    def enable_button(self, dt):
        self.enabled = True
        self.source = self.original_source 

class RestartButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'Sprites/Icons/restart.png' 
        self.allow_stretch = True 
        self.size_hint = (None, None)
        self.size = (250, 100) 

class Next(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'Sprites/Icons/Next.png'  
        self.allow_stretch = True  
        self.size_hint = (None, None)
        self.size = (230, 80) 

class VictoryPicture(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'Sprites/Icons/victory.png'
        self.allow_stretch = True  
        self.size_hint = (None, None)
        self.size = (500, 600) 
        self.pos = (720,600)

class DefeatPicture(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'Sprites/Icons/defeat.png'  
        self.allow_stretch = True 
        self.size_hint = (None, None)
        self.size = (500, 600) 
        self.pos = (720,600)

class VolumeButton(ButtonBehavior, Image):
    def __init__(self, volume_callback=None, **kwargs):
        super(VolumeButton, self).__init__(**kwargs)
        self.volume_level = 0.5
        self.low_volume_image = "Sprites/Icons/not_mute.png" 
        self.high_volume_image = "Sprites/Icons/mute.png"  
        self.size = (50, 50) 
        self.pos = (880, -470) 
        self.update_image() 
        self.bind(on_press=self.change_volume)
        self.volume_callback = volume_callback

    def update_image(self):
        if self.volume_level <= 0.5:
            self.source = self.low_volume_image
        else:
            self.source = self.high_volume_image

    def change_volume(self, *args):
        if self.volume_level <= 0.5:
            self.volume_level = 1.0 
        else:
            self.volume_level = 0.0 
        self.update_image()
        if self.volume_callback:
            self.volume_callback(self.volume_level)

class MyGame(Screen):
    def __init__(self, **kwargs):
        super(MyGame, self).__init__(**kwargs)
        self.sound = None
        self.volume_button = VolumeButton(volume_callback=self.change_sound_volume)
        self.add_widget(self.volume_button)
   
    def change_sound_volume(self, volume_level):
        if self.sound:
            self.sound.volume = volume_level
       
        for sound in self.sword_sounds:
            if sound:
                sound.volume = volume_level * 0.3 
        
        if self.bandit_dead_sound:
            self.bandit_dead_sound.volume = volume_level * 0.5
       
        if self.Knight_dead_sound:
            self.Knight_dead_sound.volume = volume_level * 0.5
        
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = volume_level * 0.8
       
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = volume_level * 0.8
      
    def on_enter(self):
        self.sound = SoundLoader.load("Sprites/OST/BanditOST.mp3") 
        if self.sound:
            self.sound.volume = 0.5
            self.sound.play()
       
        self.sword_sounds = [SoundLoader.load("Sprites/OST/Sword/Sword1.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword2.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword3.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword4.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword5.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword6.mp3"),]
        
        for sound in self.sword_sounds:
            if sound:
                sound.volume = 0.5

        self.bandit_dead_sound = SoundLoader.load("Sprites/OST/Bandit/BanditDeath.mp3")
        if self.bandit_dead_sound :
            self.bandit_dead_sound .volume = 0.7

        self.Knight_dead_sound = SoundLoader.load("Sprites/OST/Knight/KnightDeath.mp3")
        if self.Knight_dead_sound :
            self.Knight_dead_sound .volume = 0.7   
        
        self.Knight_sounds = [SoundLoader.load("Sprites/OST/Knight/Knight_Hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt6.mp3")
                             ]
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = 0.8
        self.Bandit_sounds = [SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Bandit/Bandit_hurt6.mp3")
                             ]
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = 0.8
        
        self.last_played_sound = None
        self.background_widget = BackgroundWidget() 
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Bandit(x=1120, y=250, name="Bandit", max_hp=75,hp=1, strength=0, potions=3, game_instance=self)
        self.Portal= Portal(x=0, y=350, name="Portal", game_instance=self)
        self.add_widget(self.background_widget)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        Clock.schedule_interval(self.update, 1/60)
        self.transition = FadeTransition(duration=1.5)
        self.button = AttackButton(knight_attack_callback=self.Knight_Attack,allow_stretch=True)
        self.add_widget(self.button)
        self.volume_button = VolumeButton()
        self.add_widget(self.volume_button)
        layout = BoxLayout(orientation='vertical')
        self.Knight_hurt_sound = random.choice(self.Knight_sounds)
        self.health_bar1 = HealthBar(x=600, y=160, hp=self.Knight.hp, max_hp=self.Knight.max_hp, width=200, height=30)
        self.health_bar2 = HealthBar(x=1020, y=160, hp=self.Bandit.hp, max_hp=self.Bandit.max_hp, width=200, height=30)
        self.restart_button = RestartButton(pos=(820, 750))
        self.restart_button.bind(on_press=self.restart_game)
        self.Next = Next(pos=(850, 755))
        self.Next.bind(on_press=self.GoNextRouind)
        self.victory_picture = None 
        self.defeat_picture = None 
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
        self.add_widget(self.health_bar1)
        self.add_widget(self.health_bar2)

    def show_restart_button(self):
        if not self.restart_button.parent: 
            self.add_widget(self.restart_button)
    
    def remove_restart_button(self):
        if self.restart_button.parent:  
            self.remove_widget(self.restart_button)
            self.remove_widget(self.Portal)

    def enable_button(self, dt):
        self.Next.disabled = False
        self.restart_button.disabled = False

    def update_health_bars(self):
        self.health_bar1.update_health(self.Knight.hp, self.Knight.max_hp)
        self.health_bar2.update_health(self.Bandit.hp, self.Bandit.max_hp)

    def play_random_sword_sound(self):
        if self.sword_sounds:
            available_sounds = [sound for sound in self.sword_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_random_Knight_sound(self):
        if self.Knight_sounds:
            available_sounds = [sound for sound in self.Knight_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound
    
    def play_random_Bandit_sound(self):
        if self.Bandit_sounds:
            available_sounds = [sound for sound in self.Bandit_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_bandit_dead_sound(self):
        if self.bandit_dead_sound:
            self.bandit_dead_sound.play()
    
    def play_knight_dead_sound(self):
        if self.Knight_dead_sound:
            self.Knight_dead_sound.play()

    def Knight_Attack(self, instance):
        if self.Knight.alive and self.Bandit.alive:  
            self.Knight.dash()
            Clock.schedule_once(lambda dt: self.execute_attack(), 0.7) 
                  
    def execute_attack(self):
        if self.Knight.alive and self.Bandit.alive:
            self.Knight.attack(self.Bandit)
            damage = self.Knight.strength
            self.Bandit.hp -= damage
            self.update_health_bars()  
            Clock.schedule_once(self.bandit_attack, 4.5)
            self.check_button_state()
            self.button.disabled = True 
            self.play_random_sword_sound()           
        if not self.Bandit.alive: 
                self.play_bandit_dead_sound()  
                self.show_victory_picture()

    def bandit_attack(self, dt):
        if self.Bandit.alive and self.Knight.alive:  
            self.Bandit.dash()   
            Clock.schedule_once(lambda dt: self.execute_bandit_attack(), 2.0)
            self.button.disabled = True 

    def execute_bandit_attack(self):
        if self.Knight.alive and self.Bandit.alive:
           self.Bandit.attack(self.Knight)
           damage = self.Bandit.strength  
           self.Knight.hp -= damage
           self.update_health_bars()  
           self.play_random_sword_sound() 
           Clock.schedule_once(self.enable_button, 5.0) 
        if not self.Knight.alive: 
                self.play_knight_dead_sound()          
                self.show_defeat_picture()

    def show_damage_text(self, target, damage):
    # Show Damge That's Deal to each other
        x, y = target.center_x, target.top + 20 
        colour = (1, 0, 0, 1)  
        damage_text = DamageText(x, y, damage, colour)
        self.add_widget(damage_text)  
        damage_text.parent_widget = self  
    
    def show_victory_picture(self):
        if not self.victory_picture:
            self.victory_picture = VictoryPicture() 
            self.add_widget(self.victory_picture)      
            self.Next.disabled = True 
            Clock.schedule_once(self.open_portal, 3.0)
            Clock.schedule_once(self.enable_next_button, 3.0)  
            self.add_widget(self.Next)
    
    def enable_next_button(self, dt):
        self.Next.disabled = False 
            
    def show_defeat_picture(self):
        if not self.defeat_picture:
            self.defeat_picture = DefeatPicture() 
            self.add_widget(self.defeat_picture)
            self.show_restart_button()

    def open_portal(self, dt):
        self.add_widget(self.Portal)
        if self.Portal:
            self.Portal.Open() 
            
    def check_button_state(self):
     if not self.Knight.alive or not self.Bandit.alive:
        self.button.disabled = True
        Clock.unschedule(self.execute_attack) 
        Clock.unschedule(self.execute_bandit_attack)  
     else:
        self.button.disabled = False

    def enable_button(self, dt):
        self.button.disabled = False 

    def update(self, dt):
        self.Knight.update(dt)
        self.Bandit.update(dt)
        self.Portal.update(dt)
        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            # Check if Bandit's health is less than 30% and will use potion
            if not hasattr(self, 'potion_delay_event'):
                delay = random.uniform(5,8)  
                self.potion_delay_event = Clock.schedule_once(self.use_bandit_potion, delay)

    def use_bandit_potion(self, dt):
        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            self.Bandit.use_potion()
            del self.potion_delay_event 

    def restart_game(self, instance):
       # This is for Restart Game
        self.remove_widget(self.Knight)
        self.remove_widget(self.Bandit)
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Boss(x=1120, y=250, name="Bandit", max_hp=75,hp=75, strength=0, potions=3, game_instance=self)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        self.update_health_bars()
        self.check_button_state()
        self.remove_restart_button()
        self.button.disabled = False
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
        
        if self.victory_picture:
            self.remove_widget(self.victory_picture)
            self.victory_picture = None      
        
        if self.defeat_picture:
            self.remove_widget(self.defeat_picture)
            self.defeat_picture = None

    def heal_knight(self):
        # Heal the Knight
        if self.Knight.alive:
            self.Knight.hp += 30 
            if self.Knight.hp > self.Knight.max_hp:
                self.Knight.hp = self.Knight.max_hp
            self.update_health_bars() 
            Clock.schedule_once(self.bandit_attack, 1)
   
    def GoNextRouind(self, instance):
        self.Knight.RunPortal()
        Clock.schedule_once(self.delayed_transition, 2.7)
   
    def delayed_transition(self, dt):
        self.manager.transition = self.transition  
        self.manager.current = 'Portal2'
        if self.sound:
            self.sound.stop() 

class PoratalLoad2(Screen):
    def __init__(self, **kwargs):
        super(PoratalLoad2, self).__init__(**kwargs)
        self.Portal = Portal(x=800, y=350, name="Portal", game_instance=self)
        self.add_widget(self.Portal)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 3.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'game3'
    
    def update(self, dt):
        self.Portal.update(dt)

class PortalLoad1(Screen):
    def __init__(self, **kwargs):
        super(PortalLoad1, self).__init__(**kwargs)
        self.Portal = Portal(x=800, y=350, name="Portal", game_instance=self)
        self.add_widget(self.Portal)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 3.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'game'
    
    def update(self, dt):
        self.Portal.update(dt)

class Introl1(Screen):
    def __init__(self, **kwargs):
        super(Introl1, self).__init__(**kwargs)
        self.background_widget = IntroOne() 
        self.add_widget(self.background_widget)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 4.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'intro2'
    
    def update(self, dt):
            pass
    
class Introl2(Screen):
    def __init__(self, **kwargs):
        super(Introl2, self).__init__(**kwargs)
        self.background_widget = Intro2() 
        self.add_widget(self.background_widget)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 4.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'intro3'
    
    def update(self, dt):
            pass

class Introl3(Screen):
    def __init__(self, **kwargs):
        super(Introl3, self).__init__(**kwargs)
        self.background_widget = Intro3() 
        self.add_widget(self.background_widget)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 4.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'intro5'
    
    def update(self, dt):
            pass

class Introl5(Screen):
    def __init__(self, **kwargs):
        super(Introl5, self).__init__(**kwargs)
        self.background_widget = IntroLast() 
        self.add_widget(self.background_widget)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 4.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'menu'
    
    def update(self, dt):
            pass
    
class Introl4(Screen):
    def __init__(self, **kwargs):
        super(Introl4, self).__init__(**kwargs)
        self.background_widget = Intro4() 
        self.add_widget(self.background_widget)
        Clock.schedule_interval(self.update, 1/60)
    
    def on_enter(self):
        Clock.schedule_once(self.switch_to_my_game, 4.0)

    def switch_to_my_game(self, dt):
        self.manager.current = 'After'
    
    def update(self, dt):
            pass

class MyGame3(Screen):
    def __init__(self, **kwargs):
        super(MyGame3, self).__init__(**kwargs)
        self.sound = None
        self.volume_button = VolumeButton(volume_callback=self.change_sound_volume)
        self.add_widget(self.volume_button)
    
    def change_sound_volume(self, volume_level):
        if self.sound:
            self.sound.volume = volume_level
        for sound in self.sword_sounds:
            if sound:
                sound.volume = volume_level * 0.3 
        
        if self.bandit_dead_sound:
            self.bandit_dead_sound.volume = volume_level * 0.5
        
        if self.Knight_dead_sound:
            self.Knight_dead_sound.volume = volume_level * 0.5
       
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = volume_level * 0.8
       
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = volume_level * 0.8
    
    def on_enter(self):
        self.sound = SoundLoader.load("Sprites/OST/OST3.mp3") 
        if self.sound:
            self.sound.volume = 0.4
            self.sound.play()
        self.sword_sounds = [SoundLoader.load("Sprites/OST/Sword/Sword1.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword2.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword3.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword4.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword5.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword6.mp3"),]
        for sound in self.sword_sounds:
            if sound:
                sound.volume = 0.5

        self.bandit_dead_sound = SoundLoader.load("Sprites/OST/Boss/Boss_Death.mp3")
        if self.bandit_dead_sound :
            self.bandit_dead_sound .volume = 0.6

        self.Knight_dead_sound = SoundLoader.load("Sprites/OST/Knight/KnightDeath.mp3")
        if self.Knight_dead_sound :
            self.Knight_dead_sound .volume = 0.6   
        
        self.Knight_sounds = [SoundLoader.load("Sprites/OST/Knight/Knight_Hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt6.mp3")
                             ]
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = 0.8
        self.Bandit_sounds = [SoundLoader.load("Sprites/OST/Boss/Boss_Hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt6.mp3")
                             ]
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = 0.8
        
        self.last_played_sound = None
        self.background_widget = BackgroundWidget2() 
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Boss(x=1200, y=0, name="Boss", max_hp=30,hp=1, strength=0, potions=3, game_instance=self)
        self.Portal= Portal(x=0, y=350, name="Portal", game_instance=self)
        self.add_widget(self.background_widget)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        Clock.schedule_interval(self.update, 1/60)
        self.transition = FadeTransition(duration=1.5)
        self.button = AttackButton(knight_attack_callback=self.Knight_Attack,allow_stretch=True)
        self.add_widget(self.button)
        self.volume_button = VolumeButton()
        self.add_widget(self.volume_button)
        layout = BoxLayout(orientation='vertical')
        self.Knight_hurt_sound = random.choice(self.Knight_sounds)
        self.health_bar1 = HealthBar(x=600, y=160, hp=self.Knight.hp, max_hp=self.Knight.max_hp, width=200, height=30)
        self.health_bar2 = HealthBar(x=1020, y=160, hp=self.Bandit.hp, max_hp=self.Bandit.max_hp, width=200, height=30)
        self.restart_button = RestartButton(pos=(820, 750))
        self.restart_button.bind(on_press=self.restart_game)
        self.victory_picture = None 
        self.defeat_picture = None 
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
        self.add_widget(self.health_bar1)
        self.add_widget(self.health_bar2)
       
    def show_restart_button(self):
        if not self.restart_button.parent: 
            self.add_widget(self.restart_button)
        
    def remove_restart_button(self):
        if self.restart_button.parent:  
            self.remove_widget(self.restart_button)

    def enable_button(self, dt):
        self.Next.disabled = False
        self.restart_button.disabled = False

    def update_health_bars(self):
        self.health_bar1.update_health(self.Knight.hp, self.Knight.max_hp)
        self.health_bar2.update_health(self.Bandit.hp, self.Bandit.max_hp)

    def play_random_sword_sound(self):
        if self.sword_sounds:
            available_sounds = [sound for sound in self.sword_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_random_Knight_sound(self):
        if self.Knight_sounds:
            available_sounds = [sound for sound in self.Knight_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound
    
    def play_random_Bandit_sound(self):
        if self.Bandit_sounds:
            available_sounds = [sound for sound in self.Bandit_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_bandit_dead_sound(self):
        if self.bandit_dead_sound:
            self.bandit_dead_sound.play()
    
    def play_knight_dead_sound(self):
        if self.Knight_dead_sound:
            self.Knight_dead_sound.play()

    def Knight_Attack(self, instance):
        if self.Knight.alive and self.Bandit.alive:  
            self.Knight.dash()
            Clock.schedule_once(lambda dt: self.execute_attack(), 0.7) 
                   
    def execute_attack(self):
        if self.Knight.alive and self.Bandit.alive:
            self.Knight.attack(self.Bandit)
            damage = self.Knight.strength
            self.Bandit.hp -= damage
            self.update_health_bars()  
            Clock.schedule_once(self.bandit_attack, 4.5)
            self.check_button_state()
            self.button.disabled = True 
            self.play_random_sword_sound()         
        if not self.Bandit.alive: 
                self.play_bandit_dead_sound()              
                self.show_victory_picture()

    def bandit_attack(self, dt):
        if self.Bandit.alive and self.Knight.alive:  
            self.Bandit.dash()   
            Clock.schedule_once(lambda dt: self.execute_bandit_attack(), 2.0)
            self.button.disabled = True 

    def execute_bandit_attack(self):
        if self.Knight.alive and self.Bandit.alive:
           self.Bandit.attack(self.Knight)
           damage = self.Bandit.strength  
           self.Knight.hp -= damage
           self.update_health_bars()  
           self.play_random_sword_sound() 
           Clock.schedule_once(self.enable_button, 5.0) 
        if not self.Knight.alive: 
                self.play_knight_dead_sound()                
                self.show_defeat_picture()

    def show_damage_text(self, target, damage):
    # Show Damge That's Deal to each other
        x, y = target.center_x, target.top + 20 
        colour = (1, 0, 0, 1)  
        damage_text = DamageText(x, y, damage, colour)
        self.add_widget(damage_text)  
        damage_text.parent_widget = self  
    
    def show_victory_picture(self):
        if not self.victory_picture:
            self.victory_picture = VictoryPicture() 
            self.add_widget(self.victory_picture)      
            Clock.schedule_once(self.transition_to_intro4, 4)

    def show_defeat_picture(self):
        if not self.defeat_picture:
            self.defeat_picture = DefeatPicture() 
            self.add_widget(self.defeat_picture)
            self.show_restart_button()
   
    def transition_to_intro4(self, dt):
        self.manager.current = 'intro4'  # Transition to Intro4 screen
        if self.sound:
            self.sound.stop() 
           
    def check_button_state(self):
     if not self.Knight.alive or not self.Bandit.alive:
        self.button.disabled = True
        Clock.unschedule(self.execute_attack) 
        Clock.unschedule(self.execute_bandit_attack)  
     else:
        self.button.disabled = False

    def enable_button(self, dt):
        self.button.disabled = False 

    def update(self, dt):
        self.Knight.update(dt)
        self.Bandit.update(dt)
        self.Portal.update(dt)

        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            # Check if Bandit's health is less than 30% and will use potion
            if not hasattr(self, 'potion_delay_event'):
                delay = random.uniform(5,8)  
                self.potion_delay_event = Clock.schedule_once(self.use_bandit_potion, delay)

    def use_bandit_potion(self, dt):
        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            self.Bandit.use_potion()
            del self.potion_delay_event 
    
    def restart_game(self, instance):
       # This is for Restart Game
        self.remove_widget(self.Knight)
        self.remove_widget(self.Bandit)
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Boss(x=1200, y=0, name="Boss", max_hp=30,hp=30, strength=0, potions=3, game_instance=self)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        self.update_health_bars()
        self.check_button_state()
        self.remove_restart_button()
        self.button.disabled = False
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
       
        if self.victory_picture:
            self.remove_widget(self.victory_picture)
            self.victory_picture = None
       
        if self.defeat_picture:
            self.remove_widget(self.defeat_picture)
            self.defeat_picture = None

    def heal_knight3(self):
        # Heal the Knight
        if self.Knight.alive:
            self.Knight.hp += 15 
            if self.Knight.hp > self.Knight.max_hp:
                self.Knight.hp = self.Knight.max_hp
            self.update_health_bars() 
            Clock.schedule_once(self.bandit_attack, 1)

class BossFight(Screen):
    def __init__(self, **kwargs):
        super(BossFight, self).__init__(**kwargs)
        self.sound = None
        self.volume_button = VolumeButton(volume_callback=self.change_sound_volume)
        self.add_widget(self.volume_button)
    def change_sound_volume(self, volume_level):
        if self.sound:
            self.sound.volume = volume_level
        
        for sound in self.sword_sounds:
            if sound:
                sound.volume = volume_level * 0.3 
        
        if self.bandit_dead_sound:
            self.bandit_dead_sound.volume = volume_level * 0.5
        
        if self.Knight_dead_sound:
            self.Knight_dead_sound.volume = volume_level * 0.5
        
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = volume_level * 0.8
        
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = volume_level * 0.8

    def on_enter(self):
        self.sound = SoundLoader.load("Sprites/OST/OST2.mp3") 
        if self.sound:
            self.sound.volume = 0.4
            self.sound.play()
        self.sword_sounds = [SoundLoader.load("Sprites/OST/Sword/Sword1.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword2.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword3.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword4.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword5.mp3"),
                             SoundLoader.load("Sprites/OST/Sword/Sword6.mp3"),]
        for sound in self.sword_sounds:
            if sound:
                sound.volume = 0.8

        self.bandit_dead_sound = SoundLoader.load("Sprites/OST/Boss/Boss_Death.mp3")
        if self.bandit_dead_sound :
            self.bandit_dead_sound .volume = 0.5

        self.Knight_dead_sound = SoundLoader.load("Sprites/OST/Knight/KnightDeath.mp3")
        if self.Knight_dead_sound :
            self.Knight_dead_sound .volume = 0.8  
        
        self.Knight_sounds = [SoundLoader.load("Sprites/OST/Knight/Knight_Hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Knight/Knight_Hurt6.mp3")
                             ]
        for sound in self.Knight_sounds:
            if sound:
                sound.volume = 0.8
        self.Bandit_sounds = [SoundLoader.load("Sprites/OST/Boss/Boss_Hurt1.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt2.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt3.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt4.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt5.mp3"),
                             SoundLoader.load("Sprites/OST/Boss/Boss_Hurt6.mp3")
                             ]
        for sound in self.Bandit_sounds:
            if sound:
                sound.volume = 0.8
        self.last_played_sound = None
        self.background_widget = BackgroundWidget2() 
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Boss(x=1200, y=0, name="Boss", max_hp=120,hp=120, strength=0, potions=3, game_instance=self)
        self.Portal= Portal(x=0, y=350, name="Portal", game_instance=self)
        self.add_widget(self.background_widget)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        Clock.schedule_interval(self.update, 1/60)
        self.transition = FadeTransition(duration=1.5)
        self.button = AttackButton(knight_attack_callback=self.Knight_Attack,allow_stretch=True)
        self.add_widget(self.button)
        self.volume_button = VolumeButton()
        self.add_widget(self.volume_button)
        layout = BoxLayout(orientation='vertical')
        self.Knight_hurt_sound = random.choice(self.Knight_sounds)
        self.health_bar1 = HealthBar(x=600, y=160, hp=self.Knight.hp, max_hp=self.Knight.max_hp, width=200, height=30)
        self.health_bar2 = HealthBar(x=1020, y=160, hp=self.Bandit.hp, max_hp=self.Bandit.max_hp, width=200, height=30)
        self.restart_button = RestartButton(pos=(820, 750))
        self.restart_button.bind(on_press=self.restart_game)
        self.victory_picture = None 
        self.defeat_picture = None 
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
        self.add_widget(self.health_bar1)
        self.add_widget(self.health_bar2)
       
    def show_restart_button(self):
        if not self.restart_button.parent: 
            self.add_widget(self.restart_button)

    def remove_restart_button(self):
        if self.restart_button.parent:  
            self.remove_widget(self.restart_button)

    def enable_button(self, dt):
        self.Next.disabled = False
        self.restart_button.disabled = False

    def update_health_bars(self):
        self.health_bar1.update_health(self.Knight.hp, self.Knight.max_hp)
        self.health_bar2.update_health(self.Bandit.hp, self.Bandit.max_hp)

    def play_random_sword_sound(self):
        if self.sword_sounds:
            available_sounds = [sound for sound in self.sword_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_random_Knight_sound(self):
        if self.Knight_sounds:
            available_sounds = [sound for sound in self.Knight_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound
    
    def play_random_Bandit_sound(self):
        if self.Bandit_sounds:
            available_sounds = [sound for sound in self.Bandit_sounds if sound != self.last_played_sound]
            if available_sounds:
                random_sound = random.choice(available_sounds)
                if random_sound:
                    random_sound.play()  
                    self.last_played_sound = random_sound

    def play_bandit_dead_sound(self):
        if self.bandit_dead_sound:
            self.bandit_dead_sound.play()
    
    def play_knight_dead_sound(self):
        if self.Knight_dead_sound:
            self.Knight_dead_sound.play()

    def Knight_Attack(self, instance):
        if self.Knight.alive and self.Bandit.alive:  
            self.Knight.dash()
            Clock.schedule_once(lambda dt: self.execute_attack(), 0.7) 
             
    def execute_attack(self):
        if self.Knight.alive and self.Bandit.alive:
            self.Knight.attack(self.Bandit)
            damage = self.Knight.strength
            self.Bandit.hp -= damage
            self.update_health_bars()  
            Clock.schedule_once(self.bandit_attack, 4.5)
            self.check_button_state()
            self.button.disabled = True 
            self.play_random_sword_sound()
            
        if not self.Bandit.alive: 
                self.play_bandit_dead_sound() 
                
                self.show_victory_picture()

    def bandit_attack(self, dt):
        if self.Bandit.alive and self.Knight.alive:  
            self.Bandit.dash()   
            Clock.schedule_once(lambda dt: self.execute_bandit_attack(), 2.0)
            self.button.disabled = True 

    def execute_bandit_attack(self):
        if self.Knight.alive and self.Bandit.alive:
           self.Bandit.attack(self.Knight)
           damage = self.Bandit.strength  
           self.Knight.hp -= damage
           self.update_health_bars()  
           self.play_random_sword_sound() 
           Clock.schedule_once(self.enable_button, 5.0) 
        if not self.Knight.alive: 
                self.play_knight_dead_sound() 
                self.show_defeat_picture()

    def show_damage_text(self, target, damage):
        # Show Damge That's Deal to each other
        x, y = target.center_x, target.top + 20 
        colour = (1, 0, 0, 1)  
        damage_text = DamageText(x, y, damage, colour)
        self.add_widget(damage_text)  
        damage_text.parent_widget = self  
    
    def show_victory_picture(self):
        if not self.victory_picture:
            self.victory_picture = VictoryPicture() 
            self.add_widget(self.victory_picture)      
            self.show_restart_button()
              
    def show_defeat_picture(self):
        if not self.defeat_picture:
            self.defeat_picture = DefeatPicture() 
            self.add_widget(self.defeat_picture)
            self.show_restart_button()
   
    def check_button_state(self):
     if not self.Knight.alive or not self.Bandit.alive:
        self.button.disabled = True
        Clock.unschedule(self.execute_attack) 
        Clock.unschedule(self.execute_bandit_attack)  
     else:
        self.button.disabled = False

    def enable_button(self, dt):
        self.button.disabled = False 

    def update(self, dt):
        self.Knight.update(dt)
        self.Bandit.update(dt)
        self.Portal.update(dt)

        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            # Check if Bandit's health is less than 30% and will use potion
            if not hasattr(self, 'potion_delay_event'):
                delay = random.uniform(5,8)  
                self.potion_delay_event = Clock.schedule_once(self.use_bandit_potion, delay)

    def use_bandit_potion(self, dt):
        if self.Bandit.alive and self.Bandit.hp < self.Bandit.max_hp * 0.4:
            self.Bandit.use_potion()
            del self.potion_delay_event 

    def restart_game(self, instance):
       # This is for Restart Game
        self.remove_widget(self.Knight)
        self.remove_widget(self.Bandit)
        self.Knight = Fighter(x=0, y=220, name="Knight", max_hp=100,hp=100, strength=0, potions=3, game_instance=self)
        self.Bandit= Boss(x=1200, y=0, name="Boss", max_hp=120,hp=120, strength=0, potions=3, game_instance=self)
        self.add_widget(self.Knight)
        self.add_widget(self.Bandit)
        self.update_health_bars()
        self.check_button_state()
        self.remove_restart_button()
        self.button.disabled = False
        self.potion = Potion()
        self.potion.pos = (122, 40)
        self.add_widget(self.potion)
        
        if self.victory_picture:
            self.remove_widget(self.victory_picture)
            self.victory_picture = None
       
        if self.defeat_picture:
            self.remove_widget(self.defeat_picture)
            self.defeat_picture = None

    def heal_knight4(self):
        # Heal the Knight
        if self.Knight.alive:
            self.Knight.hp += 25  
            if self.Knight.hp > self.Knight.max_hp:
                self.Knight.hp = self.Knight.max_hp
            self.update_health_bars() 
            Clock.schedule_once(self.bandit_attack, 1)

class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(Introl1(name='intro1'))
        sm.add_widget(Introl2(name='intro2'))
        sm.add_widget(Introl3(name='intro3'))
        sm.add_widget(Introl4(name='intro4'))
        sm.add_widget(Introl5(name='intro5'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PortalLoad1(name='Portal1'))
        sm.add_widget(MyGame(name='game'))
        sm.add_widget(PoratalLoad2(name='Portal2'))
        sm.add_widget(MyGame3(name='game3'))
        sm.add_widget(BossFight(name='After'))

        return sm

if __name__ == '__main__':
    MyApp().run()
