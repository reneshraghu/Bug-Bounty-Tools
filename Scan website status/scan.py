import requests
import argparse
import os

# Function to check the status code of a website
def check_status_code(url, output_file):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        
        # Write the result to the output file
        with open(output_file, 'a') as file:
            file.write(f"Status Code for {url}: {response.status_code}\n")
            if response.status_code == 200:
                file.write(f"The website is accessible (200 OK).\n")
            elif response.status_code == 301:
                file.write(f"The website has been permanently moved (301 Moved Permanently).\n")
            elif response.status_code == 302:
                file.write(f"The website has been temporarily moved (302 Found).\n")
            elif response.status_code == 403:
                file.write(f"Access forbidden (403 Forbidden).\n")
            elif response.status_code == 404:
                file.write(f"Page not found (404 Not Found).\n")
            elif response.status_code == 500:
                file.write(f"Internal server error (500 Internal Server Error).\n")
            elif response.status_code == 502:
                file.write(f"Bad Gateway (502 Bad Gateway).\n")
            elif response.status_code == 503:
                file.write(f"Service unavailable (503 Service Unavailable).\n")
            elif response.status_code == 504:
                file.write(f"Gateway Timeout (504 Gateway Timeout).\n")
            else:
                file.write(f"Other status code: {response.status_code}\n")
        
        print(f"Status Code for {url}: {response.status_code}")
        print(f"Result saved to {output_file}")

    except requests.exceptions.RequestException as e:
        with open(output_file, 'a') as file:
            file.write(f"Error accessing {url}: {e}\n")
        print(f"Error accessing {url}: {e}")

# Function to process the input file containing the URLs
def process_input_file(input_file, output_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    total_urls = len(urls)
    
    # Check status code for each URL
    for idx, url in enumerate(urls):
        url = url.strip()  # Remove any surrounding whitespace or newlines
        if url:  # Skip empty lines
            check_status_code(url, output_file)
        
        # Calculate and display the percentage completion
        percentage = (idx + 1) / total_urls * 100
        print(f"Processing: {idx + 1}/{total_urls} URLs. Completion: {percentage:.2f}%")

# Main function to parse command-line arguments
def main():
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Check status codes of websites from an input file and save the result.")
    parser.add_argument('-i', '--input', required=True, help="Input file containing the list of URLs to check")
    parser.add_argument('-o', '--output', required=True, help="Output file to save the status code results")
    
    # Parse the arguments
    args = parser.parse_args()

    # Ensure the output file is empty before starting
    if os.path.exists(args.output):
        os.remove(args.output)
    
    # Call the function to process the input file and check status codes
    process_input_file(args.input, args.output)

if __name__ == "__main__":
    main()
