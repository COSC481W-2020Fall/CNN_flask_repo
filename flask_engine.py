from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import isfile, join, dirname, realpath
from os import listdir
from time import time_ns, sleep
from base64 import b64decode
from json import loads, dumps

THIS_DIR = dirname(realpath(__file__))
HOME     = dirname(THIS_DIR)

def get_breed_info(filename):
    ret_name = join(HOME,'output', filename.split('.')[0]+".txt")
    ret = ""
    while not isfile(ret_name):
        pass
    sleep(.05)
    with open(ret_name) as file:
        ret = loads(file.read())
    return jsonify({"result" : ret})

def create_app():
    app = Flask(__name__)

    app.config.update(dict(DEBUG=False))

    CORS(app)

    @app.route("/image/", methods=['POST'])
    def post_image():
        if 'file' in request.files:
            file = request.files['file']
            if file:
                if file.filename != '':
                    filename = file.filename
                    UPLOAD_FOLDER = join(HOME, 'images')
                    file.save(join(UPLOAD_FOLDER, filename))
                    return get_breed_info(filename)
                else:
                    return jsonify({"result": "No image recieved"})
        else:
            return jsonify({'result':'Nothing recieved'})
            
    @app.route("/correction/", methods=['POST'])
    def correct_breed():
        CORR_DIR = join(HOME, 'correction')
        file_name = f"{len(listdir(CORR_DIR))}_corr.json"
        with open(join(CORR_DIR, file_name), "w+") as file:
            file.write(dumps(request.form))
        return {'result': "Submitted!"}

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
app.run(host="0.0.0.0", port=port)
