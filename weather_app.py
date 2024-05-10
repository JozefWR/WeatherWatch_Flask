from flask import Flask, render_template, request
from flask import current_app
from dotenv import load_dotenv
from datetime import datetime
import statistics
import requests
import os
import json

load_dotenv()  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    current_date = datetime.now().strftime('%m-%d')
    current_time = datetime.now().strftime('%Y-%m-%d')
    miasto = None
    dane_pogodowe = None
    imieniny_dzisiaj = ', '.join(imieniny.get(current_date, ["Brak imienin"]))
    wschod_slonca = None
    zachod_slonca = None
    predkosc_wiatru = None  

    if request.method == 'POST':
        miasto = request.form['miasto']
        klucz_api = os.getenv('KLUCZ_API')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={klucz_api}&units=metric&lang=pl'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dane_pogodowe = response.json()
                wschod_slonca = datetime.fromtimestamp(dane_pogodowe['sys']['sunrise']).strftime('%H:%M:%S')
                zachod_slonca = datetime.fromtimestamp(dane_pogodowe['sys']['sunset']).strftime('%H:%M:%S')
                predkosc_wiatru = dane_pogodowe.get('wind', {}).get('speed', 'Brak danych')  
            else:
                dane_pogodowe = {'error': 'Nie udało się pobrać danych pogodowych. Sprawdź nazwę miasta.'}
        except requests.exceptions.RequestException as e:
            dane_pogodowe = {'error': f'Wystąpił błąd podczas połączenia z API pogodowym: {str(e)}'}

    return render_template('index.html', dane_pogodowe=dane_pogodowe, current_time=current_time, imieniny=imieniny_dzisiaj, miasto=miasto, wschod_slonca=wschod_slonca, zachod_slonca=zachod_slonca, predkosc_wiatru=predkosc_wiatru)

@app.route('/pogoda_godzinowa/<miasto>')
def pogoda_godzinowa(miasto):
    klucz_api = os.getenv('KLUCZ_API')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={miasto}&appid={klucz_api}&units=metric&lang=pl"
    response = requests.get(url)
    
    if response.status_code == 200:
        dane_pogodowe = response.json()

        daty_godziny = [datetime.strptime(p['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m %H:%M') for p in dane_pogodowe['list']]
        temperatury = [p['main']['temp'] for p in dane_pogodowe['list']]

        current_time = datetime.now().date()

        return render_template('pogoda_godzinowa.html', 
                               daty_godziny=daty_godziny, 
                               temperatury=temperatury, 
                               miasto=miasto, 
                               dane_pogodowe=dane_pogodowe,
                               current_time=current_time)
    else:
        error_message = f"Nie udało się pobrać prognozy godzinowej dla miasta {miasto}."
        return render_template('error.html', error=error_message)

@app.route('/pogoda_usredniona/<miasto>')
def pogoda_usredniona(miasto):
    klucz_api = os.getenv('KLUCZ_API')
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={miasto}&appid={klucz_api}&units=metric&lang=pl"
    response = requests.get(url)
    if response.status_code == 200:
        dane_pogodowe = response.json()
        prognoza_po_dniach = {}
        opisy_poludniowe = {}
        
        current_time = datetime.now().date()

        for prognoza in dane_pogodowe['list']:
            data_prognozy = datetime.strptime(prognoza['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
            data_formatowana = data_prognozy.strftime('%d-%m') # Tutaj formatujemy datę
            
            if data_formatowana not in prognoza_po_dniach:
                prognoza_po_dniach[data_formatowana] = []
            
            prognoza_po_dniach[data_formatowana].append(prognoza['main']['temp'])
            
            if datetime.strptime(prognoza['dt_txt'], '%Y-%m-%d %H:%M:%S').time().hour == 12:
                opisy_poludniowe[data_formatowana] = prognoza['weather'][0]['description']
        
        srednie_temperatury = {data: statistics.mean(temperatury) for data, temperatury in prognoza_po_dniach.items()}
        
        return render_template('pogoda_usredniona.html', 
                       srednie_temperatury=srednie_temperatury, 
                       opisy_poludniowe=opisy_poludniowe, 
                       miasto=miasto,
                       current_time=current_time)
    else:
        return render_template('error.html', error='Nie udało się pobrać prognozy.')

def get_coordinates(city_name, api_key):
    """Zwraca tuple (latitude, longitude) dla danego miasta używając OpenWeatherMap API"""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(geo_url)
    if response.status_code == 200 and response.json():
        results = response.json()
        lat = results[0]['lat']
        lon = results[0]['lon']
        return lat, lon
    return None, None

@app.route('/jakosc_powietrza/<miasto>')
def jakosc_powietrza(miasto):
    current_app.logger.debug(f"Requesting air quality for {miasto}")
    api_key = os.getenv('KLUCZ_API')
    lat, lon = get_coordinates(miasto, api_key)
    if lat is None or lon is None:
        return render_template('error.html', error="Nie udało się uzyskać współrzędnych dla podanego miasta.")

    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(air_url)
    if response.status_code == 200:
        air_quality_data = response.json()
        current_time = datetime.now().date()
        return render_template('jakosc_powietrza.html', dane_powietrza=air_quality_data, miasto=miasto, current_time=current_time)
    else:
        error_message = f"Nie udało się pobrać danych o jakości powietrza dla miasta {miasto}."
        return render_template('error.html', error=error_message)
    
def load_imieniny():
    with open('imieniny.json', 'r', encoding='utf-8') as file:
        return json.load(file)

imieniny = load_imieniny()
    
if __name__ == '__main__':
    app.run(debug=True)
