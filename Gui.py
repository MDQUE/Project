# made by MDQUE 
# Code release year: 2019
# Version: V1.0

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Pango, GObject, Gdk, GLib
import cairo
import sys
import time
import threading
import math
import serial
import queue


########################################################################################################
##################################### Class Def - Main Window #########################################
########################################################################################################
class MyWindow(Gtk.ApplicationWindow):

	def __init__(self, app):
# Init the UI
		Gtk.Window.__init__(self, title="Main Window", application=app)
		self.set_default_size(-1, 350)
		self.Data_Path = ""
		self.textview_created = False
#		Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
#		self.maximize()
		
# Set up the Header Bar
		header_bar = Gtk.HeaderBar()
		header_bar.set_show_close_button(True)
		header_bar.set_title("Drawer App V1.0")
		Setup_button = Gtk.Button(label = "Setup")
		Setup_button.set_action_name("app.Setup_dialog_invoke")
		header_bar.pack_start(Setup_button)
		Load_button = Gtk.Button(label= "Load Code")
		Load_button.connect("clicked", self.Load_menu)
		header_bar.pack_end(Load_button)
		self.set_titlebar(header_bar)
		
# Set up The main panel Layout
		grid = Gtk.Grid()
		self.add(grid)
		
		self.text_data = "empty"
		self.Code_Box = Gtk.Box()
		listbox = Gtk.Grid()
		New_file = Gtk.Button("New File")
		New_file.connect("clicked", self.create_new_file)
		mainlable2 = Gtk.Label()
		mainlable2.set_label("Manual drive")
		Load_code = Gtk.Button(label= "Run Code")
		Load_code.set_action_name("app.Plot_invoke")
		Draw_preview = Gtk.Button(label= "Draw Preview")
		Draw_preview.set_action_name("app.Draw_field_invoke")
		self.Connect_button = Gtk.Button(label = "Connect MCU")
		self.Connect_button.set_action_name("app.Serial_com_handler_invoke")
		Manual_button = Gtk.Button(label= "x")
		Manual_button.connect("clicked", self.manual_drive)
		listbox.attach(New_file, 0, 0, 2, 1)
		listbox.attach(mainlable2, 0, 1, 1, 1)
		listbox.attach(Manual_button, 1, 1, 1, 1)
		listbox.attach(Draw_preview, 0, 2, 2, 1)
		listbox.attach(self.Connect_button, 0, 3, 2, 1)
		listbox.attach(Load_code, 0, 4, 2, 1)
		
		Codeprocess_placeholder = Gtk.Box()
		Answer_placeholder = Gtk.Box()
		
		grid.attach(self.Code_Box, 0, 0, 2, 2)
		grid.attach(listbox, 2, 0 , 1, 1)
		grid.attach(Codeprocess_placeholder, 0, 2, 2, 1 )
		grid.attach(Answer_placeholder, 2, 1, 2, 2)
		self.Code_Box.set_hexpand(True)
		self.Code_Box.set_vexpand(True)

###########################################Methods###################################

	def update_from_textfield(self):
			x = self.textbuffer.get_start_iter()
			y = self.textbuffer.get_end_iter()
			self.text_data = self.textbuffer.get_text(x,y,True)


	def create_textview(self):
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		self.Code_Box.pack_start(scrolledwindow,True,True,0)
		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		if self.Data_Path != "":
				with open(self.Data_Path, "r") as text:
					self.textbuffer.set_text(text.read())
		else:
				self.textbuffer.set_text("")
		scrolledwindow.add(self.textview)
		self.Code_Box.show_all()
		self.textview_created = True

###########################################Callbacks##################################
	def create_new_file(self, widget):
			if self.textview_created != True:
					self.Data_Path = ""
					self.create_textview()
			else: 
					self.textbuffer.set_text("")




#			self.tag_bold = self.textbuffer.create_tag("bold",
#					weight=Pango.Weight.BOLD)
#			self.tag_italic = self.textbuffer.create_tag("italic",
#					style=Pango.Style.ITALIC)
#			self.tag_underline = self.textbuffer.create_tag("underline",
#					underline=Pango.Underline.SINGLE)
#			self.tag_found = self.textbuffer.create_tag("found",
#					background="yellow")


	def manual_drive(self,widget):
		win3 = Manual_window();
		win3.connect("destroy", Gtk.main_quit)
		win3.show_all()
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
				self.Data_Path = dialog.get_filename()
				if self.textview_created != True:
						self.create_textview()
				else:
						with open(self.Data_Path, "r") as text:
								self.textbuffer.set_text(text.read())
		elif response == Gtk.ResponseType.CANCEL:
				print("Cancel clicked")
		dialog.destroy()

# Filter for the Code loading
	def add_filters(self, dialog):
		filter_Gc = Gtk.FileFilter()
		filter_Gc.set_name("G code")
		filter_Gc.add_pattern("*.gcode")
		dialog.add_filter(filter_Gc)





########################################################################################################
###################################### Class Def - Setup Window #######################################
########################################################################################################
class Setup_window(Gtk.ApplicationWindow):

	def __init__(self, app):
# Init the UI
		Gtk.Window.__init__(self, title="Setup", application = app, type=Gtk.WindowType.TOPLEVEL)
		self.connect("destroy", self.destructuion, app)
		self.execution = 0
		self.margin_setup_count = 0
		
		
