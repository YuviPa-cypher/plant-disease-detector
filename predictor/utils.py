# filepath: c:\Users\pande\plant-disease-detector\predictor\utils.py
from PIL import Image
import numpy as np

def preprocess_image(image_path, target_size=(32, 32)):
    """
    Preprocess the image for model prediction.
    - Resize the image to the target size.
    - Normalize pixel values to the range [0, 1].
    - Add a batch dimension.

    Args:
        image_path (str): Path to the image file.
        target_size (tuple): Desired image size (width, height).

    Returns:
        np.ndarray: Preprocessed image ready for prediction.
    """
    img = Image.open(image_path).resize(target_size)  # Resize to target size
    img_array = np.array(img) / 255.0  # Normalize pixel values
    return np.expand_dims(img_array, axis=0)  # Add batch dimension