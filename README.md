# ClearTrip_Assignment
Automation Script To Find Top 5 Cheapest Flight From Bengaluru

# ✈️ Cleartrip Flight Price Scraper

This is a Python automation script using Selenium to scrape the top 5 cheapest flight details (name and price) from **Cleartrip** between **Bangalore (BLR)** and multiple destination cities.

## 📌 Features

- Automates the flight search process on [Cleartrip](https://www.cleartrip.com)
- Handles popups and navigates through UI reliably
- Selects predefined departure and return dates
- Extracts top 5 flight names and their prices
- Saves results to a CSV file (`flight_prices.csv`)

## 🧰 Requirements

- Python 3.7+
- Google Chrome installed
- [ChromeDriver](https://chromedriver.chromium.org/) compatible with your Chrome version

## 🔧 Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/cleartrip-flight-scraper.git
cd cleartrip-flight-scraper

2. Install dependencies:

bash
pip install -r requirements.txt
3. Make sure chromedriver is in your system PATH or update the path in webdriver.Chrome().
python cleartrip_flight_scraper.py

