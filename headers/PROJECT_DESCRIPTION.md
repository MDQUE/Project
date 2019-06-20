#########################################PROJECT_INFO#####################################################
Author: Verena Grünzweig, Dominique Martienssen
Project: Plotter
Languages: C, C++, Python
Made at: FH TECHNIKUM WIEN
Project-Start: 09.05.2019

Anything else:
	Mbed-OS source code not included


Important Notice:
Change in mbed-os/tools/profiles/debug.json
line 12: "-std=gnu++98" to "-std=gnu++11"

#########################################ADDON##################################################

im datenblatt: genauigkeit: 0,1mm

A4988 motorsteuerung datenblatt: 
	- maximale genauigkeit: 1/16 step -> 64 steps/ umdrehung

messungen: 
	- "zahnrad" durchmesser auf motorseite: 12,5mm mit band, ohne 10,9mm
	
schlussfolgerung:
	- 10,9*3,14 = 34.226mm => umkreis des "zahnrades"
	- umkreis/64 = 0.534 mm => die maximal erreichbare genaigkeit ist bei 0,534mm / step!

##########################################################################################################


Realisation Steps:

1) XMC - Extension board communication.
		- basic barebone code anschauen und auf Mbed-os porten.


2) Basic controls
		- endschalter registrieren
		- motor steuerung

3) XMC - PC Serial communication(UART)

4) PC(client) side
		- Build Gui.
		- implement serial communication.
		- (multi thread?)


Functions:

1) Board:
		- Area init
				- initialisiert die verfügbare fläche
