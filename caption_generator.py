from transformers import pipeline
from PIL import Image

def generate_captions(image_path):
    try:
        # توليد الوصف الإنجليزي
        captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        img = Image.open(image_path)
        result = captioner(img)
        english_caption = result[0]['generated_text']
        
        # ترجمة إلى العربية
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
        translation = translator(english_caption, max_length=50)
        arabic_caption = translation[0]['translation_text']
        
        return english_caption, arabic_caption
        
    except Exception as e:
        print(f"Error in caption generation: {e}")
        return "Could not generate description", "تعذر توليد الوصف"