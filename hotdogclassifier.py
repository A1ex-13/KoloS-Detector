"""
An class for the hotdog image classifier.

@author: Weiqing Wang <Weiqing.Wang@ibm.com>, Kathy An <Kathy.An@ibm.com>
"""

import base64
import io
import os
import os.path
from os.path import isfile
from typing import Tuple

import requests
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from torch import no_grad, load, argmax, device, cuda
from torch.nn import Linear
from torch.nn.functional import softmax
import ssl


class HotDogClassifier:
    """
    A classifier for classifying if an image has a hot
    dog in it or not.
    """

    # The classes images being classified into.
    labels_array = ["KoIoS", "NOT KoIoS"]
    # Define the transformation of the pictures to feed into our model.
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    transformations = transforms.Compose([transforms.Resize((224, 224)),
                                          transforms.ToTensor(),
                                          transforms.Normalize(mean, std)])
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self) -> None:
        """
        Initialise the classifier.
        """
        # Set up the device for the model.
        self._device = device("cuda:0" if cuda.is_available() else "cpu")
        # Load the pretrained resnet18 model.
        self._model = models.resnet18(pretrained=True).to(self._device)
        # Change the final layer such that the prediction is made to 2 possible outcomes.
        self._model.fc = Linear(512, len(self.labels_array))

    def load_model(self, url: str) -> None:
        """
        Load the pre-trained model parameters into the model.

        :param url: The url for the model weight file.
        """
        # Setup the path to train save and load the model parameters.
        save_path = os.path.join(os.getcwd(), "hotdog_detector.pt")
        # Assess if the model parameters have been downloaded.
        if not isfile(save_path):
            # Send an http request to download the model parameters.
            r = requests.get(url)
            # Create a new empty file to write the model parameters.
            f = open(save_path, mode="wb+")
            # Write the downloaded bytes into the empty file created.
            f.write(r.content)
            # Close the file pipeline.
            f.close()
        # Let our model load the model parameters from the file path defined in the first line.
        self._model.load_state_dict(load(save_path, map_location=self._device))
        # Set the model to evaluation mode.
        self._model.eval()

    def predict(self, data: io.BytesIO) -> Tuple[str, str]:
        """
        Make a prediction of the give image.

        :param data: The image to classify, in format of BytesIO.
        :return: A Base64 encoding of transformed model, and the model's prediction.
        """
        # Converted the uploaded bytes into an image array.
        image = Image.open(data).convert('RGB')
        # Transform the image to a format that could be used for Neural Network prediction. (Tensor)
        tensor = self.transformations(image).unsqueeze(0).to(self._device)
        # Make the prediction.
        with no_grad():
            z = softmax(self._model(tensor), dim=1)
            y_hat = argmax(z.data, dim=1)
        # Format the prediction into natural language.
        predicted = f"Model's prediction: {self.labels_array[y_hat]}"
        # Convert the transformed image into base64 encoding (text), such that it can be
        # displayed on our front-end (html file).
        img = str(base64.b64encode(data.getvalue()))[2:-1]
        # Return the results.
        return img, predicted
