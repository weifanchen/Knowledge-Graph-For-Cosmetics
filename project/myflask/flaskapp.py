from flask import Flask, jsonify, request
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON
from Queries import queryByAttributes, queryByName, queryFindConflictedGroup, queryFindFitProduct, queryByIngredient_others, queryByIngredient_synonym, queryByIngredient
from werkzeug.datastructures import ImmutableMultiDict
 
app = Flask(__name__)
sparql = SPARQLWrapper("http://localhost:3030/ds/query")
CORS(app)

def Advanced_param(res):
    param = {
            'minicategory' :str(res.getlist('categories[]'))[1:-1], # empty = []
            'brand': res.get('brand',False),
            'price':[res.getlist('price[]')[0],res.getlist('price[]')[1]],
            'acne' : res.get('acne',False),
            'irrative': res.get('irri',False),
            'Fragrance':False,
            'Preservative':False,
            'Alcohol':False ,
            'function': str(res.getlist('function[]'))[1:-1]
        } #default
    if res.get('acne')=='1': param['acne']=False
    if res.get('irri')=='1': param['irrative']=False
    for fda in res.getlist('fda[]'):
        param[fda] = True
    return param

    

@app.route('/', methods=['GET'])
def ping_pong():
    #res = ImmutableMultiDict([('type', 'Basic'), ('product', '1932920')])
    #res = ImmutableMultiDict([('type', 'Compound'), ('ingredient', 'chem60de5d6467')])
    # res = ImmutableMultiDict([('type', 'Advanced'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('price[]', '0'), ('price[]', '280')]) # only inner qyery
    #res = ImmutableMultiDict([('type', 'Advanced'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('acne', '2'), ('irri', '3'), ('fda[]', 'Fragrance'), ('fda[]', 'Preservative'), ('price[]', '0'), ('price[]', '280'),('function[]','Emollient'),('function[]','Whitening')])   
    # two words function !
    # res = ImmutableMultiDict([('type', 'Advanced'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('brand', 'SEPHORA COLLECTION'), ('price[]', '0'), ('price[]', '260'), ('acne', '3'), ('irri', '2'),('function[]','Emollient')])
    #res = ImmutableMultiDict([('type', 'Collection'),('collections[]', 'The True Cream Aqua Bomb'),('collections[]', 'Protini™ Polypeptide Moisturizer'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('acne', '2'), ('irri', '3'), ('fda[]', 'Fragrance'), ('fda[]', 'Preservatives')])
    #res = ImmutableMultiDict([('type', 'Collection'),('collections[]', 2005023),('collections[]', 2025633), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('acne', '2'), ('irri', '3'), ('fda[]', 'Fragrance'), ('fda[]', 'Preservatives'),('price[]', '0'), ('price[]', '280')])
    #res = ImmutableMultiDict([('type', 'Collection'), ('categories[]', 'Face Oils'), ('brand', ''), ('price[]', '0'), ('price[]', '240'), ('acne', '1'), ('irri', '1'), ('fda[]', 'Fragrance'), ('collection[]', 'p_1893163')])
    res = request.args
    print(res)
    
    if res['type'] == 'Basic':
        result = queryByName(res['product'])
        #print(len(result['ingredients']))
        return jsonify(result)
    elif res['type'] == 'Compound':
        result = queryByIngredient(res['ingredient'])
        return jsonify(result)
    elif res['type'] == 'Advanced':
        result = queryByAttributes(Advanced_param(res))
        print(result)
        return jsonify(result)
    elif res['type'] == 'Collection':
        result = 'No result'
        productsFitAttributes = queryByAttributes(Advanced_param(res))
        if len(productsFitAttributes)>0:
            pids = set([int(p['product_id']) for p in productsFitAttributes])
            pids = str(pids)[1:-1]
            collections_list = res.getlist('collection[]')
            collections = str([int(cl.replace('p_','')) for cl in collections_list])[1:-1]
            conflictedgroup = queryFindConflictedGroup(collections)
            if conflictedgroup:
                print('found conflicted group, ready to queryFindFitProduct')
                result=queryFindFitProduct(pids,conflictedgroup)
            else:
                return jsonify(productsFitAttributes)
        return jsonify(result)
    else:
        return jsonify('Hello from Flask!')

# Basic Search arguments example
# res = ImmutableMultiDict([('type', 'Basic'), ('product', 'Protini™ Moisturizer')])
# 127.0.0.1 - - [20/Apr/2020 13:21:19] "GET /?type=Basic&product=Protini%E2%84%A2+Moisturizer HTTP/1.1" 200 -

# Advanced Search arguments example
# res = ImmutableMultiDict([('type', 'Advanced'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('acne', '2'), ('irri', '3'), ('fda[]', 'Fragrance'), ('fda[]', 'Preservative')])
# 127.0.0.1 - - [20/Apr/2020 13:20:28] "GET /?type=Advanced&categories[]=Moisturizers&categories[]=Face+Oils&acne=2&irri=3&fda[]=Fragrance&fda[]=Preservative HTTP/1.1" 200 -

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     data = request.get_json(silent=True)
#     print(data)

'''
function_list = [
myns:HairConditioning,
myns:SkinConditioning, myns:HairFixative, myns:Humectant, myns:Moisturizer, myns:Depilatory, myns:anti-aging, myns:Whitening
,myns:Anti-inflammatory,myns:NailConditioning, myns:OralCare	
myns:Antimicrobial
myns:Antidandruff
myns:Cellregeneration
myns:Exfoliator
myns:Antioxidant
myns:Sunscreen
myns:Anti-allergic
myns:Deodorant
myns:Smoothing
myns:Emollient
]
'''

if __name__ == '__main__':
    app.run(debug = True)
