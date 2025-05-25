# Multi-Modal AI: Text-to-Image & Image-to-Text

This project integrates two models into one application:
- BLIP (Salesforce): generates image captions (image → text)
- Stable Diffusion: generates images from text prompts (text → image)

## 🚀 Features
- Upload an image → get a caption
- Enter a prompt → get an AI-generated image
- REST API with Flask

## 🛠️ Setup

```bash
pip install -r requirements.txt
```

## 🧪 Run the app

```bash
python app.py
```

Send POST requests to:
- `/caption-image` with image file
- `/generate-image` with JSON: `{"prompt": "A robot painting a sunset"}`

## 📁 Outputs
- Caption text from image
- AI-generated image (base64 PNG)

## 👤 Author
Tahmid Al Kawsar Chowdhury
# -multimodal-ai-stable-blip
