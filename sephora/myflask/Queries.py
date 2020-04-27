from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re
from collections import defaultdict


sparql = SPARQLWrapper("http://localhost:3030/ds/query")


prefixes ="""
        prefix foaf: <http://xmlns.com/foaf/0.1/> 
        prefix myns: <http://inf558.org/chemcosmetic/> 
        prefix ns1: <http://www.w3.org/2002/07/owl#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix schema: <https://schema.org/> 
        prefix xml: <http://www.w3.org/XML/1998/namespace> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

        """
def ResultFormat_basic(results,pid):
    ans = dict()
    if results['results']['bindings']:
        ans['product_id'] = pid
        ans['product_name'] = results['results']['bindings'][0]['name']['value']
        ans['brand'] = results['results']['bindings'][0]['brand']['value']
        ans['category'] = results['results']['bindings'][0]['category']['value']
        ans['subcategory'] = results['results']['bindings'][0]['subcategory']['value']
        ans['minicategory'] = results['results']['bindings'][0]['minicategory']['value']
        ans['size'] = float(results['results']['bindings'][0]['minsize']['value'])
        ans['price'] = float(results['results']['bindings'][0]['minPrice']['value'])
        ing_list = []
        for r in results['results']['bindings']:
            ing_dict=defaultdict(lambda: None)
            ing_dict['name'] = r['ingredient_name']['value']
            ing_dict['acne'] = r['acne_index']['value'] if 'acne_index' in r.keys() else None
            ing_dict['irritant'] = r['irritant_index']['value'] if 'irritant_index' in r.keys() else None
            ing_dict['safety'] = r['safety_index']['value'] if 'safety_index' in r.keys() else None
            ing_list.append(ing_dict)
        ans['ingredients'] = ing_list
        return ans
    else:
        return None

def ResultFormat_Advance(results):
    ans_list = list()
    if results['results']['bindings']:
        for r in results['results']['bindings']:
            ans = dict()
            ans['product_id'] = r['pid']['value']
            ans['product_name'] = r['name']['value']
            ans['url'] = r['url']['value']
            ans_list.append(ans)
        return ans_list
    else:
        return None

def queryByName(pid):
    query ="""
        SELECT DISTINCT ?product ?name ?url ?category ?subcategory ?minicategory ?brand ?love ?ingredient_name ?function ?safety_index ?acne_index ?irritant_index (MIN(?price) AS ?minPrice) (MIN(?size) AS ?minsize)
        WHERE{{
            ?product a myns:skincare_product;
                myns:product_id {} ;
                myns:product_url ?url;
                myns:category [rdfs:label ?category];
                myns:subcategory [rdfs:label ?subcategory];
                myns:minicategory [rdfs:label ?minicategory];
                myns:product_name ?name;
                myns:brand [rdfs:label ?brand];
                myns:numOfLoves ?love;
                myns:size_price_pair ?spp;
                myns:hasIngredient ?ingredient.
            ?ingredient a myns:Compound ;
                foaf:name ?ingredient_name;
                OPTIONAL{{?ingredient myns:hasFunction [rdfs:label ?function]}}
                OPTIONAL{{?ingredient myns:safety ?safety_index;}}
                OPTIONAL{{?ingredient myns:acne ?acne_index;}}
                OPTIONAL{{?ingredient myns:irritant ?irritant_index;}}
            ?minspp myns:fromProduct ?product;
                myns:hasPrice ?price;
                myns:hasSize ?size.    
        
    }}GROUP BY ?product ?name ?url ?category ?subcategory ?minicategory ?brand ?love ?ingredient_name ?function ?safety_index ?acne_index ?irritant_index       
    """
    sparql.setQuery(prefixes + query.format(pid))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return ResultFormat_basic(results,pid)

