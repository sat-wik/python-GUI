import time
import datetime
from urllib.request import urlopen
from win10toast import ToastNotifier
import requests
from PIL import ImageTk, Image
import io



try:
  #for python 2
  import Tkinter as tk
  from Tkinter import *
except ImportError:
  #for python 3
  import tkinter as tk
  from tkinter import *

timeWait = True

#Here is a very minimal example which does not take into account the edges of the screen:
#To make the window draggable, put bindings for <Button-1> (mouse clicks) and <B1-Motion> (mouse movements) on the window.
class Win(tk.Tk):
    
    def __init__(self, master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self._offsetx = 0
        self._offsety = 0

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int (screen_width * 2 / 3 ) 
        y_coordinate = 0
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate))

        self.bind('<Button-3>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        self.bind('<Double-1>', self.double_click)

        self.clock = Label(self, font = ('arial', 14, 'bold'), bg = 'lightgreen')
        self.clock.grid(row=0, column=1)

    def double_click(self, event):
        self.destroy()
   
    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
      import threading
      from win10toast import ToastNotifier
      import PySimpleGUI as sg

      class clock(object):
          """Timer"""
          def __init__(self):
              self.default_mins = 20
              self.font = "Courier"
              self.font_size = 12
              self.application_name = "WASS Timer"
              self.win10_toaster = ToastNotifier()
              pass

          def show_toast(self, task):
              """show win10 toast"""
              toaster = ToastNotifier()
              toaster.show_toast(self.application_name,
                                 "Task: " + task + " over.",
                                 icon_path=None,
                                 duration=8,
                                 threaded=True)

          def run(self):
              """run"""
              layout = [
                          [sg.Text('Task', size=(8, 1), font=(self.font, self.font_size), key="_TASK1_")],
                          [sg.InputText('', do_not_clear=True, key='_TASK2_')],
                          [sg.Text('Minutes', size=(8, 1), font=(self.font, self.font_size), key="_CYCLE1_")],
                          [sg.Spin(values=[i for i in range(1, 121)],
                                   initial_value=self.default_mins, size=(6, 1), key="_CYCLE2_")],
                          [sg.Text('00:00:00', size=(15, 1), font=(self.font, 28),
                                   justification='center', key='_COUNT_DOWN_')],
                          [sg.Button('start', font=(self.font, self.font_size), focus=True),
                           sg.Button('stop/continue', font=(self.font, self.font_size), focus=False),
                           sg.Button('reset', focus=False, font=(self.font, self.font_size)),
                           sg.Quit(font=(self.font, self.font_size))]]

              window = sg.Window('WASS Timer').Layout(layout)

              is_clock_running = False
              current_left_seconds = 0
              # Event Loop
              while True:
                  event, values = window.Read(1000)
                  current_left_seconds -= 1 * (is_clock_running is True)
                  if current_left_seconds == 0 and is_clock_running: # Pomodoro over
                      task = str(values["_TASK2_"])
                      # show toast in thread
                      sub_thread = threading.Thread(target=self.show_toast, args=(task,))
                      sub_thread.start()
                      is_clock_running = False
                  if event == "start":
                      is_clock_running = True
                      clock_mins = int(values["_CYCLE2_"])
                      current_left_seconds = clock_mins * 60
                      # current_left_seconds = 3
                      window.FindElement('_TASK1_').Update(visible=False)
                      window.FindElement('_CYCLE1_').Update(visible=False)
                      window.FindElement('_TASK2_').Update(visible=False)
                      window.FindElement('_CYCLE2_').Update(visible=False)
                  if event == "stop/continue":
                      is_clock_running = not is_clock_running
                  if event == "reset":
                      window.FindElement('_CYCLE2_').Update(self.default_mins)
                      current_left_seconds = self.default_mins * 60
                      # current_left_seconds = 3
                      is_clock_running = False
                      window.FindElement('_TASK1_').Update(visible=True)
                      window.FindElement('_CYCLE1_').Update(visible=True)
                      window.FindElement('_TASK2_').Update(visible=True)
                      window.FindElement('_CYCLE2_').Update(visible=True)
                  if event is None or event == 'Quit':  # if user closed the window using X or clicked Quit button
                      break
                  # print(current_left_seconds, "debug")
                  window.FindElement('_COUNT_DOWN_').Update(
                      '{:02d}:{:02d}:{:02d}'.format(current_left_seconds // 3600, current_left_seconds // 60,
                                                    current_left_seconds % 60))


      if __name__ == "__main__":
          # toaster = ToastNotifier()
          # toaster.show_toast("Example two", "This notification is in it's own thread!", icon_path=None, duration=5)

          gui = clock()
          gui.run()


        
        

    #display clock
    def tick(self):
      hour_min_str = time.strftime("%I:%M")
      apm_str = time.strftime("%p")[:1].lower()
      date_str = datetime.date.today().strftime(" %A")[0:4]
      today_str = datetime.date.today().strftime(" %m/%d")  
      self.clock.config(text = hour_min_str + apm_str + date_str + today_str)
      self.clock.after(200, self.tick)

    def timer(self):
        info = StringVar()
        time.sleep(10)
        api_address = "http://api.openweathermap.org/data/2.5/weather?q="
        country_code = ",us&appid=4502b2f6e6b7449973a30ad9d5adc592&units=imperial"
        city = "Redlands"

        url = api_address + city + country_code
        json_data = requests.get(url).json()

        if "message" in json_data:
          info.set("Invalid City")

        else:
          city = json_data["name"]
          description = json_data["weather"][0]["description"]

          toaster = ToastNotifier()
          toaster.show_toast(city,
                             description,
                             icon_path=None,
                             duration=5,
                             threaded=True)
        
        
        
      


##display clcok
#def tick():
#  hour_min_str = time.strftime("%I:%M")
#  apm_str = time.strftime("%p")[:1].lower()
#  date_str = datetime.date.today().strftime(" %A")[0:4]
#  today_str = datetime.date.today().strftime(" %m/%d")  
#  clock.config(text = hour_min_str + apm_str + date_str + today_str)
#  clock.after(200, tick)
  
#GUI call to display clock
app=Win()
app.tick()
app.timer()
app.mainloop()
sys.exit()
