
import requests
import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Currency Information App",
    page_icon="💱",
    layout="wide"
)


# --------------------------------------------------
# SUPPORTED CURRENCIES
# --------------------------------------------------

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


# --------------------------------------------------
# FETCH EXCHANGE RATES
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_exchange_rates(base_currency):
    """
    Fetch exchange rates from the ExchangeRate API.
    Cache the result for 10 minutes.
    """

    url = (
        "https://open.er-api.com/v6/latest/"
        f"{base_currency}"
    )

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError(
            "Could not retrieve exchange rates."
        )

    return data["rates"]


# --------------------------------------------------
# APP TITLE
# --------------------------------------------------

st.title("💱 Currency Information App")

st.write(
    "Convert currencies and explore exchange rate information."
)

st.divider()


# --------------------------------------------------
# CURRENCY CONVERTER
# --------------------------------------------------

st.header("Currency Converter")

converter_col1, converter_col2 = st.columns(2)

with converter_col1:

    amount = st.number_input(
        "Enter Amount",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

    from_currency = st.selectbox(
        "From Currency",
        options=list(CURRENCIES.keys()),
        index=0
    )


with converter_col2:

    to_currency = st.selectbox(
        "To Currency",
        options=list(CURRENCIES.keys()),
        index=1
    )


if st.button("Convert Currency", type="primary"):

    try:

        rates = get_exchange_rates(from_currency)

        exchange_rate = rates[to_currency]

        converted_amount = amount * exchange_rate

        st.success("Conversion Successful!")

        st.metric(
            label=f"{amount:,.2f} {from_currency} in {to_currency}",
            value=f"{converted_amount:,.2f} {to_currency}"
        )

        st.caption(
            f"1 {from_currency} = "
            f"{exchange_rate:.4f} {to_currency}"
        )

    except requests.exceptions.RequestException:

        st.error(
            "Unable to connect to the exchange rate API. "
            "Please check your internet connection and try again."
        )

    except (ValueError, KeyError):

        st.error(
            "Unable to retrieve the selected exchange rate."
        )


st.divider()


# --------------------------------------------------
# ANALYTICS SECTION
# --------------------------------------------------

st.header("📊 Exchange Rate Analytics")

analytics_base = st.selectbox(
    "Select Base Currency",
    options=list(CURRENCIES.keys()),
    index=0,
    key="analytics_base"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "rates_df" not in st.session_state:

    st.session_state.rates_df = None


if "loaded_base" not in st.session_state:

    st.session_state.loaded_base = None


# --------------------------------------------------
# LOAD EXCHANGE RATES
# --------------------------------------------------

if st.button("Load Exchange Rates"):

    try:

        rates = get_exchange_rates(analytics_base)

        rates_data = []

        for currency_code, currency_name in CURRENCIES.items():

            if currency_code in rates:

                rates_data.append(
                    {
                        "Currency": currency_code,
                        "Currency Name": currency_name,
                        "Exchange Rate": rates[currency_code]
                    }
                )

        if not rates_data:

            st.error(
                "No exchange rates were found for the selected currency."
            )

        else:

            rates_df = pd.DataFrame(rates_data)

            rates_df = rates_df.sort_values(
                by="Exchange Rate",
                ascending=False
            )

            st.session_state.rates_df = rates_df

            st.session_state.loaded_base = analytics_base

            st.success(
                f"Exchange rates loaded successfully for {analytics_base}!"
            )

    except requests.exceptions.RequestException:

        st.error(
            "Unable to connect to the exchange rate API."
        )

    except ValueError as error:

        st.error(str(error))

    except KeyError:

        st.error(
            "The exchange rate data is incomplete."
        )


# --------------------------------------------------
# DISPLAY ANALYTICS
# --------------------------------------------------

if st.session_state.rates_df is not None:

    rates_df = st.session_state.rates_df

    loaded_base = st.session_state.loaded_base

    st.subheader(
        f"Exchange Rates Based on {loaded_base}"
    )


    # ----------------------------------------------
    # SEARCH AND SORT
    # ----------------------------------------------

    st.subheader("Exchange Rate Table")

    search_col, sort_col = st.columns(2)


    with search_col:

        search_term = st.text_input(
            "Search Currency",
            placeholder="Search by currency code or name"
        )


    with sort_col:

        sort_order = st.selectbox(
            "Sort Exchange Rates",
            options=[
                "Highest to Lowest",
                "Lowest to Highest"
            ]
        )


    # Create a separate dataframe for filtering

    filtered_df = rates_df.copy()


    # ----------------------------------------------
    # SEARCH FILTER
    # ----------------------------------------------

    if search_term:

        currency_matches = filtered_df["Currency"].str.contains(
            search_term,
            case=False,
            na=False,
            regex=False
        )

        name_matches = filtered_df["Currency Name"].str.contains(
            search_term,
            case=False,
            na=False,
            regex=False
        )

        filtered_df = filtered_df[
            currency_matches | name_matches
        ]


    # ----------------------------------------------
    # SORT FILTERED DATA
    # ----------------------------------------------

    if sort_order == "Highest to Lowest":

        filtered_df = filtered_df.sort_values(
            by="Exchange Rate",
            ascending=False
        )

    else:

        filtered_df = filtered_df.sort_values(
            by="Exchange Rate",
            ascending=True
        )


    # ----------------------------------------------
    # DISPLAY TABLE
    # ----------------------------------------------

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


    st.caption(
        f"Showing {len(filtered_df)} of "
        f"{len(rates_df)} supported currencies."
    )


    # ----------------------------------------------
    # CSV DOWNLOAD
    # ----------------------------------------------

    st.subheader("Export Exchange Rates")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="Download Exchange Rates as CSV",
        data=csv_data,
        file_name=f"{loaded_base}_exchange_rates.csv",
        mime="text/csv"
    )


    # ----------------------------------------------
    # SUMMARY METRICS
    # ----------------------------------------------

    st.subheader("Exchange Rate Summary")


    metric_col1, metric_col2, metric_col3 = st.columns(3)


    with metric_col1:

        st.metric(
            label="Currencies Available",
            value=len(rates_df)
        )


    with metric_col2:

        highest_rate = rates_df["Exchange Rate"].max()

        st.metric(
            label="Highest Exchange Rate",
            value=f"{highest_rate:,.4f}"
        )


    with metric_col3:

        lowest_rate = rates_df["Exchange Rate"].min()

        st.metric(
            label="Lowest Exchange Rate",
            value=f"{lowest_rate:,.4f}"
        )


    # ----------------------------------------------
    # CHART SECTION
    # ----------------------------------------------

    st.subheader("Exchange Rate Visualization")


    chart_type = st.radio(
        "Select Chart Type",
        options=[
            "Bar Chart",
            "Line Chart"
        ],
        horizontal=True
    )


    # ----------------------------------------------
    # DISPLAY CHART
    # ----------------------------------------------

    if not filtered_df.empty:

        if chart_type == "Bar Chart":

            fig = px.bar(
                filtered_df,
                x="Currency",
                y="Exchange Rate",
                title=f"Exchange Rates Compared to {loaded_base}",
                labels={
                    "Currency": "Currency",
                    "Exchange Rate": f"Rate per 1 {loaded_base}"
                },
                hover_data=[
                    "Currency Name",
                    "Exchange Rate"
                ]
            )


        else:

            fig = px.line(
                filtered_df,
                x="Currency",
                y="Exchange Rate",
                markers=True,
                title=f"Exchange Rates Compared to {loaded_base}",
                labels={
                    "Currency": "Currency",
                    "Exchange Rate": f"Rate per 1 {loaded_base}"
                },
                hover_data=[
                    "Currency Name",
                    "Exchange Rate"
                ]
            )


        fig.update_layout(
            xaxis_title="Currency",
            yaxis_title=f"Exchange Rate per 1 {loaded_base}",
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.warning(
            "No currencies match your search. "
            "Try another currency code or name."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Currency Information App | Built with Python, "
    "Streamlit, Pandas, Requests, and Plotly."
)