def queryByName_old(pid):
    query = """
    SELECT DISTINCT ?product ?name ?url ?category ?subcategory ?minicategory ?brand ?love #(MIN(?price) AS ?minPirce) (MIN(?size) AS ?minSize)
    WHERE{{
        ?product a myns:skincare_product;
            myns:product_id {};
            myns:product_url ?url;
            myns:category [rdfs:label ?category];
            myns:subcategory [rdfs:label ?subcategory];
            myns:minicategory [rdfs:label ?minicategory];
            myns:product_name ?name;
            myns:brand ?brand;
            myns:numOfLoves ?love;
            myns:size_price_pair ?spp;
            myns:hasIngredient ?ingredient.
        ?ingredient a myns:Compound ;
            myns:hasFunction ?function ;
            myns:safety ?safety_index; 
            myns:acne ?acne_index;
            myns:irritant ?irritant_index.

        ?spp myns:fromProduct ?product;
            myns:hasPrice ?price;
            myns:hasSize ?size.        
    }}
    """
    sparql.setQuery(prefixes + query.format(pid))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']
    

def queryByAttributes(param):
    query = """
    SELECT DISTINCT ?product ?pid ?name ?url
    WHERE{{
        ?product a myns:skincare_product;
            myns:product_id ?pid;
            myns:product_url ?url;
            myns:minicategory [rdfs:label ?minicategory];
            myns:product_name ?name;
            myns:brand [rdfs:label ?brand];
            myns:numOfLoves ?love;
            myns:size_price_pair ?spp;
            myns:hasIngredient ?ingredient.
        ?ingredient a myns:Compound.
        ?spp myns:fromProduct ?product;
            myns:hasPrice ?price;
            myns:hasSize ?size.
        ?ingredient myns:hasFunction [rdfs:label ?function].
  		FILTER (?price>={price[0]} && ?price<={price[1]})
    """
    
    query = prefixes + query
    if param['minicategory']: query +="""FILTER (?minicategory IN ({minicategory}))"""
    if param['function']: query +="""FILTER (?function IN ({function}))"""
    if param['brand']: query += """FILTER EXISTS {{?brand rdfs:label "{brand}" }}"""
    if param['Preservatives']: 
        query += """MINUS{{?product myns:hasIngredient [myns:hasAttribute myns:Preservatives].}}"""
        query += """MINUS{{?product myns:hasIngredient [myns:hasFunction myns:Preservative].}}"""
    if param['Fragrance']: query += """MINUS{{?product myns:hasIngredient [myns:hasAttribute myns:Fragrance].}}"""
    if param['Alcohol']: query += """MINUS{{?product myns:hasIngredient [myns:groupOf myns:Alcoholic].}}"""
    if param['acne']: 
        query +="""OPTIONAL{{?product myns:hasIngredient [ myns:acne ?acne_index].}}
  		FILTER (?acne_index<={acne} || !BOUND(?acne_index))"""
    if param['irrative']:
        query +="""OPTIONAL{{?product myns:hasIngredient [ myns:acne ?irrative_index].}}
  		FILTER (?irrative_index<={irrative} || !BOUND(?irrative_index))"""
    # if param['safety']: 
    #     query +="""OPTIONAL{{?product myns:hasIngredient [ myns:safety ?safety_index].}}
  	# 	FILTER (?safety_index<={safety} || !BOUND(?safety_index))"""
   
    query += """}}ORDER BY DESC(?love)"""
    # print('--------------------')
    # print(query.format(**param))
    # print('--------------------')
    sparql.setQuery(prefixes + query.format(**param))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(len(results['results']['bindings']))
    return ResultFormat_Advance(results)


def queryIfProductsConflicted(products):
    # check if a new product is conflict with the existing products
    query = """
        SELECT DISTINCT * WHERE{
  	  ?product1 a myns:skincare_product;
               myns:hasIngredient [myns:groupOf ?g1];
               myns:product_id 2058402  .
  
      ?product2 a myns:skincare_product;
  			   myns:hasIngredient [myns:groupOf ?g2];
  				myns:product_id 2311439 .
     FILTER EXISTS{?g1 myns:conflictWith ?g2} # with result = conflict
    	}"""
    # if result : conflict
    
