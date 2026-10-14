
import requests


def get_exchange_rates(base_currency):
    """Retrieve exchange rates for a base currency."""

    url = f"https://open.er-api.com/v6/latest/{base_currency}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Could not retrieve exchange rates.")

    return data["rates"]


def main():
    print("=== Currency Information App ===")

    base_currency = input(
        "Enter the currency you have (e.g. USD, NGN): "
    ).strip().upper()

    target_currency = input(
        "Enter the currency you want (e.g. EUR, GBP): "
    ).strip().upper()

    try:
        amount = float(input("Enter the amount: "))

        if amount <= 0:
            print("Please enter an amount greater than zero.")
            return

        rates = get_exchange_rates(base_currency)

        if target_currency not in rates:
            print("The target currency is not supported.")
            return

        exchange_rate = rates[target_currency]
        converted_amount = amount * exchange_rate

        print(f"\nExchange rate: 1 {base_currency} = "
              f"{exchange_rate:.4f} {target_currency}")

        print(f"{amount:,.2f} {base_currency} = "
              f"{converted_amount:,.2f} {target_currency}")

    except ValueError as error:
        print(f"Input error: {error}")

    except requests.RequestException as error:
        print(f"Network or API error: {error}")

if __name__ == "__main__":
    main()
