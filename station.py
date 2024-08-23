import adafruit_bh1750
from bmp_280 import BMP280
import adafruit_ahtx0
import board

i2c = board.I2C()


#HEX DIRS
# BH1750 = 0x23
# BMP280 = 0x76
# AHT10 = 0x38
bh1750 = adafruit_bh1750.BH1750(i2c)
bmp = BMP280(port=1, mode=BMP280.FORCED_MODE, oversampling_p=BMP280.OVERSAMPLING_P_x16, oversampling_t=BMP280.OVERSAMPLING_T_x1,
            filter=BMP280.IIR_FILTER_OFF, standby=BMP280.T_STANDBY_1000)
# aht10 = adafruit_ahtx0.AHTx0(i2c)

def get_lux():
    return bh1750.lux

def get_temp_pressure():
    temp = bmp.read_temperature()
    press = bmp.read_pressure()
    return temp, press
# 
# def get_hum():
#     return aht10.relative_humidity