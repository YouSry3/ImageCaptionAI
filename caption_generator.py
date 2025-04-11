from transformers import pipeline
from PIL import Image, ImageOps

def preprocess_image(image_path):
    """مرحلة ما قبل المعالجة للصورة"""
    try:
        
        img = Image.open(image_path)

       # less size at the beginning
        img = img.resize((224, 224))

        # Convert to grayscale if the image is not RGB
        img = img.convert("RGB")

        
        img = img.rotate(0)  # rotate the image to 0 degrees (no rotation)

        return img

    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

def generate_captions(image_path):
    try:
        # Level 1: Preprocess the image
        img = preprocess_image(image_path)
        if img is None:
            return "Error during preprocessing", "خطأ أثناء المعالجة"

        # Level 2: Generate English caption
        # Load the image captioning model
        captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        result = captioner(img)
        english_caption = result[0]['generated_text']
        
        # Level 3: Translate to Arabic
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
        translation = translator(english_caption, max_length=50)
        arabic_caption = translation[0]['translation_text']
        
        return english_caption, arabic_caption
        
    except Exception as e:
        print(f"Error in caption generation: {e}")
        return "Could not generate description", "تعذر توليد الوصف"
