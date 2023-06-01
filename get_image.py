import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json


def get_google_image(query):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        # "Referer": "https://www.example.com",
        # Add more headers if required
    }

    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    response = requests.get(search_url, headers = header)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first image result
    image_element = soup.find('img')
    print(image_element)


    # # Extract the image URL
    # image_url = image_element['src']

    # # If the image URL is relative, construct the absolute URL
    # parsed_url = urlparse(image_url)
    # if not parsed_url.netloc:
    #     base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    #     image_url = base_url + image_url

    # return image_url

    return image_element


file = open("./output/novo_dic.json", encoding="utf-8")
db = json.load(file)
file.close()

# images = []

# for key in db.keys():
#     image_element = get_google_image(key)
#     images.append(image_element)

# print(images)

get_google_image("cats")

file = open("./output/img_elements.txt","w", encoding="utf8")
file.write(images)
file.close()