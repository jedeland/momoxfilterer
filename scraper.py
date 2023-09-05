import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

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
    soup = BeautifulSoup(base_page.content, 'lxml')
    for values in soup.find_all('div', {'class': 'row new-detail-headline'}):
        height = values.find('td', {"id": "detail-value-Höhe"})
        width = values.find('td', {"id": "detail-value-Breite"})
        if int(height.text.strip().replace("cm", "")) >= min_h and int(height.text.strip().replace("cm", "")) <= max_h and int(width.text.strip().replace("cm", "")) >= min_b and int(height.text.strip().replace("cm", "")) <= max_b:
            price = soup.find('span', {'class': 'price'})
            brand = soup.find('a', {'class': 'brand-name'})
            # print('price is ', price)
            result_num = result_num + 1
            # print(f"Df: {df}\nConcat: {pd.concat([df, new_row], ignore_index=True)}",)

            new_row = pd.DataFrame({"name": [item_to_search.split("/p/")[-1]],
                                    "brand": [brand.text.strip()],
                                    "link": [item_to_search], 
                                    "height": [height.text.strip().replace("cm", "")],
                                    "width": [width.text.strip().replace("cm", "")],
                                    "price": [price.text.strip()]})
            print(f"""Item found: {item_to_search}
                  Brand: {brand.text.strip()}
                  Height: {height.text.strip()}
                  Width: {width.text.strip()}
                  Price: {price.text.strip()}""")
            return new_row
            # print(f"Df: {df}\nConcat: {pd.concat([df, new_row], ignore_index=True)}",)
            # df = pd.concat([df, new_row], ignore_index=True)
            # print(f"Df: {df}\nConcat: {pd.concat([df, new_row], ignore_index=True)}",)
            


if "__main__" == __name__:
    min_breite = 34
    max_breite = 41
    min_hohe = 22
    max_hohe = 26
    base_url_handbag = 'https://www.momoxfashion.com/de/damen/accessoires/handtaschen?farbe=bunt_gruen_rot_blau_beige_tuerkis_grau_orange_schwarz_braun_weiss&material=baumwolle_leder_kunstleder&zustand=Neuwertig_Sehr%20gut&von=6&bis=85'    
    print("Starting scraper!")
    num_pages = get_handbag_pages(base_url_handbag)
    list_of_links = []
    for i in range(1, num_pages):
        time.sleep(0.15)
        list_of_links.append(get_handbags(f"{base_url_handbag}&seite={i}"))
    g = 0
    results_counter = 0
    df = pd.DataFrame(data=None, columns=["name", "brand", "link", "height", "width", "price"])
    for items in list_of_links:
        # print(g + 1, items)
        for count, item in enumerate(items, start=1): 
            # print('Item is ' , item)
            if count % 25 == 0:
                print(f"Df: {df}")
            df = pd.concat([df, get_valid_items(min_breite, max_breite, min_hohe, max_hohe, item, results_counter
                                                )], ignore_index=True)
            # print(f"Concat: {df}")
    print("Number of results ", results_counter)
    print(df)
    df.to_excel("scraperoutput.xlsx", engine='xlsxwriter')