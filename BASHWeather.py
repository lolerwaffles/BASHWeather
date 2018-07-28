import urllib,json,pandas,sys

WU_APIkey = '' #use your WeatherUnderground API key here
geo_APIkey = '' #user your https://ipstack.com/ API key here

#if sysarg doesn't contain ZIPcode, falls back to geolocation
with urllib.request.urlopen("http://ip.jsontest.com/") as url:
    ip = json.loads(url.read().decode())
    ip = ip['ip']

with urllib.request.urlopen(f'http://api.ipstack.com/{ip}?access_key={geo_APIkey}&format=1.json') as url:
    geo_zip = json.loads(url.read().decode())
geo_zip = geo_zip['zip']

zip_code = sys.argv[1] if len(sys.argv) > 1 else geo_zip

#forcast for the current day
with urllib.request.urlopen(f'http://api.wunderground.com/api/{WU_APIkey}/forecast/q/{zip_code}.json') as url:
    current = json.loads(url.read().decode())    
forcastRain = current['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['in'] 
forcastHigh = current['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
forcastLow = current['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']

#current conditions
with urllib.request.urlopen(f"http://api.wunderground.com/api/{WU_APIkey}/conditions/q/{zip_code}.json") as url:
    conditions = json.loads(url.read().decode())    
currentTemp = conditions['current_observation']['temp_f']
currentWindDir = conditions['current_observation']['wind_dir']
currentWindSP = conditions['current_observation']['wind_mph']
currentHumidity = conditions['current_observation']['relative_humidity']
currentLocation = conditions['current_observation']['display_location']['full']

#historical conditions, because its fun
with urllib.request.urlopen(f"http://api.wunderground.com/api/{WU_APIkey}/almanac/q/{zip_code}.json") as url:
    almanac = json.loads(url.read().decode())
normalHigh = almanac['almanac']['temp_high']['normal']['F']
recordHigh = almanac['almanac']['temp_high']['record']['F']
recordHighYear = almanac['almanac']['temp_high']['recordyear']
normalLow = almanac['almanac']['temp_low']['normal']['F']
recordLow = almanac['almanac']['temp_low']['record']['F']
recordLowYear = almanac['almanac']['temp_low']['recordyear']

#output to screen
tempHiSwitch ='above' if int(forcastHigh) >= int(normalHigh) else 'below'
recTempHiSwitch ='above' if int(forcastHigh) >= int(recordHigh) else 'below'
tempLowSwitch ='above' if int(forcastLow) >= int(normalLow) else 'below'
recTempLowSwitch ='above' if int(forcastLow) >= int(recordLow) else 'below'

print(f'The current tempatue is {currentTemp}° in {currentLocation} with {forcastRain}in of rain expected and a humity level of {currentHumidity}\n')
print(f'Winds are currently {currentWindSP}mph from {currentWindDir}\n')
print('The forcast high today is {}°, which is {}° {} the normal high of {}°, and is {}° {} the record of {}° set in {}\n'.format(forcastHigh, abs(int(forcastHigh) - int(normalHigh)), tempHiSwitch, normalHigh, abs(int(forcastHigh) - int(recordHigh)), recTempHiSwitch, recordHigh, recordHighYear))
print('The forcast low today is {}°, which is {}° {} the normal low of {}°, and is {}° {} the record of {}° set in {}'.format(forcastLow, abs(int(forcastLow) - int(normalLow)), tempLowSwitch, normalLow, abs(int(forcastLow) - int(recordLow)), recTempLowSwitch, recordLow, recordLowYear))

