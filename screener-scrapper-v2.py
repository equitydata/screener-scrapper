import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_screener_data(screener_url):
    # Send an HTTP request to the URL
    print("screener_url::", screener_url)
    response = requests.get(screener_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the stock data
        table = soup.find("table", class_="data-table")

        if table:
            # Extract table headers and ensure they are unique
            headers = []
            for header in table.find_all('th'):
                header_text = header.text.strip()
                if header_text not in headers:
                    headers.append(header_text)

            # Extract table rows
            rows = []
            for row in table.find_all('tr')[1:]:  # Skip the header row
                cols = [col.text.strip() for col in row.find_all('td')]
                if len(cols) == len(headers):  # Ensure the row has the same number of columns as the headers
                    rows.append(cols)
                else:
                    print(f"Row with mismatched columns skipped: {cols}")

            # Print headers and a few rows for debugging
            print("Headers:", headers)
            print("First row:", rows[0] if rows else "No rows found")
            print("Number of columns in headers:", len(headers))
            print("Number of columns in first row:", len(rows[0]) if rows else "No rows found")

            # Create a DataFrame from the extracted data
            df = pd.DataFrame(rows, columns=headers)

            # Get the current date
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Create the file path with the current date
            file_path = f"/Users/sdash/Downloads/equitydata-screener/{screener_url.split('/')[-2]}-{current_date}.csv"
            
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False)

            print(f"Table data saved to {file_path}")
        else:
            print("Table not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# List of Screener URLs
screener_urls = [
    "https://www.screener.in/screens/1800664/equitydata-largecap/",
    "https://www.screener.in/screens/850075/equitydata-microcap/",
    "https://www.screener.in/screens/1798567/equitydata-smallcap/",
    "https://www.screener.in/screens/850075/equitydata-microcap/",
    "https://www.screener.in/screens/1794662/equitydata-nanocap/",
    "https://www.screener.in/screens/1800654/equitydata-zerocap/",
    "https://www.screener.in/screens/1645194/equitydata-filtercoffee/",
    "https://www.screener.in/screens/1645174/equitydata-pe-magic/"
    # Add more URLs as needed
]

# Iterate over each URL and scrape data
for url in screener_urls:
    scrape_screener_data(url)
