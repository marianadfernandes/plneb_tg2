import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse 
import json


header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        # "Referer": "https://www.example.com",
        # Add more headers if required
    }


def get_google_image(query):
    # Construct the Google Images search URL
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    # Send a GET request to Google Images
    response = requests.get(search_url)
    response.raise_for_status()

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first image result
    image_element = soup.find('img')

    # Extract the image URL
    image_url = image_element['src']

    # If the image URL is relative, construct the absolute URL
    parsed_url = urlparse(image_url)
    if not parsed_url.netloc:
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        image_url = base_url + image_url

    return image_url


file = open("./output/dic_mulher_final.json", encoding="utf-8")
db = json.load(file)
file.close()

images_urls = []

for key in db.keys():
    image_element = get_google_image(key)
    if image_element:
        images_urls.append(image_element)
    else:
        images_urls.append("None")
    print(image_element)


file = open("./output/img_urls.json","w", encoding="utf8")
json.dump(images_urls,file, ensure_ascii=False, indent = 4)
file.close()