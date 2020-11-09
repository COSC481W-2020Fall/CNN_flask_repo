from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import isfile


def get_breed_info(file):
    ret_name = filename.split('.')[0]+".txt"
    ret = ""
    while (not isfile(ret_name)):
        pass
    with open(ret_name) as file:
        ret = file.read()
    return ret

def create_app():
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))

    CORS(app)

    @app.route("/image/", methods=['POST'])
    def post_image():
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('..', 'images', filename))
        return get_breed_info(filename)

    @app.route("/image/", methods=['PUT'])
    def put_image():
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('..', 'images', filename))
        return get_breed_info(filename)
        

    @app.route("/breed/<string:file>", methods=['GET'])
    def get_breed():
        return get_breed_info(filename)

    @app.route("/query/", methods=['GET'], strict_slashes=False)
    def get_test():
        if request.method == 'GET':
            return jsonify({"result": "hello world"})

    return app

port = 4201
app = create_app()
app.run(host="0.0.0.0", port=port, debug=False)
