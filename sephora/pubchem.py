from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import string
import json
import pandas as pd

driver = webdriver.Chrome('./chromedriver')

compSet = set()

def getPubchem(ing):
    driver.get('https://pubchem.ncbi.nlm.nih.gov')
    time.sleep(1)
    # typeBox = driver.find_element_by_css_selector('div form[role="search"] div div input')
    driver.find_element_by_css_selector('div form[role="search"] div div input').send_keys(ing)
    driver.find_element_by_css_selector('button[data-action="search-button"]').click()
    time.sleep(2)

    try:
        driver.find_element_by_css_selector('div#featured-results div')   
        comp = driver.find_element_by_css_selector('div.f-0875 div span a').get_attribute("href")
        compid, compinfo = comp.split('/')[-1], None 
        # if comp not in compSet:
        #     compid = comp.split('/')[-1]
        #     compSet.add(comp)
        #     driver.get(comp)
        #     time.sleep(2.5)
        #     response = BeautifulSoup(driver.page_source, 'html.parser') 
        #     sysSet = set()
        #     for r in response.select('section#Synonyms section'): 
        #         sysSet.update(set([rr.text for rr in r.select('div.columns p')]))

        #     rows = response.select('div.summary tr')
        #     formula = ''
        #     safety = []
        #     for row in rows:
        #         if row.select('th') and row.select('th')[0].text == 'Molecular Formula:':
        #            formula = row.select('td a span')[0].text     
        #         if row.select('th') and row.select('th')[0].text == 'Chemical Safety:':    
        #            safety = [ s.get('data-caption') for s in row.select('td a p div')]    
        #     compinfo = {'chem_id': compid, 'chem_url': comp, 'safety': safety, 'formula': formula, 'synonyms':list(sysSet)}            
        # else:
        #     compid, compinfo = comp.split('/')[-1], None
   
    except:
        compid, compinfo = None, None
        print(';)')
    
    return compid, compinfo
    

ingredients = pd.read_json('ingredients.jl', lines=True)
compfile = open('compound2.jl', 'a')

compids = []
# enumerate(ingredients.name)
for i, ing in enumerate(ingredients.name[1065:]):
    print(i+1065, ing)
    compid, compinfo = getPubchem(ing)
    # if compinfo:
    #     compfile.write(json.dumps(compinfo) + '\n')
    #     compfile.flush()
    compids.append(compid)
    # print(compids)

import numpy as np
ingredients['chem_id'] = np.asarray(compids)

compfile.close()
driver.close()

ingredients.to_json('ingredients.jl', orient="records", lines=True)







#     driver.find_element_by_css_selector('div form[role="search"] div div input').clear()
#     driver.find_element_by_css_selector('div form[role="search"] div div input').send_keys(ing)

#     driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", typeBox, "value", "aqua")



#     "arguments[0].value = '2,1';"
#     driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[1]);", typeinBox, 'value', ing)
    
#     .send_keys(ing)
#     driver.find_element_by_css_selector('button[data-action="search-button"]').click()

#     typeinBox.submit() 
#     text=ingredient_preprocessing(product['ingredients'])
#     ingredients_list_box.send_keys(text)
#     ingredients_list_box.submit() 
#     time.sleep(random.randint(2,4))

# ingredients = pd.read_json('ingredients.jl', lines=True)

# seen = []

# for ing in ingredients.name: print(ing)
#     getPubchem(ing)