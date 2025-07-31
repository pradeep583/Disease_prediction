import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
import tflite_runtime.interpreter as tflite
import os

interpreter = tflite.Interpreter(model_path="model/model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

classes = [
    "Blight - Recommended: Bavistin + Captan (1:1 ratio, 2g/kg seed treatment)",
    "Common Rust - Recommended: 3g Katyayani Trichoderm in 1L water, evening foliar spray",
    "Gray Leaf Spot - Recommended: Apply NPK in 120:60:40 kg/ha ratio",
    "Healthy - No treatment required"
]

le = LabelEncoder()
le.fit(classes)

def getPrediction(filename):
    SIZE = 128
    img_path = os.path.join("static", filename)
    img = Image.open(img_path).resize((SIZE, SIZE))
    img = np.asarray(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_index = np.argmax(output_data)
    return le.inverse_transform([predicted_index])[0]
