# Flight Analyser

A Python tool that fetches real-time flight data over the UK using the OpenSky Network API, analyses aircraft performance using the ISA atmosphere model, and visualises flights on an interactive map.

## Features

- Fetches live ADS-B flight data over the UK
- Calculates true airspeed using the ISA atmosphere model
- Detects flight phase (climbing, cruising, descending)
- Generates an altitude vs speed scatter plot
- Plots all flights on an interactive map

## Setup
```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

## Usage

Fetch and display live flights:
```bash
python fetch_flights.py
```

Run performance analysis:
```bash
python analyse.py
```

Generate visualisations:
```bash
python visualise.py
```

## Libraries used
- `requests` — API calls
- `pandas` — data processing
- `matplotlib` — charts
- `folium` — interactive maps