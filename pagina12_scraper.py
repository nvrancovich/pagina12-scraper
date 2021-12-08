import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_links(link):
    pagina = requests.get(link)
    s_link = BeautifulSoup(pagina.text, 'lxml')
    s_noticiash2 = s_link.find_all('h2', attrs = {'class':'title-list'})
    s_noticiash3 = s_link.find_all('h3', attrs = {'class':'title-list'})
    s_noticiash4 = s_link.find_all('h4', attrs = {'class':'is-display-inline title-list'})
    s_noticias = s_noticiash2 + s_noticiash3 + s_noticiash4
    links_noticias = ['https://www.pagina12.com.ar' + seccion.find('a').get('href') for seccion in s_noticias]
    return links_noticias

def extract_elements(link):
    new = requests.get(link)
    new_s = BeautifulSoup(new.text, 'lxml')
    new_elements = {}
    new_elements['url'] = link
    date = new_s.find('time')
    if date:
        new_elements['date'] = date.get('datetime')
    else:
        new_elements['date'] = None
    new_elements['title'] = new_s.find('h1').text
    subtitle = new_s.find('h3')
    if subtitle:
        new_elements['subtitle'] = subtitle.text
    else:
        new_elements['subtitle'] = None
    body = new_s.find('div', attrs = {'class':'article-main-content article-text'})
    if body:
        new_elements['body'] = body.text
    else:
        body = new_s.find('div', attrs = {'class':'article-main-content article-text no-main-image'})
        if body:
            new_elements['body'] = body.text
        else:
            new_elements['body'] = None
    return new_elements

def run(url):
    p12 = requests.get(url)
    s = BeautifulSoup(p12.text, 'lxml')
    sections = s.find('div', attrs = {'class':'p12-dropdown-column'}).find_all('a')
    links_sections = [section.get('href') for section in sections]
    links_news = []
    for link in links_sections:
        links_news = links_news + extract_links(link)
    print(len(links_news))
    news_elements = []
    for link in links_news:
        print(links_news.index(link) + 1,'/', len(links_news))
        news_elements.append(extract_elements(link))
    return news_elements
    
data = run('https://www.pagina12.com.ar/')
df = pd.DataFrame(data)
df.to_excel('Notas Página 12.xlsx')

