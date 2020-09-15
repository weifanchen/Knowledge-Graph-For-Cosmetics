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

'''
add the ingredients that are fragrance and preservatives on the top of "compound.jl" based on FDA website
https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics
'''

fragrance_list_path = "./output/FDA_fragrance.txt"
fragrance_list= []
with open(fragrance_list_path) as ffile:
    fragrance_list = ffile.read().splitlines() 
    #fragrance_list=ffile.readlines() # will have \n

preservative_list_path = "./output/FDA_preservatives.txt"
preservative_list= []
with open(preservative_list_path) as ffile:
    preservative_list = ffile.read().splitlines() 

compound_path = "./output/compound_0412.jl"
compounds= []
with open(compound_path) as json_file:
    for i,line in enumerate(json_file):
        compounds.append(json.loads(line))

compSet = set()

for c in compounds:
    if c['chem_url'] not in compSet:
        compSet.add(c['chem_url'])

def find_compound(f,fragrances,keyword):
    for compound in compounds:
        for c in compound['synonyms']:
            if f in c:
                compound['safety'].append(keyword)
                fragrances.append({f:compound['chem_id']})
                print(f,' is found in compound.jl',compound['safety'])
                return True
    fragrances.append({f:None})
    return False

def getPubchem(ing,keyword):
    driver.get('https://pubchem.ncbi.nlm.nih.gov')
    time.sleep(1)
    driver.find_element_by_css_selector('div form[role="search"] div div input').send_keys(ing)
    driver.find_element_by_css_selector('button[data-action="search-button"]').click()
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('div#featured-results div')   
        comp = driver.find_element_by_css_selector('div.f-0875 div span a').get_attribute("href")
        if  comp not in compSet:
            compid = comp.split('/')[-1]
            compSet.add(comp)
            driver.get(comp)
            time.sleep(2.5)
            response = BeautifulSoup(driver.page_source, 'html.parser') 
            sysSet = set()
            for r in response.select('section#Synonyms section'): 
                sysSet.update(set([rr.text for rr in r.select('div.columns p')]))

            rows = response.select('div.summary tr')
            formula = ''
            safety = []
            for row in rows:
                if row.select('th') and row.select('th')[0].text == 'Molecular Formula:':
                    formula = row.select('td a span')[0].text     
                if row.select('th') and row.select('th')[0].text == 'Chemical Safety:':    
                    safety = [ s.get('data-caption') for s in row.select('td a p div')]  
                if keyword not in safety:
                    safety.append(keyword)  
            compinfo = {'chem_id': compid, 'chem_url': comp, 'safety': safety, 'formula': formula, 'synonyms':list(sysSet)}            
        else:
            compid, compinfo = comp.split('/')[-1], None
    except:
        compid, compinfo = None, None
        print(';)')
   
    return compid, compinfo

driver = webdriver.Chrome('/Users/weifanchen/chromedriver')

fragrances = list()
for f in fragrance_list:
    result=find_compound(f,fragrances,"Fragrance")
    if not result:
        compid, compinfo = getPubchem(f,'Fragrance')
        if compinfo:
            print(compid,'Fragrance')
            compounds.append(compinfo)
        else:
            print(compid,compinfo)


preservatives = list()
for f in preservative_list:
    result=find_compound(f,preservatives,"Preservatives")
    if not result:
        compid, compinfo = getPubchem(f,'Preservatives')
        if compinfo:
            print(compid,'Preservatives')
            compounds.append(compinfo)
        else:
            print(compid,compinfo)



print(fragrances)
print(preservatives)

compoundsfile = open('./output/compounds.jl', 'a+')

for c in compounds:
    compoundsfile.write(json.dumps(c) + '\n')
    compoundsfile.flush()


driver.close()




'''

count = Counter([i['chem_id'] for i in ingredients])
repeated = [k for k,v in count.items() if v>1]

for r in repeated[:]:
    check_list = []
    for ing in ingredients:
        if ing['chem_id']==r:
            temp = [ing['function'], ing['acne'], ing['irritant'],ing['safety']]
            check_list.append(temp)
    for prev,next in zip(check_list[:-1],check_list[1:]):
        if prev!=next:
            print(r,prev,next)
        else:
            print('same')
'''


    
        