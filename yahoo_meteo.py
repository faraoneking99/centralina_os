import yweather
from weather import Weather, Unit
from time import sleep
weather = Weather(unit=Unit.CELSIUS)

client = yweather.Client()

campagna_amato = client.fetch_woeid("amato di taurianova")
lookup = weather.lookup(campagna_amato)
sleep(1)
condition = lookup.condition
print(print(condition.text))