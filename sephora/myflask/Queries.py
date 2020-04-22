from SPARQLWrapper import SPARQLWrapper, JSON
import json

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

def subquery(param):
    query = """
    SELECT DISTINCT * WHERE{{
        
        ?product a myns:skincare_product;
            myns:brand ?brand;
            myns:hasIngredient ?ingredient.
        ?ingredient myns:hasFunction ?function.
        {{
            SELECT * WHERE{{
                ?ingredient a myns:Compound;
                    myns:hasFunction myns:SkinConditioning.
            
            }}

        }}UNION{{
            SELECT * WHERE{{
                ?ingredient a myns:Compound;
                    myns:hasFunction myns:Plantextract.

            }}
        
        }}
    }}
    """
    sparql.setQuery(prefixes + query.format(**param))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def queryByName(name):
    sparql = SPARQLWrapper("http://localhost:3030/ds/query")
    query = """
    SELECT DISTINCT ?product 
    WHERE{{
        ?product a myns:skincare_product;
            myns:product_name "{}";
        
    }}
    """
    sparql.setQuery(prefixes + query.format(name))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']
    

def queryByAttributes(param):
    query = """
    SELECT DISTINCT ?pid ?name ?love
    WHERE{{
        ?product a myns:skincare_product;
            myns:product_id ?pid;
            myns:minicategory [rdfs:label ?minicategory];
            myns:product_name ?name;
            myns:brand ?brand;
            myns:numOfLoves ?love;
            myns:size_price_pair ?spp.
            #myns:hasIngredient ?ingredient.
        ?spp myns:fromProduct ?product;
            myns:hasPrice ?price;
            myns:hasSize ?size.
  		FILTER (?price>={price[0]} && ?price<={price[1]})
    """
    
    query = prefixes + query
    if param['minicategory']: query +="""FILTER (?minicategory IN ({minicategory}))"""
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
    print('---------')
    print(query)
    print('---------')
    sparql.setQuery(prefixes + query.format(**param))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(len(results['results']['bindings']))
    return results['results']['bindings']

sparql = SPARQLWrapper("http://localhost:3030/ds/query")

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

