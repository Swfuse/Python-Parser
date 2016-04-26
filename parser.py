# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import csv
"""Программа-парсер, которая берет данные с сайта и записывает их в таблицу формата CSV """
BASE_URL = 'https://www.weblancer.net/jobs/'

def get_html(url):
    """Данный метод берет запрос на страницу и читает данные"""
    response = request.urlopen(url)
    return response.read()

def get_page_count(html):
    """В этом методе берем все номера страниц"""
    soup = BeautifulSoup(html, 'lxml')
    pagination =  soup.find('ul', class_= 'pagination')


    number = pagination.find_all('a')[-1]
    return int(((number.get('href'))[12:]))



def parse(html):
    """Здесь, собственно, парсим каждую страницу отдельно,
       заносим информацию в словарь"""
    soup = BeautifulSoup(html, 'lxml')
    table =  soup.find('div', class_= 'container-fluid cols_table show_visited')

    projects = []

    for row in table.find_all('div', class_='row'):
        cols = row.find_all('div', class_='col-sm-7')
        projects.append({
                'title': cols[0].a.text,
                'categories': [category.text for category in cols[0].div.find_all('a',class_='text-muted')],
                'price': [price.text.strip() for price in row.find_all('div',class_='col-sm-2 amount title')][0],
                'application': [app.text.strip() for app in row.find_all('div',class_='col-sm-3 text-right text-nowrap hidden-xs')][0]
            })

    return projects

def save(projects, path):
    """В этом методе записываем по категориям все данные,
       в таком порядке, как они были записаны раннее"""
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))

        writer.writerows(
            (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
        )



def main():
    page_count = get_page_count(get_html(BASE_URL))

    print('Всего найдено страниц %d ' % page_count)

    projects = []

    for page in range(1, 5):
        print('Парсинг %d%%' % ( page / page_count * 100))
        projects.extend(parse(get_html(BASE_URL + '?page=%d' % page)))

    save(projects, 'projects.csv')

if __name__ == '__main__':
    main()
