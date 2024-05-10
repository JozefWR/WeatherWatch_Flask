# WeatherWatch_Flask

## O projekcie

WeatherWatch_Flask to interaktywna aplikacja webowa zbudowana w oparciu o Flask, która pozwala użytkownikom monitorować warunki pogodowe oraz jakość powietrza. Aplikacja umożliwia sprawdzanie bieżącej pogody, prognoz godzinowych i dziennych, a także informuje o jakości powietrza w wybranych lokalizacjach.

## Funkcjonalności

- **Pogoda na żywo**: Wyświetla aktualną temperaturę, opis pogodowy, prędkość wiatru oraz czasy wschodu i zachodu słońca.
- **Prognoza godzinowa**: Pokazuje temperaturę na nadchodzące godziny z opisem pogodowym.
- **Średnia temperatura**: Zapewnia prognozę średniej temperatury na nadchodzące dni z opisem pogodowym w południe.
- **Jakość powietrza**: Informuje o stężeniu składników zanieczyszczających powietrze w danej lokalizacji.
- **Imieniny**: Codziennie aktualizuje informacje o imieninach.

## Technologie

- **Flask**: Pythonowy mikro-framework webowy.
- **HTML/CSS**: Struktura i styl front-endu.
- **Chart.js**: Biblioteka do tworzenia interaktywnych wykresów.
- **OpenWeatherMap API**: Źródło danych pogodowych i jakości powietrza.
- **Python**: Logika przetwarzania danych pogodowych na backendzie.

## Screenshoty

![Strona główna aplikacji](https://github.com/JozefWR/WeatherWatch_Flask/assets/166382259/2013e985-6e75-4abf-b39b-4000cec3c44a)
![Prognoza godzinowa](https://github.com/JozefWR/WeatherWatch_Flask/assets/166382259/5f2c4d0b-0428-4eb6-8f9a-1014bc4925e8)
![Prognoza uśredniona](https://github.com/JozefWR/WeatherWatch_Flask/assets/166382259/af56a843-4927-4f8e-8399-9dec70e3aa7d)
![Jakość powietrza](https://github.com/JozefWR/WeatherWatch_Flask/assets/166382259/6ea0275d-8baa-4f65-9d6f-1c6432595366)
![Wykres godzinowy](file-HYhZ7iunU3sTXGh1j7i4nep3)
![Wykres uśrednionej prognozy](file-QgirkH8oZn0cL8pTwz7fQZc6)

## Instalacja i uruchomienie
1. **Klonowanie repozytorium**
   ```bash
   git clone https://github.com/JozefWR/WeatherWatch_Flask.git
2. **Instalacja zależności**
   ```bash
   pip install -r requirements.txt
3. **Konfiguracja pliku .env**
Utwórz plik `.env` w głównym katalogu projektu i dodaj do niego klucz API z OpenWeatherMap:

4. **Uruchomienie aplikacji**
   ```bash
   python weather_app.py
