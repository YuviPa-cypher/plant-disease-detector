from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

from .models import PlantUpload

model_path = os.path.join(os.path.dirname(__file__), 'model', 'plant_disease_model.h5')
model = None
model_load_error = None


def get_model():
    global model, model_load_error

    if model is not None:
        return model

    if model_load_error is not None:
        raise model_load_error

    if not os.path.exists(model_path):
        model_load_error = FileNotFoundError(
            f"Model file not found at {model_path}. Train the model with cnn_model.py first."
        )
        raise model_load_error

    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as exc:
        model_load_error = exc
        raise

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
    recent_uploads = PlantUpload.objects.order_by('-created_at')[:8]
    return render(request, 'home.html', {
        'recent_uploads': recent_uploads,
    })

def predict_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            current_model = get_model()
        except Exception as exc:
            recent_uploads = PlantUpload.objects.order_by('-created_at')[:8]
            return render(request, 'home.html', {
                'error': str(exc),
                'recent_uploads': recent_uploads,
            }, status=503)

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
        prediction = current_model.predict(img_array)
        predicted_index = int(np.argmax(prediction))
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(prediction))

        # Debugging: Log the raw prediction and predicted class
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Raw model output: {prediction}")
        logger.info(f"Predicted class: {predicted_class}")

        upload = PlantUpload.objects.create(
            image=filename,
            predicted_label=predicted_class,
            confidence=confidence,
        )

        request.session['result_id'] = upload.id
        request.session.modified = True

        return redirect('result_page')

    recent_uploads = PlantUpload.objects.order_by('-created_at')[:8]
    return render(request, 'home.html', {
        'error': 'Please upload an image to make a prediction.',
        'recent_uploads': recent_uploads,
    })

def result_page(request):
    result_id = request.session.get('result_id')
    upload = PlantUpload.objects.filter(pk=result_id).first() if result_id else None
    recent_uploads = PlantUpload.objects.order_by('-created_at')[:8]

    return render(request, 'result.html', {
        'upload': upload,
        'recent_uploads': recent_uploads,
    })