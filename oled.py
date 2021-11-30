# ttgo_fonts.py
# Pages through all characters of four fonts on the LILYGO® TTGO T-Display.
# https://www.youtube.com/watch?v=2cnAhEucPD4
from time import sleep                          # für die Messung der Sensoren
from machine import Pin, SoftSPI, SoftI2C       # Pin (BMP180 & TFT), SoftSPI (TFT) und SoftI2C (BMP180)
import st7789py as st7789                       # TFT (Display)
from bmp180 import BMP180                       # BMP180 (Sensor)
#----------------------------------------------------------------------------------------------------------
# CHoose fonts
#----------------------------------------------------------------------------------------------------------
from romfonts import vga2_16x16 as font         # Schriftart laden

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))         # I2C (BMP180)
bmp = BMP180(i2c)                               # Objekt bmp instanzieren

#------- Initialisierung Anfang -----
spi = SoftSPI(                                  # Objekt spi (TFT) instanzieren
        baudrate=20000000,                      # Kommunikationsgeschwindikeit
        polarity=1,                             
        phase=0,                                
        sck=Pin(18),                            
        mosi=Pin(19),                           
        miso=Pin(13))                           

tft = st7789.ST7789(                            # Objekt tft intanzieren
        spi,                                    # Schnittstelle
        135,                                    # Pixel X-Achse (Hochkant)
        240,                                    # Pixel Y-Achse (Hochkant)
        reset=Pin(23, Pin.OUT),                  
        cs=Pin(5, Pin.OUT),                     
        dc=Pin(16, Pin.OUT),                    
        backlight=Pin(4, Pin.OUT),               
        rotation=1)                             # Rotation 0=000°, 1=090°, 2=180°, 3=270°

gruenLED = Pin(25, Pin.OUT)
gelbLED  = Pin(26, Pin.OUT)
rotLED   = Pin(27, Pin.OUT)
#-------- Initialisierung Ende ------


line = 0                                                                # Zeile                                         (werden hier überschrieben)
col = 0                                                                 # Spalte                                        (werden hier überschrieben)
while True:                                                             
    if bmp.temperature < 24:
        tft.fill(st7789.GREEN)    
        gruenLED.value(1)
        gelbLED.value(0)
        rotLED.value(0)
    elif bmp.temperature <25:
        tft.fill(st7789.YELLOW)
        gruenLED.value(0)
        gelbLED.value(1)
        rotLED.value(0)
    else:
        tft.fill(st7789.RED)   
        gruenLED.value(0)
        gelbLED.value(0)
        rotLED.value(1)    
    ausgabe = str(round(bmp.temperature,1))                             # ausgabe der Temperatur in string 
    ausgabe = str(ausgabe + ' \xf8C')
    tft.text(font, ausgabe, 10, 10, st7789.WHITE, st7789.BLACK)
    luftDruck = str(round(bmp.pressure / 100,1))
    ausgabe2 = str(luftDruck + ' hPa') 
    tft.text(font, ausgabe2, 10, 30, st7789.WHITE, st7789.BLACK)         # Schrift = Weiß, Schrifthintergrund = Schwarz    