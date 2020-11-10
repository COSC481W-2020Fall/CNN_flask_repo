from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import isfile, join, dirname, realpath
from time import time_ns

THIS_DIR = dirname(realpath(__file__))
HOME     = dirname(THIS_DIR)

def get_breed_info(filename):
    ret_name = join(HOME,'output', filename.split('.')[0]+".txt")
    ret = ""
    while not isfile(ret_name):
        pass
    with open(ret_name) as file:
        ret = file.read()
    return jsonify({"result" : str(ret)})

def create_app():
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))

    CORS(app)

    @app.route("/image/", methods=['POST'])
    def post_image():
        if 'file' not in request.files: # and 'bitmap' not in request.files:
            return jsonify({"result": "No image sent"})
        file = request.files['file']
        # bitmap = request.files['bitmap']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"result": "No image recieved"})
        if file:
            filename = file.filename
            UPLOAD_FOLDER = join(HOME, 'images')
            file.save(join(UPLOAD_FOLDER, filename))
            return get_breed_info(filename)
        
        # if bitmap:
        #     filename = time_ns()
        #     UPLOAD_FOLDER = join('..', 'images')
        #     file.save(join(UPLOAD_FOLDER, filename))
        #     return get_breed_info(filename)
            

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
