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
        response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid=f0e68760922b874273e55afd93f6af6f&units=metric").json()

        responseData = pd.json_normalize(response, record_path="daily")
        print(type(responseData))
        responseData = responseData[1:2]
        responseData['pop'][1] = responseData['pop'][1] *100

        msg_text = f"Amanhã teremos uma mínima de: {responseData['temp.min'][1]}°C, uma máxima de: {responseData['temp.max'][1]}°C e {responseData['pop'][1]}% de chance de precipitação."

        # set permissions
        SCOPES = ['https://www.googleapis.com/auth/gmail.send',
                  'https://www.googleapis.com/auth/gmail.modify']

        # set up credentials
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

        # Create the message
        message = MIMEMultipart('alternative')
        message['Subject'] = "Previsão do tempo de amanhã!"
        message['From'] = 'vittorvc@gmail.com'
        message['To'] = 'vittorvc@gmail.com'
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

lat = -27.6140791
lon = -48.6370861

WeatherApp(lat=lat, lon=lon)
