import rltk
import json

tokenizer = rltk.CrfTokenizer()

class Product(rltk.Record):
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return str(self.raw_object['product_id'])
    
    @rltk.cached_property
    def name_tokens(self):
        return set(tokenizer.tokenize(self.name_string.lower()))

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['product_name']
    
    @rltk.cached_property
    def brand(self):
        return set(self.raw_object['brand'])

    @rltk.cached_property
    def ingredients(self):
        return set(self.raw_object['ingredients_ids'])


product_file = './output/sephora_skincare_product_ingredient_list.jl' 
with open(product_file) as json_products:
    products = [json.loads(line) for line in json_products]

ds_products = rltk.Dataset(reader=rltk.JsonLinesReader(product_file), record_class=Product, adapter=rltk.MemoryKeyValueAdapter())
df_products = ds_products.generate_dataframe()

def name_token_similarity(prod1, prod2): 
    '''set'''
    set1 = prod1.name_tokens
    set2 = prod2.name_tokens
    return rltk.dice_similarity(set1, set2)

def name_string_similarity(prod1, prod2):
    s1 = prod1.name_string
    s2 = prod2.name_string
    return rltk.jaro_winkler_similarity(s1, s2)

def brand_similarity(prod1, prod2):
    s1 = prod1.brand
    s2 = prod2.brand
    return 1 if s1==s2 else 0
    #return rltk.jaro_winkler_similarity(s1, s2)
def ingredient_set(prod1,prod2):
    set1 = prod1.ingredients
    set2 = prod2.ingredients
    return rltk.jaccard_index_similarity(set1,set2) 

def include_keyword(prod1,prod2):
    keywords = ['mini','refill']
    for keyword in keywords:
        if keyword in prod1.name_tokens or keyword in prod2.name_tokens:
            return 1
    return 0

def rule_based_method(prod1, prod2):
    score_1 = name_string_similarity(prod1, prod2)   # string
    score_2 = name_token_similarity(prod1, prod2)
    score_3 = brand_similarity(prod1, prod2)
    score_4 = ingredient_set(prod1, prod2)
    score_5 = include_keyword(prod1,prod2)
    weight1, weight2, weight3, weight4, weight5 =0.3, 0.3, 0, 0.4, 0.1
    if score_3==0:
        return 0
    else:
        return score_1*weight1 + score_2*weight2 + score_4*weight4

result = []
for i,p in enumerate(products):
    for j in range(i+1,len(products)):
        prod1 = ds_products.get_record(str(products[i]['product_id']))
        prod2 = ds_products.get_record(str(products[j]['product_id']))
        result = rule_based_method(prod1, prod2)
        if result>0.8:
            print(result,products[i]['product_name'],'/',products[j]['product_name'])

