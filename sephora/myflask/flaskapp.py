from flask import Flask, jsonify, request
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON
from Queries import queryByAttributes, queryByName
from werkzeug.datastructures import ImmutableMultiDict
 
# print_hello()

app = Flask(__name__)
sparql = SPARQLWrapper("http://localhost:3030/ds/query")
CORS(app)

@app.route('/', methods=['GET'])
def ping_pong():
    #res = ImmutableMultiDict([('type', 'Basic'), ('product', 'Protini™ Polypeptide Moisturizer')])
    res = ImmutableMultiDict([('type', 'Advanced'), ('categories[]', 'Moisturizers'), ('categories[]', 'Face Oils'), ('acne', '2'), ('irri', '3'), ('fda[]', 'Fragrance'), ('fda[]', 'Preservatives')])    #res = request.args
    if res['type']=='Basic':
        result = queryByName(res['product'])
        return result
    elif res['type']=='Advanced':
        param = {
            'minicategory' :str(res.getlist('categories[]'))[1:-1], # empty = []
            'brand': res.get('brand',False),
            'price':[100,500],
            'acne' : res.get('acne',False),
            'irrative': res.get('irri',False),
            'Fragrance':False,
            'Preservatives':False,
            'Alcohol':False 
        } #default
        for fda in res.getlist('fda[]'):
            param[fda] = True
        print(param)
        result = queryByAttributes(param)
        return result
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

if __name__ == '__main__':
    app.run(debug = True)
