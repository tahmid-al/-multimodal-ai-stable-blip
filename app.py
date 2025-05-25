from flask import Flask, request, jsonify, send_from_directory
from transformers import BlipProcessor, BlipForConditionalGeneration
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load Stable Diffusion without float16 for CPU compatibility
text2img_model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
text2img_model.to("cuda" if torch.cuda.is_available() else "cpu")

# Serve the frontend HTML page
@app.route('/')
def homepage():
    return send_from_directory('.', 'index.html')

# Image → Text
@app.route('/caption-image', methods=['POST'])
def caption_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    image = Image.open(file.stream).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = caption_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return jsonify({"caption": caption})

# Text → Image
@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "A fantasy castle on a mountain")
    image = text2img_model(prompt).images[0]

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return jsonify({"image": base64_img})

if __name__ == '__main__':
    app.run(debug=True)