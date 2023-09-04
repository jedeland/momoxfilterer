import time
import requests
from bs4 import BeautifulSoup

# def target_momox(argument_type):
#     print("Targeting number ", argument_type)
def get_handbag_pages(base_url):
    headers = { 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    page_urls = []
    req = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    for pages in soup.find_all('nav', {'aria-label':'Page navigation'}):
        for link in pages.find_all('a', href=True):
            page_urls.append(link['href'])
    max_num = 1
    for url in page_urls:
        if url != page_urls[0]:
            print(url.rsplit('=', -1)[-1])
            num_val = url.rsplit('=', -1)[-1]
            if int(num_val) >= int(max_num):
                max_num = num_val

    print('Max num is ', max_num)
    return int(max_num)


def get_handbags(base_url_handbag):
    list_of_items = []
    headers = { 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    base_page = requests.get(base_url_handbag, headers=headers)
    soup = BeautifulSoup(base_page.content, 'html.parser')
    # print(soup.find_all('img'))
    for item in soup.find_all('div', {'class': 'col-lg-4 col-md-4 col-sm-4 col-xs-6 catalog-item'}):
        for link in item.find_all('a', href=True):
            # print(f"Follow up link is https://www.momoxfashion.com{link['href']}")
            list_of_items.append(f"https://www.momoxfashion.com{link['href']}")
    # print(list_of_items)
    return list_of_items


def get_valid_items(min_b, max_b, min_h, max_h, item_to_search, result_num):
    # print()
    headers = { 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    base_page = requests.get(item_to_search, headers=headers)
    soup = BeautifulSoup(base_page.content, 'html.parser')
    for values in soup.find_all('div', {'class': 'row new-detail-headline'}):
        height = values.find('td', {"id": "detail-value-Höhe"})
        width = values.find('td', {"id": "detail-value-Breite"})
        if int(height.text.strip().replace("cm", "")) >= min_h and int(height.text.strip().replace("cm", "")) <= max_h and int(width.text.strip().replace("cm", "")) >= min_b and int(height.text.strip().replace("cm", "")) <= max_b:
            print(f"Item found: {item_to_search}\nHeight: {height.text.strip()}\nWidth: {width.text.strip()}")
            result_num = result_num + 1


if "__main__" == __name__:
    min_breite = 34
    max_breite = 41
    min_hohe = 22
    max_hohe = 26
    base_url_handbag = 'https://www.momoxfashion.com/de/damen/accessoires/handtaschen?zustand=Neuwertig_Sehr%20gut'    
    print("Starting scraper!")
    num_pages = get_handbag_pages(base_url_handbag)
    list_of_links = []
    for i in range(1, num_pages):
        time.sleep(0.15)
        list_of_links.append(get_handbags(f"{base_url_handbag}&seite={i}"))
    g = 0
    results_counter = 0
    for items in list_of_links:
        # print(g + 1, items)
        for item in items: 
            # print('Item is ' , item)
            get_valid_items(min_breite, max_breite, min_hohe, max_hohe, item, results_counter)
    print("Number of results ", results_counter)