# Set up The main panel Layout
		mainbox = Gtk.Box()
		grid = Gtk.Grid()
		mainbox.pack_start(grid, True, 0, 0)
		self.add(mainbox)
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
		Settingsbox.pack_start(Settingsgrid, True, 0, 0)
		Settingsgrid.set_row_homogeneous(True)
		
		
		################################## Everything else ######################################
		Labelbox = Gtk.Box()
		self.Instruction_label = Gtk.Label()
		self.Instruction_label.set_label("Drive to the Left Endstop")
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
		# Buttons for Step size selection
		Stepbox  = Gtk.Box()
		Steplabel = Gtk.Label()
		Steplabel.set_label("Stepsize: ")
		self.X1 = Gtk.ToggleButton.new_with_label("0,1")
		self.X1.connect("pressed", self.on_toggled_X1)
		self.X10 = Gtk.ToggleButton.new_with_label("1")
		self.X10.connect("pressed", self.on_toggled_X10)
		self.X100 = Gtk.ToggleButton.new_with_label("10")
		self.X100.connect("pressed", self.on_toggled_X100)
		self.X100.set_active(True)
		Stepbox.pack_start(Steplabel, True, 0, 0)
		Stepbox.pack_start(self.X1, False, 0, 0)
		Stepbox.pack_start(self.X10, False, 0, 0)
		Stepbox.pack_start(self.X100, False, 0, 0)
		# Checkboxes for Axis Flip
		axflipbox = Gtk.Box()
		Xfliplabel = Gtk.Label()
		Xfliplabel.set_label("Flip X Axis:")
		Yfliplabel = Gtk.Label()
		Yfliplabel.set_label("Flip Y Axis:")
		Xflipcheckbox = Gtk.CheckButton()
		Xflipcheckbox.connect("toggled", self.on_toggled_Xflip)
		Yflipcheckbox = Gtk.CheckButton()
		Yflipcheckbox.connect("toggled", self.on_toggled_Yflip)
		axflipbox.pack_start(Xfliplabel, True, 0, 0)
		axflipbox.pack_start(Xflipcheckbox, False, 0, 0)
		axflipbox.pack_start(Yfliplabel, True, 0, 0)
		axflipbox.pack_start(Yflipcheckbox, False, 0, 0)
		
		grid.attach(Labelbox, 0, 0, 4, 1)
		grid.attach(Settingsbox, 0, 1 , 1, 5)
		grid.attach(Stepbox, 1, 1 , 3, 1)
		grid.attach(Move_Up, 2, 2 , 1, 1)
		grid.attach(Move_Left, 1, 3 , 1, 1)
		grid.attach(Move_Right, 3, 3 , 1, 1)
		grid.attach(Move_Down, 2, 4, 1, 1)
		grid.attach(axflipbox, 1, 5, 3, 1)
		grid.attach(Set_reference, 0, 6, 4, 1)
		print("setup win construction done")
		
	####################################### Callbacks ###########################################
	
	##### Axis inversion Callbacks #####
	
	def on_toggled_Xflip(self, button):
			if button.get_active() == True:
					app.plotset.set_x_inversion(True)
					print("axis inversin set")
			else:
					app.plotset.set_x_inversion(False)
					print("axis inversin reset")
	
	def on_toggled_Yflip(self, button):
			if button.get_active() == True:
					app.plotset.set_y_inversion(True)
					print("axis inversin set")
			else:
					app.plotset.set_y_inversion(False)
					print("axis inversin reset")
	
	##### Stepsize set callbacks #####
	def on_toggled_X1(self, button):
		if self.X1.get_active() != True:
			self.X10.set_active(False)
			self.X100.set_active(False)
			vara = 'S'+ str(int(0.1 / app.plotset.get_Step_length()))
			app.s_q.put(vara)
			print("Stepsize set to 1")
		else:
			self.X1.set_active(True)
	
	def on_toggled_X10(self, button):
		if self.X10.get_active() != True:
			self.X1.set_active(False)
			self.X100.set_active(False)
			vara = 'S'+ str(int(1 / app.plotset.get_Step_length()))
			app.s_q.put(vara)
			print("Stepsize set to 10")
		else:
			self.X10.set_active(True)
	
	def on_toggled_X100(self, button):
		if self.X100.get_active() != True:
			self.X10.set_active(False)
			self.X1.set_active(False)
			vara = 'S'+ str(int(10 / app.plotset.get_Step_length()))
			app.s_q.put(vara)
			print("Stepsize set to 100")
		else:
			self.X100.set_active(True)
	
	##### Ref Point Set Callback ######
	def on_set_ref_clicked(self, button):
		if app.plotset.get_Limit_right() == 0 or app.plotset.get_Limit_top() == 0:
				self.Instruction_label.set_label("ERROR: Please Setup Endstops First")
		elif self.margin_setup_count == 4:
				self.Instruction_label.set_label("ERROR: Please Setup Margins First")
		else:
				self.destructuion(None, app)
		
	##### Drive button Callbacks #####
	def on_Move_up_Pressed(self, button):
		self.execution += 1
		app.s_q.put("U1")
		if self.execution == 1:
				app.s_q.put("E1")
		print("Move Up")
		
	def on_Move_up_Released(self, button):
		self.execution -= 1
		app.s_q.put("U0")
		if self.execution == 0:
				app.s_q.put("E0")
		print("end Move Up")
		
	def on_Move_Left_Pressed(self, button):
		self.execution += 1
		app.s_q.put("L1")
		if self.execution == 1:
				app.s_q.put("E1")
		print("Move Left")
		
	def on_Move_Left_Released(self, button):
		self.execution -= 1
		app.s_q.put("L0")
		if self.execution == 0:
				app.s_q.put("E0")
		print("end Move Left")
		
	def on_Move_Right_Pressed(self, button):
		self.execution += 1
		app.s_q.put("R1")
		if self.execution == 1:
				app.s_q.put("E1")
		print("Move Right")
		
	def on_Move_Right_Released(self, button):
		self.execution -= 1
		app.s_q.put("R0")
		if self.execution == 0:
				app.s_q.put("E0")
		print("end Move Right")
		
	def on_Move_Down_Pressed(self, button):
		self.execution += 1
		app.s_q.put("D1")
		if self.execution == 1:
				app.s_q.put("E1")
		print("Move Down")
		
	def on_Move_Down_Released(self, button):
		self.execution -= 1
		app.s_q.put("D0")
		if self.execution == 0:
				app.s_q.put("E0")
		print("end Move Down")
		
		
	##### Margin Setter Callbacks ######
	def on_check_SB_LM_toggled(self, button):
		if app.plotset.get_Limit_right() == 0 or app.plotset.get_Limit_top() == 0:
				self.Instruction_label.set_label("ERROR: Please Setup Endstops First")
		else:
				a = self.spinbutton_LM.get_value()
				print(a)
				app.plotset.set_Margin_left(a / app.plotset.get_Step_length())
				print(a / app.plotset.get_Step_length())
				self.Instruction_label.set_label("Left Margin Set")
				self.margin_setup_count += 1
		
	def on_check_SB_RM_toggled(self, button):
		if app.plotset.get_Limit_right() == 0 or app.plotset.get_Limit_top() == 0:
				self.Instruction_label.set_label("ERROR: Please Setup Endstops First")
		elif app.plotset.get_Margin_left() == 0:
				self.Instruction_label.set_label("ERROR: Please Set the Left Margin First")
		else:
				a = app.plotset.get_Limit_right() - \
				(self.spinbutton_RM.get_value()/ app.plotset.get_Step_length())
				b = app.plotset.get_Margin_left()
				print(app.plotset.get_Limit_right())
				print(a, b)
				if (a <= b):
						self.Instruction_label.set_label("Right Margin can,t be smaller/equal to Left Margin!")
				else:
						app.plotset.set_Margin_right(a)
						self.Instruction_label.set_label("Righ Margin Set")
						self.margin_setup_count += 1
	
	def on_check_SB_BM_toggled(self, button):
		if app.plotset.get_Limit_right() == 0 or app.plotset.get_Limit_top() == 0:
				self.Instruction_label.set_label("ERROR: Please Setup Endstops First")
		else:
				a = self.spinbutton_BM.get_value()
				print(a)
				app.plotset.set_Margin_bottom(a / app.plotset.get_Step_length())
				self.Instruction_label.set_label("Bottom Margin Set")
				self.margin_setup_count += 1
	
	def on_check_SB_TM_toggled(self, button):
		if app.plotset.get_Limit_right() == 0 or app.plotset.get_Limit_top() == 0:
				self.Instruction_label.set_label("ERROR: Please Setup Endstops First")
		elif app.plotset.get_Margin_bottom() == 0:
				self.Instruction_label.set_label("ERROR: Please Set the Bottom Margin First")
		else:
				a = app.plotset.get_Limit_top() - \
				(self.spinbutton_TM.get_value()/ app.plotset.get_Step_length())
				b = app.plotset.get_Margin_bottom()
				if (a <= b):
						self.Instruction_label.set_label("Right Top can,t be smaller/equal to Left Margin!")
				else:
						app.plotset.set_Margin_top(a)
						self.Instruction_label.set_label("Top Margin Set! \nPlease set Refernce point")
						self.margin_setup_count += 1
		
	def destructuion(self,data, app):
		app.window.set_sensitive(True)
		app.s_q.put('Q')
		app.setup_thread.join()
		########################################################################################################
