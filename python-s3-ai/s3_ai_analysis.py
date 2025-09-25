import boto3
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions, MobileNetV2

model = MobileNetV2(weights='imagenet')  # Load AI model

s3 = boto3.client('s3')
bucket_name = 'your-bucket-name'

def analyze_file(file_key):
    if not file_key.lower().endswith(('.jpg', '.jpeg', '.png')):
        return "Non-image file"

    # Download file temporarily
    tmp_file = f"/tmp/{file_key.split('/')[-1]}"
    s3.download_file(bucket_name, file_key, tmp_file)

    try:
        image = Image.open(tmp_file).resize((224, 224))
        img_array = np.array(image.convert('RGB'))
        img_batch = np.expand_dims(img_array, axis=0)
        img_preprocessed = preprocess_input(img_batch)
        prediction = model.predict(img_preprocessed)
        decoded = decode_predictions(prediction, top=1)[0][0]
        return f"{decoded[1]} ({decoded[2]*100:.2f}%)"
    except Exception as e:
        return f"AI error: {str(e)}"
