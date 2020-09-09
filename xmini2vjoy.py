
##########################################################################################
#                                                                                        #
#                                   xmini2vjoy.py                                        #
#                                                                                        #
#                                   FreePIE Script                                       #
#                                     v.Beta.0.9                                         #
#                                                                                        #
#                                                                                        #
#            Midi Controller Behringer X-Touch Mini ---> X-Plane, FSX, ...               #
#                      1x vJoy: 16 Encoders, 2 Sliders, 48 Buttons                       #
#                                                                                        #
#                                                                                        #
#               This script will let you take control of your sim's axes,                #
#               knobs and buttons easily using the Behringer X-Touch Mini                #
#                                                                                        #
#                                     Installation:                                      #
#                                                                                        #
#                   1. Download and run vJOY v2.1.9 & FreePIE v1.11.724.0                #
#                                                                                        #
#     http://vjoystick.sourceforge.net/site/index.php/download-a-install/download        #
#                       https://andersmalmgren.github.io/FreePIE/                        #
#                                                                                        #
#                                                                                        #
#                   2. Use Behringer's X-Touch Editor to set the encoders                #
#                   of your Mini to CC, Relative2 mode.                                  #
#                                                                                        #
#                   3. Use vJoyConf to generate 1 virtual joystick                       #
#                   with 2 axes and 80 buttons (no POVs are needed.)                     #
#                   That's all we will need to model X-Touch Mini's                      #
#                   layers A and B.                                                      #
#                                                                                        #
#                   4. Place this script on FreePIE's main folder:                       #
#                   C:\Program Files(x86)\FreePIE. Make sure that                        #
#                   the file gets saved as xmini2vjoy.py                                 #
#                                                                                        #
#                   5. On the same folder, make a new text file named                    #
#                   xmini2vjoy.bat with the following contents:                     	 #
#                                                                                        #
#                        @echo off                                                       #
#                        START /min FreePIE.exe "xmini2vjoy.py" /r                       #
#                                                                                        #
#                   6. Create a link to this file (xmini2vjoy.bat)                   	 #
#                   and place it on the desktop. Run it before starting                  #
#                   X-plane. On X-Plane settings you'll see the virtual	    			 #
# 					joystick and will be able to assign its axes and                     #
#                   buttons to control the sim's functions, or manage                    #
#                   them assisted by FlyWithLua.                                         #
#                                                                                        #
#                                                                                        #
#                          Josep Zambrano, December 30, 2019                       		 #
#                                                                                        #
#                                                                                        #
#                                                                                        #
##########################################################################################


speed = 64  # type: int
drive = 0   # type: int
times = 0   # type: int
axis = 0    # type: int

# Delays ~0.013, depends on your CPU, adjust if you find trouble reading encoders, axes and buttons.

loop_delay = 0.010   # type: float
cycle_delay = 0.020  # type: float


def map_cc_buttons(cc, button1, button2):

    """ maps an X-Mini's relative encoder to two vJoy buttons, back and forth.

        X-Mini's relative encoder mode 2 works like this: when you move an
        encoder to your left, it will give you cc messages 63, 62, 61...
        depending on how fast you turn it. When you move it to your right,
        will send cc messages 65, 66, 67, etc.

         This function gives one or more button presses of button1 or button2
         depending on the direction and speed of turn of the encoder """

    if (midi[0].data.buffer[0] == cc) and (midi[0].data.status == MidiStatus.Control):
        speed = midi[0].data.buffer[1]
        drive = speed - 64
        times = abs(drive)
        if drive < 0:
            for i in range(times):
                vJoy[0].setPressed(button1)
                midi[0].data.buffer[0] = 99
                time.sleep(loop_delay)
        elif drive > 0:
            for i in range(times):
                vJoy[0].setPressed(button2)
                midi[0].data.buffer[0] = 99
                time.sleep(loop_delay)  # CC    ENCODER     BTNS 1,2