######################################### Manual Drive ################################################
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

########################################################################################################
############################################# Popover #################################################
########################################################################################################
class Popover_feedback(Gtk.Window):

		def __init__(self, data):
				Gtk.Window.__init__(self, title="System Response")
				self.resize(300, 100)
				container = Gtk.Box()
				self.add(container)
				msg = Gtk.Label()
				msg.set_label(data)
				okbutton = Gtk.Button(label = "OK")
				okbutton.connect("clicked", self.quit_this)
				container.pack_start(msg, True,0, 0)
				container.pack_end(okbutton, False, 0, 0)
				
		def quit_this(self,daata):
				self.close()


########################################################################################################
############################################### Gui ###################################################
########################################################################################################

class Path_container:

		def __init__(self):
				self.Path_Routes = []
				self.iterator = 0
		
		#Depracticed!! use goto_next_element and get_element_property instead!
		def get_next_element(self):
				self.iterator += 1
				if self.iterator -1  >= len(self.Path_Routes):
						#print("iterator len:", self.iterator, "pat_len: ", len(self.Path_Routes))
						return -1
				else:
#						print("return val from get_next: ", self.Path_Routes[self.iterator-1].get_Cairo_Property())
						return self.Path_Routes[self.iterator-1].get_Cairo_Property()
		
		def add_element(self, element, switch = 0):
				print('element in addelement is:', element)
				pathelement = Path_object(element, switch)
				self.Path_Routes.append(pathelement)
				
		def modify_element_value(self, property_type, value):
				print('element modify val is:', value)
				if property_type == 0: #Cairo modification
						self.Path_Routes[-1].Add_Cairo_Property(value)
				elif property_type == 1: #G-code modification
						self.Path_Routes[-1].Add_G_code_property(value)
				elif property_type == 2: #Plotter code modification
						self.Path_Routes[-1].Add_Plotter_property(value)
		
		def reset_iterator(self):
				self.iterator = 0
		
		def reset(self):
				self.Path_Routes.clear()
		
		def decrease_iterator(self):
				self.iterator -= 1
		
		def goto_next_element(self):
				self.iterator += 1
		
		def get_element_property(self, typeof):
				if typeof == 0:
						return self.Path_Routes[self.iterator].get_Cairo_Property()
				elif typeof == 1:
						return self.Path_Routes[self.iterator].get_G_code_Property()
				elif typeof == 2:
						return self.Path_Routes[self.iterator].get_Plotter_Property()
						
		
		def get_length(self):
				return len(self.Path_Routes)


