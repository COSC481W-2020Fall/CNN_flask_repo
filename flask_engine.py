from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import isfile, join, dirname, realpath
from time import time_ns, sleep
from base64 import b64decode

THIS_DIR = dirname(realpath(__file__))
HOME     = dirname(THIS_DIR)

def get_breed_info(filename):
    ret_name = join(HOME,'output', filename.split('.')[0]+".txt")
    ret = ""
    while not isfile(ret_name):
        pass
    sleep(.05)
    with open(ret_name) as file:
        ret = file.read()
    return jsonify({"result" : ret})

def create_app():
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))

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
        elif 'file' in request.form:
            encodedImg = request.form['file']
            if encodedImg:
                imgdata = b64decode(encodedImg)
                filename = time_ns()
                UPLOAD_FOLDER = join(HOME, 'images')
                with open(join(UPLOAD_FOLDER, filename), "wb") as file:
                    file.write(imgdata)
                return get_breed_info(filename)
        else:
            return jsonify({'result':'Nothing recieved'})
            
        
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
