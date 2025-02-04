# Crawler script created by Renesh Raghu
# Enhanced with threading and colorful terminal output
import requests
from bs4 import BeautifulSoup
import argparse
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def read_keywords(input_file):
    """Reads the list of keywords from a given input file."""
    keywords = []
    try:
        with open(input_file, 'r') as file:
            keywords = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"Error: File {input_file} not found.")
        exit(1)
    return keywords

def process_page(url, keywords, lock, executor, futures, visited):
    """Processes a single page, extracts links, appends a quote to URLs, and prints them."""
    try:
        response = requests.get(url)
        print(Fore.GREEN + f"URL: {url}, Status Code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Iterate through all the links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Check if the link contains any of the specified keywords
            if any(keyword in href for keyword in keywords):
                # Resolve relative URLs
                if href.startswith('/'):
                    href = urljoin(url, href)
                
                # Append a single quote at the end of the URL
                href_with_quote = href + "'"
                
                # Print the modified URL
                print(Fore.CYAN + f"Modified URL: {href_with_quote}")

                # Add to visited URLs for threading
                if href not in visited:
                    visited.add(href)
                    # Add to the thread pool to process the next page
                    futures.append(executor.submit(process_page, href, keywords, lock, executor, futures, visited))

    except requests.RequestException as e:
        print(Fore.YELLOW + f"Warning: Error retrieving {url}: {e}")

def crawl(url, keywords, num_threads=10):
    """Starts the crawling process using threading."""
    visited = set([url])  # Keep track of visited URLs
    lock = threading.Lock()  # To synchronize file writing
    futures = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures.append(executor.submit(process_page, url, keywords, lock, executor, futures, visited))

        # Wait for all threads to complete
        for future in as_completed(futures):
            pass  # Thread completion is handled by process_page

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument('-u', '--url', type=str, required=True, help="URL to start crawling from")
    parser.add_argument('-k', '--keywords_file', type=str, required=True, help="Input file containing URL keywords")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads to use (default 10)")

    # Parse the arguments
    args = parser.parse_args()

    # Read the keywords from the input file
    keywords = read_keywords(args.keywords_file)

    # Start the crawling process with threading
    print(Fore.CYAN + f"Crawling {args.url} using {args.threads} threads...")

    # Start crawling with the specified number of threads
    crawl(args.url, keywords, num_threads=args.threads)

    print(Fore.CYAN + f"Finished crawling.")

if __name__ == "__main__":
    main()