class Path_object:
		
		def __init__(self):
				self.Cairo_property = []
				self.G_code_property = []
				self.Plotter_Property = []
				
		def __init__(self, Cairo_prop):
				#print ("thats what in the object:", Cairo_prop)
				self.Cairo_property = Cairo_prop.copy()
				self.G_code_property = []
				self.Plotter_Property = []
		
		def __init__(self, Universal_prop, prop_int):
				self.Cairo_property = []
				self.G_code_property = []
				self.Plotter_Property = []
				if prop_int == 0:
						self.Cairo_property = Universal_prop
				elif prop_int == 1:
						self.G_code_property = Universal_prop
				elif prop_int == 2:
						self.Plotter_Property = Universal_prop

		def Add_Cairo_Property(self, Property):
				self.Cairo_property = Property
				
		def Add_G_code_property(self, Property):
				self.G_code_property = Property
				
		def Add_Plotter_property(self, Property):
				self.Plotter_property = Property
				
		def get_Cairo_Property(self):
				return (self.Cairo_property)

		def get_G_code_Property(self):
				return (self.G_code_property)

		def get_Plotter_Property(self):
				return self.Plotter_property
				
				
class MouseButtons:
    
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Draw_feedback(Gtk.ApplicationWindow):

		def __init__(self, app):
				super(Draw_feedback, self).__init__()
				
				self.init_ui()

		def init_ui(self):    

				self.darea = Gtk.DrawingArea()
				self.darea.connect("draw", self.on_draw)
				self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
				self.add(self.darea)
				print(app.screenh, app.screenw)
				self.scaling_factor = 1
				self.daw = ((app.plotset.get_Margin_right() - app.plotset.get_Margin_left()) * app.plotset.get_Step_length())
				self.dah = ((app.plotset.get_Margin_top() - app.plotset.get_Margin_bottom()) * app.plotset.get_Step_length())
				print(self.dah, self.daw)
				if (app.screenh < self.dah or app.screenw < self.daw):
						hv = app.screenh / self.dah
						wv = app.screenw / self.daw
						print("im modifying drawarea settings")
						
						if hv > wv:
								self.scaling_factor = wv
						else:
								self.scaling_factor = hv

				self.enableflag = 0
				self.last_state = 0
				self.lokal_coords = []
				self.temp_coords = []
									   
				self.darea.connect("button-press-event", self.on_button_press)
				self.darea.connect("motion-notify-event", self.on_mouse_moove)
				print("scaling_factor =", self.scaling_factor)
				self.set_title("Lines")
				self.resize( self.daw * self.scaling_factor, self.dah * self.scaling_factor)
				self.set_position(Gtk.WindowPosition.CENTER)
				self.show_all()
				
		
		def on_draw(self, wid, cr):

				cr.set_source_rgb(0, 0, 0)
				cr.set_line_width(0.5)
				

#				Draw Lines
				def pathdraw(coordinates):
						sf = self.scaling_factor
						if len(coordinates) >=2:
								for i in range(1, len(coordinates)):
										x = coordinates[i-1]
										y = coordinates[i]
										cr.move_to(x[0] * sf, x[1] * sf)
										cr.line_to(y[0] *sf, y[1] * sf) 
										cr.stroke()
						else:
								return 
								
				app.paths.reset_iterator()
				# loop trough elements in paths object and Draw it
				sf = self.scaling_factor
				for i in range(0, app.paths.get_length()):
						dummy_iterator =0 
						try:
								op_id, coords = app.paths.get_element_property(0)
								print("drawn element:", op_id, coords)
								if op_id == 1:
										pathdraw(coords)
								if op_id == 2:
										cr.move_to((coords[0])*sf, (coords[1])*sf)
										cr.arc((-1* coords[2])*sf + (coords[0])*sf, (coords[1])*sf , (coords[2])*sf, 0, 2* math.pi)
										cr.stroke()
						except:
								print("coud not draw: ",app.paths.get_element_property(0))
								dummy_iterator += 1
						app.paths.goto_next_element()
				pathdraw(self.lokal_coords)
				if self.enableflag == 1:
						cr.move_to(self.lokal_coords[-1][0], self.lokal_coords[-1][1])
						cr.line_to(self.temp_coords[0][0], self.temp_coords[0][1])
						cr.stroke()

									       
									       
		def on_button_press(self, w, e):
				
				if e.type == Gdk.EventType.BUTTON_PRESS \
						and e.button == MouseButtons.LEFT_BUTTON:
						
						self.enableflag = 1 # flag to indicate draw in process
						self.lokal_coords.append([e.x, e.y])
						self.darea.queue_draw()
						
				if e.type == Gdk.EventType.BUTTON_PRESS \
						and e.button == MouseButtons.RIGHT_BUTTON:
						
						print("in daatahandling")
						# add path elements to paths object
						app.paths.reset_iterator()
						for i in range(0, app.paths.get_length()-1):
								app.paths.goto_next_element()
						while(1):
								latest_instruction = app.paths.get_element_property(0)
								if len(latest_instruction) == 0:
										app.paths.decrease_iterator()
								else:
										break
						latest_endpoint = latest_instruction[1][1]
						lx, ly = latest_endpoint
						sl = app.plotset.get_Step_length()
						sf = self.scaling_factor
						if len(self.lokal_coords) >= 2: # check if worth to add
								app.paths.add_element([])
								app.paths.modify_element_value(2, [4, [True]])
								x = self.lokal_coords[0][0] - lx
								y = (self. lokal_coords[0][1] - ly) * -1 #reverse sign because cairo handles y axis inverse
								app.paths.add_element([])
								app.paths.modify_element_value(2, [1, [x/ sl / self.scaling_factor ,y / sl/ self.scaling_factor]])
								app.paths.add_element([])
								app.paths.modify_element_value(2, [4, [False]])
								for i in range(1, len(self.lokal_coords)):
										lx , ly = self.lokal_coords[i-1]
										ax , ay = self.lokal_coords[i]
										#add Cairo property
										app.paths.add_element([1, [[lx, ly], [ax, ay]]])
										#add Plotter property
										app.paths.modify_element_value(2, [1, [(ax- lx)/sl/sf, (ay-ly)*-1/sl/sf]])
						self.lokal_coords = []
						self.enableflag = 0
						print("enableflag reset")
						self.darea.queue_draw()
						
		def on_mouse_moove(self,w,e):
				if (self.enableflag == 1):
						self.temp_coords.clear()
						self.temp_coords.append([e.x, e.y])
						self.darea.queue_draw()


