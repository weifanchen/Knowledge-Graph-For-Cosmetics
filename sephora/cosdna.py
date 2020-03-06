from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time


driver = webdriver.Chrome(executable_path="./chromedriver")

driver.get('http://www.cosdna.com/eng/ingredients.php')

example = list()
example.append("-Papaya, Pineapple, and Pumpkin Enzymes: Naturally enhance skin exfoliation without overdrying. -Lactic Acid, Salicylic Acid, and Silica: Lactic and salicylic acid provide chemical exfoliation while natural ingredient silica works to physically exfoliate dead skin cells from the surface. -Aloe Vera, Honey, and Vitamin E: Help smooth and soften skin. Aqua/Water/Eau, Lactic Acid, Silica, Glycine Soja (Soybean) Oil, Pectin, Cetearyl Alcohol, Carica Papaya (Papaya) Fruit, Ceteareth-20, Cetyl Alcohol, Phenoxyethanol, Dehydroxanthan Gum, Glyceryl Stearate, PEG-100 Stearate, Salicylic Acid, Lactobacillus/Pumpkin Ferment Extract, Alcohol Denat., Sorbic Acid, Cinnamal, Mel/Honey/Miel, Citrus Aurantium Bergamia (Bergamot) Fruit Oil, Eugenol, Potassium Sorbate, Limonene, Linalool, Lavandula Angustifolia (Lavender) Oil, Beta-Carotene, Aloe Barbadensis Leaf Juice Powder, Bromelain, Papain, Retinyl Palmitate, Tocopheryl Acetate, Cinnamomum Cassia Leaf Oil, Acetic Acid, Pogostemon Cablin Oil, Pelargonium Graveolens Flower Oil, Aniba Rosaeodora (Rosewood) Wood Extract, Citrus Aurantium Dulcis (Orange) Peel Oil, CI 75810 (Chlorophyllin-Copper Complex).")
# https://www.sephora.com/product/exfolikate-intensive-exfoliating-treatment-P232915?icid2=bestsellerskincare_us_skugrid_ufe:p425877:product

# <textarea class="form-control mb-3" rows="10" name="q" placeholder="Ingredients List" autofocus="" required=""></textarea>
ingredients_list_box = driver.find_element_by_css_selector('textarea.form-control')
ingredients_list_box.send_keys(example[0])
ingredients_list_box.submit() 

# wait !
element = driver.find_element_by_css_selector('table.table.table-hover.border')
html = driver.execute_script("return arguments[0].outerHTML;", element)
soup = BeautifulSoup(html, 'html.parser')

def temp(column,keyword,ingredient_info):
    if column==['']:
        ingredient_info[keyword]=None
    elif len(column)==1:
        ingredient_info[keyword]=[int(column[0])]
    else:
        ingredient_info[keyword]=list(range(int(column[0]),int(column[1])+1))

'''
FORMAT
{'name': string, 'function': list, 'acne': None/int, 'irritant': None/list, 'safety': None/list}, 
**** change acne to list as well?
{'name': 'Linalool', 'function': ['Fragrance'], 'acne': None, 'irritant': None, 'safety': [5]}, 
{'name': 'Lavandula Angustifolia Oil', 'function': ['Fragrance', 'Emollient', 'Plant extract'], 'acne': None, 'irritant': None, 'safety': [1]}
'''


ingredients = soup.find_all(lambda x: ('tr-i' in x.attrs.get('class',[]) and 'none' not in x.attrs.get('class',[])))
ingredient_info_list = list()
for ingredient in ingredients:
    columns = ingredient.select('td')
    ingredient_info = {}
    ingredient_info['name'] = columns[0].select("a div span")[0].text.strip()
    function = [i.strip() for i in columns[1].text.split(',')]
    acne = columns[2].text.strip()
    irritant = columns[3].text.strip().split('-')
    ingredient_info['function']=function if function!=[''] else None
    ingredient_info['acne']=int(acne) if acne!='' else None
    # ingredient_info['irritant']=int(irritant) if 
    #     ingredient_info['irritant']=int(irritant) if irritant!='' else None
    # except ValueError:
    #     ingredient_info['irritant']
    temp(irritant,'irritant',ingredient_info)
    pre_safety = columns[4].select('a')[0]
    if pre_safety.find('span'):
        safety=[i.text for i in pre_safety.select('span')]
        temp(safety,'safety',ingredient_info)
        # if len(safety)==1:
        #     ingredient_info['safety']=[int(safety[0])]
        # else:
        #     ingredient_info['safety']=list(range(int(safety[0]),int(safety[1])+1))
    else:
        ingredient_info['safety'] = None
    ingredient_info_list.append(ingredient_info)

    
        






driver.quit()