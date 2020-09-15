import json
from collections import Counter

with open('./sephora/output/ingredients_0411.jl') as json_ingredients:
    ingredients = [json.loads(line) for line in json_ingredients]

count = Counter([i for ing in ingredients for i in ing['function']])
len(count.keys())

sum([1 for ing in ingredients if len(ing['synonym'])==0]) # 355
sum([1 for ing in ingredients if len(ing['synonym'])==1 and ing['name'] in ing['synonym']]) # 2690
sum([1 for ing in ingredients if ing['name'] in ing['synonym']]) # 3802

for ing in ingredients:
    if len(ing['synonym'])==0:
        ing['synonym'].append(ing['name'])

for ing in ingredients:
    if '' in ing['synonym']:
        ing['synonym'].remove('')

for ing in ingredients:
    print(ing['synonym'])
    for i in range(len(ing['function'])):
        if ing['function'][i]=='skin protecting':
            ing['function'][i]='Skin Protecting'

remove_keyword('Hair and Skin conditioning',replacement)
remove_keyword('Skin and hair conditioning',replacement)
remove_keyword('Cleansing',['Cleaning agent'])
remove_keyword('Cleansing',['Binding agent'])

replacement=['Skin Conditioning','Hair Conditioning']
def remove_keyword(keyword,replacement):
    for ing in ingredients:
        if keyword in ing['function']:
            ing['function'].remove(keyword)
            for repla in replacement:
                ing['function'].append(repla)

hey = 'Bulking Agent'

big_small_case(hey.lower(),hey)
def big_small_case(keyword,replacement):
    for ing in ingredients:
        for i in ing['function']:
            if i.lower()==keyword:
                ing['function'].remove(i)
                ing['function'].append(replacement)

for c in count.keys():
    if c.lower()=='hair conditioning':
        print(c)

sum([1 for ing in ingredients if 'Hair and Skin conditioning' in ing['function']])

tot = [i for ing in ingredients for i in ing['function'] if i=='']


'''
ingredientfile = open('./sephora/output/ingredients_0411_5.jl', 'a+')

for ingredient in ingredients:
        ingredientfile.write(json.dumps(ingredient) + '\n')
        ingredientfile.flush()
ingredientfile.close()
'''
sum([ing['function']==[''] for ing in ingredients for fun in ing['function']])
