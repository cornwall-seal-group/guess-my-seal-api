from PIL import Image
from predictions.pattern_detection import get_pattern_predictions
import uuid
import os
from image.crop import crop_image
from image.normalise import normalise_image
from image_meta.store import store_seal_img_metadata, store_seal_metadata
import config

IMAGES_FOLDER = config.IMAGES_FOLDER
EXT = '.jpg'


def process_image(folder_path, image_path, filename):

    img = Image.open(image_path).convert('RGB')

    prediction_images = process_predictions(img, folder_path, image_path)
    print prediction_images

    processed_images = [folder_path + '/' + filename] + prediction_images

    # Save metadata of seal and its predictions
    # seal_folder = IMAGES_FOLDER + seal_name
    # store_seal_img_metadata(seal_folder, seal_name, processed_images)

    # # Save seal name for reference so we know what seals we have images for
    # store_seal_metadata(IMAGES_FOLDER, seal_name)

    return processed_images


def process_predictions(img, folder_path, original_image_path):
    processed_images = []
    pattern_predictions = get_pattern_predictions(original_image_path)

    predictions = pattern_predictions['predictions']

    prediction_index = 1
    # Loop through all the predictions
    for prediction in predictions:

        cropped_img = crop_image(img, prediction)
        normalised_img = normalise_image(cropped_img)

        # Create unique name for img (seal + index + prediction probability)
        predicted_img_name = str(prediction_index) + \
            '-' + str(prediction.probability) + EXT

        save_normalised_image(predicted_img_name, normalised_img, folder_path)

        processed_images.append(predicted_img_name)
        prediction_index += 1

    return processed_images


def save_normalised_image(img_name, img, folder_path):
    saved_path = os.path.join(folder_path, img_name)
    img.save(saved_path)

    return saved_path
