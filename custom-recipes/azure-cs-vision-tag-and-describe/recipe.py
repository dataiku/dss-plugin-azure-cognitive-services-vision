import os
import json
import dataiku
import pandas as pd
from dataiku.customrecipe import *
from dku_azure_cs import *
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes

#==============================================================================
# SETUP
#==============================================================================

connection_info = get_recipe_config().get('connection_info')
language = get_recipe_config().get('language', 'en')

input_folder_name = get_input_names_for_role('input-folder')[0]
input_folder = dataiku.Folder(input_folder_name)
input_folder_path = input_folder.get_path()

output_dataset_name = get_output_names_for_role('output-dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

#==============================================================================
# RUN
#==============================================================================

def process_image(image, client):
    row = {}
    visual_features = [VisualFeatureTypes.categories, VisualFeatureTypes.description]
    response = client.analyze_image_in_stream(image, visual_features, language=language)
    categories = []
    for cat in response.categories:
        categories.append(cat.name)
    row["categories"] = json.dumps(categories)
    if len(response.description.captions):
        row["caption"] = response.description.captions[0].text
    row["tags"] = json.dumps(response.description.tags[0:5])
    return row, response

def run(process_image, client):
    rows = []
    for filepath in os.listdir(input_folder_path):
        row = {}
        if supported_image_format(filepath):
            path = os.path.join(input_folder_path, filepath)
            image = open(path, "rb")
            row, response = process_image(image, client)
            row["raw_results"] = json.dumps(response, default=lambda x: x.__dict__)
        else:
            logger.warn("Cannot score file (only JPEG, JPG and PNG extension are supported): " + filepath)
        row["file_name"] = filepath
        rows.append(row)
    return pd.DataFrame(rows)

client = get_client(connection_info)
df = run(process_image, client)

output_dataset.write_with_schema(df)
