from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import Models as dbHandler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import os
import cv2 as cv2
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_fficientNetB3_PATH = r'C:\Users\lenovo\Desktop\Preduict_Save_Life\TrainModel\EfficientNetB3.h5'

# Load your trained model
MODEL_fficientNetB3 = load_model(MODEL_fficientNetB3_PATH)
MODEL_fficientNetB3.make_predict_function()


def load(img_path):
    img = plt.imread(img_path)
    img_size = (300, 300)
    img = cv2.resize(img, img_size)
    img = np.expand_dims(img, axis=0)
    return img


# Labels
classes = {1: "Normal cell", 0: "Leukemia cell "}


def model_predict(img_path, model):
    image = load(img_path)
    pred = model.predict(image)
    index = np.argmax(pred[0])
    klass = classes[index]
    probability = round((pred[0][index] * 100), 2)
    results = {
        'probability': probability,
        'klass': klass
    }
    return results


@app.route('/uploaded', methods=['POST', 'GET'])
def uploaded():
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/uploads/upload_img.jpg")
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)

        file_path = os.path.join(basepath, "static/uploads/upload_img.jpg")

        # Make prediction
        preds = model_predict(file_path, MODEL_fficientNetB3)
        return render_template('Results.html', output=preds['klass'], percentage=preds['probability'],
                               img=file_path)
    return None


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/About.html', methods=['POST', 'GET'])
def About():
    return render_template('About.html')


@app.route('/AboutUs.html', methods=['POST', 'GET'])
def AboutUs():
    return render_template('AboutUs.html')


@app.route('/Predict.html', methods=['POST', 'GET'])
def Predict():
    return render_template('Predict.html')


@app.route('/signin.html', methods=['POST', 'GET'])
def signin2():
    return render_template('signin.html')


@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_re_enter = request.form['password_re_enter']
        ou = ""
        if password != password_re_enter:
            ou = "password not equals to Re-enter Password"
            return render_template('signup.html', ou=ou)
        else:
            Users = dbHandler.insertUser(id, name, email, password, password_re_enter)
            if Users:
                return render_template('signin.html')
            else:
                ou = "ID is already used"
                return render_template('signup.html', ou=ou)
    else:
        return render_template('signup.html')


@app.route('/', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        id = int(request.form['id'])
        password = request.form['password']
        us = dbHandler.retrieveUsers(id, password)
        output = ""
        if (len(us)) == 0:
            output = "Incorrect ID or Password"
            return render_template('signin.html', output=output)
        elif (len(us)) > 0:
            return render_template('index.html', output=output)
    else:
        return render_template('signin.html')


@app.route('/forgetPassword.html', methods=['POST', 'GET'])
def forgetPassword():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        info = dbHandler.forgetPassword(name, email)
        information = ""
        if (len(info)) == 0:
            information = "Incorrect name or email"
            return render_template('forgetPassword.html', information=information)
        elif (len(info)) > 0:
            information = info
            return render_template('forgetPassword.html', information=information)
    else:
        return render_template('forgetPassword.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
