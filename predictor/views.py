from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'plant_disease_model.h5')
model = tf.keras.models.load_model(model_path)

# Class labels (must match the dataset structure)
class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___healthy',
    'Potato___Late_blight',
    'Tomato___Target_Spot',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___Tomato_YellowLeaf__Curl_Virus',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___healthy',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites_Two_spotted_spider_mite'
]

def predictor_view(request):
    return render(request, 'home.html')

def predict_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        img_path = fs.path(filename)

        # Preprocess the image
        img_obj = image.load_img(img_path, target_size=(224, 224))  # Ensure target size matches model input
        img_array = image.img_to_array(img_obj)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Predict the disease
        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction)]

        # Debugging: Log the raw prediction and predicted class
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Raw model output: {prediction}")
        logger.info(f"Predicted class: {predicted_class}")

        # Store result in session
        request.session['result'] = str(predicted_class)  # Ensure data is a string
        request.session['image_url'] = fs.url(filename)
        request.session.modified = True  # ✅ Force Django to update session

        return redirect('result_page')

def result_page(request):
    result = request.session.get('result', 'No prediction available')
    image_url = request.session.get('image_url', '')

    # Use logging instead of print for debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Data sent to template - Result: {result}")
    logger.info(f"Data sent to template - Image URL: {image_url}")

    return render(request, 'result.html', {'result': result, 'image_url': image_url})