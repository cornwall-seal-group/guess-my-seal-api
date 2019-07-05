from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import config

endpoint = config.ENDPOINT
project_id = config.OD_PROJECT_ID
iteration_name = config.OD_ITERATION_NAME
prediction_key = config.OD_PREDICTION_KEY


def get_pattern_predictions(image_path):
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

    print 'About to OD the image ' + image_path
    # Open the image and get back the prediction results.
    with open(image_path, mode="rb") as test_data:
        print 'Opened file'
        results = predictor.detect_image(project_id, iteration_name, test_data)

    print results
    # TODO: order the predictions in order to aid readability

    return {
        "predictions": results.predictions
    }
