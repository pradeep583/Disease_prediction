import numpy as np
import tensorflow
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model 


def getPrediction(filename):
    
    classes = ['Disease:"Blight" ; Recommended fertilizer: Bavistin + Captan in 1:1 ratio@2g/kg ','Disease:"Common Rust";Recommended Fertilizer : Dissolve 3g of Katyayani Trichoderm  in one litre of water and spray on leaf during evening hours.','Disease:"Gray Leaf Spot";Recommended Fertilizer: 120:60:40 ratio of NPK kg/hectare','Healthy']
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])
    
    
    #Load model
    my_model=load_model(r"D:\ML\model\my_model.h5")
    
    SIZE = 128 #Resize to same size as training images
    img_path = 'static/images/'+filename
    img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
    
    img = img/255      #Scale pixel values
    
    img = np.expand_dims(img, axis=0)  #Get it ready as input to the network       
    
    pred = my_model.predict(img) #Predict                  
    
    #Convert prediction to class name
    pred_class = le.inverse_transform([np.argmax(pred)])[0]
    print("Diagnosis  and recommendation:", pred_class)
    return pred_class


