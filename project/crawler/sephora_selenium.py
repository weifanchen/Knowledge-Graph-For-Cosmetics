from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import string
import json

def processIngredient(string):
    substring = 'Clean at Sephora products are formulated without:'
    try:
        return string[:string.index(substring)].strip()
    except:
        return string

def selenium(url):
    gaps = 0.5
    # driver = webdriver.Chrome('./sephora/sephora/spiders/chromedriver')
    driver = webdriver.Chrome('./chromedriver')

    driver.get(url)
    time.sleep(gaps*4)
    try:
        spare = driver.find_element_by_css_selector('div#inside_holder')
        ActionChains(driver).move_to_element_with_offset(spare, 150, 0).click().perform()
    except:
        print(':)')     
    
    response = BeautifulSoup(driver.page_source, 'html.parser') 
        
    sizepriceflag = False
        
    if not response.select('div.css-v7k1z0 span.css-10b3y5z'): 
        number = response.select('div.css-v7k1z0')[-1].text.split()[-1]
    else:
        # pattern : SIZE 5 oz/ 150 mL•ITEM 2259935
        sizeitem = response.select('div.css-v7k1z0')[-1].text.split('•')
        number = sizeitem[-1].split()[-1]
        sizes = [sizeitem[0][5:]]
        prices = [response.find_all(attrs={"data-comp": "Price Box "})[-1].text]
        sizepriceflag = True

    brand = response.select('h1.css-140z8k4 a.css-es084o span.css-euydo4')[-1].text
    product = response.select('h1.css-140z8k4 span.css-0')[-1].text
    loves = response.select('span[data-at="product_love_count"]')[-1].text
    reviews = response.select('span[data-at="number_of_reviews"]')[-1].text.split()[0]
    stars = response.select('div[data-comp="StarRating "]')[0].get('aria-label').split()[0]
    
    driver.find_element_by_css_selector('button#tab2').click()
    ingredients = driver.find_element_by_css_selector('div#tabpanel2 div').text

    if not sizepriceflag:
        boxes = driver.find_elements_by_xpath('//div[@data-comp="ProductSwatchItem "]')
        prices = []
        sizes = []
        for box in boxes: 
            # sizes.append(box.text)
            ActionChains(driver).move_to_element(box).perform()
            prices.append(driver.find_element_by_css_selector('div[data-comp="Price Box "]').text)
            sizes.append(driver.find_element_by_css_selector('span[data-comp="ProductVariation Text Box "]').text[6:])

    response.select('a.css-dvzm2b ')[0].text
   
    category = response.select('a.css-dvzm2b ')[0].text
    subcategory = response.select('a.css-dvzm2b ')[1].text
    minicategory = response.select('a.css-lrl8sh ')[0].text

    product = {'url': url, 'product_id': number, 'product_name': product, 'brand': brand, 
               'sizes': sizes, 'prices': prices, 'loves': loves, 'reviews': reviews, 'stars': stars,
               'ingredients': processIngredient(ingredients), 'category': category, 'subcategory': subcategory, 'minicategory': minicategory}

    scroll_window = 'window.scrollTo(0, document.body.scrollHeight/4+%d);'
    length = 0
    while True:
        driver.execute_script(scroll_window%length) 
        # time.sleep(gaps*4)
        time.sleep(gaps)
        try:
            next6 = driver.find_element_by_css_selector('button.css-frqcui ')
            next6.click()
            # length += 0
        except:
            break
    
    response = BeautifulSoup(driver.page_source, 'html.parser') 
    reviewlist = response.select('div[data-comp="Review "]')
    reviews = []
    for r in reviewlist: 
        if len(r.select('span[data-at="nickname"]')) > 0:
            # print(r.select('span[data-at="nickname"]'))
            user_id = r.select('span[data-at="nickname"]')[0].text
            temp = dict((string.capwords(rr.select('b')[-1].text), string.capwords(rr.text).replace(string.capwords(rr.select('b')[-1].text), '').strip()) for rr in r.select('div.css-10lg0rx '))
            temp['user_id'] = user_id
            temp['product_id'] = number
            reviews.append(temp)
    
    driver.close()
    return product, reviews


with open('sephora_url.txt', 'r') as fd:
    product_urls = fd.read().split('\n')

# product_urls = ['https://www.sephora.com/product/the-ordinary-marine-hyaluronics-P455899?icid2=justarrivedskincare_us_skugrid_ufe:p455899:product',
#             'https://www.sephora.com/product/the-inkey-list-oat-cleansing-balm-P455364?icid2=justarrivedskincare_us_skugrid_ufe:p455364:product',
#             'https://www.sephora.com/product/oil-water-double-cleanser-P447779?icid2=similar%20products:p447779:product']

productfile = open('sephora_skincare_product.jl', 'w')
reviewfile = open('sephora_skincare_review.jl', 'w')

for url in product_urls[:]:
    product, reviews = selenium(url)
    productfile.write(json.dumps(product) + '\n')
    reviewfile.write('\n'.join([json.dumps(r) for r in reviews])+'\n')
    productfile.flush()
    reviewfile.flush()