########################################################################################################
############################################## Interpreter ############################################
########################################################################################################
class Plotter_settings:
		def __init__(self):
				self.Pen_pos = [0,0, True] #[x,y,z] (step,step, bool)
				self.Margin_left = 0 #(step)
				self.Margin_bottom = 0 #(step)
				self.Margin_top = 0 #(step)
				self.Margin_right = 0 #(step)
				self.Limit_top = 0 #(step)
				self.Limit_right = 0 #(step)
				self.Step_length = 0.01136 #(mm/step)
				self.X_inversion = False
				self.Y_inversion = False

		def set_x_inversion(self,value):
				self.X_inversion = value
		
		def set_y_inversion(self,value):
				self.Y_inversion = value
				
		def get_x_inversion(self):
				return(self.X_inversion)
		
		def get_y_inversion(self):
				return(self.Y_inversion)

		def set_Margin_left(self,value):
				self.Margin_left = (value)

		def set_Margin_bottom(self, value):
				self.Margin_bottom = (value)

		def set_Margin_right(self, value):
				self.Margin_right = (value)

		def set_Margin_top(self, value):
				self.Margin_top = (value)

		def set_Pen_pos(self, value):
				self.Pen_pos = value

		def set_Step_length(self, value):
				self.Step_length = value

		def set_Limit_top(self, value):
				self.Limit_top = value

		def set_Limit_right(self, value):
				self.Limit_right = value
				
		def get_Limit_top(self):
				return self.Limit_top
				
		def get_Limit_right(self):
				return self.Limit_right

		def get_Step_length(self):
				return self.Step_length

		def get_Margin_left(self):
				return self.Margin_left

		def get_Margin_right(self):
				return self.Margin_right

		def get_Margin_top(self):
				return self.Margin_top

		def get_Margin_bottom(self):
				return self.Margin_bottom

		def get_Pen_pos(self):
				return self.Pen_pos


class Translation_settings:
		
		def __init__(self):
				self.Virtual_pen_pos = [] #[X-steps, Y-steps, Z-Bool]
				self.lokality = False
				self.mode = 0
				self.current_line = 0
		
		def set_Virtual_pen_pos(self, value):
				self.Virtual_pen_pos = value
		
		def set_Lokality(self, value):
				self.lokality = value

		def set_Mode(self, value):
				self.mode = value
		
		def set_Current_line(self, value):
				self.current_line = value
		
		def get_Virtual_pen_pos(self):
				return self.Virtual_pen_pos
		
		def get_Current_line(self):
				return self.current_line
		
		def get_Lokality(self):
				return self.lokality
		
		def get_Mode(self):
				return self.mode 


