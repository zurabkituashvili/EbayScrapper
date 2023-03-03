import os
import requests
from bs4 import BeautifulSoup
import csv
import sys

# Function to scrape eBay search results
def scrape_ebay(keywords, min_price, max_price):
    # Create the URL to search on eBay
    keywords_str = '+'.join(keywords)
    url = "https://www.ebay.com/sch/i.html?_nkw={}&_ipg=200&_sop=12&_udlo={}&_udhi={}".format(keywords_str, min_price, max_price)
    
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the search result items
    items = soup.find_all('div', {'class': 's-item__wrapper'})
    
    # Loop through each item and extract the relevant data
    results = []
    for item in items:
        link = item.find('a', {'class': 's-item__link'})
        if link:
            link = link['href']
        else:
            continue
        
        title = item.find('h3', {'class': 's-item__title'})
        if title:
            title = title.text.strip()
        else:
            title = ''
        
        price = item.find('span', {'class': 's-item__price'})
        if price:
            price = price.text.strip()
            # Remove any non-numeric characters from price
            price = ''.join(c for c in price if c.isdigit() or c == '.')
            try:
                # Try to convert price to a float
                price = float(price)
            except ValueError:
                # If price cannot be converted to a float, set it to 0.0
                price = 0.0
        else:
            price = 0.0
        
        # Append the data to the results list
        results.append([link, title, price])
    
    # Sort the results by price in ascending order
    results.sort(key=lambda x: x[2])
    
    return results


if __name__ == '__main__':
    # Get the keywords and price range from command line arguments
    keywords = sys.argv[1].split(',')
    min_price = sys.argv[2]
    max_price = sys.argv[3]
    
    # Scrape eBay search results
    results = scrape_ebay(keywords, min_price, max_price)
    
    # Get the path to the directory where the Python file is located
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # Write the results to a CSV file
    with open(os.path.join(dir_path, 'ebay_results.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link', 'Keyword', 'Price'])
        
        for result in results:
            # Get the keywords as a comma-separated string
            keywords_str = ', '.join(keywords)
            writer.writerow([result[0], keywords_str, result[2]])
    
    print('Done!')
