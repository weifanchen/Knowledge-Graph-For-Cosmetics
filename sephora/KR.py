from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS, XSD, OWL
from datetime import datetime
from datetime import date
import json
import re

# RDF.class or SCHEMA.class

with open('./output/sephora_skincare_product_ingredient_list.jl') as json_product:
    products = [json.loads(line) for line in json_product]

# with open('./output/sephora_skincare_review.jl') as json_review:
#     review = [json.loads(line) for line in json_review

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
MYNS = Namespace('http://inf558.org/chemcosmetic/')
SCHEMA=Namespace("http://schema.org/")



class productGraph:
    def __init__(self):
        self.my_kg = Graph()
        self.my_kg.bind('my_ns', MYNS) 
        self.my_kg.bind('foaf', FOAF) 
        self.my_kg.bind('schema', SCHEMA)
        self.category_dict = {}
        self.subcategory_dict = {}
        self.minicategory_dict = {}
    
    def define_class(self):
        product_id_uri = URIRef(MYNS['product_id']) 
        self.my_kg.add((product_id_uri, RDF.type, RDFS.Class))
        self.my_kg.add((product_id_uri, RDFS.subClassOf, MYNS['skincare_product']))

        product_url_uri = URIRef(MYNS['product_url']) 
        self.my_kg.add((product_url_uri, RDF.type, RDFS.Class))
        self.my_kg.add((product_url_uri, RDFS.subClassOf, MYNS['skincare_product']))

        #product
    
    def define_category(self):
        category_uri = URIRef(MYNS['category']) 
        self.my_kg.add((category_uri,RDF.type, RDFS.Class))
        self.my_kg.add((category_uri,RDFS.subClassOf, MYNS['skincare_product']))

        subcategory_uri = URIRef(MYNS['subcategory']) 
        self.my_kg.add((subcategory_uri,RDF.type, RDFS.Class))
        self.my_kg.add((subcategory_uri,RDFS.subClassOf,MYNS['category']))

        minicategory_uri = URIRef(MYNS['minicategory']) 
        self.my_kg.add((minicategory_uri, RDF.type, RDFS.Class))
        self.my_kg.add((minicategory_uri,RDFS.subClassOf,MYNS['subcategory']))
    
    def define_property(self):
        # size cost price
        cost_uri = URIRef(MYNS['has_price']) 
        self.my_kg.add((cost_uri, RDF.type, RDF.Property))
        self.my_kg.add((cost_uri, RDFS.label,Literal('has_price')))
        self.my_kg.add((cost_uri, RDFS.domain, MYNS['size']))
        self.my_kg.add((cost_uri, RDFS.range, MYNS['price']))
        # price with size
        size_uri = URIRef(MYNS['has_size']) 
        self.my_kg.add((size_uri, RDF.type, RDF.Property))
        self.my_kg.add((size_uri, RDFS.label,Literal('has_size')))
        self.my_kg.add((size_uri, RDFS.domain, MYNS['price']))
        self.my_kg.add((size_uri, RDFS.range, MYNS['size']))


        
    def declare(self):
        node_uri = URIRef(MYNS['skincare_product']) 
        self.my_kg.add((node_uri, RDF.type, RDFS.Class)) #OWL.ontology
        self.my_kg.add((node_uri,MYNS['product_id'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['product_url'],XSD.string))
        self.my_kg.add((node_uri,MYNS['product_name'],XSD.string))
        self.my_kg.add((node_uri,MYNS['brand'],XSD.string))
        self.my_kg.add((node_uri,MYNS['size_price_pair'],XSD.string))
        self.my_kg.add((node_uri,MYNS['size'],XSD.string)) #### unify to ml or ?
        self.my_kg.add((node_uri,MYNS['price'],XSD.double))
        self.my_kg.add((node_uri,MYNS['numOfReviews'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['numOfLoves'],XSD.integer))
        self.my_kg.add((node_uri,MYNS['stars'],XSD.double))
        self.my_kg.add((node_uri,MYNS['category'],XSD.string))
        self.my_kg.add((node_uri,MYNS['subcategory'],XSD.string))
        self.my_kg.add((node_uri,MYNS['minicategory'],XSD.string))
        self.my_kg.add((node_uri,MYNS['ingredient_description'],XSD.string))
        self.my_kg.add((node_uri,MYNS['ingredient'],XSD.string))

    

    def generate_category_items(self,keyword):
        # keyword = 'category', 'subcategory', 'minicategory'
        category_set=set([p[keyword] for p in products])
        cate_dict=dict()
        for c in category_set:
            c_uri = c.replace('&','n').replace(' ','_')
            cate_dict[c] = c_uri
            cate_uri = URIRef(c_uri)
            self.my_kg.add((cate_uri,RDF.type,MYNS[keyword]))
            self.my_kg.add((cate_uri,RDFS.label,Literal(c)))
        if keyword=='category': self.category_dict=cate_dict
        elif keyword=='subcategory': self.subcategory_dict=cate_dict
        elif keyword=='minicategory': self.minicategory_dict=cate_dict
    
    def string_K_to_int(self,string):
        match=re.match(r"\d+(\.\d+)?[K]",string)
        if match:
            return int(float(string[:-1])*1000)
        else:
            return int(string)

    def extract_size(self,string):
        match=re.search(r'([0-9\.]+) oz',string)
        if match:
            return float(match.group(1)) #oz
        else:
            return string
            #print(string)

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
        product_uri = URIRef('p_'+str(p['product_id']))
        self.my_kg.add((product_uri,RDF.type, MYNS['skincare_product']))
        self.my_kg.add((product_uri,MYNS['product_id'], Literal(p['product_id'])))
        self.my_kg.add((product_uri,MYNS['product_name'], Literal(p['product_name'])))
        self.my_kg.add((product_uri,MYNS['product_url'], Literal(p['url'])))
        self.my_kg.add((product_uri,MYNS['brand'], Literal(p['brand'])))
        self.my_kg.add((product_uri,MYNS['stars'], Literal(self.extract_star(p['stars']))))
        self.my_kg.add((product_uri,MYNS['numOfLoves'], Literal(self.string_K_to_int(p['loves']))))
        self.my_kg.add((product_uri,MYNS['numOfReviews'], Literal(self.string_K_to_int(p['reviews']))))
        self.my_kg.add((product_uri,MYNS['category'], MYNS[self.category_dict[p['category']]]))
        self.my_kg.add((product_uri,MYNS['subcategory'], MYNS[self.subcategory_dict[p['subcategory']]]))
        self.my_kg.add((product_uri,MYNS['minicategory'], MYNS[self.minicategory_dict[p['minicategory']]]))
        # add size and price
        if len(p['prices'])==len(p['sizes']) and len(p['prices'])>0: 
            for i in range(len(p['prices'])):
                self.my_kg.add((product_uri, MYNS['price'], Literal(self.extract_price(p['prices'][i]))))
                self.my_kg.add((product_uri, MYNS['sizes'], Literal(self.extract_size(p['sizes'][i]))))
        elif len(p['prices'])==0:
            print('empty price/size ' ,p['product_id'])
        else:
            print('price and size does not match' ,p['product_id'])


graph = productGraph()
graph.define_class()
graph.define_property()
graph.define_category()
graph.declare()
graph.generate_category_items('category')
graph.generate_category_items('subcategory')
graph.generate_category_items('minicategory')

for p in products[:]:
    #print(p['url'])
    graph.add_product(p)
graph.my_kg.serialize("qqqq.ttl", format="turtle")

'''
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







