from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time


# Step 1) Open Firefox 
driver = webdriver.Firefox()
# Step 2) Navigate to Facebook
driver.get("http://www.facebook.com")
# Step 3) Search & Enter the Email or Phone field & Enter Password
username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
submit   = driver.find_element_by_name("login")
username.send_keys("6503849237")
password.send_keys("B0ga13:87")
# Step 4) Click Login
submit.click()

wait = WebDriverWait(driver,10)

position = 1
keepgoing = 1

driver.get("https://www.facebook.com/khitthitnews/")

#div[aria-posinset='13'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div

first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
        
    nativemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span")
    while nativemessage:
#         print("message at position:"+str(position)+" : "+message.text)
        position += 1
        time.sleep(SCROLL_PAUSE_TIME)
#         first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
#         message = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div")
        
        #check if there is see more
        
        timestamp = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div >div > div:nth-child(2)>div>div:nth-child(2)")
        postlink = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div >div > div>div>a")
        
        try:
            seemore = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div:last-child > div > div")
            if seemore:
                print("see more clicked")
                seemore.click()
            time.sleep(SCROLL_PAUSE_TIME)
        
        except:
            print("see more native language is not there")
        finally:
            nativemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span")
        
        seetranslation = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +div > div > div > span > div")
        if seetranslation:
            print("see translation clicked")
            seetranslation.click()
        
        try:
            seemoretrans = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +blockquote > span > div > div >span > div:last-child >div > div")
            seemoretrans.click()
            time.sleep(SCROLL_PAUSE_TIME)
        except:
            print("see more traslated language is not there")
        finally:
            time.sleep(SCROLL_PAUSE_TIME)
            translatemessage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message'] +blockquote")
            
        
        #getting images links
        try:
            images = driver.find_elements_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div > div >a >div>div>div>img")
            for image in images:
                    print("image link: "+ image.get_attribute('src'))
        except:
            print('nested image links not there')
            
        
        try:
            singleimage = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div >a>div>div>div>div>img")
            print("single image link: "+ singleimage.get_attribute('src'))
        except:
            print('single nested image link not there')
        
        try:
            hasmoreimages = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div > div:last-child >a>div+div>div")
            print("more images: "+ hasmoreimages.text)
        except:
            print("no additional images")
            
            
        print("timestamp: "+str(position)+" : "+timestamp.text )
        print("postlink: "+postlink.get_attribute('href'))
        print("nativemessage: "+nativemessage.text )
        print("translatemessage: "+translatemessage.text )
        
        nativemessage.location_once_scrolled_into_view
        time.sleep(4)
        
    driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        
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
# first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
# if first_result:
#     message = driver.find_element_by_css_selector("div[data-ad-preview='message']  div > div > span > div > div")
#     while message:
#         print("message at position:"+str(position)+" : "+message.text)
#         position += 1
#         first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div[aria-posinset='"+str(position)+"']")))
#         message = driver.find_element_by_css_selector("div[aria-posinset='"+str(position)+"'] > div >div > div > div > div > div > div > div > div[data-ad-preview='message']  div > div > span > div > div")
            
            
