from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import random
import re


'''
tending to deduplicate ingredients 
'''

ingredient_list_path = "./output/ingredients.jl"
#product_list_path = "./output/ingredients_with_chemid.jl"

ingredient_list = []
with open(ingredient_list_path) as json_file:
    for line in json_file:
        ingredient_list.append(json.loads(line))

log_file = open('./output/ingredients_log2.txt',"a+")
ingredientfile = open('./output/ingredients_new2.jl', 'a+')

driver = webdriver.Chrome('/Users/weifanchen/chromedriver')

def add_ingredient_dict(ingredient_dict,synonym_list,ing,ing_id):
    if ing not in ingredient_dict.keys():
        ingredient_dict[ing] = ing_id
    for syn in synonym_list:
        if syn not in ingredient_dict.keys():
            ingredient_dict[syn] = ing_id


def checkingredient(ingredient):
    driver.get('https://www.cosdna.com/eng/stuff.php')
    time.sleep(1)
    input_box = driver.find_element_by_css_selector('input#q')
    # ing = 'Bacillus/Soybean/Folic Acid Ferment Extract'
    # ing = 'Titanium Dioxide Titanium(IV) Oxide'
    ing = ingredient['name']
    input_box.send_keys(ing)
    input_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(1,3))

    try:
        # if multiple results listed, click the first one
        first_result=driver.find_element_by_css_selector('div.flex-grow-1 table.table tbody tr td a.d-block').get_attribute('href')
        driver.get(first_result)
        time.sleep(1)
    except:
        # only one result, directly send to the info page
        pass

    match = re.match(r'https://www.cosdna.com/eng/([A-Za-z0-9]+).html',driver.current_url)
    ing_id=match.group(1)
    ingredient['ingredient_id'] = ing_id
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    soup_name=soup.select('div.h4.text-vampire')[0].text
    if soup_name !=ingredient['name']:
        log_file.write('different title: {} {} {}\n'.format(ingredient['name'],soup_name ,driver.current_url))
        ingredient['name'] = soup_name

    soup_synonym=soup.select('div.mb-2')[0].text
    soup_synonym = re.sub('\s+',' ',soup_synonym)
    synonym = [s.strip() for s in soup_synonym.split(', ')]
    ingredient['synonym'] = synonym
    add_ingredient_dict(ingredient_dict,synonym,ing,ing_id)

    if not ingredient['function']:
        soup_function = soup.select('div.linkb1.ls-2.lh-1')[0].text
        soup_function = re.sub('\s+',' ',soup_function)
        function = [s.strip() for s in soup_function.split(';')]
        ingredient['function'] = function 

    soup_safety=soup.select('div span.safety')
    if not ingredient['safety'] and soup_safety: 
        ingredient['safety'] = soup_safety[0].text 

    #print(driver.current_url,ingredient)
    return ingredient
    

ingredient_dict = dict()
for ingredient in ingredient_list[:]:
    if ingredient['name'] not in ingredient_dict.keys():
        new_ingredient = checkingredient(ingredient)
        ingredientfile.write(json.dumps(new_ingredient) + '\n')
    else:
        log_file.write('duplication: {} {}\n'.format(ingredient['name'], ingredient_dict[ingredient['name']]))
    
    

driver.quit()
ingredientfile.close()
log_file.close()