class Code_translater:

		def __init__(self,app):
				print("this is useless")
		
		def __init__(self,app, data):
				self.analyzed_string = data
				self.translation_setting = Translation_settings()
				self.translation_setting.set_Virtual_pen_pos(app.plotset.get_Pen_pos())
				#import penpos from setup to translation settings !!!
						
		def Analyze(self, app, line):
				# default Variables
				ymax  = 500 # temp variable for test pourposes/ represents the max y(vertical) value
				Xfactor = 0.0
				Yfactor = 0.0
				Zfactor = self.translation_setting.get_Virtual_pen_pos()[2]
				Rfactor = 0.0
				xflag = False
				yflag = False
				# BIG Switch-Case for overwriting default Variables.
				for word in line.split(' '):
						Instruction = word[0]
						Data = word[1:]
						try:
								float(Data)
						except:
								continue
						#G-code instruction determination
						if Instruction == 'G':
								if int(Data) == 0:
										self.translation_setting.set_Mode(0)
								elif int(Data) == 1:
										self.translation_setting.set_Mode(0)
										print("setting mode to G1")
								elif int(Data) == 2:
										self.translation_setting.set_Mode(2)
										print("setting mode to G2")
								elif int(Data) == 3:
										self.translation_setting.set_Mode(3)
								elif int(Data) == 90:
										self.translation_setting.set_Lokality(False)
								elif int(Data) == 91:
										self.translation_setting.set_Lokality(True)
								else:
										response = "Unknown Instruction in line:" + line + "please correct it"
										app.Popup_feed(response)
										return -2 #(bad instruction)
						elif Instruction == 'N':
								self.translation_setting.set_Current_line(int(Data))
						elif Instruction == 'X':
								Xfactor = float(Data)
								xflag = True
						elif Instruction == 'Y':
								Yfactor = float(Data)
								yflag = True
						elif Instruction == 'Z':
								Zfactor = bool(int(Data))
						elif Instruction == 'R':
								Rfactor = float(Data)
								if Rfactor <= 0.25:
										response = "radius to small in line:" + line + "please correct it"
										app.Popup_feed(response)
										return -3 #(to small radius)
						elif Instruction == '%':
								print("program ID: ", Data)
						else:
								response = "Unknown Instruction in line:" + line + "please correct it"
								app.Popup_feed(response)
								return -2 #(bad instruction)
								
				
				#Get last settings
				x, y, z = self.translation_setting.get_Virtual_pen_pos()
				stl = app.plotset.get_Step_length()
				#Translating coordinates if in Absolute (G90)
				if self.translation_setting.get_Lokality() == False:
						if xflag == True:
								Xfactor = Xfactor-((x - app.plotset.get_Pen_pos()[0]) * stl)
						if yflag == True:
								Yfactor = Yfactor-((y - app.plotset.get_Pen_pos()[1]) * stl)
				#Writing the results to respective container objects
				if self.translation_setting.get_Mode() == 0:
						#make new element with Gcode stored
						app.paths.add_element([line], 1)
						#add Plotter property
						if Zfactor != z:
								self.translation_setting.set_Virtual_pen_pos([x, y, Zfactor])
								app.paths.modify_element_value(2,[4, [Zfactor]])
						elif (Xfactor == 0 or Yfactor == 0 or Xfactor == Yfactor):
								if Xfactor != 0:
										xsteps = Xfactor/stl
								else:
										xsteps = 0
								if Yfactor != 0:
										ysteps = Yfactor/stl
								else:
										ysteps = 0
								app.paths.modify_element_value(2,[0, [xsteps, ysteps]])
								self.translation_setting.set_Virtual_pen_pos([x+xsteps, y+ysteps, z])
								vala = self.check_for_margin_violation(app, self.translation_setting.get_Virtual_pen_pos())
								if vala == True:
										response = "Margin violation on Line:\n" + line + "\nTranslation terminates, please correct the error"
										app.Popup_feed(response)
										return -1
						else:  #steps in x and y dir
								xsteps = Xfactor/stl
								ysteps = Yfactor/stl
								app.paths.modify_element_value(2,[1, [xsteps, ysteps]])
								self.translation_setting.set_Virtual_pen_pos([x+xsteps, y+ysteps, z])
								vala = self.check_for_margin_violation(app, self.translation_setting.get_Virtual_pen_pos())
								if vala == True:
										response = "Margin violation on Line:\n" + line + "\nTranslation terminates, please correct the error"
										app.Popup_feed(response)
										return -1
						#add draw Property
						if Zfactor != True :
								y_correction = ymax - y*stl
								app.paths.modify_element_value(0,[1, [[x*stl, y_correction],[(x*stl+Xfactor), 								(y_correction-Yfactor)]]])
				#When in G2
				elif self.translation_setting.get_Mode() == 2:
						print("translation mode 2 entered")
						app.paths.add_element([2,[x * stl, (ymax - y* stl) , Rfactor]])
						app.paths.modify_element_value(2, [2, Rfactor/ stl])
				return 1

		def check_for_margin_violation(self, app, VP):
				x, y, z = VP
				if x >= app.plotset.get_Margin_right() or x <= app.plotset.get_Margin_left():
						return True
				elif y >= app.plotset.get_Margin_top() or y <= app.plotset.get_Margin_bottom():
						return True
				else: 
						return False

		def clear_for_comments(self, stringie):
				clean_string = ''
				unprocessed_string = stringie
				while(1):
						if unprocessed_string.find('(') != -1:
								i = unprocessed_string.find('(')
								x = unprocessed_string.find(')', i)
								if unprocessed_string.find('\n', i, x) != -1:
										clean_string += unprocessed_string[0:i]+'\n'
										unprocessed_string = unprocessed_string[x+1:]
								else:
										clean_string += unprocessed_string[0:i]
										unprocessed_string = unprocessed_string[x+1:]
						else:
								clean_string += unprocessed_string
								break
				retext = ''
				for line in clean_string.splitlines():
						freeline = (line + '.')[:-1]
						freeline.strip(' \r')
						try:
								if freeline[0] == '\n':
										continue
								else:
										retext += line + '\n'
						except:
								continue
				clean_string = retext
				return clean_string

		def translate(self, app ):
				clean_string = self.clear_for_comments(self.analyzed_string)
				for line in clean_string.splitlines():
						retval = self.Analyze(app, line)
						if retval <= -1:
								return -1
				return 1
				print("Succesfully translated!")

########################################################################################################
############################################### Main ##################################################
########################################################################################################

