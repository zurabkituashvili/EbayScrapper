import csv
import webbrowser


def open_links(filename):
    # Open the CSV file and read the links
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader: # if there is many rows in the csv file just iterate over few of them
            link = row[0]
            webbrowser.open_new_tab(link)



# Test the function with the example CSV file
open_links('C:\\Users\\Zura\\OneDrive\\Desktop\\personal python project\\EbayScraper\\ebay_results.csv')
