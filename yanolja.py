import json

import requests
from bs4 import BeautifulSoup


def crawl_yanolja(place_id):
  base_url = "https://place-site.yanolja.com/places/"
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
    hotel_name = data['name']

    # 숙소 주소
    hotel_address = {'detail': data['address']['addressLocality'], 'lat': data['geo']['latitude'],
                     'lng': data['geo']['longitude']}
    # 메인 사진
    main_photo = soup.select_one('img.css-sr2c7j')['src']

    # 해당 페이지 URL
    hotel_url = search_url
    hotel = {'name': hotel_name, 'address': hotel_address, 'thumbnail': main_photo, 'url': hotel_url}
    # 결과 출력
    print("야놀자 예시:"+ hotel.__str__())
    print("------------------------")


  else:
    print(f"페이지를 가져오지 못했습니다. 상태 코드: {response.status_code}")
