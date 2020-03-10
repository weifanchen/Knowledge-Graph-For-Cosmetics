from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import random


#driver = webdriver.Chrome('/Users/weifanchen/chromedriver')
#driver = webdriver.Chrome(executable_path="./chromedriver")
#driver.get('http://www.cosdna.com/eng/ingredients.php')


def deal_with_list(column,keyword,ingredient_info):
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
        save_single_ingredient(ingredient_info)
        full_ingredient_list.append(ingredient_info)
    return full_ingredient_list

def ingredient_preprocessing(text):
    if '\n\n' in text:
        main_text = text.split('\n\n')[1:]



def get_soup(driver,product):
    #driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get('http://www.cosdna.com/eng/ingredients.php')
    ingredients_list_box = driver.find_element_by_css_selector('textarea.form-control')
    text=ingredient_preprocessing(product['ingredients'])
    ingredients_list_box.send_keys(text)
    ingredients_list_box.submit() 
    time.sleep(random.randint(2,4))

    element = driver.find_element_by_css_selector('table.table.table-hover.border')
    html = driver.execute_script("return arguments[0].outerHTML;", element)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def save_single_ingredient(ingredient_info):
    if ingredient_info not in ingredient_profile:
        ingredient_profile.append(ingredient_info)
        ingredientfile.write(json.dumps(ingredient_info) + '\n')
    else:
        pass 
        

product_list_path = "./sephora/output/sephora_skincare_product.jl"
product_list = []
with open(product_list_path) as json_file:
    for line in json_file:
        product_list.append(json.loads(line))

ingredient_profile_path = 'ingredients.jl'
ingredient_profile = []
with open(ingredient_profile_path) as f:
    for line in f:
        ingredient_profile.append(json.loads(line))

productfile = open('sephora_skincare_product_2.jl', 'a+')
ingredientfile = open('ingredients.jl', 'a+')


for product in product_list[:]:
    driver = webdriver.Chrome('/Users/weifanchen/chromedriver')
    soup = get_soup(driver,product)
    ingredient_info_list = get_ingredient_info(soup,ingredient_profile)
    product['ingredient_list'] = [i['name'] for i in ingredient_info_list]
    productfile.write(json.dumps(product) + '\n')
    driver.quit()
    time.sleep(random.randint(0,5))

for i in ingredient_profile:
    ingredientfile.write(i+'\n')

ingredientfile.close()
productfile.close()


'''
FORMAT
{'name': string, 'function': list, 'acne': None/int, 'irritant': None/list, 'safety': None/list}, 
**** change acne to list as well?
{'name': 'Linalool', 'function': ['Fragrance'], 'acne': None, 'irritant': None, 'safety': [5]}, 
{'name': 'Lavandula Angustifolia Oil', 'function': ['Fragrance', 'Emollient', 'Plant extract'], 'acne': None, 'irritant': None, 'safety': [1]}
'''
'''
manually find ingredient
2325165
'''

'''
[p['product_id'] for p in product_list if p['ingredient_list']==[]]
[2031417, 2263713, 2264810, 2241057, 2051944, 662429, 1589118, 1064062, 2070811, 2264109, 1818772]
[p['product_id'] for p in product_list if p['ingredient_list']==[]]
[len(p['ingredients'].split('\n\n')) for p in product_list if '\n\n' in p['ingredients']] # only 207?

testfile = open('ingredients_test.jl','w')

temp_list=[]
for product in product_list[:]:
    id=product['product_id']
    ingredient=product['ingredients']
    temp={'id':id,'ingredient':ingredient}
    temp_list.append(temp)
    #testfile.write(json.dumps(temp) + '\n')

for k,v in temp_list:
    if '\n\n' in v:
sum([True for d in temp_list if '\n\n' in d['ingredient']])
testfile.close()

[d['ingredient'] for d in temp_list if d['id']==1686427]
[(d['id'],len(d['ingredient'].split('\n\n'))) for d in temp_list if '\n\n' in d['ingredient']]
'''

    
        






