# made by MDQUE

import serial
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

	def __init__(self):
# Init the UI
		Gtk.Window.__init__(self, title="Fuck U")
		
# Set up the Header Bar
		header_bar = Gtk.HeaderBar()
		header_bar.set_show_close_button(True)
		header_bar.set_title("Drawer App V1.0")
		Setup_button = Gtk.Button(label = "Setup")
		Setup_button.connect("clicked", self.Setup_dialog)
		header_bar.pack_start(Setup_button)
		Load_button = Gtk.Button(label= "Load Code")
		Load_button.connect("clicked", self.Load_menu)
		header_bar.pack_end(Load_button)
		self.set_titlebar(header_bar)
		
# Set up The main panel Layout
#		self.box = Gtk.Box(spacing=3)
#		self.add(self.box)
		grid = Gtk.Grid()
		self.add(grid)
		
		Treeview_placeholder = Gtk.Box(spacing = 3)
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		Codeprocess_placeholder = Gtk.Box(spacing = 3)
		Answer_placeholder = Gtk.Box(spacing = 3)
		
		grid.attach(Treeview_placeholder, 0, 0, 2, 2)
		grid.attach(listbox, 2, 0 , 1, 1)
		grid.attach(Codeprocess_placeholder, 0, 2, 2, 1 )
		grid.attach(Answer_placeholder, 2, 1, 2, 2)
		
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox.pack_start(vbox, True, True, 0)

		
#		self.button1 = Gtk.Button(label="Hello")
#		self.button1.connect("clicked", self.on_button1_clicked)
#		self.box.pack_start(self.button1, True, True, 0)
#		
#		self.button2 = Gtk.Button(label="Goodbye")
#		self.button2.connect("clicked", self.on_button2_clicked)
#		self.box.pack_start(self.button2, True, True, 0)
#		
#	def on_button1_clicked(self, widget):
#		print("Hello")
#		self.button1.set_label("nello")
#	
#	def on_button2_clicked(self, widget):
#		print("Goodbye")
		
	def Setup_dialog(self,widget):
		print("Setup mode entered")
		
	def Load_menu(self,widget):
		print("opening the load Menu")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


#port = serial.Serial("/dev/ttyUSB0", baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=3.0)
##port.open()
#while (port.is_open):
#		port.write(b'#')
#		port.write(b't')
#		port.write(b'e')
#		port.write(b's')
#		port.write(b't')
#		port.write(b'$')
#		print ("msg sent out")
#		rcv = port.read(10)
#		print(rcv)

