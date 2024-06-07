import requests
import subprocess
from datetime import datetime

def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def merge_blocklists(urls, output_file):
    with open(output_file, 'w') as outfile:
        # Add the header lines
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        header_lines = [
            "[Adblock Plus 2.0]",
            "! Title: leminhhieuctvn combined list",
            f"! Last modified: {current_time} UTC",
            "! Expires: 4 hours (update frequency)",
            "!"
        ]
        for line in header_lines:
            outfile.write(line + '\n')
        
        # Download and append content from each URL
        for url in urls:
            content = download_file(url)
            if content:
                outfile.write(content + '\n')

def run_fanboy_sorter(perl_script, input_file):
    command = ['perl', perl_script, input_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running sorter: {result.stderr}")
    else:
        print(f"Sorter output: {result.stdout}")

# URLs to download blocklists
blocklist_urls = [
    'https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn_ublock.txt',
    'https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/filters/filters.min.txt',
    'https://ublockorigin.github.io/uAssetsCDN/filters/badware.min.txt',
    'https://ublockorigin.github.io/uAssetsCDN/filters/privacy.min.txt',
    'https://cdn.jsdelivr.net/gh/uBlockOrigin/uAssetsCDN@main/filters/quick-fixes.min.txt',
    'https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/filters/unbreak.min.txt',
    'https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties/easylist.txt',
    'https://filters.adtidy.org/extension/ublock/filters/2_without_easylist.txt',
    'https://cdn.statically.io/gh/uBlockOrigin/uAssetsCDN/main/thirdparties/easyprivacy.txt'
]

filtered_combined_filename = 'filtered_combined_blocklist.txt'
merge_blocklists(blocklist_urls, filtered_combined_filename)

perl_script = 'sorter.pl'
run_fanboy_sorter(perl_script, filtered_combined_filename)