import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL of the Screener.in page
screener_url = "https://www.screener.in/screens/1645194/equitydata-filtercofee/"

# Send an HTTP request to the URL
response = requests.get(screener_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table containing the stock data
    table = soup.find("table", class_="data-table")

    if table:
        # Extract table headers
        headers = [header.text for header in table.find_all('th')]

        # Extract table rows
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cols = [col.text for col in row.find_all('td')]
            rows.append(cols)

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(rows, columns=headers)

        # Save the DataFrame to a CSV file
        df.to_csv("/tmp/equitydata-filter-cofee.csv", index=False)

        print("Table data saved to /tmp/equitydata-filter-cofee.csv ")
    else:
        print("Table not found.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

