import requests
import streamlit as st


# Configure the page
st.set_page_config(
    page_title="Currency Information App",
    page_icon="💱",
    layout="wide"
)


# Application title
st.title("💱 Currency Information Dashboard")

st.write(
    "Convert currencies and explore exchange rates "
    "using data from an external API."
)


# Supported currencies for our initial dropdowns
CURRENCIES = {
    "USD": "US Dollar",
    "NGN": "Nigerian Naira",
    "EUR": "Euro",
    "GBP": "British Pound",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "INR": "Indian Rupee",
    "JPY": "Japanese Yen",
    "GHS": "Ghanaian Cedi",
    "ZAR": "South African Rand",
}


def get_exchange_rates(base_currency):
    """Retrieve exchange rates for a base currency."""

    url = (
        "https://open.er-api.com/v6/latest/"
        f"{base_currency}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Could not retrieve exchange rates.")

    return data["rates"]


# Create the converter section
st.header("Currency Converter")

col1, col2 = st.columns(2)

with col1:
    base_currency = st.selectbox(
        "From currency",
        options=list(CURRENCIES.keys()),
        index=1
    )

with col2:
    target_currency = st.selectbox(
        "To currency",
        options=list(CURRENCIES.keys()),
        index=0
    )


amount = st.number_input(
    "Amount to convert",
    min_value=0.01,
    value=1000.0,
    step=100.0
)


if st.button("Convert Currency", type="primary"):

    try:
        with st.spinner("Retrieving exchange rates..."):

            rates = get_exchange_rates(base_currency)

            exchange_rate = rates[target_currency]
            converted_amount = amount * exchange_rate

        st.success("Conversion completed!")

        st.metric(
            label=f"Amount in {target_currency}",
            value=f"{converted_amount:,.2f} {target_currency}"
        )

        st.write(
            f"1 {base_currency} = "
            f"{exchange_rate:,.4f} {target_currency}"
        )

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(
            "Unable to complete the conversion. "
            "Please try again."
        )

        print(f"Conversion error: {error}")


st.caption(
    "Exchange rates are provided by an external service. "
    "Actual rates offered by banks and payment providers may differ."
)