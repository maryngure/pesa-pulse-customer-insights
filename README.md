# Pesa Pulse — API Data Analysis Using Python Structures

## Project Overview

Pesa Pulse retrieves customer data from a REST API and analyses it using Python data structures and pandas. The project demonstrates API requests, nested JSON exploration, data extraction, counting, tabular analysis, CSV exports, and data visualization.

## Tools and Libraries

- Python
- Requests — retrieving data from the API
- pandas — data manipulation and analysis
- Matplotlib — data visualization

## Data Source

The project uses the JSONPlaceholder Users API:

https://jsonplaceholder.typicode.com/users

The API returns customer-like sample records containing personal contact details, addresses, geographical coordinates, and company information.

## Approach

1. Retrieved records from the API using the Requests library, with a timeout and HTTP error handling.
2. Explored nested JSON records and printed field names and their Python data types.
3. Extracted the required attributes into flat dictionaries, including email domains and numerical latitude and longitude values.
4. Used Python sets to identify unique cities and dictionaries to count customers by city and email top-level domain.
5. Converted the cleaned records into a pandas DataFrame and verified the results using `value_counts()`.
6. Exported the cleaned records and city counts to CSV files.
7. Generated a bar chart showing the distribution of customers by email top-level domain.

Nested fields include address.city, address.zipcode, address.geo.lat, address.geo.lng, and company.name. The deepest field path is address.geo.lat or address.geo.lng, each nested two levels below the top-level customer record.

## Key Findings

- The API returned 10 customer records representing 10 unique cities. Each city appeared once in this sample.
- The `.biz` email top-level domain was the most common, appearing in 3 of the 10 records (30%).
- There were 8 distinct email top-level domains across the 10 records.

Chart comparison: The email top-level domain chart is more informative for this sample because the 10 customers represent 10 different cities, resulting in identical city counts. Email-TLD counts show variation, with .biz appearing three times. These findings describe the sample data only and should not be treated as evidence of broader customer or market behaviour.

## Output Files

- `output/customers.csv` — cleaned customer records with 12 attributes.
- `output/city_counts.csv` — customer counts for each city.
- `output/customer_distribution.png` — bar chart of customer counts by email top-level domain.
- `output/city_distribution.png` - bar chart of customer distribution by city.

## How to Run

1. Install Python.
2. Clone or download this repository.
3. Create and activate a virtual environment.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the analysis:

   ```bash
   python analysis.py
   ```

The script retrieves the latest available records from the API and regenerates the output files.

## Assumptions and Limitations

- The API provides sample customer data for demonstration purposes; the records should not be treated as verified real-world customer information.
- Each API record is treated as one customer.
- The email top-level domain is extracted from the text following the final period in the email address.
- City counts and email-domain counts describe only the records returned by the API at the time of execution.
- Successful generation of the outputs depends on API availability and an internet connection.