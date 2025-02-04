import requests
import argparse
from bs4 import BeautifulSoup
import sys

# The phrase to check
error_phrase = "It seems that this page does not exist"

# Function to check the page content
def check_page(url):
    try:
        # Send a GET request to the page
        response = requests.get(url)
        
        # If the response status is not 200 (OK), skip the URL
        if response.status_code != 200:
            return False
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if the error phrase is in the content
        if error_phrase in soup.get_text():
            return False
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error with URL {url}: {e}")
        return False

def main(input_file, output_file):
    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = file.readlines()
    
    # Remove any leading/trailing whitespace characters
    urls = [url.strip() for url in urls]
    
    # List to store valid URLs
    valid_urls = []
    
    total_urls = len(urls)
    processed_urls = 0

    # Check each URL and add valid ones to the list
    for url in urls:
        if check_page(url):
            valid_urls.append(url)
        
        # Update processed URLs and calculate percentage
        processed_urls += 1
        percentage = (processed_urls / total_urls) * 100
        
        # Print the progress (flush to overwrite the previous line)
        sys.stdout.write(f"\rProcessing: {processed_urls}/{total_urls} URLs - {percentage:.2f}%")
        sys.stdout.flush()
    
    # Save the valid URLs to the output file
    with open(output_file, 'w') as file:
        for valid_url in valid_urls:
            file.write(valid_url + '\n')

    print(f"\nValid URLs have been saved to {output_file}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Check URLs for error page content")
    parser.add_argument('-i', '--input', required=True, help="Input file containing URLs")
    parser.add_argument('-o', '--output', required=True, help="Output file to save valid URLs")
    
    args = parser.parse_args()
    
    # Call the main function with the input and output file arguments
    main(args.input, args.output)
