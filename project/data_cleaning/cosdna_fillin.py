from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import random
import re

'''
# examination
len(set([p['product_id'] for p in product_org]))
len([p['ingredients']=='' for p in product_org])
len([p for p in product_list if p['ingredients']==''])
for i in product_org:
    if i['product_id']==id_dup[-1]:
        print(i)

product_list
'''
[p['product_name'] for p in product_list_new if p['ingredient_list']==[]]
len([p['product_name'] for p in product_list if p['ingredients']==''])

product_list_path = "./sephora/output/sephora_skincare_product_6_updated3.jl"
product_list_new= []
with open(product_list_path) as json_file:
    for i,line in enumerate(json_file):
        product_list_new.append(json.loads(line))

product_list_path = "./sephora/output/sephora_skincare_product_ingredient_list.jl"
product_list= []
with open(product_list_path) as json_file:
    for i,line in enumerate(json_file):
        product_list.append(json.loads(line))

product_list_path = "./sephora/output/sephora_skincare_product_6.jl"
product_org_tt= []
with open(product_list_path) as json_file:
    for i,line in enumerate(json_file):
        #print(i)
        product_org_tt.append(json.loads(line))

pl3 = [p['ingredients'] for p in product_list3 if p['ingredient_list']==[]]
pl = [p['product_id'] for p in product_list]
pl_wo = [p['product_id'] for p in product_list_wo]

set(pl)-set(pl_wo)-set(pl3)


'''
useless_paragraph = 'Please be aware that ingredient lists may change or vary from time to time. Please refer to the ingredient list on the product package you receive for the most up to date list of ingredients.'
useless_paragraph = 'Please be aware that ingredient lists may change or vary from time to time.\ufffd Please refer to the ingredient list on the product package you receive for the most up to date list of ingredients.'
useless_paragraph = 'Please be aware that ingredient lists may change or vary from time to time. Please refer to the ingredient list on the product package you receive for the most up-to-date list of ingredients.'
useless_paragraph = 'Please be aware that ingredient lists may change or vary from time to time.'
useless_paragraph = '*'
len([p['product_id'] for p in product_list if useless_paragraph in p['ingredients']])
for p in product_list:
    if useless_paragraph in p['ingredients']:
        p['ingredients'] = p['ingredients'].replace(useless_paragraph,'')
    

productfile = open('sephora_skincare_product_revised.jl', 'w')

for p in product_list:
    productfile.write(json.dumps(p) + '\n')
    productfile.flush()

len([p['ingredients'].split('\n\n')[2] for p in product_list if len(p['ingredients'].split('\n\n'))>2])

for p in product_list 

'''


ingredient_profile_path = './output/ingredients.jl'
ingredient_profile = []
with open(ingredient_profile_path) as f:
    for line in f:
        ingredient_profile.append(json.loads(line))

product_wo_ingredient_path = './sephora/output/product_wo_ingredient.jl'
product_wo_ingredient = []
with open(product_wo_ingredient_path) as f:
    for line in f:
        product_wo_ingredient.append(json.loads(line))
productfile = open('./output/sephora_skincare_product_3.jl', 'a+')
ingredientfile = open('./output/ingredients.jl', 'a+')

driver = webdriver.Chrome('/Users/weifanchen/chromedriver')

for p in product_wo_ingredient:
    driver.get('https://www.cosdna.com/eng/product.php')
    product_name_box = driver.find_element_by_css_selector('input.form-control')
    name = p['brand']+ ' '+p['product_name']
    product_name_box.send_keys(name)
    product_name_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(2,4))
    try:
        sort_latest = driver.find_element_by_css_selector('div.sort a:first-of-type') #CLICK THE FIRST ONE
        sort_latest.click()
        first_product = driver.find_element_by_css_selector('table.table.table-hover tbody tr td.pl-0 a:first-of-type') # click 
        first_product.click()

        element = driver.find_element_by_css_selector('table.table.table-hover.border')
        html = driver.execute_script("return arguments[0].outerHTML;", element)
        soup = BeautifulSoup(html, 'html.parser')
        print(name)
    except:
        print('no result: ',name)

driver.quit()

ingredientfile.close()
productfile.close()


product_list_path = "./sephora/output/ingredients_1.jl"
ingredients= []
with open(product_list_path) as json_file:
    for i,line in enumerate(json_file):
        #print(i)
        ingredients.append(json.loads(line))

new_list = []

for i in ingredients:
    if i not in new_list:
        new_list.append(i)

productfile = open('./sephora/output/ingredient_3896.jl', 'a+')

for p in new_list:
    productfile.write(json.dumps(p) + '\n')
    productfile.flush()


product_list_path = "./sephora/output/sephora_skincare_product_ingredient_list.jl"
product_list= []
with open(product_list_path) as json_file:
    for i,line in enumerate(json_file):
        product_list.append(json.loads(line))

ing_dict = dict()
for ing in new_list:
    ing_dict[ing['name']] = ing['ingredient_id']
    if ing['synonym']:
        for syn in ing['synonym']:
            ing_dict[syn] = ing['ingredient_id']

for ing in new_list:


for p in products[:100]:
    p['ingredient_ids'] = []
    for ping in p['ingredient_list']:
        try:
            p['ingredient_ids'].append(ing_dict[ping])
        except:
            print(ping)


for p in products:
    temp = p['ingredient_list']
    if len(temp) != len(set(temp)):
        print(len(temp),len(set(temp)),p['product_name'],len([k for k,v in Counter(temp).items() if v==1]))
        p['ingredient_list'] = list(Counter(temp).keys())

for p in products:
    #p['ingredient_ids'] =[]
    for ing in p['ingredient_list']:
        if ing not in 
        #p['ingredient_ids'].append(ingredients_dict[ing])
[ing  for p in products for ing in p['ingredient_list'] if ing not in ingredients_dict.keys()]