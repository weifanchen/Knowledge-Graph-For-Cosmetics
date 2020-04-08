from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import random
import re

'''
scrapy the ingredients('ingredient_list') and its information(safety, acne etc) from cosdna according ingredient description('ingredients')
also save the ingredients in ingredients.jl

'''

def deal_with_list(column,keyword,ingredient_info):
    # for the columns that are not only integer e.g. 1-3
    if column==['']:
        ingredient_info[keyword]=None
    elif len(column)==1:
        ingredient_info[keyword]=[int(column[0])]
    else:
        ingredient_info[keyword]=list(range(int(column[0]),int(column[1])+1))



def get_ingredient_info(soup,ingredient_profile):
    table = soup.find_all(lambda x: ('tr-i' in x.attrs.get('class',[]) and 'none' not in x.attrs.get('class',[])))
    full_ingredient_list = list()
    for row in table:
        columns = row.select('td')
        ingredient_info = {}
        ingredient_info['name'] = columns[0].select("a div span")[0].text.strip()
        function = [i.strip() for i in columns[1].text.split(',')]
        ingredient_info['function']=function if function!=[''] else None
        acne = columns[2].text.strip().split('-')
        irritant = columns[3].text.strip().split('-')
        deal_with_list(acne,'acne',ingredient_info)
        deal_with_list(irritant,'irritant',ingredient_info)
        pre_safety = columns[4].select('a')[0]
        if pre_safety.find('span'):
            safety = [i.text for i in pre_safety.select('span')]
            deal_with_list(safety,'safety',ingredient_info)
        else:
            ingredient_info['safety'] = None

        save_new_ingredient(ingredient_info)
        full_ingredient_list.append(ingredient_info)
    return full_ingredient_list

def ingredient_preprocessing(text):
    if '\n\n' in text:
        main_text = text.split('\n\n')[1:]
        main_text = ', '.join(main_text) +'\n'
    else:
        main_text = text
    main_text = main_text+ ', '.join(re.findall(r'\-(.*?)\:',text))
    main_text = main_text.replace(':',',')
    return main_text


def get_soup_by_ingredient(driver,product):
    driver.get('http://www.cosdna.com/eng/ingredients.php')
    time.sleep(random.randint(2,4))
    ingredients_list_box = driver.find_element_by_css_selector('textarea.form-control')
    text=ingredient_preprocessing(product['ingredients'])
    ingredients_list_box.send_keys(text)
    ingredients_list_box.submit() 
    time.sleep(random.randint(2,4))
    try:
        element = driver.find_element_by_css_selector('table.table.table-hover.border')
        html = driver.execute_script("return arguments[0].outerHTML;", element)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except:
        return ''

def save_new_ingredient(ingredient_info):
    # save new ingredient to ingredient.jl
    if ingredient_info not in ingredient_profile:
        ingredient_profile.append(ingredient_info)
        ingredientfile.write(json.dumps(ingredient_info) + '\n')
    else:
        pass 
        
def get_soup_via_name(driver,keyword):
    # for product without ingredients
    driver.get('https://www.cosdna.com/eng/product.php')
    product_name_box = driver.find_element_by_css_selector('input.form-control')
    product_name_box.send_keys(keyword)
    product_name_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(1,3))
    try:
        sort_latest = driver.find_element_by_css_selector('div.sort a:first-of-type') #CLICK THE FIRST ONE
        sort_latest.click()
        first_product = driver.find_element_by_css_selector('table.table.table-hover tbody tr td.pl-0 a:first-of-type') # click 
        first_product.click()

        element = driver.find_element_by_css_selector('table.table.table-hover.border')
        html = driver.execute_script("return arguments[0].outerHTML;", element)
        soup = BeautifulSoup(html, 'html.parser')
        print('search by name: ',keyword)
        return soup
    except:
        print('no result by name: ',keyword)
        return ''

# product_list_path = "./output/sephora_skincare_product_ingredient_list.jl"
product_list_path = "./output/sephora_skincare_product_6_updated2.jl"

product_list = []
with open(product_list_path) as json_file:
    for line in json_file:
        product_list.append(json.loads(line))

ingredient_profile_path = './output/ingredients.jl'
ingredient_profile = []
with open(ingredient_profile_path) as f:
    for line in f:
        ingredient_profile.append(json.loads(line))

productfile = open('./output/sephora_skincare_product_6_updated3.jl', 'a+')
ingredientfile = open('./output/ingredients.jl', 'a+')
#product_wo_ingredient = open('./output/product_wo_ingredient.jl', 'a+')

driver = webdriver.Chrome('/Users/weifanchen/chromedriver')


for product in product_list[:]:
    soup=''
    if product['ingredient_list'] == []:
        #print('empty ingredient list',product['product_name'])
        if product['ingredients'] != '':
            soup = get_soup_by_ingredient(driver,product)
        if not soup:
            #print('empty ingredient description',product['product_name'])
            keyword = product['brand']+ ' '+product['product_name']
            soup = get_soup_via_name(driver,keyword)
    if soup:
        ingredient_info_list =  get_ingredient_info(soup,ingredient_profile)
        product['ingredient_list'] = [i['name'] for i in ingredient_info_list]
    #productfile.write(json.dumps(product) + '\n')

for p in product_list:
    productfile.write(json.dumps(p) + '\n')
    

driver.quit()

ingredientfile.close()
productfile.close()
#product_wo_ingredient.close()


'''
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"table.table.table-hover.border"}
  (Session info: chrome=80.0.3987.132)

raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response
'''

    
        






