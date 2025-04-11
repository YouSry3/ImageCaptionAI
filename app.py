from flask import Flask, request, jsonify, render_template
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

app = Flask(__name__)

# تحميل المعالج والنموذج
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# حفظ النموذج في ملف محلي عند أول تشغيل (اختياري)
# torch.save(model.state_dict(), "caption_model.pth")  # Uncomment to save the model

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

    # توليد التسمية (caption) باستخدام BLIP
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # إرسال التسمية المُولدة كرد
    return jsonify({"caption": caption})

if __name__ == "__main__":
    app.run(debug=True)
