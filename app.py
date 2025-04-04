from flask import Flask, render_template, request, jsonify
import joblib
import scheme
import pandas as pd
import os
import image
from mimetypes import guess_type
import math
import parse


app = Flask(__name__)

data = {
    "rarity_to_property_count": scheme.rarity_to_property_count,
    "items_to_pp": scheme.name_to_pps,
    "pp": scheme.pp,
    "sp": scheme.sp
}

model_directory = "models"
models = [f for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f))]

name_to_models = {}
for file_name in models:
    model = joblib.load(os.path.join(model_directory, file_name))
    name_to_models[file_name] = model

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Check if file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", names=scheme.names, raritys=scheme.raritys, data=data, models=models)

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({'error': 'No image file found'}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PNG and JPG/JPEG are allowed.'}), 400

    mime_type = guess_type(file.filename)[0]
    if mime_type not in ["image/png", "image/jpeg"]:
        return jsonify({'error': 'Invalid MIME type. Only PNG and JPG/JPEG are allowed.'}), 400
    
    image_obj = image.file_to_image(file)

    text = image.image_to_text(image_obj)
    item, text = parse.parse_text(text)
    
    # item needs to be flat
    for name, value in item["pp"]:
        item[name] = value

    for name, value in item["sp"]:
        item[name] = value

    del item["pp"]
    del item["sp"]

    print(item)
    return jsonify(item)

@app.route("/submit", methods=["POST"])
def submit():
    print(request.form)
    name = request.form.get("name-selection")
    rarity = request.form.get("rarity-selection")

    item = scheme.get_empty_item()
    
    item[f"name_{name}"] = 1
    item[f"rarity_{rarity}"] = 1

    for key, value in request.form.items():
        if key in scheme.property_types:
            property_value = float(value)
            item[key] = property_value
    
    df = pd.DataFrame([item])

    model = name_to_models[request.form.get("model-selection")]

    # Ensure the dataframe has the same columns as the model was trained on
    model_columns = model.feature_names_in_
    df = pd.DataFrame([item], columns=model_columns)

    predictions = model.predict(df)

    result = int(predictions[0])
    price = str(result) + "g"

    return jsonify(price)

if __name__ == '__main__':
    app.run()
