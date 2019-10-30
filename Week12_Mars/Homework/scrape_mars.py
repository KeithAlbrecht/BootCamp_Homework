#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


# In[2]:


# def init_browser():
#         return webdriver.Chrome("chromedriver")


# In[3]:


# def scrape_info():
#     browser = init_browser()
#     url = "https://mars.nasa.gov/news/"
#     browser.get(url)
#     time.sleep(1)
#     html = browser.page_source
#     soup = bs(html, "html.parser")

# I got stuck here for a long time... I never really understood why this didn't work.  
# I tried to do the same thing as the class activity...  
# I ended up using the response method instead to scrape the data.  
# I think that this is ok but I would like to understand this better.


# In[4]:

def scrape_info():
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # print(soup).prettify()


# In[5]:


    title = soup.find('div', class_='content_title')
    newsTitle = title.text
    # print(newsTitle)


# In[6]:


    news = soup.find('div', class_='rollover_description_inner')
    newsText = news.text
    # print(newsText)


# In[7]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_base = 'https://www.jpl.nasa.gov/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    result = soup.find('article', class_='carousel_item').attrs
    # print(result)


# In[8]:


    style = str(result['style'])
    style


# In[9]:


    style_trim = style.replace("background-image:", "")
    style_trim


# In[10]:


    style_trim2 = style_trim.replace(" url('", "")
    style_trim2


# In[11]:


    style_trim3 = style_trim2.replace("');", "")
    style_trim3


# In[12]:


    image = url_base + style_trim3
    # print(image)


# In[13]:


    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    result = soup.find('div', class_="js-tweet-text-container")
    # print(result)


# In[14]:


    weather = result.p.text
    # print(weather)


# In[17]:


    table_url = "https://space-facts.com/mars/"
    Mars_facts = pd.read_html(table_url)
    Mars_facts


# In[23]:


    Mars_table1 = pd.DataFrame(Mars_facts[0])
    Mars_table1.columns=['Characteristic', 'Mars', 'Earth']
    Mars_table1


# In[24]:


    Mars_table2 = pd.DataFrame(Mars_facts[1])
    Mars_table2.columns=['Characteristic', 'Data']
    Mars_table2


# In[25]:


    Mars_table1=Mars_table1.to_html()


# In[26]:


    Mars_table2=Mars_table2.to_html()


# In[50]:


    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    result = soup.find_all('div', class_="item")
    # print(result)


# In[28]:


    url_list = []
    for y in result:
        link = y.find('a')['href']
        url_list.append(link)   
    # print(url_list)


# In[70]:

    hemisphere_url_images=[]
    for x in url_list:
        url_base = 'https://astrogeology.usgs.gov'
        url = url_base + x
    #     print(url)
        response = requests.get(url)
        time.sleep(5)
        soup = bs(response.text, 'html.parser')
    #     print(soup)
        result1 = soup.find('img', class_="wide-image")
    #     print(result1)
        image = url_base + result1["src"]
        # print(image)
        result2 = soup.find('h2', class_='title')
        title = result2.text
        title = title.rsplit(' ', 1)[0]
        # print(title)
        Mars_Dictionary = {"Title": title, "Image_URL": image}
        hemisphere_url_images.append(Mars_Dictionary)
        
        time.sleep(10)


# In[71]:


    # print(hemisphere_url_images)    


# In[ ]:

    mars_data = {"Title": newsTitle, "Info": newsText, "Image": image, "Weather": weather, "Facts1": Mars_table1, "Facts2": Mars_table2, "Hemispheres": hemisphere_url_images}

    return mars_data
