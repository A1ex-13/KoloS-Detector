# ----------------- Write your code below this line. -------------------- #
import os
from io import BytesIO

from flask import Flask, render_template, request

from config import config
from hotdogclassifier import HotDogClassifier

# create a Flask app
app = Flask(__name__)

# load the pre-trained model
model = HotDogClassifier()
model.load_model(config["model_weight"])


@app.route("/", methods=["GET"])
def home():
    """
    This function handles the GET requests for end-point `/`.

    In simple terms, this function handles what the app will do when you open the
    app in the browser. Naturally, it will return the home page of our webapp.
    """
    # Return the home page of our web app.
    return render_template("index.html",
                           flag=False,
                           project_description=config["project_description"],
                           project_name=config["project_name"])


@app.route("/", methods=["POST"])
def classify():
    """
    This function handles the POST requests for end-point `/`.

    In design of our front-end (html), this endpoint is called whenever a successful
    upload of an image is made. This function will return a page with the image and
    the model's prediction.
    """
    # Extract uploaded the file from the request.
    uploaded_file = request.files["files"]
    # Convert the extracted file into a series of bytes for further processing.
    data = BytesIO(uploaded_file.read())
    # Assess if an empty file was uploaded.
    if uploaded_file.filename != "":
        # Let our model make the prediction.
        img, predicted = model.predict(data)
    else:
        # No prediction could be made.
        predicted, img = "", ""
    # return the rendered home page with response.
    return render_template("index.html",
                           predicted=predicted,
                           img=img,
                           flag=True,
                           project_description=config["project_description"],
                           project_name=config["project_name"])


# ----------------- You do NOT need to understand what the code below does. -------------------- #

if __name__ == '__main__':
    PORT = os.environ.get('PORT') or 8080
    DEBUG = os.environ.get('DEBUG') != 'TRUE'
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
