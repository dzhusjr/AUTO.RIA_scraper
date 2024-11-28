import requests
from bs4 import BeautifulSoup

def extract_photos(images):
    count = 0
    result = []
    for i in range(10): # only get first 10
        try:
            image_link = images[i]["src"]
            if "auto/photo" in image_link:
                result.append(image_link)
            count += 1
        except:
            pass
    return result

def fetch_cars(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    cars = []
    for item in soup.select(".ticket-item"):
        title = item.select_one(".ticket-title").text.strip()
        price = item.select_one(".price-ticket").text.strip().split("•")[0].replace("  ", "").strip()
        link = item.select_one("a.address").get("href")
        mileage = item.select_one(".item-char.js-race").text
        location = item.select_one(".item-char.view-location.js-location").text.strip().split(" ")[0].strip()
        photos = extract_photos(BeautifulSoup(requests.get(link, headers=headers).text, "html.parser").findAll('img'))

        cars.append({
            "title": title,
            "price": price,
            "mileage": mileage,
            "location": location,
            "link": link,
            "photos": photos,
        })

    return cars
