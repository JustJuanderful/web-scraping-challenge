# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import os
import sys
import pymongo

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Nasa site 
    news_url = 'https://mars.nasa.gov/news/'

    # Retrieve page
    response = requests.get(news_url)

    # Parse bs object
    soup = bs(response.text, 'html.parser')

    # Get News Article title
    title = soup.find('div', class_="content_title").text.strip()

    # Get News Article Paragraph
    paragraph = soup.find('div', class_="image_and_description_container").text.strip()

    # Nasa Images site
    nasa_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_images_url)

    # Get Featured Image URL
    image_html = browser.html

    # Parse bs object
    image_soup = bs(image_html, 'html.parser')

    article = image_soup.find('a', class_='button fancybox')
    href = article['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + href

    # Mars Weather Twitter site
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    weather_html = browser.html

    # Parse bs object
    weather_soup = bs(weather_html, 'html.parser')
    mars_weather = weather_soup.find('div', class_='css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text

    # Mars Facts Page
    mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts.columns=["Description", "Value"]
    mars_facts.set_index("Description", inplace=True)
    mars_f = mars_facts.to_html()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html

    # Parse bs object
    soup = bs(hemisphere_html, 'html.parser')

    results = soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for r in results: 
        heading = r.find('h3').text.replace('Enhanced', '')
        link = r.find('a')['href']
        url = "https://astrogeology.usgs.gov" + link
        browser.visit(url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        img_url = soup.find('div', class_="downloads").find('a')['href']
        print(heading)
        print(img_url)
        hemisphere = {
            'title': heading,
            'img_url': img_url
        }
        hemisphere_image_urls.append(hemisphere)

    # Collect mars data
    mars_df = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_f,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_df