def queryFindConflictedGroup(collections):
    # find conflicted group for the collections
    query = """
    SELECT DISTINCT ?conflictedGroup WHERE{{
        ?product_list myns:product_id ?product_ids;
   			          myns:hasIngredient ?ingredient.
     ?ingredient myns:groupOf [myns:conflictWith ?conflictedGroup].
	FILTER (?product_ids IN ({}))
    	}}
    """
    query = prefixes + query
    sparql.setQuery(prefixes + query.format(collections))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    return ['myns:'+r['conflictedGroup']['value'].split('/')[-1] for r in results]
    
def queryFindFitProduct(pids,conflictedgroup):
    # find products qualified for conflicted group and pid
    query="""
    SELECT DISTINCT ?product ?pid ?name ?url ?minicategory  ?brand ?love ?price ?size
    WHERE{{
        ?product a myns:skincare_product;
            myns:product_id ?pid;
            myns:product_url ?url;
            myns:minicategory [rdfs:label ?minicategory];
            myns:product_name ?name;
            myns:brand ?brand;
            myns:numOfLoves ?love;
            myns:size_price_pair ?spp.
        ?spp myns:fromProduct ?product;
            myns:hasPrice ?price;
            myns:hasSize ?size.
      FILTER (?pid IN ({}))
    """.format(pids)
    for c in conflictedgroup:
        query += """MINUS {{?product myns:hasIngredient [myns:groupOf {}]}}\n""".format(c)
    query += "}"
    # print('-----------------------')
    # print(query)
    # print('-----------------------')
    sparql.setQuery(prefixes + query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(len(results['results']['bindings']))
    return ResultFormat_Advance(results)






# 酒精
# 變性酒精 alcohol denat.
# alcohol中总分有两大类：低分子类对皮肤有害，包括ethyl alcohol（乙醇），methanol（甲醇）， isopropyl alcohol（异丙醇），benzyl alcohol（苯甲醇）；高分子类对皮肤有益，包括cetyl alcohol （鲸蜡醇）, stearyl alcohol（硬脂醇）, cetearyl alcohol（棕榈醇）, lanolin alcohol（羊毛脂醇）。

# param = {
#     'brand': "CLINIQUE",
#     'minicategory':False,
#     'price':[100,500],
#     'acne':False,
#     'irrative':2, #
#     'safety':2,
#     'fragrance':False,
#     'preservatives':False,
#     'alcohol':False # "ingredient_id": "fe88f2158"
# }
# result = queryByAttributes(param)
# result = queryByName('Green Tea Hydrating Cleansing Oil')
# temp = result["results"]["bindings"]
    
# with open('./output/query_result.json', 'w') as fp:
#     json.dump(temp, fp)
# print(len(result["results"]["bindings"]))
# for result in results["results"]["bindings"]:
#     print result["label"]["value"]


'''
import pandas as pd
products=pd.read_json('./sephora/output/sephora_skincare_product_ingredient_list.jl',lines=True)
ingredients=pd.read_json('./sephora/output/ingredients.jl',lines=True)

products.prices
tmp = temp[temp.map(lambda d: len(d)) > 0]
tmp.map(foo)
def foo(x):
    coll = list()
    for string in x:
        match=re.search(r'\$([0-9\.]+)',string)
        if match:
            coll.append(float(match.group(1)))
    return max(coll)
with open('./output/query_result.json') as json_file:
    results = json.load(json_file)
import pandas as pd


results = pd.read_json('./sephora/output/query_result.json') # dataframe
df =results.applymap(lambda x:x['value'])

temp = df[df['product']=='http://inf558.org/chemcosmetic/p_1014554']
df.groupby(['product','ingredient'])


'''

