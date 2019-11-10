import json
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import Details
from msrest.authentication import CognitiveServicesCredentials

SUPPORTED_IMAGE_FORMATS = ['jpeg', 'jpg', 'png', 'gif', 'bmp']

def supported_image_format(filepath):
    extension = filepath.split(".")[-1].lower()
    return extension in SUPPORTED_IMAGE_FORMATS

def get_client(connection_info):
    if connection_info is None:
        raise ValueError("No Azure credentials provided")
    if connection_info.get('api_key') is None:
        raise ValueError("Bad credentials: API Key not provided")
    if connection_info.get('azure_location') is None:
        raise ValueError("Bad credentials: Azure location not provided")
    endpoint = "https://{}.api.cognitive.microsoft.com/".format(connection_info.get('azure_location'))
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(connection_info.get("api_key")))

def detect_objects(image_file, client):
    row = {}
    response = client.detect_objects_in_stream(image_file)
    image_pil = Image.open(image_file)
    bbox_list = []
    for obj in response.objects:
        bbox_list.append({
            "label": obj.object_property,
            "score": obj.confidence,
            "top": obj.rectangle.y / image_pil.height,
            "left": obj.rectangle.x  / image_pil.width,
            "height": obj.rectangle.h / image_pil.height,
            "width": obj.rectangle.w / image_pil.width
        })
    if len(bbox_list):
        row["detected_objects"] = json.dumps(bbox_list)
    return row, response, bbox_list


def detect_brands(image_file, client):
    row = {}
    response = client.analyze_image_in_stream(image_file, [VisualFeatureTypes.brands])
    image_pil = Image.open(image_file)
    bbox_list = []
    for obj in response.brands:
        bbox_list.append({
            "label": obj.name,
            "score": obj.confidence,
            "top": obj.rectangle.y / image_pil.height,
            "left": obj.rectangle.x  / image_pil.width,
            "height": obj.rectangle.h / image_pil.height,
            "width": obj.rectangle.w / image_pil.width
        })
    if len(bbox_list):
        row["detected_brands"] = json.dumps(bbox_list)
    return row, response, bbox_list


def describe_image(image, client, language='en', max_tags=5):
    row = {}
    visual_features = [VisualFeatureTypes.categories, VisualFeatureTypes.description]
    response = client.analyze_image_in_stream(image, visual_features, language=language)
    categories = []
    for cat in response.categories:
        categories.append(cat.name)
    row["predicted_categories"] = json.dumps(categories)
    if len(response.description.captions):
        row["predicted_caption"] = response.description.captions[0].text
    row["predicted_tags"] = json.dumps(response.description.tags[0:max_tags])
    return row, response


def detect_landmarks(image_file, client):
    row = {}
    response = client.analyze_image_in_stream(image, details=Details.landmarks)
    landmarks = []
    landmarks_names = []
    for cat in response.categories:
        if cat.detail is not None and cat.detail.landmarks is not None:
            for lm in cat.detail.landmarks:
                if lm.name not in landmarks_names:
                    landmarks_names.append(lm.name)
                    landmarks.append({'name': lm.name, 'confidence': lm.confidence})
    if len(landmarks):
        row["landmarks"] = json.dumps(landmarks)
    return row, response


def detect_adult_content(image, client):
    row = {}
    response = client.analyze_image_in_stream(image, [VisualFeatureTypes.adult])
    row["is_adult_content"] = response.adult.is_adult_content
    row["adult_score"] = response.adult.adult_score
    row["is_suggestive_content"] = response.adult.is_racy_content
    row["suggestive_score"] = response.adult.racy_score
    row["is_violent_content"] = response.adult.is_gory_content
    row["violence_score"] = response.adult.gore_score
    return row, response