def map_cc_axis(cc):

    """ maps an X-Mini's slider to a vJoy axis, axis value returned """

    if (midi[0].data.buffer[0] == cc) and (midi[0].data.status == MidiStatus.Control):
        return filters.mapRange(midi[0].data.buffer[1], 0, 127, -17873, 17873)  # CC    FADER	    AXIS
    # usage:  vJoy[0].x = map_cc_axis(slider_cc)

def map_note_button(note, button):

    """ maps an X-Mini's midi note to a vJoy button """

    vJoy[0].setPressed(button, midi[0].data.buffer[0] == note and midi[0].data.buffer[1] == 127
                       and (midi[0].data.status == MidiStatus.NoteOn))


#      Layer A: Rotary Encoders        #######################################  MIDI ## CONTROL ### X-PLANE ###

base_button = 48    # type: int
base_cc = 1         # type: int

for n in range(8):
    map_cc_buttons(base_cc + n, base_button + 2 * n, base_button + 2 * n + 1)  # CC  Encoders 1-8  Buttons 49-64


#      Layer A: Slider                 #######################################  MIDI  ## CONTROL ### X-PLANE ###

slider_cc = 9                                                                   # CC9    Slider 1	  AXIS 1
# slider_axis = vJoy[0].x

if (midi[0].data.buffer[0] == slider_cc) and (midi[0].data.status == MidiStatus.Control):
    vJoy[0].x = filters.mapRange(midi[0].data.buffer[1], 0, 127, -16382, 16382)


#      Layer B: Rotary Encoders        #######################################  MIDI  ## CONTROL ### X-PLANE ###

base_button = 64    # type: int
base_cc = 11        # type: int

for n in range(8):
    map_cc_buttons(base_cc + n, base_button + 2 * n, base_button + 2 * n + 1)   # CC  Encoders 9-16  Buttons 65-80


#      Layer B: Slider                 #######################################  MIDI  ## CONTROL ### X-PLANE ###

slider_cc = 10                                                                  # CC10   Slider 1	  AXIS 2
# slider_axis = vJoy[0].y

if (midi[0].data.buffer[0] == slider_cc) and (midi[0].data.status == MidiStatus.Control):
    vJoy[0].y = filters.mapRange(midi[0].data.buffer[1], 0, 127, -16382, 16382)


#      Layer A: Encoder Buttons        #######################################  MIDI  ## CONTROL ### X-PLANE ###

base_button = 0     # type: int
base_note = 0       # type: int

for n in range(8):
    map_note_button(base_note + n, base_button + n)                             # Note  Encoders 1-8  Buttons 1-8

#      Layer A: Square Buttons         #######################################  MIDI  ## CONTROL ### X-PLANE ###

base_button = 8     # type: int
base_note = 8       # type: int

for n in range(16):
    map_note_button(base_note + n, base_button + n)                             # Note Sqr Button 9-24 Buttons 9-24


#      Layer B: Encoder Buttons        #######################################  MIDI  ## CONTROL ### X-PLANE ###

base_button = 24    # type: int
base_note = 24      # type: int

for n in range(8):
    map_note_button(base_note + n, base_button + n)                             # Note  Encoders 9-16 Buttons 25-32


#      Layer B: Square Buttons         #######################################  MIDI  ## CONTROL ### X-PLANE ###

base_button = 32    # type: int
base_note = 32      # type: int

for n in range(16):
    map_note_button(base_note + n, base_button + n)                             # Note Sqr Button 33-48 Buttons 33-48


#      Midi Monitor for FreePIE's Console      ###############

def update():

    diagnostics.watch(midi[0].data.channel)
    diagnostics.watch(midi[0].data.status)
    diagnostics.watch(midi[0].data.buffer[0])
    diagnostics.watch(midi[0].data.buffer[1])


if starting:
    midi[0].update += update

#      Stabilizing Delay to allow time for getting encoder and button data      #############

import time

time.sleep(cycle_delay)
