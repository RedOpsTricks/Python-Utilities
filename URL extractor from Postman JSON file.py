import json
import os

def extract_urls_from_postman_collection(item, domain_to_remove, urls):
    if 'request' in item:
        request = item['request']
        method = request.get('method')
        url = request.get('url', {}).get('raw', '')

        # Remove the specified domain from the URL
        if domain_to_remove in url:
            url = url.replace(domain_to_remove, '')

        urls.add(f"{method} {url}")  # Use a set to avoid duplicates

    # Check if the item is a folder and process its children
    if 'item' in item:  # Check for nested items (folders)
        for child_item in item['item']:
            extract_urls_from_postman_collection(child_item, domain_to_remove, urls)

def main():
    file_path = input("Please enter the file path: ")  # Replace with your file path
    domain_to_remove = input("Please enter the domain to remove: ")  # Replace with the domain you want to remove

    with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding
        collection = json.load(file)

    urls = set()  # Use a set to collect unique URLs
    for item in collection.get('item', []):
        extract_urls_from_postman_collection(item, domain_to_remove, urls)

    # Create the output file name by appending '_url' to the input file name
    base_name = os.path.splitext(file_path)[0]  # Get the file name without extension
    output_file_name = f"{base_name}_url.txt"  # Append '_url' and add .txt

    with open(output_file_name, 'w', encoding='utf-8') as output_file:  # Updated output file name
        for url in sorted(urls):  # Sort URLs before writing
            output_file.write(url + '\n')

if __name__ == "__main__":
    main()
