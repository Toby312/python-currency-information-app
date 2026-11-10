# Currency Information App

A beginner-friendly Python application that retrieves exchange rates from an external API and converts amounts between currencies.

## Features

- Retrieve exchange rates using a currency API.
- Convert amounts between supported currencies.
- Display the exchange rate used for a conversion.
- Handle invalid inputs and API request errors.

## Technologies Used

- Python
- Requests
- ExchangeRate-API (Open access endpoint)

## Requirements

- Python 3.12 or a compatible Python version
- Internet connection

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Toby312/python-currency-information-app.gitY_URL
   ```

2. Navigate into the project directory:

   ```bash
   cd currency-app
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment on Linux:

   ```bash
   source venv/bin/activate
   ```

5. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```
6. Install the used packages
        ```bash
       python -m pip install streamlit pandas plotly requests
       ```

## Usage

Run the application:

```bash
python -m streamlit run app.py
```

Follow the prompts to enter the source currency, target currency, and amount.

## Learning Objectives

Current stopping point:
- Currency conversion.
- Exchange-rate analytics.
- Pandas data tables.
- CSV downloads.
- Summary metrics.
- Interactive Plotly charts.
- Streamlit Session State.
- API caching.
- Currency search and sorting.

## Disclaimer

Exchange rates are provided by an external API and may differ from rates offered by banks, payment providers, or currency exchange services.