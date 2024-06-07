import requests
import subprocess
import re

def download_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_list(raw_list):
    lines = raw_list.splitlines()
    filtered_lines = set()

    # Filter out comments and empty lines
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith(('#', '!', '[', ']', '/*', '*', '*/')):
            filtered_lines.add(stripped_line)
    
    return filtered_lines

def save_list(list_set, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in sorted(list_set):
            f.write(item + '\n')

def run_fanboy_sorter(perl_script, input_file):
    command = ['perl', perl_script, input_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running sorter: {result.stderr}")
    else:
        print(f"Sorter output: {result.stdout}")

# URLs to download blocklists and whitelists
blocklist_urls = [
    ('https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn_ublock.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/filters.min.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/badware.min.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/privacy.min.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/quick-fixes.min.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/unbreak.min.txt'),
    ('https://raw.githubusercontent.com/uBlockOrigin/uAssets/gh-pages/filters/annoyances-cookies.txt'),
    ('https://easylist.to/easylist/easylist.txt'),
    ('https://easylist.to/easylist/easyprivacy.txt'),
    ('https://secure.fanboy.co.nz/fanboy-cookiemonster.txt'),
    ('https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/platforms/extension/ublock/filters/2_without_easylist.txt'),
    ('https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/platforms/extension/ublock/filters/3_optimized.txt'),
    ('https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/platforms/extension/ublock/filters/17_optimized.txt'),
    ('https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/platforms/extension/ublock/filters/18_optimized.txt')
]

whitelist_urls = [
    ('https://raw.githubusercontent.com/AdguardTeam/HttpsExclusions/master/exclusions/banks.txt'),
    ('https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/allowlist.txt'),
    ('https://raw.githubusercontent.com/leminhhieuctvn/hosts/master/whitelist_custom')
]

# Download blocklists
blocklists = [download_list(url) for url in blocklist_urls]
blocklist_set = set()
for blocklist in blocklists:
    blocklist_set.update(parse_list(blocklist))

# Download whitelists
whitelists = [download_list(url) for url in whitelist_urls]
whitelist_set = set()
for whitelist in whitelists:
    whitelist_set.update(parse_list(whitelist))

# Remove whitelisted items from blocklist
filtered_blocklist_set = blocklist_set - whitelist_set

# Save filtered blocklist to a single file
filtered_combined_filename = 'filtered_combined_blocklist.txt'
save_list(filtered_blocklist_set, filtered_combined_filename)

perl_script = 'sorter.pl'
run_fanboy_sorter(perl_script, filtered_combined_filename)