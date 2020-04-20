from flask import Flask, jsonify, request
from flask_cors import CORS
from CosQuery import queryFormula
# print_hello()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def ping_pong():
    print(request.args)
    # return jsonify(queryFormula())
    return jsonify('Hello from Flask!')

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     data = request.get_json(silent=True)
#     print(data)

if __name__ == '__main__':
    app.run(debug = True)
