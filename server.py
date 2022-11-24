from flask import Flask, redirect, render_template, jsonify, request
import cv2, os, sys, imutils
import numpy as np
import tensorflow as tf

MODEL_PATH = 'mnist_model'

app = Flask(__name__)
app.config['DEBUG'] = False

# Load the Model
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imagefile = request.files['imagefile']
    imagepath = "./images/"+imagefile.filename
    imagefile.save(imagepath)
    return render_template('index.html',prediction = "Predicted")
    

@app.route('/infer', methods=['POST'])
def hand_classifier():
    # Receive the encoded frame and convert it back to a Numpy Array
    encoded_image = np.frombuffer(request.data, np.uint8)
    image = cv2.imdecode(encoded_image, -1) # Decode image without converting to BGR
    
    image = np.expand_dims([image], axis=-1) # Add dimensions to create appropriate tensor shapes
    
    # Run inference on the frame
    hand = model.predict(image)

    return jsonify(str(np.argmax(hand))) # Because only string can be converted to JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)