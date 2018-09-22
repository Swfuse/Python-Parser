# 1 Parse one process
# 2 Time tracker
# 3 Multiprocessing Pool
# 4 Time tracker
# 5 Export in csv

import requests

from bs4 import BeautifulSoup

import csv

from datetime import datetime

from multiprocessing import Pool


def get_html(url):
    r = requests.get(url) #respone object
    return r.text         #return html


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    
    links = []

    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        name = soup.find('h1', class_='details-panel-item--name').text.strip() # strip delete symbols

    except:
        name = ''

    try:
        price = soup.find('span', class_='details-panel-item--price__value').text.strip()

    except:
        price = ''
    
    data = {'name': name,
            'price': price}

    return data

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['name'],
                          data['price']) )

        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)



def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links( get_html(url) )

#    for index, url in enumerate(all_links):
#        html = get_html(url)
#        data = get_page_data(html)
#        write_csv(data)
#        print(index)

    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()

    print(str(end - start))


if __name__=='__main__':
    main()