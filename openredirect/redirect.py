import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
from threading import Lock  # Import Lock from threading

# List of keywords to look for in the URL
keywords = [
    "go", "return", "r_url", "returnUrl", "returnUri", "locationUrl", 
    "goTo", "return_url", "return_uri", "ref=", "referrer=", 
    "backUrl", "returnTo", "successUrl", "red=", "link=", "ret=", "page=", 
    "r2=", "q=", "img=", "url=", "u=", "redirect=", "return=", "end_display=", 
    "r=", "url=", "URL=", "location=", "Next=", "toredirect=", "ReturnUrl=", 
    "redirectBack=", "page=", "AuthState=", "uri=", "Referer=", "path=", 
    "redir=", "referrer=", "returnUrl=", "image_path=", "redirect_url=", "ActionCodeURL=", 
    "forward=", "return url=", "open=", "newurl=", "file=", "From=", "lang", "To=", 
    "rb=", "|=", "Goto=", "file=", "old=", "aspxerrorpath=", "back="
]

# Function to handle fetching the status code of each link
def check_link_status(full_url, status_code_filters, output_file, progress_lock, total_links, processed_links):
    try:
        # Send a GET request for the full URL with allow_redirects=False to capture status codes like 301, 302, 403
        link_response = requests.get(full_url, allow_redirects=False)  # Prevent auto-following redirects
        if link_response.status_code in status_code_filters:
            output_file.write(f"{full_url} (Status Code: {link_response.status_code})\n")
    except requests.RequestException as e:
        output_file.write(f"Failed to fetch: {full_url}, Error: {e}\n")
    
    # Update progress
    with progress_lock:
        processed_links[0] += 1
        percentage = (processed_links[0] / total_links) * 100
        print(f"\rProcessed {processed_links[0]}/{total_links} links - {percentage:.2f}% complete", end="")

# Function to crawl a website and extract all links
def crawl_website(url, status_code_filters, output_file):
    try:
        response = requests.get(url, allow_redirects=False)  # Prevent auto-following redirects
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        output_file.write(f"Failed to fetch: {url}, Error: {e}\n")
        return
    
    # If the request was successful (status code 200)
    if response.status_code == 200:
        output_file.write(f"Successfully fetched: {url} (Status Code: {response.status_code})\n")
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags (which define hyperlinks)
        links = soup.find_all('a')

        # Total number of links to process
        total_links = len(links)

        # Use a ThreadPoolExecutor to make requests for links concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of full URLs
            full_urls = []
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)

                    # Skip non-HTTP URLs like mailto:, javascript:, etc.
                    if full_url.startswith(('mailto:', 'javascript:')):
                        continue  # Skip mailto: and javascript: links

                    # Check if the URL contains any of the specified keywords
                    if any(keyword in full_url for keyword in keywords):
                        output_file.write(f"Found URL with keyword: {full_url}\n")

                    full_urls.append(full_url)

            # Progress tracking variables
            processed_links = [0]
            progress_lock = Lock()  # Used to synchronize the update of processed links

            # Submit the requests to the executor to be processed concurrently
            futures = [executor.submit(check_link_status, full_url, status_code_filters, output_file, progress_lock, total_links, processed_links) for full_url in full_urls]

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

            # Print final completion message
            print(f"\nFinished processing {total_links} links.")

    else:
        output_file.write(f"Failed to fetch: {url}, Status Code: {response.status_code}\n")

# Main function to parse arguments and start crawling
def main():
    parser = argparse.ArgumentParser(description="Crawl a website and check URLs.")
    parser.add_argument('-u', '--url', required=True, help="URL of the website to crawl")
    parser.add_argument('-s', '--status', required=True, help="Comma-separated list of status codes to filter by (e.g., 301, 302, 403)")
    parser.add_argument('-o', '--output', default='output.txt', help="Output file to save results (default: output.txt)")

    args = parser.parse_args()

    # Convert the comma-separated status codes string to a list of integers
    status_code_filters = [int(code.strip()) for code in args.status.split(',')]

    # Open a file in write mode to save the output
    with open(args.output, 'w') as output_file:
        crawl_website(args.url, status_code_filters, output_file)
    
    print(f"Output saved to '{args.output}'")

if __name__ == "__main__":
    main()
