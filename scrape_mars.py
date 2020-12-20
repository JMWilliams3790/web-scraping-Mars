#Perform Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "C:/Users/JMWil/Desktop/Bootcamp/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


######################
#Scrape the news page#
######################
def scrape_news():
    browser = init_browser()

    # Visit Nasa Mars News Page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Walk down the HTML tree
    first_t = soup.find('ul', class_='item_list')
    second_t = first_t.find('li', class_='slide')
    third_t = second_t.find('div', class_='content_title').get_text()
    paragraph = second_t.find('div', class_='article_teaser_body').get_text()

    # Store data in a dictionary
    mars_news = {
        "news_t": third_t,
        "news_p": paragraph
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_news




###########################
#Scrape the featured image#
###########################
def scrape_image():
    browser = init_browser()

    # Visit Nasa Mars News Page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Walk down the HTML tree
    first_i = soup.find('div', id="main_container")
    second_i = first_i.find('footer')
    third_i = second_i.find('a', class_='fancybox')['data-link']
    fourth_i = "https://www.jpl.nasa.gov" + third_i
    browser.visit(fourth_i)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    fifth_i = soup.find('img', class_='main_image')['src']
    featured_image_url = f"https://www.jpl.nasa.gov{fifth_i}"

    featured_image_dict = {
    "featured_image_url": featured_image_url,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return featured_image_dict


#######################
#Scrape the Mars facts#
#######################
def scrape_table():
     # Visit Nasa Mars Facts Page
    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    
    tables_df = tables[0]
    tables_df = tables_df.rename(columns={tables_df.columns[0]: "Description", tables_df.columns[1]: "Mars"}).set_index("Description")
    tables_df = tables_df.to_html(classes = "table table-striped")

    hemi_dict = {
    "table_html": tables_df,
    }
    
    

    # Return results
    return hemi_dict




##################################
#Scrape the hemisphere image page#
##################################
def scrape_hemi():
    browser = init_browser()

    # Visit Nasa Mars News Page
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    store_hemi_list = []
    hemisphere_list = ["Cerberus Hemisphere Enhanced",
        "Schiaparelli Hemisphere Enhanced",
        "Syrtis Major Hemisphere Enhanced",
        "Valles Marineris Hemisphere Enhanced"
    ]
    
    
    
    for hemisphere in hemisphere_list:
        browser.links.find_by_partial_text(hemisphere).click()
        
        time.sleep(1)
        
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        title = soup.find('h2').get_text()
        find = soup.find("div", class_="downloads")
        find_2 = find.find('a')
        img_url = find_2['href']
        
        
        browser.back()
    # Store data in a dictionary
        hemi_dict = {
            "title": title,
            "img_url": img_url
        }
        store_hemi_list.append(hemi_dict)
    # Close the browser after scraping
    browser.quit()

    # Return results
    return store_hemi_list



def scrape():
    news = scrape_news()
    image = scrape_image()
    table = scrape_table()
    hemi = scrape_hemi()

    mars_dict = {
        "news" : news,
        "image" : image,
        "table" : table,
        "hemisphere" : hemi
    }
    return mars_dict
