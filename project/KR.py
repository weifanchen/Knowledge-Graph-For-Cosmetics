from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS, XSD, OWL
from datetime import datetime
from datetime import date
import json
import re
# RDF.class or SCHEMA.class

with open('./output/sephora_skincare_product_ingredient_list.jl') as json_products:
    products = [json.loads(line) for line in json_products]

with open('./output/ingredients.jl') as json_ingredients:
    ingredients = [json.loads(line) for line in json_ingredients]

'''
with open('./output/ingredient_dict.json') as json_ingredients:
    ingredients_dict = json.load(json_ingredients)

for p in products:
    p['ingredients_ids'] = []
    for ing in p['ingredient_list']:
        try:
            p['ingredients_ids'].append(ingredients_dict[ing])
        except:
            print("{}   {}".format(p['product_name'],ing))
'''

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
MYNS = Namespace('http://inf558.org/chemcosmetic/')
SCHEMA=Namespace("http://schema.org/")


class productGraph:
    def __init__(self):
        self.my_kg = Graph()
        self.my_kg.bind('myns', MYNS) 
        self.my_kg.bind('foaf', FOAF) 
        self.my_kg.bind('schema', SCHEMA)
        self.category_dict = {}
        self.subcategory_dict = {}
        self.minicategory_dict = {}
        self.brand_dict = {}
        self.func_dict = {}
    
    def load_ttl(self):
        self.my_kg.parse("./output/RDF_compounds.ttl", format="ttl")

    def define_class(self):
        product_id_uri = URIRef(MYNS['product_id']) 
        self.my_kg.add((product_id_uri, RDF.type, RDFS.Class))
        self.my_kg.add((product_id_uri, RDFS.subClassOf, MYNS['skincare_product']))

        product_url_uri = URIRef(MYNS['product_url']) 
        self.my_kg.add((product_url_uri, RDF.type, RDFS.Class))
        self.my_kg.add((product_url_uri, RDFS.subClassOf, MYNS['skincare_product']))

        product_brand_uri = URIRef(MYNS['brand']) 
        self.my_kg.add((product_brand_uri, RDF.type, RDFS.Class))
        #self.my_kg.add((product_brand_uri, RDFS.subClassOf, MYNS['skincare_product']))

        category_uri = URIRef(MYNS['category']) 
        self.my_kg.add((category_uri,RDF.type, RDFS.Class))
        #self.my_kg.add((category_uri,RDFS.subClassOf, MYNS['skincare_product']))

        subcategory_uri = URIRef(MYNS['subcategory']) 
        self.my_kg.add((subcategory_uri,RDF.type, RDFS.Class))
        self.my_kg.add((subcategory_uri,RDFS.subClassOf,MYNS['category']))

        minicategory_uri = URIRef(MYNS['minicategory']) 
        self.my_kg.add((minicategory_uri, RDF.type, RDFS.Class))
        self.my_kg.add((minicategory_uri,RDFS.subClassOf,MYNS['subcategory']))
    
    def define_property(self):
        # # size cost price
        cost_uri = URIRef(MYNS['hasPrice']) 
        self.my_kg.add((cost_uri, RDF.type, RDF.Property))
        self.my_kg.add((cost_uri, RDFS.label,Literal('has price')))
        self.my_kg.add((cost_uri, RDFS.domain, MYNS['size_price_pair']))
        self.my_kg.add((cost_uri, RDFS.range, XSD.double))
        # # price with size
        size_uri = URIRef(MYNS['hasSize']) 
        self.my_kg.add((size_uri, RDF.type, RDF.Property))
        self.my_kg.add((size_uri, RDFS.label,Literal('has size')))
        self.my_kg.add((size_uri, RDFS.domain, MYNS['size_price_pair']))
        self.my_kg.add((size_uri, RDFS.range, XSD.double))

        size_uri = URIRef(MYNS['hasUnit']) 
        self.my_kg.add((size_uri, RDF.type, RDF.Property))
        self.my_kg.add((size_uri, RDFS.label,Literal('has unit')))
        self.my_kg.add((size_uri, RDFS.domain, MYNS['size_price_pair']))
        self.my_kg.add((size_uri, RDFS.range, XSD.string))

        from_product_uri = URIRef(MYNS['fromProduct']) 
        self.my_kg.add((from_product_uri, RDF.type, RDF.Property))
        self.my_kg.add((from_product_uri, RDFS.label,Literal('from product')))
        self.my_kg.add((from_product_uri, RDFS.domain, MYNS['size_price_pair']))
        self.my_kg.add((from_product_uri, RDFS.range, MYNS['skincare_product']))

        has_ingredient_uri = URIRef(MYNS['hasIngredient']) 
        self.my_kg.add((has_ingredient_uri, RDF.type, RDF.Property))
        self.my_kg.add((has_ingredient_uri, RDFS.label,Literal('has ingredient')))
        self.my_kg.add((has_ingredient_uri, RDFS.domain, MYNS['skincare_product']))
        self.my_kg.add((has_ingredient_uri, RDFS.range, MYNS['Compound']))

        
    def declare(self):
        # need to update
        node_uri = URIRef(MYNS['skincare_product']) 
        self.my_kg.add((node_uri, RDF.type, RDFS.Class)) #OWL.ontology
        self.my_kg.add((node_uri,MYNS['product_id'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['product_url'],XSD.string))
        self.my_kg.add((node_uri,MYNS['product_name'],XSD.string))
        self.my_kg.add((node_uri,MYNS['brand'],XSD.string))
        self.my_kg.add((node_uri,MYNS['size_price_pair'],XSD.string))
        #self.my_kg.add((node_uri,MYNS['size'],XSD.string)) #### unify to ml or ?
        #self.my_kg.add((node_uri,MYNS['price'],XSD.double))
        self.my_kg.add((node_uri,MYNS['numOfReviews'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['numOfLoves'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['stars'],XSD.double))
        self.my_kg.add((node_uri,MYNS['category'],XSD.string))
        self.my_kg.add((node_uri,MYNS['subcategory'],XSD.string))
        self.my_kg.add((node_uri,MYNS['minicategory'],XSD.string))
        self.my_kg.add((node_uri,MYNS['ingredient_description'],XSD.string))
        self.my_kg.add((node_uri,MYNS['hasIngredient'],XSD.string))
    

    def add_categories(self,keyword):
        # keyword = 'category', 'subcategory', 'minicategory'
        category_set=set([p[keyword] for p in products])
        cate_dict=dict()
        for c in category_set:
            c_uri = c.replace('&','n').replace(' ','_')
            cate_dict[c] = c_uri
            cate_uri = URIRef(MYNS[c_uri])
            self.my_kg.add((cate_uri,RDF.type,MYNS[keyword]))
            self.my_kg.add((cate_uri,RDFS.label,Literal(c)))

        if keyword=='category': self.category_dict=cate_dict
        elif keyword=='subcategory': self.subcategory_dict=cate_dict
        elif keyword=='minicategory': self.minicategory_dict=cate_dict

    def add_brands(self):
        brand_set=set([p['brand'] for p in products])
        for b in brand_set:
            b_uri = b.replace(' ','_')
            self.brand_dict[b] = b_uri
            brand_uri = URIRef(MYNS[b_uri])
            self.my_kg.add((brand_uri,RDF.type,MYNS['brand']))
            self.my_kg.add((brand_uri,RDFS.label,Literal(b)))

    def string_K_to_int(self,string):
        match=re.match(r"\d+(\.\d+)?[K]",string)
        if match:
            return int(float(string[:-1])*1000)
        else:
            return int(string)

    def add_size_func(self,uri,string):
        match=re.search(r'([0-9\.]+) oz|([0-9\.]+)oz|([0-9\.]+) fl oz',string)
        if match:
            match_list = [match.group(1),match.group(2),match.group(3)]
            match_string = [m for m in match_list if m][0]
            self.my_kg.add((uri, MYNS['hasSize'],Literal(float(match_string))))
            self.my_kg.add((uri, MYNS['hasUnit'], Literal('oz')))
        else:
            match2 = re.match(r'([0-9]+) (.*$)',string)
            if match2:
                self.my_kg.add((uri, MYNS['hasSize'],Literal(float(match2.group(1)))))
                self.my_kg.add((uri, MYNS['hasUnit'], Literal(match2.group(2))))
            else:
                self.my_kg.add((uri, MYNS['hasSize'], Literal(string)))

    # def extract_size(self,string):
    #     match=re.search(r'([0-9\.]+)oz| oz| fl oz',string)
    #     match=re.search(r'([0-9]+) (.*$)',string)
    #     if match:
    #         #return float(match.group(1)) #oz
    #     else:
    #         return string
 

    def extract_price(self,string):
        match=re.search(r'\$([0-9\.]+)',string)
        if match:
            return float(match.group(1))
        else:
            pass
            #print('price not match    ',string)

    def extract_star(self,string):
        if string=='No':
            return None
        else:
            return float(string)


    def add_product(self,p):
        product_uri = URIRef(MYNS['p_'+str(p['product_id'])])
        self.my_kg.add((product_uri,RDF.type, MYNS['skincare_product']))
        self.my_kg.add((product_uri,MYNS['product_id'], Literal(p['product_id'])))
        self.my_kg.add((product_uri,MYNS['product_name'], Literal(p['product_name'])))
        self.my_kg.add((product_uri,MYNS['product_url'], Literal(p['url'])))
        self.my_kg.add((product_uri,MYNS['brand'], MYNS[self.brand_dict[p['brand']]]))
        self.my_kg.add((product_uri,MYNS['stars'], Literal(self.extract_star(p['stars']))))
        self.my_kg.add((product_uri,MYNS['numOfLoves'], Literal(self.string_K_to_int(p['loves']))))
        self.my_kg.add((product_uri,MYNS['numOfReviews'], Literal(self.string_K_to_int(p['reviews']))))
        self.my_kg.add((product_uri,MYNS['category'], MYNS[self.category_dict[p['category']]]))
        self.my_kg.add((product_uri,MYNS['subcategory'], MYNS[self.subcategory_dict[p['subcategory']]]))
        self.my_kg.add((product_uri,MYNS['minicategory'], MYNS[self.minicategory_dict[p['minicategory']]]))
        self.my_kg.add((product_uri,MYNS['ingredient_description'],Literal(p['ingredients'])))
        for ing_id in p['ingredients_ids']:
            self.my_kg.add((product_uri,MYNS['hasIngredient'],MYNS['chem'+ing_id]))
        # add size and price
        if len(p['prices'])==len(p['sizes']) and len(p['prices'])>0: 
            for i in range(len(p['prices'])):
                each_size_uri = URIRef(MYNS['ssp_'+str(p['product_id'])+'_'+str(i)])
                self.my_kg.add((product_uri, MYNS['size_price_pair'], each_size_uri))
                self.my_kg.add((each_size_uri, MYNS['hasPrice'], Literal(self.extract_price(p['prices'][i]))))
                self.add_size_func(each_size_uri,p['sizes'][i])
                #self.my_kg.add((each_size_uri, MYNS['hasSize'], Literal(self.extract_size(p['sizes'][i]))))
                self.my_kg.add((each_size_uri, MYNS['fromProduct'], product_uri))
        # elif len(p['prices'])==0:
        #     print('empty price/size ' ,p['product_id'])
        # else:
        #     print('price and size does not match' ,p['product_id'])


graph = productGraph()
graph.load_ttl()
graph.define_class()
graph.define_property()
graph.add_brands()
graph.add_categories('category')
graph.add_categories('subcategory')
graph.add_categories('minicategory')
# graph.print()
# graph.declare()

for p in products[:]:
    #print(p['url'])
    graph.add_product(p)
graph.my_kg.serialize("./output/RDF_full.ttl", format="turtle")


'''
{"name": "Propylene Glycol Dipelargonate", "function": ["Viscosity Control"], "acne": [2], "irritant": [2], "safety": [1], "ingredient_id": "db8a651199", "synonym": ["PG Dipelargonate"]}

product = {"url": "https://www.sephora.com/product/original-skin-retexturizing-mask-with-rose-clay-P397890?icid2=products%20grid:p397890", 
"product_id": 2175396, 
"product_name": "Original Skin\u2122 Retexturizing Mask with Rose Clay", 
"brand": "Origins", 
"sizes": ["2.5 oz/ 75 mL", "1 oz/ 30 mL"], 
"prices": ["$26.00", "$13.00"], 
"loves": "77.6K", 
"reviews": "1K", 
"stars": "4.5", 
"ingredients": "", 
"category": "Skincare", 
"subcategory": "Masks", 
"minicategory": "Face Masks", 
"ingredient_list": ["Water", "Butylene Glycol", "Kaolin", "Montmorillonite", "Polysorbate 20", "Jojoba esters", "PEG-100 Stearate", "Bentonite", "Glycerin", "Citrus Grandis Peel Oil", "Lavandula Angustifolia Oil", "Pelargonium Graveolens Flower Oil", "Amyris Balsamifera Bark Oil", "Salvia Sclarea Oil", "Anthemis Nobilis Flower Oil", "Rosa Centifolia Flower Extract", "Limonene", "Linalool", "Geraniol", "Epilobium Angustifolium Flower/Leaf/Stem Extract", "Castanea Sativa Seed Extract", "Albizia Julibrissin Bark Extract", "Lecithin", "Ethylhexylglycerin", "Caprylyl Glycol", "Propylene glycol laurate", "Propylene glycol stearate", "PEG 150 Distearate", "Hypnea Musciformis Extract", "Algae Extract", "Simethicone", "Sodium Hyaluronate", "Sorbitan laurate", "Hexylene Glycol", "Dehydroacetic Acid", "Xanthan Gum", "Trisodium EDTA", "Phenoxyethanol", "Titanium Dioxide", "Iron Oxides (CI 77491, CI 77492, CI 77499)"]}
'''

'''
with open('./sephora/output/compound.jl') as json_compound:
    compounds_old = [json.loads(line) for line in json_compound]

with open('ingredients.jl') as json_ingredients:
    ingredients = [json.loads(line) for line in json_ingredients]


result = []
for ing in ingredients:
    if ing['chem_id'] is None:
        for com in compounds:
            if set(ing['synonym']).intersection(set(com['synonyms'])):
                ing['chem_id'] = com['chem_id']
                result.append(com['chem_id'])
                #print(com['chem_id'],ing['name'])

len([ing for ing in ingredients if ing['chem_id'] is not None]) # 1134[]
# after running intersection between ingredient's synonym and compound's synonyms
len([ing for ing in ingredients if ing['chem_id'] is not None]) # 1191[]

set([com['chem_id'] for com in compounds]).intersection(set([com['chem_id'] for com in compounds_old]))

count = 0
for com in compounds:
    if 'Fragrance' in com['safety']:
        print(com['chem_id'])
        count+=1
'''