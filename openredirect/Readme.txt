Open Redirect 
This Python script crawls a website, extracts links, and filters them based on specified status codes (e.g., 301, 302, 403). Results are saved to an output file.

Requirements
    Python 3.x
     Install dependencies: requests, beautifulsoup4

     pip install requests beautifulsoup4
Usage
    Run the script with the following command:

python redirect.py -u <URL> -s <status_codes> -o <output_file>
      -u <URL>: Website URL to crawl (e.g., https://example.com)
      -s <status_codes>: Comma-separated list of status codes to filter (e.g., 301,302,403)
       -o <output_file>: File to save the results (default: output.txt)
Example:

python redirect.py -u https://example.com -s 301,302,403 -o results.txt
Features
    Crawls website and extracts links.
    Filters links based on status codes (e.g., 301, 302).
    Supports concurrent link checking.
    Logs results with status codes and filtered links.
Output

Results are saved in the specified output file (output.txt by default) with the following format:

Found URL with keyword: https://example.com/redirect1
https://example.com/redirect1 (Status Code: 301)
Processed 100/200 links - 50% complete
License
© Renesh Raghu. All rights reserved.