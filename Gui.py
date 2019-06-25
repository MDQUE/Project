# made by MDQUE

import serial
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


########################################################################################################
########################################### Class Def ##################################################
########################################################################################################
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


###########################################Callbacks##################################

# Callback for the Setup Button
	def Setup_dialog(self,widget):
		print("Setup mode entered")
		win2 = Setup_window()
		win2.connect("destroy", Gtk.main_quit)
		win2.show_all()
		Gtk.main()



# Callback for the "Load Code" Button
	def Load_menu(self,widget):
		
		print("opening the load Menu")
		dialog = Gtk.FileChooserDialog("Please choose a file", self,
																	Gtk.FileChooserAction.OPEN,
																	(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
																	Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.add_filters(dialog)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
				print("Open clicked")
				print("File selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
				print("Cancel clicked")
		dialog.destroy()

# Filter for the Code loading
	def add_filters(self, dialog):
		filter_cpp = Gtk.FileFilter()
		filter_cpp.set_name("C++")
		filter_cpp.add_pattern("*.cpp")
		dialog.add_filter(filter_cpp)
		
		
		
########################################################################################################
########################################### Class Def ##################################################
########################################################################################################
class Setup_window(Gtk.Window):

	def __init__(self):
# Init the UI
		Gtk.Window.__init__(self, title="Setup")
		
		
# Set up The main panel Layout
		grid = Gtk.Grid()
		self.add(grid)
		################################# Settings Box ########################################
		Settingsbox = Gtk.Box();
		Label_RM = Gtk.Label("Set right Margin")
		Label_LM = Gtk.Label("Set left Margin")
		Label_TM = Gtk.Label("Set top Margin")
		Label_BM = Gtk.Label("Set bottom Margin")
		adjustment_RM = Gtk.Adjustment(10.0, 0.0, 400, 1.0, 10, 0)
		adjustment_LM = Gtk.Adjustment(5.0, 0.0, 400, 1, 10, 0)
		adjustment_TM = Gtk.Adjustment(10.0, 0.0, 400, 1, 10, 0)
		adjustment_BM = Gtk.Adjustment(5.0, 0.0, 400, 1, 10, 0)
		self.spinbutton_RM = Gtk.SpinButton()
		self.spinbutton_LM = Gtk.SpinButton()
		self.spinbutton_TM = Gtk.SpinButton()
		self.spinbutton_BM = Gtk.SpinButton()
		self.spinbutton_RM.set_adjustment(adjustment_RM)
		self.spinbutton_LM.set_adjustment(adjustment_LM)
		self.spinbutton_TM.set_adjustment(adjustment_TM)
		self.spinbutton_BM.set_adjustment(adjustment_BM)
		check_SB_RM = Gtk.Button.new_with_label("Apply")
		check_SB_RM.connect("clicked", self.on_check_SB_RM_toggled)
		check_SB_LM = Gtk.Button.new_with_label("Apply")
		check_SB_LM.connect("clicked", self.on_check_SB_LM_toggled)
		check_SB_TM = Gtk.Button.new_with_label("Apply")
		check_SB_TM.connect("clicked", self.on_check_SB_TM_toggled)
		check_SB_BM = Gtk.Button.new_with_label("Apply")
		check_SB_BM.connect("clicked", self.on_check_SB_BM_toggled)
		Settingsgrid = Gtk.Grid()
		Settingsgrid.attach(check_SB_RM, 2, 0, 1, 1)
		Settingsgrid.attach(check_SB_LM, 2, 1, 1, 1)
		Settingsgrid.attach(check_SB_TM, 2, 2, 1, 1)
		Settingsgrid.attach(check_SB_BM, 2, 3, 1, 1)
		Settingsgrid.attach(self.spinbutton_RM, 1, 0, 1, 1)
		Settingsgrid.attach(self.spinbutton_LM, 1, 1, 1, 1)
		Settingsgrid.attach(self.spinbutton_TM, 1, 2, 1, 1)
		Settingsgrid.attach(self.spinbutton_BM, 1, 3, 1, 1)
		Settingsgrid.attach(Label_RM, 0, 0, 1,1)
		Settingsgrid.attach(Label_LM, 0, 1, 1,1)
		Settingsgrid.attach(Label_TM, 0, 2, 1,1)
		Settingsgrid.attach(Label_BM, 0, 3, 1,1)
		Settingsbox.pack_start(Settingsgrid, True, True, 0)
		################################## Everything else ######################################
		Labelbox = Gtk.Box()
		self.Instruction_label = Gtk.Label("This is some Instruction")
		Labelbox.pack_start(self.Instruction_label,True,True, 0)
		Set_reference = Gtk.Button.new_with_label("Set Reference Point")
		Set_reference.connect("clicked", self.on_set_ref_clicked)
		Move_Up = Gtk.Button.new_with_label("Up")
		Move_Up.connect("pressed", self.on_Move_up_Pressed)
		Move_Up.connect("released", self.on_Move_up_Released)
		Move_Right = Gtk.Button.new_with_label("Right")
		Move_Right.connect("pressed", self.on_Move_Right_Pressed)
		Move_Right.connect("released", self.on_Move_Right_Released)
		Move_Left = Gtk.Button.new_with_label("Left")
		Move_Left.connect("pressed", self.on_Move_Left_Pressed)
		Move_Left.connect("released", self.on_Move_Left_Released)
		Move_Down = Gtk.Button.new_with_label("Down")
		Move_Down.connect("pressed", self.on_Move_Down_Pressed)
		Move_Down.connect("released", self.on_Move_Down_Released)
		
		grid.attach(Labelbox, 0, 0, 4, 1)
		grid.attach(Settingsbox, 0, 1 , 1, 3)
		grid.attach(Move_Up, 2, 1 , 1, 1)
		grid.attach(Move_Left, 1, 2 , 1, 1)
		grid.attach(Move_Right, 3, 2 , 1, 1)
		grid.attach(Move_Down, 2, 3, 1, 1)
		grid.attach(Set_reference, 0, 4, 4, 1)
		grid.set_column_homogeneous(True)
		grid.set_row_homogeneous(True)
		
	####################################### Callbacks ###########################################
	def on_set_ref_clicked(self, button):
		print("Refpoint Set")
		
	def on_Move_up_Pressed(self, button):
		print("Move Up")
		
	def on_Move_up_Released(self, button):
		print("end Move Up")
		
	def on_Move_Left_Pressed(self, button):
		print("Move Left")
		
	def on_Move_Left_Released(self, button):
		print("end Move Left")
		
	def on_Move_Right_Pressed(self, button):
		print("Move Right")
		
	def on_Move_Right_Released(self, button):
		print("end Move Right")
		
	def on_Move_Down_Pressed(self, button):
		print("Move Down")
		
	def on_Move_Down_Released(self, button):
		print("end Move Down")
		
	def on_check_SB_LM_toggled(self, button):
		a = self.spinbutton_RM.get_value()
		self.Instruction_label.set_label("Left Margin Set")
		print(a)
		
	def on_check_SB_RM_toggled(self, button):
		a = self.spinbutton_RM.get_value()
		b = self.spinbutton_LM.get_value()
		if (a <= b):
			self.Instruction_label.set_label("Right Margin can,t be smaller/equal to Left Margin!")
			print("ERROR1")
			return
		self.Instruction_label.set_label("Righ Margin Set")
		print(a)
	
	def on_check_SB_BM_toggled(self, button):
		a = self.spinbutton_BM.get_value()
		self.Instruction_label.set_label("Bottom Margin Set")
		print(a)
	
	def on_check_SB_TM_toggled(self, button):
		a = self.spinbutton_TM.get_value()
		b = self.spinbutton_BM.get_value()
		if (a <= b):
			self.Instruction_label.set_label("Top Margin can,t be smaller/equal to Bottom Margin!")
			print("ERROR1")
			return
		self.Instruction_label.set_label("Top Margin Set")
		print(a)
		
		
		########################################################################################################
########################################### Class Def ##################################################
########################################################################################################
class Manual_window(Gtk.Window):

	def __init__(self):
# Init the UI
		Gtk.Window.__init__(self, title="Manual Drive")
		
		
# Set up The main panel Layout
		grid = Gtk.Grid()
		self.add(grid)
		
		Pen_UpDown = Gtk.Button.new_with_label("Put Pen Down")
		Pen_UpDown.connect("clicked", self.on_Pen_pos_clicked)
		Move_Up = Gtk.Button.new_with_label("Up")
		Move_Up.connect("pressed", self.on_Move_up_Pressed)
		Move_Up.connect("released", self.on_Move_up_Released)
		Move_Right = Gtk.Button.new_with_label("Right")
		Move_Right.connect("pressed", self.on_Move_Right_Pressed)
		Move_Right.connect("released", self.on_Move_Right_Released)
		Move_Left = Gtk.Button.new_with_label("Left")
		Move_Left.connect("pressed", self.on_Move_Left_Pressed)
		Move_Left.connect("released", self.on_Move_Left_Released)
		Move_Down = Gtk.Button.new_with_label("Down")
		Move_Down.connect("pressed", self.on_Move_Down_Pressed)
		Move_Down.connect("released", self.on_Move_Down_Released)
		
		grid.attach(Pen_UpDown, 0, 0, 3, 1)
		grid.attach(Move_Up, 1, 1 , 1, 1)
		grid.attach(Move_Left, 0, 2 , 1, 1)
		grid.attach(Move_Right, 2, 2 , 1, 1)
		grid.attach(Move_Down, 1, 3, 1, 1)
		grid.set_column_homogeneous(True)
		grid.set_row_homogeneous(True)
		
	def on_Pen_pos_clicked(self, button):
		if (button.get_label() == "Put Pen Down"):
			button.set_label("Get Pen Up")
		else :
			button.set_label("Put Pen Down")
		print("Pen Pos Changed")
		
	def on_Move_up_Pressed(self, button):
		print("Move Up")
		
	def on_Move_up_Released(self, button):
		print("end Move Up")
		
	def on_Move_Left_Pressed(self, button):
		print("Move Left")
		
	def on_Move_Left_Released(self, button):
		print("end Move Left")
		
	def on_Move_Right_Pressed(self, button):
		print("Move Right")
		
	def on_Move_Right_Released(self, button):
		print("end Move Right")
		
	def on_Move_Down_Pressed(self, button):
		print("Move Down")
		
	def on_Move_Down_Released(self, button):
		print("end Move Down")

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

