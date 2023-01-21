from django.shortcuts import render
from django.http import JsonResponse
import requests
import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import baza_ogloszen
from django.utils import timezone
import datetime

def PageUpdateUrl(request):
    dict={'mój_klucz':'działą_Jason'}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pass
    return JsonResponse({'dict': dict})


def get_url():
    url3='https://ereceptura2.herokuapp.com/'


    url = 'https://www.otodom.pl/pl/wyszukiwanie/sprzedaz/mieszkanie/mazowieckie/legionowski/legionowo/legionowo?distanceRadius=0&page=1&limit=36&market=ALL&priceMax=350000&by=PRICE&direction=ASC&viewType=listing'
    url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/legionowo?distanceRadius=0&page=1&limit=36&market=ALL&locations=%5Bcities_6-724%5D&priceMax=350000&by=DEFAULT&direction=DESC&viewType=listing'
    #url='https://pl.wikipedia.org/wiki/Hey'
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    url_content=session.get(url).text#content
    return url_content


# def home(request):
#     content=get_url()
#     cls = "css-1rhznz4 es62z2j11"
#     soup = BeautifulSoup(content, 'html5lib')#.encode("utf-8")
#     #estates=soup.find('li', attrs={'class' : "css-p74l73 es62z2j19"}).text
#     #estates=soup.find_all('h3', attrs={'class' : cls})
#     estates = soup.find_all(lambda tag: tag.name == 'h4')
#     #estates = soup.find_all( 'body.div[1].div[2].main.div.div[2].div[1].div[2].div[1].div.ul.li[1].a.article.div[1].h3')
#     #from urllib.parse import unquote
#     print('estates',len(estates))
#     sys.stdout.flush()
#     ret=[]
#     for i in estates:
#         ret.append(i.text)
#         #print(soup.body.div[1].div[2].main.div.div[2].div[1].div[2].div[1].div.ul.li[1].a.article.div[1].h3.text)
#         #print('content',i.text.encode('1252', 'ignore').decode('1252'))
#         sys.stdout.flush()
#     return render(request,'home.html',{'ret':soup})

driver = webdriver.Chrome()
def loadDriver(url):
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    itemTargetCount = 100
    items=50
    while itemTargetCount>items:
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        time.sleep(1)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver

def home(request):
    urls = ['https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/legionowo?distanceRadius=0&page=1&limit=36&market=ALL&locations=%5Bcities_6-724%5D&priceMax=350000&by=DEFAULT&direction=DESC&viewType=listing',
            'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/pruszkow?distanceRadius=0&page=1&limit=72&market=ALL&locations=%5Bcities_6-840%5D&priceMax=350000&by=PRICE&direction=ASC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&searchingCriteria=legionowo',]
    ogl = []
    def oto_dom_scraper(url):
        if url[:21]=='https://www.otodom.pl':
            driver = loadDriver(url)
            ###################################################
            last_height = driver.execute_script("return document.body.scrollHeight")
            itemTargetCount = 100

            while itemTargetCount > 10:
                driver.execute_script("window.scroll(0, document.body.scrollHeight);")
                time.sleep(1)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            ##########################################################
            ogloszenia = driver.find_elements(By.XPATH, '//ul')

            lista_ogl = []
            for i in ogloszenia:
                lista_ogl += i.find_elements(By.XPATH, './li[@data-cy="listing-item"]')
            count=0
            ogl.append(str(len(lista_ogl)))
            for i in lista_ogl:
                count+=1
                ogl.append(str(count))
                try:
                    tytul = i.find_element(By.XPATH, "./a/article/div")
                    ogl.append(tytul.text)
                except:
                    tytul = 'nie podano'
                    ogl.append(tytul)
                try:
                    url_link = i.find_element(By.XPATH, "./a")
                    # print('url_link', url_link.get_attribute('href').encode("utf-8"))
                except:
                    url_link = 'nie podano'
                try:
                    lokalizacja = i.find_element(By.XPATH, "./a/article/p")
                except:
                    lokalizacja = 'nie podano'

                try:
                    cena = i.find_element(By.XPATH, "./a/article/div[2]/span[1]")
                except:
                    cena = 'nie podano'

                try:
                    cena_za_metr = i.find_element(By.XPATH, "./a/article/div[2]/span[2]")
                except:
                    cena_za_metr = 'nie podano'

                try:
                    liczba_pokoi = i.find_element(By.XPATH, "./a/article/div[2]/span[3]")
                except:
                    liczba_pokoi = 'nie podano'
                try:
                    powierzchnia = i.find_element(By.XPATH, "./a/article/div[2]/span[4]")
                except:
                    powierzchnia = 'nie podano'
                print('baza', baza_ogloszen.objects.filter(tytul=tytul.text).exists())
                if baza_ogloszen.objects.filter(tytul=tytul.text).exists():
                    print('baza', baza_ogloszen.objects.filter(tytul=tytul).exists())
                    pass
                else:
                    baza_ogloszen.objects.create(tytul=tytul.text, url_link=url_link.get_attribute("href"),
                                                 lokalizacja=lokalizacja.text, powierzchnia=powierzchnia.text,
                                                 cena=cena.text, cena_za_metr=cena_za_metr.text,
                                                 liczba_pokoi=liczba_pokoi.text,
                                                 data_wystawienia=datetime.datetime.now(tz=timezone.utc),
                                                 data_zakonczenia=None)
            return ogl
        return False
    for url in urls:
        oto_dom_scraper(url)


    for i in baza_ogloszen.objects.all():

        if i.tytul in ogl:
            pass
        else:
            i.data_zakonczenia=datetime.datetime.now(tz=timezone.utc)
            i.save()


    return render(request, 'home.html', {'ret': ogl,'text':"text"})
