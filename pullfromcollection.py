from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from datetime import datetime
import uuid
import pandas as pd
from sqlalchemy import create_engine

# Step 1) Open Firefox 
driver = webdriver.Firefox()
# Step 2) Navigate to Facebook
driver.get("http://www.facebook.com")
# Step 3) Search & Enter the Email or Phone field & Enter Password
username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
submit   = driver.find_element_by_name("login")
username.send_keys("username")
password.send_keys("password")
# Step 4) Click Login
submit.click()

wait = WebDriverWait(driver,10)


collectionurl="https://www.facebook.com/saved/list/10100366009151675"
driver.get(collectionurl)


linklist = []
items = []

# Get scroll height.
last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page.
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:

        break

    last_height = new_height

    
try:
    links = driver.find_elements_by_css_selector("div>div>div>div>div:nth-child(2)>a")
    for link in links:
        linklist.append(link.get_attribute('href'))

except:
    print("error")
    

for url in linklist:
#     url = "https://www.facebook.com/permalink.php?story_fbid=1073824409765875&id=100014149783648"
    item = {}
    driver.get(url)
    
    try:
        profile = driver.find_element_by_css_selector("div[aria-posinset='1'] > div >div>div>div>div>div:nth-child(2)>div>div:nth-child(2) > div > div >div>a").get_attribute('href')
    except:
        profile = "no profile"
    
    try:
        posted_date = driver.find_element_by_css_selector("div[aria-posinset='1'] > div >div>div>div>div>div:nth-child(2)>div>div:nth-child(2) > div > div:nth-child(2)>div>div:nth-child(2)").text
    except:
        posted_date = "no posted_date"
    
    try:
        message = driver.find_element_by_css_selector("div[data-ad-preview]").text
    except:
        message = "no message"
    
    try:
        seeTranslation = driver.find_element_by_css_selector("div[data-ad-preview] +div >div >div>span>div").click()
        translatedmessage = driver.find_element_by_css_selector("div[data-ad-preview] +blockquote").text
    except:
        translatedmessage = "no translated message"
        
    try:
        images = driver.find_elements_by_css_selector("a > div >div > div > img")
        imagelinks = ""
        if images:
            for image in images:
                imagelinks = imagelinks + ";" + image.get_attribute('src')
    except:    
        imagelinks = "images unavailable"
    
    item['created_at'] = datetime.now()
    item['id'] = str(uuid.uuid4()) 
    item['postlink'] = url
    item['profile'] = profile
    item['posted_date'] = posted_date
    item['message'] = message
    item['translatemessage'] = translatedmessage
    item['imagelinks'] = imagelinks
    items.append(item)
        
        
engine = create_engine('mysql+mysqlconnector://username:password!@localhost/ingestdata?auth_plugin=mysql_native_password', echo=False)
connection = engine.raw_connection()

series = pd.DataFrame.from_dict(items)
series.to_sql('collections', con=engine, if_exists='append', index= False)

# driver.quit()

items