"""
This is a script for retrieving weather information from a determined location on Earth.
It makes use of the requests library to access the OpenWeatherMap API.
Then the data retrieved is treated properly with Pandas, filtering by daily measures only.
Finally, it sends and e-mail with the retrieved information using the Gmail API.
Because this app is not verified by google and makes used of restricted scopes, it takes
an extra step of authorization to access the gmail account.
"""

import requests
import pandas as pd
import pickle
import os
import base64
import googleapiclient.discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow

class WeatherApp():
    def __init__(self, lat, lon):

        # Makes a request to the OpenWeatherMap API and retrieves the data
        response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={os.environ.get('OWM_API_KEY')}&units=metric").json()

        # Builds a Pandas DataFrame with the data retrieved from the API
        responseData = pd.json_normalize(response, record_path="daily")
        print(responseData)

        # Selects only the first row, meaning the information for the day after today
        responseData = responseData[1:2]
        # Puts the precipitation chance in percentage
        responseData['pop'][1] = responseData['pop'][1] * 100

        # Plain text to be sent by e-mail
        msg_text = f"Amanhã teremos uma mínima de: {responseData['temp.min'][1]}°C, uma máxima de: {responseData['temp.max'][1]}°C e {responseData['pop'][1]}% de chance de precipitação."

        # Set permissions
        SCOPES = ['https://www.googleapis.com/auth/gmail.send',
                  'https://www.googleapis.com/auth/gmail.modify']

        # Set up credentials
        home_dir = os.getcwd()

        json_path = os.path.join(home_dir, 'credentials.json')

        flow = InstalledAppFlow.from_client_secrets_file(json_path, SCOPES)

        creds = flow.run_local_server(port=0)

        pickle_path = os.path.join(home_dir, 'gmail.pickle')
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)

        home_dir = os.getcwd()
        pickle_path = os.path.join(home_dir, 'gmail.pickle')
        creds = pickle.load(open(pickle_path, 'rb'))

        # Build the service
        service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

        # Create the message to be sent
        message = MIMEMultipart('alternative')
        message['Subject'] = "Previsão do tempo de amanhã!"
        message['From'] = os.environ.get('USER_EMAIL')
        message['To'] = os.environ.get('USER_EMAIL')
        messageHtml = '<b>Weather Update!</b>'
        messagePlain = msg_text
        message.attach(MIMEText(messageHtml, 'html'))
        message.attach(MIMEText(messagePlain, 'plain'))
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}

        message_first = body
        message_full = (
            service.users().messages().send(
                userId="me", body=message_first).execute())
        print('Message sent!')

# Geografical coordinates of Florianópolis - SC, Brazil
lat = -27.6140791
lon = -48.6370861

WeatherApp(lat=lat, lon=lon)
