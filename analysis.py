"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Failed to retrieve customer data: {error}")
        return []



def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a nested record with its type and indentation."""

    if isinstance(record, dict):
        for key, value in record.items():
            print(" " * indent + f"{key}: {type(value).__name__}")

            if isinstance(value, (dict, list)):
                explore(value, indent + 4)

    elif isinstance(record, list):
        for item in record:
            explore(item, indent + 4)




def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dictionary per customer with the required attributes."""
    rows = []

    for customer in customers:
        email = customer["email"]

        row = {
            "id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": email,
            "email_domain": email.rsplit("@", 1)[-1],
            "phone": customer["phone"],
            "city": customer["address"]["city"],
            "zipcode": customer["address"]["zipcode"],
            "latitude": float(customer["address"]["geo"]["lat"]),
            "longitude": float(customer["address"]["geo"]["lng"]),
            "company": customer["company"]["name"],
            "website": customer["website"]
        }

        rows.append(row)

    return rows

    


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    cities = set()

    for customer in customers:
        city = customer["address"]["city"]
        cities.add(city)

    return cities
    


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a dictionary."""
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]

        if city in counts:
            counts[city] += 1
        else:
            counts[city] = 1

    return counts



def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers by email top-level domain."""
    domains = {}

    for customer in customers:
        email = customer["email"]
        domain = email.rsplit(".", 1)[-1]

        if domain in domains:
            domains[domain] += 1
        else:
            domains[domain] = 1

    return domains


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert cleaned customer records into a pandas DataFrame."""
    df = pd.DataFrame(rows)
    return df


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    sorted_counts = dict(
        sorted(counts.items(), key=lambda item: item[1], reverse=True)
    )

    plt.figure(figsize=(9, 5))
    plt.bar(sorted_counts.keys(), sorted_counts.values())
    plt.title("Customer Distribution by Email Top-Level Domain")
    plt.xlabel("Email Top-Level Domain")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45)
    plt.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()


if __name__ == "__main__":
    customers = get_customers()

    print("Number of customers:", len(customers))
    print("First customer:")
    print(customers[0] if customers else "No data retrieved")

    print("\nExploring the first customer:")
    if customers:
        explore(customers[0])

    rows = extract_attributes(customers)

    print("\nFirst cleaned customer:")
    print(rows[0] if rows else "No data to display")

    cities = unique_cities(customers)

    print("\nUnique cities:", cities)
    print("Number of unique cities:", len(cities))
    print("Number of customers:", len(customers))

    counts = city_counts(customers)

    print("\nCustomers per city (most common first):")
    for city, count in sorted(
        counts.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{city}: {count}")

    domain_counts = email_domain_counts(customers)

    print("\nCustomers by email top-level domain (most common first):")
    for domain, count in sorted(
        domain_counts.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{domain}: {count}")

    df = to_dataframe(rows)

    print("\nDataFrame shape (rows, columns):", df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nCustomers by city using pandas:")
    print(df["city"].value_counts())

    print("\nCustomers by email domain using pandas:")
    print(df["email_domain"].value_counts())

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export cleaned customer data
    df.to_csv(output_dir / "customers.csv", index=False)

    # Export city counts
    city_df = pd.DataFrame(
        list(counts.items()),
        columns=["city", "customer_count"]
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    print("\nCSV files exported successfully!")
    print("Saved:", output_dir / "customers.csv")
    print("Saved:", output_dir / "city_counts.csv")

    chart_path = output_dir / "customer_distribution.png"
    plot_distribution(domain_counts, chart_path)

    print("Saved chart:", chart_path)