from flask import Flask, render_template, request, jsonify
import joblib
import scheme
import pandas as pd
import os
import image
from mimetypes import guess_type
import math

app = Flask(__name__)

data = {
    "rarity_to_property_count": scheme.rarity_to_property_count,
    "items_to_pp": scheme.items_to_pp,
    "pp": scheme.pp,
    "sp": scheme.sp
}

model_directory = "models"
models = [f for f in os.listdir(model_directory) if os.path.isfile(os.path.join(model_directory, f))]

name_to_models = {}
for file_name in models:
    model = joblib.load(os.path.join(model_directory, file_name))
    name_to_models[file_name] = model

image_model = joblib.load('image_recognition/image_25K_2025-03-16_RandomForestRegressor.joblib')

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
    text = text.replace("\n", "\\n")

    predictions = image_model.predict([text])
    prediction_dict = dict(zip(scheme.output_columns, predictions[0]))
    print(prediction_dict)

    rarity = "Rare"
    name = "AdventurerBoots"
    rarity_value = 0
    name_value = 0
    for key, value in prediction_dict.items():
        if key.startswith("rarity_"):
            if prediction_dict[key] > rarity_value:
                rarity_value = prediction_dict[key]
                rarity = key.replace("rarity_", "")
        elif key.startswith("name_"):
            if prediction_dict[key] > name_value:
                name_value = prediction_dict[key]
                name = key.replace("name_", "")

    result = {
        "name": name,
        "rarity": rarity,
    }

    pp = scheme.items_to_pp[name]
    for p in pp:
        result[p] = prediction_dict[p]

    highest_sp = sorted(
        ((key, value) for key, value in prediction_dict.items() if key.startswith('s')),
        key=lambda item: item[1], reverse=True
    )

    property_count = scheme.rarity_to_property_count[rarity]

    top_n_sp_values = highest_sp[:property_count]
    for p, value in top_n_sp_values:
        result[p] = value

    print(result)
    return jsonify(result)

@app.route("/submit", methods=["POST"])
def submit():
    print(request.form)
    name = scheme.name_ids[request.form.get("name-selection")]
    rarity = scheme.rarity_to_property_count[request.form.get("rarity-selection")]

    item = scheme.get_empty_item()
    
    item = {
        f"name_{name}": 1,
        f"rarity_{rarity}": 1,
    }

    for key, value in request.form.items():
        if key in scheme.property_types:
            property_value = float(value)
            item[key] = property_value

    df = pd.DataFrame([item])

    model = name_to_models[request.form.get("model-selection")]

    predictions = model.predict(df)

    result = math.exp(int(predictions[0]))
    price = str(result) + "g"

    return jsonify(price)

if __name__ == '__main__':
    app.run()
