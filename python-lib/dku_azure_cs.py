from azure.cognitiveservices.vision.computervision import ComputerVisionClient
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
