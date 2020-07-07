from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty,ObjectProperty
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.event import EventDispatcher
from kivymd.uix.button import MDRectangleFlatButton,MDRoundFlatButton,MDRectangleFlatButton,MDRaisedButton
import json 
import requests
import time
from kivy.network.urlrequest import UrlRequest
import random
from urllib.request import urlopen
from kivy.uix.popup import Popup
from kivy.graphics import Color
import urllib.parse
import urllib.request
import inspect, os
import _thread
import threading
from kivy.core.window import Window
from database import DataBase
Window.clearcolor = (.666, 1, .372, 1)
# Register fonts
LabelBase.register(
	name="Roboto",
	fn_regular="Quando.ttf",
	fn_bold="Quando.ttf"
)
class Question():
	def __init__(self, question, answer, option2, option3, option4, correct):
		self.question = question
		self.answer = answer
		self.option2 = option2
		self.option3 = option3
		self.option4 = option4
		self.correct = correct
class ListQuestions():
	def __init__(self,directory="/questions"):
		self.directory = directory
		self.questions_python = []
		self.read_questions()
	def get_question_python(self):
		return self.questions_python[random.randint(0, len(self.questions_python) - 1 )]
	def read_questions(self):		
		with open(os.getcwd()+'/questions/firebase.json') as json_file:
			json_data = json.load(json_file)
			for q in json_data:
				if(q["category"] =="python"):
					self.questions_python.append(Question(q["quest"], q["answer"], q["option2"], q["option3"], q["option4"], q["correct"]))
				else:
					print("else")
	def update(self):
		url = "https://samplefirebaseapp-3de75.firebaseio.com/export.json"
		response = request.get(url)
		data = json.load(response)
		with open(os.getcwd()+'/questions/firbase.json', 'w') as outfile:# w is write mode or r is read mode
			json.dump(data, outfile)
		print(os.getcwd())
class NextScreen(Screen):
	pass

class TaskCreator():
	def __init__(self):
		self.questions = ListQuestions()

	def get_task(self, mode=1):
		question_1 = ""
		answers_1 = ""
		option_1 = ""
		option_2 = ""
		option_3 = ""
		option_4 = ""
		correct_1 = ""

		if mode == 2:
			question_python = self.questions.get_question_python()
			question_1 = question_python.question
			answers_1 = question_python.answer
			option_1 = question_python.answer
			option_2 = question_python.option2
			option_3 = question_python.option3
			option_4 = question_python.option4 
			correct_1 = question_python.correct
			
		operands = [question_1, answers_1]
		answers = [option_1, option_2, option_3, option_4]
		random.shuffle(answers)
		whole_task = operands + answers + [correct_1]
		return whole_task    
class AboutScreen(Screen):
	def about_text(self):
		return "Hi =)\n" \
			   "This is a simple project.\n" 
class CreateAccount(Screen):
	namee = ObjectProperty(None)
	email = ObjectProperty(None)
	password = ObjectProperty(None)
	def submit(self):
		if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
			if self.password != "":
				db.add_user(self.email.text, self.password.text, self.namee.text)
				self.reset()
				self.manager.current = "menu"
			else:
				invalidForm()
		else:
			invalidForm()

	def login(self):
		self.reset()
		self.manager.current = "login"

	def reset(self):
		self.email.text = ""
		self.password.text = ""
		self.namee.text = ""

class StartScreen(Screen):
	pass
class SigninWindow(Screen):
	email = ObjectProperty(None)
	password = ObjectProperty(None)

	def loginBtn(self):
		if db.validate(self.email.text, self.password.text):
			MainWindow.current = self.email.text
			self.reset()
			self.manager.current = "menu"
			
		else:
			invalidLogin()

	def createBtn(self):
		self.reset()
		self.manager.current = "create"

	def reset(self):
		self.email.text = ""
		self.password.text = ""
		


class HelpScreen(Screen):
	def help_text(self):
		return "Hi \n" \
			   "This game will provide you some questions about General Knowledge.\n" \
			   
class Menu(Screen):
	def update_game(self):
		pop = Popup(title='Updating', content=Label(text='Questions been updated'), auto_dismiss=False)
		pop.open()
		Clock.schedule_once(self.update, 0)
		pop.dismiss()
		
	def update(self,event):
		l = ListQuestions()
		l.update()  

