from django.shortcuts import render
from django.core.files.storage import default_storage
import random
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.densenet import preprocess_input

class_names = [
    "actinic keratosis",
    "basal cell carcinoma",
    "dermatofibroma",
    "melanoma",
    "nevus",
    "pigmented benign keratosis",
    "seborrheic keratosis",
    "squamous cell carcinoma",
    "vascular lesion"
]

def predict_image(img_path):
    model = load_model("skin_cancer_custom_cnn.h5")
    img = load_img(img_path, target_size=(224, 224))  
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)   
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    return class_names[predicted_class_idx]

def Home(request):
    return render(request, 'predictor/home.html')

def Predict(request):
    prediction = None
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        file_path = default_storage.save('uploads/' + image.name, image)
        prediction = predict_image(default_storage.path(file_path))  # corrected line

    return render(request, "predictor/predict.html", {'prediction': prediction})
