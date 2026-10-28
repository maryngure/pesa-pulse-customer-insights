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
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": email,
            "email_domain": email.rsplit(".", 1)[-1],
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
    """Return the set of distinct customer cities."""
    return {customer["address"]["city"] for customer in customers}
    


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
    domains = {
        customer["email"].rsplit(".", 1)[-1]
        for customer in customers
    }

    return {
        domain: sum(
            1
            for customer in customers
            if customer["email"].rsplit(".", 1)[-1] == domain
        )
        for domain in domains
    }


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert cleaned customer records into a pandas DataFrame."""
    df = pd.DataFrame(rows)
    return df


def plot_distribution(
    counts: dict[str, int],
    path: Path,
    title: str,
    xlabel: str
) -> None:
    """Save a labelled bar chart of a distribution."""
    sorted_counts = sorted(
        counts.items(), key=lambda x: (-x[1], x[0])
    )

    labels = [item[0] for item in sorted_counts]
    values = [item[1] for item in sorted_counts]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=150)
    plt.close()



if __name__ == "__main__":
    customers = get_customers()

    # Stop execution if the API returns no data
    if not customers:
        raise SystemExit("Analysis stopped: no customer data was retrieved.")

    print("Number of customers:", len(customers))
    print("First customer:")
    print(customers[0])

    print("\nExploring the first customer:")
    explore(customers[0])

    rows = extract_attributes(customers)

    print("\nFirst cleaned customer:")
    print(rows[0])

    cities = unique_cities(customers)

    print("\nUnique cities:", cities)
    print("Number of unique cities:", len(cities))
    print("Number of customers:", len(customers))

    counts = city_counts(customers)

    print("\nCustomers per city (most common first):")
    for city, count in sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    ):
        print(f"{city}: {count}")

    domain_counts = email_domain_counts(customers)

    print("\nCustomers by email top-level domain (most common first):")
    for domain, count in sorted(
        domain_counts.items(), key=lambda item: (-item[1], item[0])
    ):
        print(f"{domain}: {count}")

    df = to_dataframe(rows)

    print("\nDataFrame shape (rows, columns):", df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nCustomers by city using pandas:")
    print(df["city"].value_counts())

    print("\nCustomers by email top-level domain using pandas:")
    print(df["email_domain"].value_counts())

    # Findings summary
    print("\n" + "=" * 45)
    print("PESA PULSE: CUSTOMER ANALYSIS SUMMARY")
    print("=" * 45)
    print(f"Total customers analysed: {len(df)}")
    print(f"Unique cities: {len(cities)}")
    print(f"Distinct email top-level domains: {len(domain_counts)}")

    top_domain, top_count = sorted(
        domain_counts.items(), key=lambda item: (-item[1], item[0])
    )[0]
    print(f"Most common email TLD: .{top_domain} ({top_count} customers)")

    print(
        "\nMarketing insight: Email TLD distribution is more informative "
        "for this sample because each city has only one customer, "
        "while some email TLDs occur more frequently."
    )

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export cleaned customer data
    df.to_csv(output_dir / "customers.csv", index=False)

    # Export city counts, sorted by count and then alphabetically
    sorted_city_counts = sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    )
    city_df = pd.DataFrame(
        sorted_city_counts,
        columns=["city", "customer_count"]
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    print("\nCSV files exported successfully!")
    print("Saved:", output_dir / "customers.csv")
    print("Saved:", output_dir / "city_counts.csv")

    # Save city distribution chart
    city_chart_path = output_dir / "city_distribution.png"
    plot_distribution(
        counts,
        city_chart_path,
        "Customer Distribution by City",
        "City"
    )
    print("Saved chart:", city_chart_path)

    # Save email TLD distribution chart
    domain_chart_path = output_dir / "customer_distribution.png"
    plot_distribution(
        domain_counts,
        domain_chart_path,
        "Customer Distribution by Email Top-Level Domain",
        "Email Top-Level Domain"
    )
    print("Saved chart:", domain_chart_path)
