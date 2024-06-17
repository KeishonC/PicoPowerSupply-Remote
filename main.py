#PicoPowerSupply
# The PicoPowerSupply is a code base that interfaces with the PicoW
# a buck converter and a I2C OLED display.  The Power output is controlled
# by a voltage divider that interfaces with the buck-converter and gives output
# to the Pico Analog input pin.

import machine
from machine import Pin, SoftI2C
import ssd1306
from time import sleep
from utime import sleep
from machine import ADC

#Set voltage divider output pin to Analog.
analog = ADC(28) 

#Setup OLED pins
i2c = machine.SoftI2C(scl=machine.Pin(1), sda=machine.Pin(0)) 

pin = machine.Pin(16, machine.Pin.OUT)
#set GPIO16 low to reset OLED
pin.value(0)
#while OLED is running, must set GPIO16 in high
pin.value(1) 

#OLED screen 
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Volts = Analog.read/analogConversion
analogConversion = float(3552.8387)

maxVoltage = float(18.8)
maxAnalog = float(65535)

#Sleep in seconds
sleepSeconds = float(0.1)
decimalPlaces = 1

reading0 = float(0)
reading1 = float(0)
reading2 = float(0)
reading3 = float(0)
reading4 = float(0)
reading5 = float(0)
reading6 = float(0)
reading7 = float(0)
reading8 = float(0)
reading9 = float(0)

analogReadingArray = [reading0, reading1, reading2, reading3, reading4, reading5, reading6, reading7, reading8, reading9]

readingTotal = 0
readingTotalString = " "
trailingVChar = "V"
oledOutput = ""

while True:
    for y in range(0, len(analogReadingArray)):
        #Read analog pin every period
        #Store 10 values and round to 4 decimal places.
        analogReadingArray[y] = round((analog.read_u16()/analogConversion),decimalPlaces)
        sleep(sleepSeconds)    
        
    readingTotal = 0

    #Add all elements in Array.
    for z in range(0,len(analogReadingArray)):
        readingTotal = readingTotal + analogReadingArray[z]
    
    #Calculate Average
    readingAverage = round(readingTotal / len(analogReadingArray),decimalPlaces)
    
    
    #Convert to string
    readingTotalString = str(readingAverage)
    oledOutput = readingTotalString + trailingVChar
    
    #Display Average Voltage
    oled.fill(0)
    oled.text("Voltage", 0, 0)
    oled.text(oledOutput, 0, 30)
    oled.show()
        
    #Maintenance: 
    # Print readingTotalString line to serial. Then print current analog reading.
    print(readingTotalString,  "readingTotalString")
    print(analog.read_u16(), "AnalogPin" )
