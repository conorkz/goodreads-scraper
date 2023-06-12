from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import csv
roi = 'no info on the website'
url = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1'
s = Service("PATH_TO_CHROMEDRIVER")
driver = webdriver.Chrome(service=s)
with open('goodreads.csv', "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Berlin time', 'URL', 'Book cover url', 'Title', 'Author', 'Description', 'Rating out of 5', 'Number of ratings', 'Number of reviews', 'First published', 'Number of pages', 'Number of people currently reading', 'Number of people want to read', 'About the author', 'ISBN', 'ISBN10', 'Language'])
    while True:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for b in soup.select('a.bookTitle'):
            link = 'https://www.goodreads.com' + b['href']
            driver.get(link)
            time.sleep(5)
            try:
                ss = driver.find_element(By.CSS_SELECTOR, '[aria-label="Book details and editions"]')
                driver.execute_script("arguments[0].click();",ss)
                time.sleep(3)
            except:
                pass
            sorpa = BeautifulSoup(driver.page_source, "html.parser")
            if sorpa.select_one('img.ResponsiveImage'):
                cover = sorpa.select_one('img.ResponsiveImage')['src']
            else:
                cover = roi
            if sorpa.select_one('[data-testid=bookTitle]'):
                title = sorpa.select_one('[data-testid=bookTitle]').text
            else:
                title = roi
            if sorpa.select_one('[data-testid=name]'):
                author = sorpa.select_one('[data-testid=name]').text
            else:
                author = roi
            if sorpa.select_one('[data-testid=description] .Formatted'):
                descrip = sorpa.select_one('[data-testid=description] .Formatted').text
                if descrip == '':
                    descrip = roi
            else:
                descrip = roi
            if sorpa.select_one('[data-testid=ratingsCount]'):
                ratings = sorpa.select_one('[data-testid=ratingsCount]').text.replace('ratings', '').replace('rating', '')
            else:
                ratings = roi
            if sorpa.select_one('[data-testid=reviewsCount]'):
                reviews = sorpa.select_one('[data-testid=reviewsCount]').text.replace('reviews', '').replace('review', '')
            else:
                reviews = roi
            if sorpa.find(class_='RatingStatistics__rating'):
                rating = sorpa.find(class_='RatingStatistics__rating').text
            else:
                rating = roi
            if sorpa.select_one('[data-testid=publicationInfo]'):
                publiinfo = sorpa.select_one('[data-testid=publicationInfo]').text.replace('First published', '').replace('Published', '')
            else:
                publiinfo = roi
            if sorpa.select_one('[data-testid=pagesFormat]'):
                ava = sorpa.select_one('[data-testid=pagesFormat]').text
                if re.search(r'\d+', ava):
                    pages = re.search(r'\d+', ava).group()
                else:
                    pages = roi
            else:
                pages = roi
            if sorpa.select_one('[data-testid=currentlyReadingSignal]'):
                avas = sorpa.select_one('[data-testid=currentlyReadingSignal]').text
                if re.search(r'\d+(,\d+)*', avas):
                    if 'k' in avas:
                        number = int(re.search(r'\d+(,\d+)*', avas).group())
                        number *= 1000
                        curreading = number
                    elif 'm' in avas:
                        numberr = int(re.search(r'\d+(,\d+)*', avas).group())
                        numberr *= 1000000
                        curreading = numberr
                    else:
                        curreading = re.search(r'\d+(,\d+)*', avas).group()
                else:
                    curreading = roi
            else:
                curreading = roi
            if sorpa.select_one('[data-testid=toReadSignal]'):
                avass = sorpa.select_one('[data-testid=toReadSignal]').text
                if re.search(r'\d+(,\d+)*', avass):
                    if 'k' in avass:
                        numbere = int(re.search(r'\d+(,\d+)*', avass).group())
                        numbere *= 1000
                        toread = numbere
                    elif 'm' in avass:
                        numberre = int(re.search(r'\d+(,\d+)*', avass).group())
                        numberre *= 1000000
                        toread = numberre
                    else:
                        toread = re.search(r'\d+(,\d+)*', avass).group()
                else:
                    toread = roi
            else:
                toread = roi
            if sorpa.find(class_='AuthorPreview'):
                abauthor = sorpa.find(class_='AuthorPreview').find_next_sibling().find(class_='Formatted').text
                if abauthor == '':
                    abauthor = roi
            else:
                abauthor = roi
            if sorpa.find(class_='DescList'):
                aq = sorpa.find(class_='DescList')
                if aq.find(string='ISBN'):
                    agg = str(aq)
                    if re.findall(r'\d{13}', agg):
                        isbn = re.findall(r'\d{13}', agg)[0]
                    else:
                        isbn = roi
                    if re.findall(r'ISBN10:\s*(\d{10})', agg):
                        isbn10 = re.findall(r'ISBN10:\s*(\d{10})', agg)[0]
                    else:
                        isbn10 = roi
                else:
                    isbn = roi
                    isbn10 = roi
            else:
                isbn = roi
                isbn10 = roi
            if sorpa.find('dt', string='Language'):
                language = sorpa.find('dt', string='Language').find_next_sibling('dd').find('div', {'data-testid': 'contentContainer'}).text
            else:
                language = roi
            berlin = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S %Z')
            writer.writerow([berlin, link, cover, title, author, descrip, rating, ratings, reviews, publiinfo, pages, curreading, toread, abauthor, isbn, isbn10, language])
        if soup.select_one('a.next_page'):
            url = 'https://www.goodreads.com' + soup.select_one('a.next_page')['href']
            print(url)
        else:
            break