class WorldChangingApp(Gtk.Application):
		def __init__(self):
				Gtk.Application.__init__(self, application_id="apps.test.plotterapp",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
				self.connect("activate", self.on_activate)
				self.portstate = False # has to do with the "Connect MCU" Button
				self.q = queue.Queue() # init queue for serial thread
				self.s_q = queue.Queue()
				self.loop_count = 1
				self.lastinst = []
				self.get_screen_vals()

		#On Startup Main Window
		def on_activate(self, data=None):
				self.window = MyWindow(self)
				self.window.show_all()
				self.add_window(self.window)
				print (self.window.get_id())

		#Startup operations
		def do_startup(self):
				Gtk.Application.do_startup(self)
				Setup_action = Gio.SimpleAction.new("Setup_dialog_invoke", None)
				Setup_action.connect("activate", self.Setup_dialog)
				app.add_action(Setup_action)
				Draw_action = Gio.SimpleAction.new("Draw_field_invoke", None)
				Draw_action.connect("activate", self.Draw_making)
				app.add_action(Draw_action)
				Serial_com_handler = Gio.SimpleAction.new("Serial_com_handler_invoke", None)
				Serial_com_handler.connect("activate", self.Serial_establish)
				app.add_action(Serial_com_handler)
				Printer = Gio.SimpleAction.new("Plot_invoke", None)
				Printer.connect("activate", self.Transmit_data2)
				app.add_action(Printer)
				self.paths = Path_container()
				self.plotset = Plotter_settings()
        
		#### get max screensize ###
		def get_screen_vals(self):
				self.screenh = 0
				self.screenw = 0
				gw = Gtk.Window()
				gw.maximize()
				def p():
						self.screenw, self.screenh  = gw.get_size()
						gw.close()
						print(self.screenh, self.screenw)
				GLib.timeout_add(200, p)
				gw.show()

    #Open Setup Window
		def Setup_dialog(self,action, parameter):
				if len(threading.enumerate()) != 2: #check if com thread active
						self.Popup_feed("MCU not Connected! \nPlease connect to  the MCU First")
				else:
						self.setup_thread = threading.Thread(target=self.Setup_transmitter, args = (self.q, self.s_q))
						self.setup_thread.daemon = True
						self.setup_thread.start()
						self.window.set_sensitive(False)
						self.S_window = Setup_window(self)
						self.add_window(self.S_window)
						self.S_window.show_all()

		#Open Freedraw mode + translate Code
		def Draw_making(self, action, parameter):
				print("Draw mode entered")
				okflag = 0
				self.paths.reset()
				try:
						self.window.update_from_textfield()
						textie = self.window.text_data
				except:
						self.Popup_feed("No Project open! \nPlease open a Project first")
						okflag = 1
				if okflag == 0:
						self.trans = Code_translater(self, textie)
						a = self.trans.translate(self)
						if a == 1:
								self.D_window = Draw_feedback(self)
								self.D_window.show_all()
								self.add_window(self.D_window)
						else: 
								self.paths.reset()
				
		# Translate Coordinates for easyer interpretation, assemble final msg
		def serialize(self, instruction, mode_select = 0):
				x, y = instruction
				if x >= 0:
						if self.plotset.get_x_inversion() != True:
								xprefix = 'P'
						else:
								xprefix = 'N'
				else:
						if self.plotset.get_x_inversion() != True:
								xprefix = 'N'
						else:
								xprefix = 'P'
				if y >= 0:
						if self.plotset.get_y_inversion() != True:
								yprefix = 'P'
						else:
								yprefix = 'N'
				else:
						if self.plotset.get_y_inversion() != True:
								yprefix = 'N'
						else:
								yprefix = 'P'
				if mode_select == 0:
						response = '#' + xprefix + str(abs(int(x))) + ':' + yprefix + str(abs(int(y))) + '$'
				elif mode_select == 1:
						response = '#D' + xprefix + str(abs(int(x))) + ':' + yprefix + str(abs(int(y))) + '$'
				return response
				
		def Update_instruction_lable(self, msg):
				self.S_window.Instruction_label.set_label(msg)
				
		def Update_Boundaries(self, bx, by):
				self.plotset.set_Limit_top(by)
				self.plotset.set_Limit_right(bx)
				
		def Update_Reference_p(self, VP):
				self.plotset.set_Pen_pos(VP)
				
		# Forward instructions from Setup window to Serial_Messenger
		def Setup_transmitter(self, q, setup_queue):
				print("in thread")
				counter  =0
				endstop_counter = 0
				last_instruction = "#S1$"
				Boundary_x = 0
				Boundary_y = 0
				Dir_l = False
				Dir_r = False
				Dir_u = False
				Dir_d = False
				Exec = False
				Stepsize = 1000
				Nextflag = False
				Virtual_pen_pos = [50000, 50000, True] # x(step), y(step) , z(bool)
				# Let Serial thread know, that Setup is entered
				q.put("SETUP")
				q.put("#S1$")
				#enter main communication loop
				while(True):
						#rcv and eval Msg
						if setup_queue.empty() != True:
								msg_out = setup_queue.get(False, 0)
								counter = 0
								print("s_msg is", msg_out)
								if msg_out == "RESEND":
										q.put(last_instruction)
								else:
										if msg_out[:1] == 'R':
												Dir_r = bool(int(msg_out[1:2]))
										elif msg_out[:1] == 'L':
												Dir_l = bool(int(msg_out[1:2]))
										elif msg_out[:1] == 'N':
												Nextflag = True
										elif msg_out[:1] == 'U':
												Dir_u = bool(int(msg_out[1:2]))
										elif msg_out[:1] == 'D':
												Dir_d = bool(int(msg_out[1:2]))
										elif msg_out[:1] == 'E':
												Exec = bool(int(msg_out[1:2]))
										elif msg_out[:1] == 'S':
												Stepsize = int(msg_out[1:])
										elif msg_out[:1] == 'X':
												endstop_counter +=1
												if endstop_counter == 1:
														Virtual_pen_pos[0] = 0
														GLib.idle_add(self.Update_instruction_lable, "Move the Pen to the Bottom End")
														print("Virtual_pen_pos = ", Virtual_pen_pos)
												if endstop_counter == 2:
														Virtual_pen_pos[1] = 0
														GLib.idle_add(self.Update_instruction_lable, "Move the Pen to the Right End")
														print("Virtual_pen_pos = ", Virtual_pen_pos)
												if endstop_counter == 3:
														Boundary_x = Virtual_pen_pos[0]
														GLib.idle_add(self.Update_instruction_lable, "Move the Pen to the Top End")
														print("Virtual_pen_pos = ", Virtual_pen_pos)
												if endstop_counter == 4:
														Boundary_y = Virtual_pen_pos[1]
														GLib.idle_add(self.Update_instruction_lable, "Set up the Margins")
														GLib.idle_add(self.Update_Boundaries, Boundary_x, Boundary_y)
														print("Virtual_pen_pos = ", Virtual_pen_pos)
										elif msg_out[:1] == 'Q':
												GLib.idle_add(self.Update_Reference_p, Virtual_pen_pos)
												break
										else:
												print("unknown instruction:", msg_out)
						# Send new instruction if needed
						if Nextflag == True and Exec == True:
								Nextflag = False
								counter += 1
								print("this S_ msg was sent times", counter)
								x = int(Dir_l) * Stepsize * -1 + int(Dir_r) * Stepsize
								y = int(Dir_d) * Stepsize * -1 + int(Dir_u) * Stepsize
								Virtual_pen_pos[0] = x + Virtual_pen_pos[0]
								Virtual_pen_pos[1] = y + Virtual_pen_pos[1]
								msg = self.serialize([x, y])
								last_instruction = msg
								q.put(msg)
				q.put("SETUP")
		
		def Transmit_data2(self, action, parameter):
				self.paths.reset_iterator()
				self.Transmit_data()
		
		def instruction_recurse(self):
				try:
										self.instruction = self.paths.get_element_property(2)
				except:
										self.paths.goto_next_element()
										self.recurse_counter += 1
										if self.recurse_counter <= 7:
												print(self.recurse_counter, self.instruction)
												self.instruction_recurse()
												
										else: 
												self.recurse_counter = 0
										

		#start sending the compiled data
		def Transmit_data(self, resend = 0):
				self.recurse_counter = 0
				print("Data Transmission started")
				if resend == 1:
						self.q.put(self.last_instruction)
				else:
						if len(self.lastinst) == 0:
								self.instruction = self.paths.get_element_property(2)
								self.paths.goto_next_element()
						else: 
								self.instruction = self.lastinst
						if self.instruction[0] == 0:
								response = self.serialize(self.instruction[1])
								self.last_instruction = response
								self.q.put(response)
						elif self.instruction[0] == 1:
								response = self.serialize(self.instruction[1], 1)
								self.last_instruction = response
								self.q.put(response)
						elif self.instruction[0] == 2:
								response = "#K" + str(int(self.instruction[1])) + "$"
								self.last_instruction = response
								self.q.put(response)
						elif self.instruction[0] == 4:
								response = str("#S"+str(int(self.instruction[1][0]))+"$")
								self.last_instruction = response
								self.q.put(response)
						
		#Costume Popup Msg-es
		def Popup_feed(self, data):
				popup_win = Popover_feedback(data)
				popup_win.show_all()
				self.add_window(popup_win)
		
		#Evaluate Responses from XMC
		def Make_sens_of_response(self, response):
				response = str(response)
				Response  = response[2:-2]
				if Response == "ACK":
						self.q.put("HOLD")
						print("msg acknowledged")
				elif Response == "NACK":
						print("msg not Acknowledged")
						self.Transmit_data(1)
				elif Response == "DONE":
						print("job done")
						self.Transmit_data()
				else:
						print("i have no idea of this msg: ", response)
				
		def Make_sense_of_setup_Response(self, response):
				response = str(response)
				Response  = response[2:-2]
				if Response == "ACK":
						self.q.put("HOLD")
						print("msg acknowledged")
				elif Response == "NACK":
						print("msg not Acknowledged")
						self.s_q.put("RESEND")
				elif Response == "DONE":
						self.s_q.put("N")
						print("job done")
				elif Response[:2] == "ER":
						self.s_q.put("X")
						self.s_q.put("N")
				else:
						print("i have no idea of this msg: ", response)
				
		#Thread for sending and reciving Msges
		def Serial_Messenger(self , q):
				self.port = serial.Serial("/dev/ttyUSB0", baudrate=115200,bytesize=8, parity='N', stopbits=1, 				timeout = 1)
				counter = 0
				counterflag = 1
				setup_flag = 0
				try:
						self.port.open()
				except:  
						GLib.idle_add(self.Popup_feed, "port open, youre good to go")
				while (self.port.is_open):
						if q.empty() != True:
								msg_out = q.get(False, 0)
								print(" qued msg is", msg_out)
								if msg_out == "STOP":
										self.port.close()
										continue
								elif msg_out == "HOLD":
										counterflag = 1
										continue
								elif msg_out == "SETUP":
										if setup_flag == 0:
												setup_flag = 1
										else:
												setup_flag = 0
										continue
								else:
										counterflag = 0
						#msg_out = "#your MOM$"
								for letter in msg_out:
									a = self.port.write(str.encode(letter))
									print ("msg:", letter," sent out with bytecount:", a)
									time.sleep(0.01)
								msg_out = ""
						if self.port.readable() == True:
								rcv = self.port.read_until(b'#', 50)
								print("recieved:" , str(rcv))
								if len(rcv) == 0 and counterflag == 0: #Timeout for resending msg
										counter += 1
										if counter >= 3:
												counter = 0
												if setup_flag == 0:
														GLib.idle_add(self.Make_sens_of_response, "::NACK::")
												else:
														GLib.idle_add(self.Make_sense_of_setup_Response, "::NACK::")
										continue
								counter = 0
								if len(rcv) != 0:
										if setup_flag == 0:
												GLib.idle_add(self.Make_sens_of_response, rcv)
										else:
												GLib.idle_add(self.Make_sense_of_setup_Response, rcv)

		#Setup Com Thread / Destroy it
		def Serial_establish(self, action, parameter):
				print("Open Serial Communication")
				if self.portstate == False:
						self.portstate = True
						self.thread = threading.Thread(target=self.Serial_Messenger, args = (self.q, ), name = "com_thread")
						self.thread.daemon = True
						self.thread.start()
						self.window.Connect_button.set_label("Disconnect MCU")
				else:
						self.q.put("STOP")
						self.portstate = False
						self.window.Connect_button.set_label("Connect MCU")
						self.thread.join()


#### the "real" main launcher ############

if __name__ == "__main__":
		app = WorldChangingApp()
		app.run(sys.argv)
		sys.exit(exit_status)



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

