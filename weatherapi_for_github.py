#import json and requests to get access to connectivity features

import requests
import json
from requests.auth import HTTPDigestAuth


#the temperature data is in Kelvins, convert this to Fahreinheit
def convertToKelvin(theTemp):
	temperatureInFahrenheit = 9 / 5 * (float(theTemp) - 273) + 32
	return temperatureInFahrenheit

#show the weather to the user
def displayTheWeather(cityName,temperatureInFahrenheit,weather):
		#display the information in a user friendly way
		print("The current temperature in " + cityName + " is " + str(format(round(temperatureInFahrenheit,2))) + " fahrenheit." )
		print("The weather is currently: "+weather)

#this function does all of the heavy lifting. Ask for data from openweathermap, interpret it, display it, and return any errors received
def getWeather(theZipCode):
	
	#take the zip code inputted by the user and ask for data from openweathermap. You can get an api key for free by registering at openweathermap.org
	url = "http://api.openweathermap.org/data/2.5/weather?zip="+theZipCode+",us&APPID=<api key>"
	
	#store the response
	myResponse = requests.get(url)
	
	#check if the response is good, otherwise return the error
	if(myResponse.ok):

		#convert the response to JSON
		data = myResponse.json()

		#find the City and temperature in the JSON and store them
		cityName = data['name']
		temperature = data['main']['temp']
		#the temperature data is in Kelvins, convert this to Fahreinheit	
		temperatureInFahrenheit = convertToKelvin(temperature)

		#find the weather description and store it
		weather = data['weather'][0]['description']

		#show the weather to the user
		displayTheWeather(cityName,temperatureInFahrenheit,weather)
	
	#if you received a bad response then error out, this should trigger the Except clause
	else:
		myResponse.raise_for_status()


#using this "while" loop allows you to submit multiple requests

while True: 

	#get input from the user and let them know they can stop the program
	print('Type "done" to exit')
	zipCode = input("What zip code's weather would you like to check? \n")

	#user can quit the program by inputtting "done"
	if zipCode == 'done': 
		quit()

	#using a try/except here to make sure they user is inputting a valid zip code. The request will return errors when receiving anything other than zip codes
	try :
		getWeather(zipCode)
	except:
		print("Invalid zip code")
		continue