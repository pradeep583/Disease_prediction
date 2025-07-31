import numpy as np
# import pillow for image processing

from PIL import Image
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model 
import os

my_model = load_model("model/my_model.h5") 

classes = [
    "Blight - Recommended: Bavistin + Captan (1:1 ratio, 2g/kg seed treatment)",
    "Common Rust - Recommended: 3g Katyayani Trichoderm in 1L water, evening foliar spray",
    "Gray Leaf Spot - Recommended: Apply NPK in 120:60:40 kg/ha ratio",
    "Healthy - No treatment required"
]


le = LabelEncoder()
le.fit(classes)
le.inverse_transform([2])

def getPrediction(filename):
    SIZE = 128 
    img_path = os.path.join("static", filename)

    try:
        img = Image.open(img_path).convert("RGB").resize((SIZE, SIZE))
        img = np.asarray(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = my_model.predict(img)
        predicted_index = np.argmax(pred)
        pred_class = le.inverse_transform([predicted_index])[0]
        return pred_class

    except Exception as e:
        return f"Error in prediction: {str(e)}"


