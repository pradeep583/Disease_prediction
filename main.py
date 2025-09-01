import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import os

# Load TFLite model
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

def getPrediction(filename):
    SIZE = 128
    img_path = os.path.join("static", filename)

    # Load + resize
    img = Image.open(img_path).convert("RGB").resize((SIZE, SIZE))

    # Handle input dtype
    input_dtype = input_details[0]['dtype']
    if input_dtype == np.float32:
        img = np.asarray(img, dtype=np.float32) / 255.0
    elif input_dtype == np.uint8:
        img = np.asarray(img, dtype=np.uint8)
    else:
        raise ValueError(f"Unsupported dtype: {input_dtype}")

    img = np.expand_dims(img, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    predicted_index = int(np.argmax(output_data))
    confidence = float(output_data[predicted_index])

    if confidence < 0.5:  
        return "Invalid"
    return classes[predicted_index]

