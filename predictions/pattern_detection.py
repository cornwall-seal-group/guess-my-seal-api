from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import config

endpoint = config.ENDPOINT
project_id = config.PROJECT_ID
iteration_name = config.ITERATION_NAME
prediction_key = config.PREDICTION_KEY


def get_pattern_predictions(image_path):
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

    # Open the image and get back the prediction results.
    with open(image_path, mode="rb") as test_data:
        results = predictor.detect_image(project_id, iteration_name, test_data)

    # TODO: order the predictions in order to aid readability

    return {
        "predictions": results.predictions
    }
