import random
from kivy.uix.popup import Popup

from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.button import Button
import datetime
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from neurosdk.scanner import Scanner
from em_st_artifacts.utils import lib_settings
from em_st_artifacts.utils import support_classes
from em_st_artifacts import emotional_math
from neurosdk.cmn_types import *
from threading import Thread

import concurrent.futures

from threading import Thread


class MainMenu(Screen):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        Window.size = (800, 600)
        background = Image(source="юфу.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        layout = RelativeLayout()

        rand = random.randint(1, 3)
        if rand == 1:
            title_label = Label(text="Добро пожаловать в приложение Каста\n     Совет дня, меньше играй в игры)", font_size=60,pos_hint={'center_x': 0.5, 'center_y': 0.7})
        elif rand == 2:
            title_label = Label(text="Добро пожаловать в приложение Каста\nСледи за здоровьем не только в игре!", font_size=60,pos_hint={'center_x': 0.5, 'center_y': 0.7})
        elif rand == 3:
            title_label = Label(text="Добро пожаловать в приложение Каста\nТы зависим от игр? Ты киберспортсмен)", font_size=60,pos_hint={'center_x': 0.5, 'center_y': 0.7})

        layout.add_widget(title_label)

        button1 = Button(
            text="Новая игра",
            size_hint=(None, None),
            size=(dp(400), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        button1.bind(on_press=self.start_new_game)
        layout.add_widget(button1)

        button2 = Button(
            text="Входной тест!",
            size_hint=(None, None),
            size=(dp(400), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        button2.bind(on_press=self.go_to_test)
        layout.add_widget(button2)


        button3 = Button(
            text="Выход",
            size_hint=(None, None),
            size=(dp(400), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        button3.bind(on_press=self.exit_app)
        layout.add_widget(button3)

        self.add_widget(layout)


    def button_pressed(self, button):
        x, y = button.coords
        colors = {0: (0, 1, 0, 1), 1: (1, 1, 1, 1)}
        button.background_color = colors[self.status.defaultvalue[x][y]]
        self.status.defaultvalue[x][y] ^= 1
        print(list(map(lambda x: x.background_color, self.children)))



    def get_buttons(self):
        return self.buttons
    def start_new_game(self, instance):
        # Actions when "Новая игра" button is pressed
        self.manager.current = 'newgame'
        print("Начало новой игры")

    def go_to_test(self, instance):
        popup = Popup(title='Введите ваше имя', size_hint=(None, None), size=(400, 200))

        layout = BoxLayout(orientation='vertical')

        game_name_input = TextInput(hint_text="Имя", multiline=False, size_hint=(None, None), size=(200, 50))
        layout.add_widget(game_name_input)

        confirm_button = Button(text="Подтвердить", size_hint=(None, None), size=(200, 50))
        confirm_button.bind(on_press=lambda instance: self.save_player_name(game_name_input.text, popup))
        layout.add_widget(confirm_button)

        popup.content = layout
        popup.open()
        self.manager.current = 'test'

    def save_player_name(self, player_name, popup):
        file_path = "player_names.txt"
        with open(file_path, "a") as file:
            file.write(player_name + "\n" )
        popup.dismiss()


    def exit_app(self, instance):
        app.stop()


class New_game(Screen):
    def __init__(self, **kwargs):
        super(New_game, self).__init__(**kwargs)

        background = Image(source="юфу2.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        layout = BoxLayout(orientation='vertical')

        title_label = Label(text="Ты купил еще одну игру?)", font_size=100)
        layout.add_widget(title_label)

        game_name_input = TextInput(hint_text="Введите название игры", multiline=False, size_hint=(None, None),
                                    size=(600, 100),pos_hint={'center_x': 0.5, 'center_y': 0.7})
        layout.add_widget(game_name_input)

        confirm_button = Button(text="Подтвердить", size_hint=(None, None), size=(600, 100), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        confirm_button.bind(on_press=lambda instance: self.save_game_name(game_name_input.text))
        layout.add_widget(confirm_button)

        back_button = Button(text="Назад в главное меню", size_hint=(None, None), size=(400, 50))
        back_button.bind(on_press=self.go_back_to_main_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def save_game_name(self, game_name):
        file_path = "game_names.txt"
        with open(file_path, "a") as file:
            file.write(game_name + "\n")

    def go_back_to_main_menu(self, instance):
        self.manager.current = 'main'
class Test(Screen):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        background = Image(source="юфу3.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        flLayout = FloatLayout()
        boxLayout = BoxLayout(orientation='vertical')

        title_label = Label(text="Привет, ты решил поиграть?\nПройди тест и начинай играть!", font_size=70)
        boxLayout.add_widget(title_label)

        title_label = Label(text="Выбери число от 1 до 10\n (это число будет обозначать твое \nэмоционально состояние на данный момент):", font_size=50)
        boxLayout.add_widget(title_label)

        title_label = Label(text="- Очень плохо. У меня депрессия.",font_size=40, pos_hint={'center_x': 0.32, 'center_y': 0.444})
        flLayout.add_widget(title_label)

        title_label = Label(text="- Очень хорошо. Я счастлив.", font_size=40, pos_hint={'center_x': 0.29, 'center_y': 0.065})
        flLayout.add_widget(title_label)
        self.count = 0
        for i in range(1, 11):
            if (i < 4):
                str1 = 1,0, 0, 1
            if (i >=4 and i<=6):
                str1 = 0,1, 1, 1
            if (i > 6):
                str1 = 0,1,0,1
            button = Button(text=str(i), size_hint=(None, None), size=(50, 50),background_color=(str1), pos_hint={'center_x': 0.1, 'center_y': 0.4})
            button.bind(on_press=self.set_flag)
            boxLayout.add_widget(button)

        back_button = Button(text="Назад в главное меню", size_hint=(None, None), size=(400, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        back_button.bind(on_press=self.go_back_to_main_menu)
        boxLayout.add_widget(back_button)

        self.add_widget(boxLayout)
        self.add_widget(flLayout)

    def set_flag(self, instance):
        button_value = instance.text
        print(f"Button {button_value} pressed")
        current_datetime = datetime.datetime.now()

        buttonstr=str({button_value})
        formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        file_path = "output.txt"
        file_path2 = "player_names.txt"
        with open(file_path2, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                print(last_line)
            else:
                print("Файл пуст")
        with open(file_path, "a") as file:
            if (self.count==0):
                file.write("Дата и время захода в игру: ")
                file.write(formatted_datetime)
                file.write(" Имя пользователя: "+ last_line)
                file.write(" <3 Эмоциональное состояние: ")
                file.write(buttonstr)

                import emotions

                self.count += 1
            else:
                if (self.count == 1):
                    file.write("Дата и время выхода из игры: ")
                    file.write(formatted_datetime)
                    file.write(" Имя пользователя: "+ last_line)
                    file.write("<3 Эмоциональное состояние после игры: ")
                    file.write(buttonstr)
                    file.write("\n")
                    self.count = 0


        print(f"Current datetime ({formatted_datetime}) has been written to the file '{file_path}'.")


    def go_back_to_main_menu(self, instance):
        # Go back to the main menu screen
        self.manager.current = 'main'


class KastaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(Test(name='test'))
        sm.add_widget(New_game(name='newgame'))
        return sm

if __name__ == '__main__':
    app = KastaApp()
    app.run()
    th_main = Thread(target=app.run)
    th_main.run()