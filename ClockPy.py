from tkinter import Tk, Frame, Button, PhotoImage, Label, Toplevel, Spinbox
from tkinter.colorchooser import askcolor
from playsound import playsound
import sys
import time 
import sqlite3

		# =============================================
		# =           ClockPy Program                 =
		# =============================================

class MyGUI():

	def __init__(self, root, frame):

		self.root = root
		self.root.title("ClockPy")
		#self.root.resizable(0,0)
		self.root.maxsize(width=385, height=550)
		self.root.minsize(width=385, height=550)
		self.root.iconbitmap("./icons/clock.ico")
		self.frame = frame

		# -----------  Function Refresh Clock  -----------
		
		def tick():
			time_string = time.strftime("%I:%M")
			time_string2 = time.strftime(":%S")
			time_day = time.strftime("%a, %d %B")
			time_m = time.strftime("%p")
			self.clock.config(text=time_string)
			self.clock_s.config(text=time_string2)
			self.clock_d.config(text=time_day)
			self.clock_m.config(text=time_m)
			self.clock.after(200, tick)

		# -----------  Function DataBASE  -----------
		#Load database
		db_name = 'database.db'
		# Operation database
		query = 'SELECT * FROM color' 		
		query_alarm = 'SELECT * FROM alarm' 
		query2 = 'UPDATE color SET hexa=?'
		query_alarm2 = 'UPDATE alarm SET state=?'
		query_alarm3 = 'UPDATE alarm SET hours=?, minutes=?, meridiam=?'

		# Database Consult Update
		def db_query(query, parameters =(), alarm = None):
			with sqlite3.connect(db_name) as conn:
				cursor = conn.cursor()
				result = cursor.execute(query, parameters)
				conn.commit()
				if(parameters==()):
					if(alarm==None):
						for row in result:
							return row[1]
					else: 
						for row in result:
							return row[1:5]

		hexa_c = db_query(query)
		self.frame.config(width="385", height="550", bg=hexa_c)

		# -----------  Function Check Status Alarm  -----------

		def check_alarm():
			self.data_alarm_check = db_query(query_alarm, alarm = "Y")
			time_check_h = time.strftime("%I")
			time_check_m = time.strftime("%M")
			time_check_mr = time.strftime("%p")
			time_check_s = time.strftime("%S")

			if(self.data_alarm_check[0] < 10):
				hours_check = "0" + str(self.data_alarm_check[0])
			else: 
				hours_check = str(self.data_alarm_check[0])

			if(self.data_alarm_check[1] < 10):
				minutes_check = "0" + str(self.data_alarm_check[1])
			else:
				minutes_check = str(self.data_alarm_check[1])

			# Check Alarm and playsound
			if(self.data_alarm_check[3]=="on"):
				if(time_check_s == "00"):
					if(time_check_h == hours_check):
						if(time_check_m == minutes_check):
							if(time_check_mr== self.data_alarm_check[2]):
								playsound("./sound/alarm_sound.mp3")
								self.root.deiconify()
								self.root.focus_set()

			self.root.after(1000, check_alarm)

		# -----------  Windows Clock Alarm  -----------

		def windows():

			hexa_c = db_query(query)
			self.main_wn = Toplevel(self.root, takefocus=True, bg=hexa_c)
			self.main_wn.focus_force()
			self.main_wn.title("ClockPy Alarm")
			self.main_wn.geometry("320x158")
			self.main_wn.resizable(0,0)
			self.main_wn.iconbitmap("./icons/clock.ico")
			self.main_wn.grab_set() 


			self.date_alarm = db_query(query_alarm, alarm = "Y")
			self.img_on = PhotoImage(file="./icons/on.png")
			self.img_off = PhotoImage(file="./icons/off.png")
			self.img_menu = PhotoImage(file="./icons/menu.png")

			self.switch = self.date_alarm[3]

			def check_state_alarm():

				if(self.date_alarm[0]<10):
					self.lb_hours.config(text="0" + str(self.date_alarm[0]))
				else:
					self.lb_hours.config(text=self.date_alarm[0])

				if(self.date_alarm[1]<10):
					self.lb_minutes.config(text= ":0"+ str(self.date_alarm[1]))
				else:
					self.lb_minutes.config(text= ":"+ str(self.date_alarm[1]))

				self.lb_meridiam.config(text=self.date_alarm[2])
				if(self.switch=="on"):
					self.bt_switch.config(image=self.img_on)
				else:
					self.bt_switch.config(image=self.img_off)

			def change_switch():
				if(self.switch=="off"):
					self.bt_switch.config(image=self.img_on)
					self.switch = "on"
					db_query(query_alarm2, ("on",))
				else: 
					self.bt_switch.config(image=self.img_off)
					self.switch = "off"
					db_query(query_alarm2, ("off",))
				
			self.space_alarm = Frame(self.main_wn, width=300, height=100, bg="white" )
			self.space_alarm.place(x=10, y=20)

			self.lb_hours = Label(self.space_alarm, font=("Roboto Light", 54), bg="white")
			self.lb_hours.place(x=10, y=0)

			self.lb_minutes = Label(self.space_alarm, font=("Roboto Light", 54), bg="white")
			self.lb_minutes.place(x=90, y=0)

			self.lb_meridiam = Label(self.space_alarm, font=("Roboto Light", 14), bg="white")
			self.lb_meridiam.place(x=190, y=15)

			self.bt_switch = Button(self.space_alarm, activebackground="white", command=lambda:change_switch())
			self.bt_switch.config(bg="white", bd=0, highlightthickness=0, relief='flat')
			self.bt_switch.place(x=245, y=10)

			self.bt_config_alarm = Button(self.space_alarm, image=self.img_menu, activebackground="white")
			self.bt_config_alarm.config(bg="white", bd=0, highlightthickness=0, relief='flat', command=lambda:setting_alarm())
			self.bt_config_alarm.place(x=250, y= 55)
			check_state_alarm()


			# -----------  Windows Settings Alarm  -----------
			
			def setting_alarm():

				self.settings_wn = Toplevel(self.main_wn, bg=hexa_c, takefocus=True)
				self.settings_wn.focus_force()
				self.settings_wn.geometry("470x165")
				self.settings_wn.iconbitmap("./icons/clock.ico")
				self.settings_wn.grab_set()
				self.settings_wn.resizable(0,0)
				self.settings_wn.title("ClockPy Alarm")

				self.space_alarm2 = Frame(self.settings_wn, width=450, height=100, bg="white" )
				self.space_alarm2.place(x=10, y=20)


				self.select_hours = Spinbox(self.space_alarm2, from_=1, to=12, width=2, font=("Roboto Light", 50), bd=0, relief='flat', activebackground="white",textvariable=2, state="readonly")
				self.select_hours.config(buttondownrelief="flat", readonlybackground="white")
				self.select_hours.place(x=10, y=5)

				self.select_minutes = Spinbox(self.space_alarm2, from_=00, to=59, format="%02.0f", width=2, font=("Roboto Light", 50), bd=0, relief='flat', activebackground="white")
				self.select_minutes.config(buttondownrelief="flat", readonlybackground="white", state="readonly")
				self.select_minutes.place(x=150, y=5)
				
				self.select_meridiam = Spinbox(self.space_alarm2, values=("AM", "PM"), width=3, font=("Roboto Light", 50), bd=0, relief='flat', activebackground="white")
				self.select_meridiam.config(buttondownrelief="flat", readonlybackground="white", state="readonly")
				self.select_meridiam.place(x=285, y=5)

				self.bt_save_sttg = Button(self.settings_wn, text="Save", font=("Roboto Light", 12), bd=0, relief="flat", bg="white", command=lambda:save_sttg())
				self.bt_save_sttg.place(x=415, y=125)

				def save_sttg():
					h = self.select_hours.get()
					m = self.select_minutes.get()
					md = self.select_meridiam.get()
					db_query(query_alarm3,(h, m, md,))
					self.date_alarm = db_query(query_alarm, alarm = "Y")
					check_state_alarm()
					self.settings_wn.destroy()				


		# -----------  Function Change Color  -----------
		
		def change_color():		
			rgb, hexa = askcolor()
			self.frame.config(bg=hexa)
			self.clock.config(bg=hexa)
			self.clock_s.config(bg=hexa)
			self.clock_m.config(bg=hexa)
			self.clock_d.config(bg=hexa)
			self.button1.config(bg=hexa, activebackground=hexa)
			self.button2.config(bg=hexa, activebackground=hexa)
			#self.lb.config(bg=hexa)
			# Update Value color database
			if(hexa!=None):
				db_query(query2,(hexa,))

		# -----------  Clock Configure  -----------

		# Clock Hours Minutes
		self.clock = Label(self.frame, font=("Roboto Light", 64), bg=hexa_c, foreground="white")
		self.clock.place(x=65, y=150)
		# Clock Seconds
		self.clock_s = Label(self.frame, font=("Roboto Light", 22), bg=hexa_c, foreground="white")
		self.clock_s.place(x=272, y=200)
		# Clock Meridiem
		self.clock_m = Label(self.frame, font=("Roboto Light", 22), bg=hexa_c, foreground="white")
		self.clock_m.place(x=272, y=165)
		# Day Month
		self.clock_d = Label(self.frame, font=("Roboto Light", 14), bg=hexa_c, foreground="white")
		self.clock_d.place(x=80, y=240)
		tick()
		check_alarm()

		# -----------  Button Change Color  -----------

		self.img= PhotoImage(file="./icons/color.png")	
		self.img2= PhotoImage(file="./icons/alarm.png")		

		# Button Pallete Colors
		self.button1= Button(self.frame, image=self.img, activebackground=hexa_c, command=lambda:change_color())
		self.button1.config(bg=hexa_c, bd=0, highlightthickness=0, relief='flat')
		self.button1.place(x=5, y=505)

		# Button Settings
		self.button2= Button(self.frame, image=self.img2, activebackground=hexa_c,command=lambda:windows())
		self.button2.config(bg=hexa_c, bd=0, highlightthickness=0, relief='flat')
		self.button2.place(x=340, y=505)
		self.frame.pack()
		

if __name__=='__main__':
	root = Tk()
	frm = Frame(root)
	gui = MyGUI(root, frm)
	root.mainloop()

			# ======   End of ClockPy Program       =======