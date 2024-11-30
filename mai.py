import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model # type: ignore


def getPrediction(filename):
    
    classes = ['Blight','Common Rust','Gray Leaf Spot','Healthy']
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])
    
    
    #Load model
    my_model=load_model("my_model.h5")
    
    SIZE = 128 #Resize to same size as training images
    img_path = 'static/images/'+filename
    img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
    
    img = img/255. #Scale pixel values
    
    img = np.expand_dims(img, axis=0)     
    
    pred = my_model.predict(img)                  
    
    #Convert prediction to class name
    pred_class = le.inverse_transform([np.argmax(pred)])[0]
    print("Diagnosis is:", pred_class)
    return pred_class
