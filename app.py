from flask import Flask, request, jsonify, render_template, send_from_directory
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from googletrans import Translator
import os
import torch

app = Flask(__name__)

# تحميل المعالج والنموذج
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# تهيئة مترجم Google
translator = Translator()

# مسار حفظ الصور المرفوعة
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# إعداد Flask لتقديم الصور من المجلد
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return render_template('index.html')  # عرض صفحة HTML

@app.route("/generate_caption", methods=["POST"])
def generate_caption():
    # التأكد من أن الصورة تم إرسالها في الطلب
    if 'image' not in request.files:
        return jsonify({"error": "No image found in request"}), 400

    # قراءة الصورة
    image_file = request.files['image']
    image = Image.open(image_file)

    # حفظ الصورة في مجلد uploads
    image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image.save(image_filename)

    # توليد التسمية (caption) باستخدام BLIP
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    caption_en = processor.decode(out[0], skip_special_tokens=True)  # التسمية بالإنجليزية

    # التحقق من إذا كان الوصف تم إنشاؤه بنجاح
    if not caption_en:
        caption_en = "No caption generated"

    # ترجمة التسمية إلى العربية
    caption_ar = translator.translate(caption_en, src='en', dest='ar').text  # الترجمة للعربية

    # إعادة التوجيه إلى الصفحة الرئيسية مع عرض الوصف باللغتين والصورة
    return render_template('index.html', caption_en=caption_en, caption_ar=caption_ar, image_filename=image_file.filename)

if __name__ == "__main__":
    app.run(debug=True)
