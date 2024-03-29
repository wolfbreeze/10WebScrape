#Code from https://github.com/Ghernandez1991/Flask-Mongodb
#Thank you for your time Joe
# Sempre ubi sub ubi!

import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time

# starts up Chrome browser, headless and no extention as Mac Chrome does not need it
def start_browser():
    
    return Browser("chrome", headless=False)

#Let the scraping of websites begin!
def scrape ():
    browser = start_browser()
    mars_data = {}

    # visit the NASA Mars News site and scrape headlines
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # takes URL and goes to browser to load webpage

    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')
    # calls BeautifulSoup to parse of text of the browsed webpage

    list_of_news = nasa_soup.find('ul', class_='item_list')
    #finds unordered list in a class of item_list in html puts all this into list_of_news
    first_item_of_list = list_of_news.find('li', class_='slide')
    #finds listed item in a class of slide in list_of_news puts all this into first_item_of_list
    header = first_item_of_list.find('div', class_='content_title').text
    #finds div in a class of content_title puts the text into header
    synoposis = first_item_of_list.find('div', class_='article_teaser_body').text
    #finds div in a class of article_teaser_body puts the text into synoposis

    
    results1 = nasa_soup.find_all('li', class_="slide")
#finds all listed items in a class of slide puts the into results1

    mars_data["nasa_headline"] = header
    #puts text of header into mars_data dictionary as nasa_headline
    mars_data["nasa_teaser"] = synoposis
     #puts text of synoposis into mars_data dictionary as nasa_data


   #Visit the url for JPL Featured Space Image here.

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
     #takes URL and goes to browser to load webpage
    browser.click_link_by_partial_text('FULL IMAGE')
# clicks hypertextlink to pull FUll Image of webpage first image


    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    time.sleep(1)
    #stops the loading of an iframe

    image_url_html = browser.html
    image_soup = BeautifulSoup(image_url_html, 'html.parser')
    # calls BeautifulSoup to parse of text of the browsed webpage
# grabbing down teh html text to find the latest photo of Mars
    img_relative_path = image_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{img_relative_path}'
    mars_data["feature_image_src"] = featured_image_url

    #Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
#Save the tweet text for the weather report as a variable called mars_weather.
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    # calls BeautifulSoup to parse of text of the browsed webpage
    tweets = twitter_soup.find('div', class_='stream')
#Scrape twitter page for latest weather data
    for tweet in tweets:
        try:
            text_of_tweets = tweets.find('p', class_= "tweet-text").text
         #The time and date of article publication
            if(text_of_tweets):
                print('-----------------')
                print(text_of_tweets)
                
                
                
        #Tweet Title and text of tweet put into a dictionary
         # Dictionary to be inserted into MongoDB
                post = {
                    'Tweet Title': text_of_tweets
                }
# Insert dictionary into MongoDB as a document
                collection1.insert_one(post)
        
        except AttributeError as e:
            print(e)
        tweet_link=e
        break  
        mars_data["weather_summary"] = tweet_link
#this places the tweet into the Mongo db


     #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter,

    mars_url = "https://space-facts.com/mars/"

    browser.visit(mars_url)
    
    mars1_html = browser.html
    mars1_soup = BeautifulSoup(mars1_html, 'html.parser')
# calls BeautifulSoup to parse of text of the browsed webpage

    mars_table = mars1_soup.find('section', class_='sidebar widget-area clearfix')
    first_table = mars_table.find('table', class_='tablepress tablepress-id-p-mars')


    
    url5 = "https://space-facts.com/mars/"


    tables = pd.read_html(url5)
       
    #table 1 is the needed table 
    tables[1]

    df = tables[1]
    df.columns = ['Identifier', 'Measurments']
    df
    mars_table_html = df.to_html(header=False, index=False)
    mars_data["fact_table"] = mars_table_html
#taking mars facts table into panda dataframe without headers and index into  mars_table_html that is placed into Mongo DB mars_data blob

    #grabbing hemisphere1
    # looking for and grabbing a photo title and URL
    
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')

    hemi_list1 = hemi_soup.find ('div', class_= "downloads")
    
    cereberus = ''

    for a in hemi_list1('a', href=True):
        print ("Found the URL:", a['href'])
        cereberus=a['href']
        break

    #Grab hemi 2
# looking for and grabbing a photo title and URL

    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    hemi_html1 = browser.html
    hemi_soup1 = BeautifulSoup(hemi_html1, 'html.parser')

    hemi_list2 = hemi_soup1.find ('div', class_= "downloads")

    schiaparelli = ''

    for a in hemi_list2('a', href=True):
        print ("Found the URL:", a['href'])
        schiaparelli=a['href']
    
        break


    #find hemi 3
    # looking for and grabbing a photo title and URL
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')

    hemi_html2 = browser.html
    hemi_soup2 = BeautifulSoup(hemi_html2, 'html.parser')

    hemi_list3 = hemi_soup2.find ('div', class_= "downloads")

    syrtis = ''

    for a in hemi_list3('a', href=True):
        print ("Found the URL:", a['href'])
        syrtis=a['href']
        break

    # find hemisphere 4
    # looking for and grabbing a photo title and URL
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')

    hemi_html3 = browser.html
    hemi_soup3 = BeautifulSoup(hemi_html3, 'html.parser')

    hemi_list4 = hemi_soup3.find ('div', class_= "downloads")

    valles= ''

    for a in hemi_list4('a', href=True):
        print ("Found the URL:", a['href'])
        valles=a['href']
        break
    
    # saving locations URLS of 4 photos and their titles in a dictionary
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": valles},
    {"title": "Cerberus Hemisphere", "img_url": cereberus},
    {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli},
    {"title": "Syrtis Major Hemisphere", "img_url": syrtis},
    ]

    #Saving dictionary of URL and tittels in Mongo db
    mars_data["hemisphere_imgs"] = hemisphere_image_urls