from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import config
import os

endpoint = config.ENDPOINT
project_id = config.CLASSIFIER_PROJECT_ID
iteration_name = config.CLASSIFIER_ITERATION_NAME
prediction_key = config.CLASSIFIER_PREDICTION_KEY


def find_seal(image_path):
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

    # Open the image and get back the prediction results.
    with open(image_path, mode="rb") as image_contents:
        results = predictor.classify_image(
            project_id, iteration_name, image_contents.read())

    return results


def id_seal(folder_path, processed_images):

    predictions = {}
    for image_path in processed_images:
        full_path = os.path.join(folder_path, image_path)
        results = find_seal(full_path)
        image_predictions = {}

        for prediction in results.predictions:
            image_predictions[prediction.tag_name] = prediction.probability
            print ("\t" + prediction.tag_name +
                   ": {0:.2f}%".format(prediction.probability * 100))

        predictions[full_path] = image_predictions

    return predictions
