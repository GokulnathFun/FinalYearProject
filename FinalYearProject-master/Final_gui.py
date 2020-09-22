# from tkinter import *
#
# root = Tk()
#
# with open("output.txt", "r") as f:
#     Label(root, text=f.read()).pack()
#
# root.mainloop()

from serial import *
from tkinter import *

serialPort1 = "../../../dev/ttyACM0"
serialPort2 = "../../../dev/ttyACM1"

baudRate = 9600
ser1 = Serial(serialPort1, baudRate, timeout=0, writeTimeout=0)  # ensure non-blocking
ser2 = Serial(serialPort2, baudRate, timeout=0, writeTimeout=0)  # ensure non-blocking

# make a TkInter Window
root = Tk()
root.wm_title("Data Logger")

# make a scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# make a text box to put the serial output
log = Text(root, width=50, height=20, takefocus=0)
log.pack()

# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)

# make our own buffer
# useful for parsing commands
# Serial.readline seems unreliable at times too
serBuffer = ""

def readSerial2():
    while True:
        d = ser2.read().decode("ascii")
        if len(d) == 0:
            break
        # get the buffer from outside of this function
        global serBuffer

        # check if character is a delimeter
        if d == '\r':
            d = ''  # don't want returns. chuck it

        if d == '\n':
            serBuffer += "\n"  # add the newline to the buffer

            # add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            serBuffer = ""  # empty the buffer
        else:
            serBuffer += d  # add to the buffer

    root.after(10, readSerial1)  # check serial again soon

def readSerial1():
    while True:
        c = ser1.read().decode("ascii")    # attempt to read a character from Serial

        # was anything read?
        if len(c) == 0:
            break

        # get the buffer from outside of this function
        global serBuffer

        # check if character is a delimeter
        if c == '\r':
            c = ''  # don't want returns. chuck it

        if c == '\n':
            serBuffer += "\n"  # add the newline to the buffer


            # add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            serBuffer = ""  # empty the buffer
        else:
            serBuffer += c  # add to the buffer

    root.after(10, readSerial2)

# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial1)

root.mainloop()
