from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import random
import re

'''
tend to deduplicate ingredients 
'''

ingredient_list_path = "./output/ingredients.jl"

ingredient_list = []
with open(ingredient_list_path) as json_file:
    for line in json_file:
        ingredient_list.append(json.loads(line))

log_file = open('./output/ingredients_log_0409.txt',"a+")
ingredientfile = open('./output/ingredients_0409.jl', 'a+')
dict_file = open('./output/dict_0409.txt',"a+")

driver = webdriver.Chrome('/Users/weifanchen/chromedriver')

def add_ingredient_dict(ingredient_dict,synonym_list,ing,ing_id):
    if ing not in ingredient_dict.keys():
        ingredient_dict[ing] = ing_id
        dict_file.write('{}\t{}\n'.format(ing,ing_id))
    for syn in synonym_list:
        if syn not in ingredient_dict.keys():
            ingredient_dict[syn] = ing_id
            dict_file.write('{}\t{}\n'.format(syn,ing_id))


def checkingredient(ingredient):
    driver.get('https://www.cosdna.com/eng/stuff.php')
    time.sleep(1)
    input_box = driver.find_element_by_css_selector('input#q')
    input_box.send_keys(ingredient['name'])
    input_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(1,2))

    try:
        # if multiple results listed, click the first one
        first_result=driver.find_element_by_css_selector('div.flex-grow-1 table.table tbody tr td a.d-block').get_attribute('href')
        driver.get(first_result)
        time.sleep(1)
    except:
        # only one result, directly send to the info page
        pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    soup_name=soup.select('div.h4.text-vampire')[0].text
    soup_synonym=soup.select('div.mb-2')[0].text
    soup_synonym = re.sub('\s+',' ',soup_synonym)
    synonym = [s.strip() for s in soup_synonym.split(', ')]

    if ingredient['name'].lower() !=soup_name.lower() and ingredient['name'] not in synonym:
        # doesn't match
        ingredient['ingredient_id'] = 'nm' + str(abs(hash(ingredient['name'])))
        ingredient['synonym'] = []
        add_ingredient_dict(ingredient_dict,ingredient['synonym'],ingredient['name'],ingredient['ingredient_id'])
        print(ingredient['name'], ingredient['ingredient_id'])
        log_file.write('different title: {} {} {}\n'.format(ingredient['name'],soup_name ,driver.current_url))
        return ingredient
        
    synonym.append(soup_name)
    ingredient['synonym'] = synonym

    if not ingredient['function']:
        soup_function = soup.select('div.linkb1.ls-2.lh-1')[0].text
        soup_function = re.sub('\s+',' ',soup_function)
        function = [s.strip() for s in soup_function.split(';')]
        print('function update: ',ingredient['name'],function)
        ingredient['function'] = function 

    soup_safety=soup.select('div span.safety')
    if not ingredient['safety'] and soup_safety: 
        ingredient['safety'] = soup_safety[0].text 

    match = re.match(r'https://www.cosdna.com/eng/([A-Za-z0-9]+).html',driver.current_url)
    ing_id=match.group(1)
    ingredient['ingredient_id'] = ing_id
    add_ingredient_dict(ingredient_dict,synonym,ingredient['name'],ing_id)


    #print(driver.current_url,ingredient)
    return ingredient
    

def load_ing_dict(ingredient_dict):
    dict_path = "./output/dict_0409.txt"
    with open(dict_path) as txtfile:
        dict_list=txtfile.read().splitlines()
    for dict_line in dict_list:
        temp = dict_line.split('\t')
        ingredient_dict[temp[0]]=temp[1]
    return ingredient_dict

ingredient_dict = dict()
ingredient_dict = load_ing_dict(ingredient_dict)

for ingredient in ingredient_list[:]:
    if ingredient['name'] not in ingredient_dict.keys():
        new_ingredient = checkingredient(ingredient)
        ingredientfile.write(json.dumps(new_ingredient) + '\n')
        ingredientfile.flush()
    else:
        log_file.write('duplication: {} {}\n'.format(ingredient['name'], ingredient_dict[ingredient['name']]))
        log_file.flush()

with open('ingredient_dict.json', 'w') as fp:
    json.dump(ingredient_dict, fp)

driver.quit()
ingredientfile.close()
log_file.close()
fp.close()
