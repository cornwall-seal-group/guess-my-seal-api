from PIL import Image
from predictions.pattern_detection import get_pattern_predictions
import uuid
import os
from image.crop import crop_image
from image.normalise import normalise_image
from image_meta.store import store_seal_img_metadata, store_seal_metadata
import config

IMAGES_FOLDER = config.IMAGES_FOLDER
MIN_IMG_WIDTH = config.MIN_IMG_WIDTH
MIN_IMG_HEIGHT = config.MIN_IMG_HEIGHT
EXT = '.jpg'


def process_image(folder_path, image_path, filename):

    img = Image.open(image_path).convert('RGB')

    prediction_images = process_predictions(img, folder_path, image_path)

    # Save metadata of seal and its predictions
    # seal_folder = IMAGES_FOLDER + seal_name
    # store_seal_img_metadata(seal_folder, seal_name, processed_images)

    # # Save seal name for reference so we know what seals we have images for
    # store_seal_metadata(IMAGES_FOLDER, seal_name)

    return prediction_images


def process_predictions(img, folder_path, original_image_path):
    processed_images = []
    pattern_predictions = get_pattern_predictions(original_image_path)

    predictions = pattern_predictions['predictions']

    prediction_index = 1
    # Loop through all the predictions
    for prediction in predictions:

        # Only use predicted image if over 10% probability
        if prediction.probability > 0.1:
            cropped_img = crop_image(img, prediction)

            use_image = True
            width, height = cropped_img.size
            if width < MIN_IMG_WIDTH:
                use_image = False
            if height < MIN_IMG_HEIGHT:
                use_image = False

            if use_image:
                normalised_img = normalise_image(cropped_img)

                # Create unique name for img (seal + index + prediction probability)
                predicted_img_name = str(prediction_index) + \
                    '-' + str(prediction.probability) + EXT

                save_normalised_image(predicted_img_name,
                                      normalised_img, folder_path)

                processed_images.append(predicted_img_name)
                prediction_index += 1

    return processed_images


def save_normalised_image(img_name, img, folder_path):
    saved_path = os.path.join(folder_path, img_name)
    img.save(saved_path)

    return saved_path
