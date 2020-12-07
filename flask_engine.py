from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
from os.path import isfile, join, dirname, realpath
from os import listdir
from time import time_ns, sleep
from base64 import b64decode
from json import loads, dumps
from pyheif import read_heif
from PIL import Image

THIS_DIR = dirname(realpath(__file__))
HOME     = dirname(THIS_DIR)

ALLOWED_IMAGES = ["png", "jpeg", "jpg"]

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

    app.config.update(dict(DEBUG=True))

    CORS(app)

    @app.route("/", methods=['GET','POST'])
    def home():
        return render_template('index.html')

    @app.route("/image/", methods=['GET','POST'])
    def post_image():
        if request.method == 'POST':
            if 'file' in request.files:
                file = request.files['file']
                if file:
                    if file.filename != '':
                        filename = file.filename
                        ext = filename.split(".")[-1].lower()
                        if ext in ALLOWED_IMAGES:
                            UPLOAD_FOLDER = join(HOME, 'images')
                            file.save(join(UPLOAD_FOLDER, filename))
                        elif ext in ['heic', 'avif']:
                            CONV_FOLDER = join(HOME, 'conversion')
                            UPLOAD_FOLDER = join(HOME, 'images')
                            file.save(join(CONV_FOLDER, filename))
                            with open(join(CONV_FOLDER, filename), 'rb') as file:
                                i = read_heif(file)
                                pi = Image.frombytes(
                                    mode=i.mode,
                                    size=i.size,
                                    data=i.data
                                )
                                pi.save(join(UPLOAD_FOLDER,filename.split(".")[0] + '.jpeg'), format="jpeg")
                        return get_breed_info(filename)
                    else:
                        return jsonify({"result": "No image recieved"})
            elif 'file' in request.form:
                file = request.form['file']
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
        if request.method == 'GET':
            return render_template('upload.html')
            
    @app.route("/correction/", methods=['GET','POST'])
    def correct_breed():
        if request.method == 'POST':
            try:
                CORR_DIR = join(HOME, 'correction')
                file_name = f"{len(listdir(CORR_DIR))}_corr.json"
                user_input=""
                if 'file' in request.files:
                    file = request.files['file']
                    if file:
                        if file.filename != '':
                            filename = file.filename
                            ext = filename.split(".")[-1].lower()
                            if ext in ['heic', 'avif']:
                                filename = filename.split(".")[0] + ".jpg"
                            user_input=dumps({"image": filename, "breed": request.form["breed"]})
                        else:
                            return jsonify({"result": "No image recieved"})
                else:
                    user_input = dumps(request.form)
                if len(user_input) <= 2:
                    raise BaseException
                with open(join(CORR_DIR, file_name), "w+") as file:
                    file.write(user_input)
                return jsonify({'result': "Submitted!"})
            except BaseException as e:
                print(e)
                return jsonify({'result': 'Error has occured, please try again'})
        if request.method == 'GET':
            return render_template('correction.html')


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
