import serial
import time
from oled import OLED
from oled import Font
from oled import Graphics

# Connect to the display on /dev/i2c-0
dis = OLED(1)

# Start communication
dis.begin()

# Start basic initialization
dis.initialize()

# Do additional configuration
dis.set_memory_addressing_mode(0)
dis.set_column_address(0, 127)
dis.set_page_address(0, 7)

# Clear display
dis.clear()

# Set font scale x2
f = Font(2)

# Set serial communication
port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
port.flush()

# Functions
def listToFloat(s):
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    fl = float(str1)
    return fl

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

# variables
line = ""
a=[]
b=[]
c=[]
tmp=0
k=0
count=0

while port.is_open:
    if port.in_waiting > 0:

        #guarda nums/signos en lista 'a'
        while line != "=":
            line = port.read().decode('utf-8').rstrip()
            if line != '':
                a.append(line)
                f.print_string(count, 0, line) # print to OLED
                print(line) #print to terminal
                dis.update()
                count+=12
        #guarda solo numeros en lista 'c'
        for i in a:
            b.append(i) # 'b' es una lista temporal
            if i in ["+", "-", "/", "*","="]:
                b.pop()
                num = listToFloat(b)
                c.append(num)
                b.clear()
        #hace operaciones en orden de aparicion
        tmp = c[k]
        for i in a:
            if i == "+":
                k += 1
                tmp += c[k]
            if i == "-":
                k += 1
                tmp -= c[k]
            if i == "/":
                k += 1
                tmp /= c[k]
            if i == "*":
                k += 1
                tmp *= c[k]

        print (tmp)
        dis.clear()
        f.print_string(0, 0, listToString(a))
        f.print_string(0, 32, str(tmp))
        dis.update()
        break