class ActionScreen(Screen):
	errors_made = 0
	round_number = 1
	max_rounds = 2
	count = 0
	task_values = [0, 0, 0, 0, 0, 0, 0] # list for quest,amswer,opt1,opt2,opt3,opt4
	current_mode = 1
	def new_game(self):
		self.Tasks = TaskCreator()
		self.round_number = 0
		self.count = 0
		self.errors_made = 0
		self.set_next_task()
		#when it shows first question round becomes 1
	
	def set_next_task(self):
		self.task_values = self.Tasks.get_task(self.current_mode)
		self.ids.task.text = self.task_values[0]
		self.ids.button_1.text = str(self.task_values[2])
		self.ids.button_2.text = str(self.task_values[3])
		self.ids.button_3.text = str(self.task_values[4])
		self.ids.button_4.text = str(self.task_values[5])
		Clock.schedule_once(self.update_label, 1)
		self.ids.label_1.text = "Errors: " + str(self.errors_made)
		#self.ids.label_2.text = str(self.current_mode) + str(self.current_mode)
		self.ids.label_2.text = "Score: " + str(self.count)
		self.ids.label_3.text = str(self.round_number) + " / " + str(self.max_rounds)
		self.ids.button_1.background_normal = "./data/normal.png"
		self.ids.button_2.background_normal = "./data/normal.png"
		self.ids.button_3.background_normal = "./data/normal.png"
		self.ids.button_4.background_normal = "./data/normal.png"
	def update_label(self, *args):
		cut_off = 20
		self.ids.label_4.text = str(int(self.ids.label_4.text) + 1)
		if int(self.ids.label_4.text) < cut_off:
			Clock.schedule_once(self.update_label, 1)
	def check_answer(self, button_pressed):
		if button_pressed.text == self.task_values[1]:
			button_pressed.background_normal = './data/correct.png'
			self.round_number += 1
			self.count += 2
			self.errors_made = 0
			self.ids.label_2.text = "Score :"+str(self.count)
			self.ids.label_1.text = "Errors: " + str(self.errors_made)
			self.ids.label_3.text = str(self.round_number) + " / " + str(self.max_rounds)
					#when answer is wrong it goes to else part
		else:
			self.round_number += 1
			self.ids.label_3.text = str(self.round_number) + " / " + str(self.max_rounds)
			self.ids.label_2.text = "Score :"+str(self.count)
			self.errors_made += 1
			self.ids.label_1.text = "Errors: " + str(self.errors_made)
			self.ids.task.markup = True
			#it shows incorrect button in red colour
			self.ids.task.text = '[color=#ff3333]'+self.task_values[6]+'[/color]'
			button_pressed.background_normal = './data/error.png'  
	
		if self.round_number == self.max_rounds:
			self.manager.current = 'result'
		else:
			t2 = threading.Thread(target=self.response)
			t2.start()
	def response(self):     
		time.sleep(1)#update widgets after specific time
		self.ids.button_1.disabled = True
		self.ids.button_2.disabled = True
		self.ids.button_3.disabled = True
		self.ids.button_4.disabled = True    
		time.sleep(1)
		self.ids.button_1.disabled = False
		self.ids.button_2.disabled = False
		self.ids.button_3.disabled = False
		self.ids.button_4.disabled = False
		self.set_next_task()
class ResultScreen(Screen):
	def calculate_result(self, screen):
		if screen.errors_made <= 1:
			self.ids.star_5.source = './data/star.png'
			self.ids.star_4.source = './data/star.png'
			self.ids.star_3.source = './data/star.png'
			self.ids.star_2.source = './data/star.png'
			self.ids.star_1.source = './data/star.png'
			self.ids.label.text = 'Excellent!\n\n'
		elif screen.errors_made <= 2:
			self.ids.star_4.source = './data/star.png'
			self.ids.star_3.source = './data/star.png'
			self.ids.star_2.source = './data/star.png'
			self.ids.star_1.source = './data/star.png'
			self.ids.label.text = 'Very good!\n\n Close to perfect. Keep up!'
		elif screen.errors_made <= 4:
			self.ids.star_3.source = './data/star.png'
			self.ids.star_2.source = './data/star.png'
			self.ids.star_1.source = './data/star.png'
			self.ids.label.text = 'Good!\n\n Train more!'
		elif screen.errors_made <= 6:
			self.ids.star_2.source = './data/star.png'
			self.ids.star_1.source = './data/star.png'
			self.ids.label.text = 'Good!\n\n Train more!'
		elif screen.errors_made <= 8:
			self.ids.star_1.source = './data/star.png'
			self.ids.label.text = 'Good!\n\n Train more!'
		else:
			self.ids.label.text = 'Okay...\n\n Try again to get all the stars!'
		self.ids.label_4.text = "Score:" +str(screen.count)
class PopUpQuit(Popup):
	pass
class SignupWindow(Screen):
	pass
def invalidLogin():
	pop = Popup(title='Invalid Login',
				  content=Label(text='Invalid username or password.'),
				  size_hint=(None, None), size=(400, 400))
	pop.open()


def invalidForm():
	pop = Popup(title='Invalid Form',content=Label(text='Please fill in all inputs with valid information.'),
				  size_hint=(None, None), size=(400, 400))

	pop.open()
db = DataBase("users.txt")

class MainWindow(Screen):
	n = ObjectProperty(None)
	created = ObjectProperty(None)
	email = ObjectProperty(None)
	current = ""

	def logOut(self):
		self.manager.current = "login"

	def on_enter(self, *args):
		password, name, created = db.get_user(self.current)
		self.n.text = "Account Name: " + name
		self.email.text = "Email: " + self.current
		self.created.text = "Created On: " + created

class MainApp(MDApp):
	sm = ScreenManager(transition=FadeTransition())
	def build(self):
		self.sm.add_widget(SigninWindow(name='login'))
		self.sm.add_widget(Menu(name='menu'))
		self.sm.add_widget(ActionScreen(name='game'))
		self.sm.add_widget(MainWindow(name='main'))
		self.sm.add_widget(StartScreen(name='start'))
		self.sm.add_widget(NextScreen(name='progress'))
		self.sm.add_widget(HelpScreen(name='help'))
		self.sm.add_widget(AboutScreen(name='about'))
		self.sm.add_widget(ResultScreen(name='result'))
		self.sm.add_widget(SignupWindow(name='signup'))
		self.sm.add_widget(CreateAccount(name = 'create'))

		#Bind to keyboard to make the back button under android work
		Window.bind(on_keyboard=self.handle_keyboard)
		self.title = 'GenerealKnowledgeQuiz'
		return self.sm
	def handle_keyboard(self, window, key, *largs):
		#keycode 273 equals up button, just for test purposes
		if key == 27 or key == 273:
			if self.sm.current_screen.name == 'game':
				popup = PopUpQuit()
				popup.open()
			elif self.sm.current_screen.name == 'menu':
				quit()

			return True

if __name__ == '__main__':
	MainApp().run()
