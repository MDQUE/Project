import serial
#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gtk

#class MyWindow(Gtk.Window):

#    def __init__(self):
#        Gtk.Window.__init__(self, title="Hello World")

#        self.box = Gtk.Box(spacing=6,)
#        self.add(self.box)

#        self.button1 = Gtk.Button(label="Hello")
#        self.button1.connect("clicked", self.on_button1_clicked)
#        self.box.pack_start(self.button1, True, True, 0)

#        self.button2 = Gtk.Button(label="Goodbye")
#        self.button2.connect("clicked", self.on_button2_clicked)
#        self.box.pack_start(self.button2, True, True, 0)

#    def on_button1_clicked(self, widget):
#        print("Hello")
#        self.button1.set_label("nello")

#    def on_button2_clicked(self, widget):
#        print("Goodbye")

#win = MyWindow()
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()


port = serial.Serial("/dev/ttyUSB0", baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=3.0)
#port.open()
while (port.is_open):
		port.write(b'#')
		port.write(b't')
		port.write(b'e')
		port.write(b's')
		port.write(b't')
		port.write(b'$')
		print ("msg sent out")
		rcv = port.read(10)
		print(rcv)

