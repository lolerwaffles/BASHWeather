import urllib,json,pandas,sys

zip_code = sys.argv[1] if len(sys.argv) > 1 else input("What is your ZIP code?\n")
API_Key = ''#use your WeatherUnderground API key here

#We really don't need all these variables to be pulled, but hey you might want them for the dislplay

#forcast for the current day
with urllib.request.urlopen(f'http://api.wunderground.com/api/{API_Key}/forecast/q/{zip_code}.json') as url:
    current = json.loads(url.read().decode())
    
forcastRain = current['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['in'] 
forcastHigh = current['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
forcastLow = current['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
forcastWindDir = current['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir']
forcastWindSp = current['forecast']['simpleforecast']['forecastday'][0]['avewind']['mph']
forcastSnow = current['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['in']
forcastHumidity = current['forecast']['simpleforecast']['forecastday'][0]['avehumidity']

#current conditions
with urllib.request.urlopen(f"http://api.wunderground.com/api/{API_Key}/conditions/q/{zip_code}.json") as url:
    conditions = json.loads(url.read().decode())
    
current1hrRain = conditions['current_observation']['precip_1hr_in']
currentTemp = conditions['current_observation']['temp_f']
currentWindDir = conditions['current_observation']['wind_dir']
currentWindSP = conditions['current_observation']['wind_mph']
currentHumidity = conditions['current_observation']['relative_humidity']
currentLocation = conditions['current_observation']['display_location']['full']

#historical conditions, because its fun
with urllib.request.urlopen(f"http://api.wunderground.com/api/{API_Key}/almanac/q/{zip_code}.json") as url:
    almanac = json.loads(url.read().decode())

normalHigh = almanac['almanac']['temp_high']['normal']['F']
recordHigh = almanac['almanac']['temp_high']['record']['F']
recordHighYear = almanac['almanac']['temp_high']['recordyear']
normalLow = almanac['almanac']['temp_low']['normal']['F']
recordLow = almanac['almanac']['temp_low']['record']['F']
recordLowYear = almanac['almanac']['temp_low']['recordyear']

#output to screen
print('The current tempatue is {}° in {} with {}in of rain expected and a humity level of {}%\n'.format(currentTemp, currentLocation, forcastRain, currentHumidity))
print('Winds are currently {}mph from {}\n'.format(currentWindSP, currentWindDir))

tempHiSwitch ='above' if int(forcastHigh) >= int(normalHigh) else 'below'
recTempHiSwitch ='above' if int(forcastHigh) >= int(recordHigh) else 'below'
print('The forcast high today is {}°, which is {}° {} the normal high of {}°, and is {}° {} the record of {}° set in {}\n'.format(forcastHigh, abs(int(forcastHigh) - int(normalHigh)), tempHiSwitch, normalHigh, abs(int(forcastHigh) - int(recordHigh)), recTempHiSwitch, recordHigh, recordHighYear))

tempLowSwitch ='above' if int(forcastLow) >= int(normalLow) else 'below'
recTempLowSwitch ='above' if int(forcastLow) >= int(recordLow) else 'below'
print('The forcast low today is {}°, which is {}° {} the normal low of {}°, and is {}° {} the record of {}° set in {}\n'.format(forcastLow, abs(int(forcastLow) - int(normalLow)), tempLowSwitch, normalLow, abs(int(forcastLow) - int(recordLow)), recTempLowSwitch, recordLow, recordLowYear))