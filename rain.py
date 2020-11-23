import requests,pyperclip,json
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
api_key = os.environ.get('OWM_API_KEY')

lat = 53.511 # replace with latitude
lon = 9.993 # replace with longitude
url = 'https://api.openweathermap.org/data/2.5/onecall'

params = {'lat': lat,'lon': lon,'appid': api_key,'exclude':'current,minutely,daily,alerts'}

response = requests.get(url,params=params)

response.raise_for_status()


weather = response.json()

hourly = weather['hourly']

# get twelve hours
for i in range(12):
    hour_data = hourly[i]
    any_rain = any(condition['id'] < 600 for condition in hour_data['weather'])
    if any_rain:
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                             body="It's going to rain today. Remember to bring an \u2602",
                             from_=os.environ.get('FROM_PHONE'),
                             to=os.environ.get('TO_PHONE')
                         )

        print(message.status)
        break












