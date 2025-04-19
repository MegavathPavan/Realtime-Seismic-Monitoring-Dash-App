# Realtime-Seismic-monitoring-dash-app
An interactive Dash app that visualizes real-time global earthquake data using Plotly, Pandas, and the USGS API.

# 🌍 Live Earthquake Monitor Dashboard

An interactive web dashboard built with [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/python/) that visualizes real-time earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php). Explore earthquakes worldwide through dynamic maps, charts, and data tables.

---

## Demo

![Live Earthquake Dashboard Demo_1](https://github.com/MegavathPavan/Realtime-Seismic-Monitoring-Dash-App/blob/main/WebApp_Demo_1.png?raw=true)
![Live Earthquake Dashboard Demo_2](https://github.com/MegavathPavan/Realtime-Seismic-Monitoring-Dash-App/blob/main/WebApp_Demo_2.png?raw=true)

---

## Features

- **Worldwide Earthquake Coverage**
- Filter by time period: Last 24 hours, 7 days, or 30 days
- Multiple interactive visualizations:
  - Map with quake magnitude
  - Histogram of magnitude distribution
  - Time series of quake counts
  - Scatter plot (Magnitude vs Depth)
  - Bar chart of top affected regions
- Region-based filtering (e.g., North America, Asia)
- Minimum magnitude filtering
- Interactive data table with quake details
- **_Refresh button_** for live data updates

---

## Installation

### Clone the repository

```bash
git clone https://github.com/MegavathPavan/Realtime-Seismic-Monitoring-Dash-App.git
cd Realtime-Seismic-Monitoring-Dash-App
```

### Install dependencies

It's recommended to use a virtual environment.

```bash
pip install pandas numpy plotly dash dash-bootstrap-components pyngrok
```

### or

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python Seisemic_Dash_App.py
```

Open your browser and go to: `http://127.0.0.1:8050`

---

## Customization

You can customize the following:

- Add new regions in the `REGIONS` dictionary
- Modify the style using Dash’s `style` dictionaries or custom CSS
- Add additional metrics or visualizations using `Plotly`

---

## Data Source

All data is sourced live from the [USGS Earthquake API](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/):

- Past Day: `all_day.csv`
- Past Week: `all_week.csv`
- Past Month: `all_month.csv`


---
