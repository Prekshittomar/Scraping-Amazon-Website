import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def get_title(soup):
    title = soup.find("span", attrs={'id' : "productTitle"}).text.strip()
    return title

def get_price(soup):
    price_element = soup.find("span", attrs={'class' : "a-price-whole"})
    if price_element:
        price = price_element.text
    else:
        price = "Price not available"
    return price

def get_rating(soup):
    rating = soup.find("span", attrs={'class' : "a-icon-alt"}).text.strip()
    return rating

def scrape_page(url):
    HEADERS = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0','Accept-Language':'en-US, en;q=0.5'})
    URL=url
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content,'html.parser')
    links = soup.find_all("a",attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list=[]
    for link in links:
        links_list.append(link.get('href'))
    
    title=[]
    price=[]
    rating=[]
    
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content,'html.parser')
        
        title.append(get_title(new_soup))
        price.append(get_price(new_soup))
        rating.append(get_rating(new_soup))
        
    return title,price,rating

base_url = 'https://www.amazon.in/s?i=electronics&rh=n%3A4363159031&fs=true&page={}&qid=1712326227&ref=sr_pg_{}'

title_all=[]
price_all = []
rating_all = []

p1,p2 = 1,1

while True:
    url=base_url.format(p1,p2)
    title,price,rating=scrape_page(url)
    if not title:
        break
    title_all.extend(title)
    price_all.extend(price)
    rating_all.extend(rating)
    p1=p1+1
    p2=p2+1
    
data = {'Title':title_all,
        'Prices':price_all,
        'Ratings':rating_all
        }

amazon_df=pd.DataFrame(data)
amazon_df.to_csv('Amazon Samsung data.csv',index=False)
