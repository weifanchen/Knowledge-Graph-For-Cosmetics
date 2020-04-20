from flask import Flask, jsonify, request
from flask_cors import CORS
from CosQuery import queryFormula
# print_hello()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def ping_pong():
    res = request.args
    print(res['type'])
    # return jsonify(queryFormula())
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
