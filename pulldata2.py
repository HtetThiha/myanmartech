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


engine = create_engine('mysql+mysqlconnector://<username>:<password>@localhost/ingestdata?auth_plugin=mysql_native_password', echo=False)
connection = engine.raw_connection()

items = []
stableitems = []

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

position = 1
keepgoing = 1

# driver.get("https://www.facebook.com/khitthitnews/")
# driver.get("https://www.facebook.com/MizzimaDaily/")
# driver.get("https://www.facebook.com/rfaburmese")
# driver.get("https://www.facebook.com/myanmarnownews")
# driver.get("https://www.facebook.com/VoA.Burmese.News/")
# driver.get("https://www.facebook.com/theirrawaddyburmese/")
driver.get("https://www.facebook.com/DVBTVNews/")
# driver.get("https://www.facebook.com/ElevenMediaGroup/")

# driver.get("https://www.facebook.com/NewsWatchJournal/")
# driver.get("https://www.facebook.com/kamayutmedia/")
# driver.get("https://www.facebook.com/frontiermyanmar.net/")
# driver.get("https://www.facebook.com/crph.official.mm/")
# driver.get("https://www.facebook.com/kumudranews/")











#div[aria-posinset='13'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div

first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
        
    nativemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div:nth-child(3) > div")
    while nativemessage:
        item = {}
        item['created_at'] = datetime.now()
        item['id'] = str(uuid.uuid4())
        
#         print("message at position:"+str(position)+" : "+message.text)
        position += 1
        time.sleep(SCROLL_PAUSE_TIME)
#         first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
#         message = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div")
        
        #check if there is see more
        
        try:
            timestamp = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div >div > div:nth-child(2)>div>div:nth-child(2)")
#         print("timestamp: "+str(position)+" : "+timestamp.text )
            item['timestamp'] = timestamp.text
        except:
            item['timestamp'] = "no time stamp"
        
        try:
            postlink = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div >div > div>div>a")
#         print("postlink: "+postlink.get_attribute('href'))
            item['postlink'] = postlink.get_attribute('href')
        except:
            item['postlink'] = "no postlink"
    
        try:
            seemore = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div:last-child > div > div")
            if seemore:
                print("see more clicked")
                seemore.click()
            time.sleep(SCROLL_PAUSE_TIME)
        
        except:
            print("see more native language is not there")
        
        try:
            nativemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div:nth-child(3) > div")
#         print("nativemessage: "+nativemessage.text )
            item['nativemessage'] = nativemessage.text
        except:
            item['nativemessage'] = "no message"
        
        
        try:
            seetranslation = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +div > div > div > span > div")
            if seetranslation:
                print("see translation clicked")
                seetranslation.click()
        except:
            print("see translation not there")
        
        try:
            seemoretrans = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +blockquote > span > div > div >span > div:last-child >div > div")
            seemoretrans.click()
            time.sleep(SCROLL_PAUSE_TIME)
        except:
            print("see more traslated language is not there")
            
        try:
            translatemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +blockquote")
            #         print("translatemessage: "+translatemessage.text )
            item['translatedmessage'] = translatemessage.text
        except:
            item['translatedmessage'] = "no translated message"
        
#         item['images'] = []
        #getting images links
        imagelinks = ""
        try:
            images = driver.find_elements_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div > div >a >div>div>div>img")
            if images:
                for image in images:
        #                 print("image link: "+ image.get_attribute('src'))
        #                 item['images'].append(image.get_attribute('src'))
                    imagelinks = imagelinks + ";" + image.get_attribute('src')
        except:
            print('nested image links not there')
            
        
        try:
            singleimage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div >a>div>div>div>div>img")
#             print("single image link: "+ singleimage.get_attribute('src'))
#             item['images'].append(singleimage.get_attribute('src'))
            imagelinks = imagelinks + ";" + singleimage.get_attribute('src')
        except:
            print('single nested image link not there')
        
        item['images'] = imagelinks
        
        
        try:
            hasmoreimages = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div > div:last-child >a>div+div>div")
#             print("more images: "+ hasmoreimages.text)
            item['hasmoreimages'] = hasmoreimages.text
        except:
            print("no additional images")
            item['hasmoreimages'] = '0'
        
        
        
        items.append(item)
        stableitems.append(item)
        
        if position%10 == 0:
            series = pd.DataFrame(None)
            series = pd.DataFrame.from_dict(items)
            series.to_sql('DVBTVNews', con=engine, if_exists='append', index= False)
            items = []

        
#         nativemessage.location_once_scrolled_into_view
#         driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"})', nativemessage)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1080)")
        time.sleep(4)
    
#     keepgoing = 0
#     break
#     driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

   

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    

driver.quit()


stableitems

# first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
# if first_result:
#     message = driver.find_element_by_css_selector("div[data-ad-preview='message']  div > div > span > div > div")
#     while message:
#         print("message at position:"+str(position)+" : "+message.text)
#         position += 1
#         first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
#         message = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div")
            
            
