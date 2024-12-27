import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from collections import Counter

# website colors
webblue = "#3c40c6"
webgray = "#d2dae2"
weborange = "#ffc048"
webred = "#ff5e57"
webyellow = "#ffdd59"

app = Flask(__name__)

img_path = "static/images/battery_park_winter.jpeg"

def process_colors(img_path):
    img = Image.open(img_path)
    img = img.convert("RGB")
    img = img.resize((300, 300), Image.LANCZOS)
    img = np.array(img)
    # Convert RGB array to hexadecimal
    hex_array = np.apply_along_axis(lambda x: '#{:02x}{:02x}{:02x}'.format(*x), 2, img)
    # Flatten the hex array to a 1D list
    hex_flattened = hex_array.flatten()
    nbr_colors = len(hex_flattened)
    print(f'number of colors detected: {nbr_colors}')
    
    # Count occurrences of each color
    color_counts = Counter(hex_flattened)
    # Find the 10 most common colors
    most_common_colors = color_counts.most_common(10)
    # Output results
    most_common_colors = [(color, f"{count/nbr_colors:.2%}") for color, count in most_common_colors]
    return most_common_colors
    


@app.route("/")
def home():
    colors = process_colors(img_path)
    return render_template("home.html", colors=colors, image_path=img_path[7:])


@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    # Save the file as "user_image.jpg"
    img_path = os.path.join('static/images', 'user_image.jpg')
    file.save(img_path)
    colors = process_colors(img_path)
    return render_template("home.html", colors=colors, image_path=img_path[7:])


if __name__ == "__main__":
    app.run(debug=True)
