import json

import requests
from bs4 import BeautifulSoup
from urllib import parse

def crawl_yeogi(place_id):
    base_url = "https://www.yeogi.com/domestic-accommodations/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    search_url = f"{base_url}{place_id}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = [
          json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")
        ][0]
        # 숙소 이름
        hotel_name = data['mainEntity']['name']

        # 숙소 주소
        hotel_address = {'detail': data['mainEntity']['address']['streetAddress']}
        url = parse.urlparse('https://brownbears.tistory.com?name=불곰&params=123')

        query = parse.parse_qs(url.query)
        result = parse.urlencode(query, doseq=True)

        # 메인 사진
        main_photo = data['mainEntity']['image'][0]

        # 해당 페이지 URL
        hotel_url = search_url
        hotel = {'name': hotel_name, 'address': hotel_address, 'thumbnail': main_photo, 'url': hotel_url}

        # 결과 출력
        print("여기어때 예시:" + hotel.__str__())
        print("------------------------")

    else:
        print(f"페이지를 가져오지 못했습니다. 상태 코드: {response.status_code}")