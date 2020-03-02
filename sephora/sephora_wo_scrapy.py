from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

start_urls = ["http://www.sephora.com/shop/moisturizing-cream-oils-mists",
                    "http://www.sephora.com/shop/cleanser",
                    "http://www.sephora.com/shop/facial-treatments",
                    "http://www.sephora.com/shop/eye-treatment-dark-circle-treatment",
                    "http://www.sephora.com/shop/face-mask",
                    "http://www.sephora.com/shop/sunscreen-sun-protection",
                    "http://www.sephora.com/shop/self-tanning-products",
                    "http://www.sephora.com/shop/lip-treatments"]


def parse_content(driver,f,g):

    while True:
        height = driver.execute_script("return document.body.scrollHeight;")
        offset = driver.execute_script("return window.pageYOffset")
        if height-offset<1000:
            break
        else:
            driver.execute_script("window.scrollBy(0, 700);")
            time.sleep(0.5)

    # check_height = driver.execute_script("return document.body.scrollHeight;")    
    # for num in range(1,7):
    #     driver.execute_script("window.scrollBy(0, 700);")
    #     driver.execute_script("window.scrollTo(0, "+str(check_height//6)+");") #can't scroll too fast
    #     time.sleep(2)
    #     el = driver.find_elements_by_css_selector('div.css-12egk0t')[-1].text
    category = driver.find_element_by_css_selector('h1.css-fgy0ne').text
    current_page = driver.find_element_by_css_selector('button.css-nnom91').text
    items = driver.find_elements_by_css_selector('div.css-12egk0t a[href]')
    #urls = [i.get_attribute('href') for i in items]
    g.write("{} {} {}\n".format(category,current_page,len(items)))
    for i in items:
        tmp_url = i.get_attribute('href')
        f.write("{}\n".format(tmp_url))

def parse(url):
    driver = webdriver.Chrome(executable_path="/Users/weifanchen/chromedriver")
    driver.get(url)
    time.sleep(3)
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#inside_holder')))
    #test=driver.find_element_by_css_selector('header.Header')
    #test=driver.find_element_by_css_selector('div#inside_holder')
    test=driver.find_element_by_css_selector('body.css-1rq8sta')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(test, 150, 20) #move 150 pixels to the right to access Help link
    action.click()
    action.perform()
    g = open('sephora_log.txt',"a+")
    f = open("sephora_url.txt", "a+")
    parse_content(driver,f,g)
    total_page = int(driver.find_elements_by_css_selector("ul.css-m5oht li")[-1].text)
    for i in range(2,total_page+1):
        driver.get(url+"?currentPage="+str(i))
        time.sleep(3)
        parse_content(driver,f,g)

    # next_page_botton = driver.find_element_by_css_selector('button[aria-label="Next"]')
    # if not next_page_botton.get_attribute("disabled"):
    #     next_page_botton.click()
    #     parse_content(driver,f)
    #     

    driver.quit()
    f.close()
    g.close()


for url in start_urls:
    print('start',url)
    parse(url)