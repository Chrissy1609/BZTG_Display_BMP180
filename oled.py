# ttgo_fonts.py
# Pages through all characters of four fonts on the LILYGO® TTGO T-Display.
# https://www.youtube.com/watch?v=2cnAhEucPD4
from time import sleep                          # für die Messung der Sensoren                                          # Bibliothek Wartezeit
from machine import Pin, SoftSPI, SoftI2C       # Pin (BMP180 & TFT), SoftSPI (TFT) und SoftI2C (BMP180)                # Bibliothek Pin, Busssystem
import st7789py as st7789                       # TFT (Display)                                                         # Bibliothek Display
from bmp180 import BMP180                       # BMP180 (Sensor)                                                       # Bibliothek Sensor BMP180 (Temperatur,Luftdruck)
#----------------------------------------------------------------------------------------------------------
# CHoose fonts
#----------------------------------------------------------------------------------------------------------
from romfonts import vga2_16x16 as font         # Schriftart laden                                                      # Schriftart aus Ordner laden

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))         # I2C (BMP180)                                                          # Busssystem mit den Pins verbunden
bmp = BMP180(i2c)                               # Objekt bmp instanzieren                                               # Sensor mit Busssystem verbunden

#------- Initialisierung Anfang -----
spi = SoftSPI(                                  # Objekt spi (TFT) instanzieren                                         # Parameter Busssystem eingestellt
        baudrate=20000000,                      # Kommunikationsgeschwindikeit
        polarity=1,                             
        phase=0,                                
        sck=Pin(18),                            
        mosi=Pin(19),                           
        miso=Pin(13))                           

tft = st7789.ST7789(                            # Objekt tft intanzieren                                                # Parameter Display eingestellt
        spi,                                    # Schnittstelle
        135,                                    # Pixel X-Achse (Hochkant)          
        240,                                    # Pixel Y-Achse (Hochkant)
        reset=Pin(23, Pin.OUT),                  
        cs=Pin(5, Pin.OUT),                     
        dc=Pin(16, Pin.OUT),                    
        backlight=Pin(4, Pin.OUT),               
        rotation=1)                             # Rotation 0=000°, 1=090°, 2=180°, 3=270°                               # Ausrichtung der Schrift auf dem Display

gruenLED = Pin(25, Pin.OUT)                                                                                             # Pin(25) Ausgang an Led verbunden
gelbLED  = Pin(26, Pin.OUT)                                                                                             # Pin(26) Ausgang an Led verbunden
rotLED   = Pin(27, Pin.OUT)                                                                                             # Pin(27) Ausgang an Led verbunden
#-------- Initialisierung Ende ------


line = 0                                        # Zeile     (werden hier überschrieben)
col = 0                                         # Spalte    (werden hier überschrieben)
while True:                                                                                                             # Wiederholende Schleife
    if bmp.temperature < 24:                                                                                            # Wenn die Temperatur unter 24°C ist dann mach das:
        tft.fill(st7789.GREEN)                                                                                          # Hintergrund Display Grün
        gruenLED.value(1)                                                                                               # Ausgang Grüne Led freischalten
        gelbLED.value(0)                                                                                                # Ausgang Gelbe Led ausschalten
        rotLED.value(0)                                                                                                 # Ausgang Rote Led ausschalten         sonst mache:
    elif bmp.temperature <25:                                                                                           # Wenn die Temperatur unter 25°C ist dann mach das:  
        tft.fill(st7789.YELLOW)                                                                                         # Hintergrund Display Gelb
        gruenLED.value(0)                                                                                               # Ausgang Grüne Led ausschalten
        gelbLED.value(1)                                                                                                # Ausgang Gelbe Led freischalten
        rotLED.value(0)                                                                                                 # Ausgang Rote Led ausschalten
    else:                                                                                                               # Sonst mach das:
        tft.fill(st7789.RED)                                                                                            # Hintergrund Display Rot
        gruenLED.value(0)                                                                                               # Ausgang Grüne Led ausschalten
        gelbLED.value(0)                                                                                                # Ausgang Gelbe Led ausschalten
        rotLED.value(1)                                                                                                 # Ausgang Rote Led freischalten
    ausgabe = str(round(bmp.temperature,1))       # ausgabe der Temperatur in string                                    # str für Werte für das Display 
    ausgabe = str(ausgabe + ' \xf8C')                                                                                   # \xf8 = ° Unicode
    tft.text(font, ausgabe, 10, 10, st7789.WHITE, st7789.BLACK)                                                         # Ausgabe auf dem Display mit weißer Schrift, Schwarzer Hintergrund
    luftDruck = str(round(bmp.pressure / 100,1))
    ausgabe2 = str(luftDruck + ' hPa') 
    tft.text(font, ausgabe2, 10, 30, st7789.WHITE, st7789.BLACK)                                                        # Schrift = Weiß, Schrifthintergrund = Schwarz    