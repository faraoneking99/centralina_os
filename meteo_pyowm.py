from pyowm import OWM
from time import sleep


API_key = ""
owm = OWM(API_key=API_key)


amato_latitudine, amato_longitudine = 38.369992, 15.954787
roma_latitudine, roma_longitudine = 41.903942, 12.550115

# w.get_status()) ritorna il meteo (sole, nuovole, pioggia, ect)
# w.get_rain()) ritorna le info sulla pioggia
# w.get_temperature(unit="celsius")) ritorna temp, temp_max, temp_min

def get_current_weather( latitudine, longitudine):
    obs = owm.weather_at_coords(latitudine, longitudine)
    w = obs.get_weather()
    sleep(0.05)
    return w

