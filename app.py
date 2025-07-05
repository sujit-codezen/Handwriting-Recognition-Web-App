from flask import Flask, render_template, request
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    image_path = None

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)

                image_pil = Image.open(image_path).convert("RGB")
                pixel_values = processor(images=image_pil, return_tensors="pt").pixel_values
                generated_ids = model.generate(pixel_values)
                text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return render_template('index.html', text=text, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
