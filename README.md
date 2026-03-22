# Ceneo Web Scraper

Projekt webowej aplikacji w Pythonie z użyciem Flask.

## Opis projektu

Aplikacja służy do pobierania opinii o produktach z serwisu Ceneo na podstawie `product_id`.
Pobrane dane są zapisywane do plików oraz prezentowane w aplikacji webowej.

## Funkcjonalności

- pobieranie danych produktu i opinii
- zapis opinii do plików JSON, CSV i XLSX
- zapis informacji o produkcie do JSON
- lista zapisanych produktów
- strona produktu ze statystykami
- tabela opinii
- filtrowanie i sortowanie opinii
- wykres rekomendacji
- wykres rozkładu ocen

## Użyte technologie

- Python
- Flask
- requests
- BeautifulSoup
- pandas
- Chart.js

## Struktura projektu

- `app/models.py` — modele danych `Product` i `Opinion`
- `app/scraper.py` — pobieranie i parsowanie danych z Ceneo
- `app/helpers.py` — statystyki, zapis i odczyt plików
- `app/routes.py` — route aplikacji Flask
- `app/templates/` — szablony HTML
- `app/static/` — style CSS
- `run.py` — uruchamianie aplikacji

## Uruchomienie projektu

1. utworzenie środowiska:
   ```bash
   py -m venv venv