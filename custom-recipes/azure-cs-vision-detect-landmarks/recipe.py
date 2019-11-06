import os
import json
import dataiku
import pandas as pd
from dataiku.customrecipe import *
from dku_azure_vision import *
from azure.cognitiveservices.vision.computervision.models import Details

#==============================================================================
# SETUP
#==============================================================================

connection_info = get_recipe_config().get('connection_info')

input_folder_name = get_input_names_for_role('input-folder')[0]
input_folder = dataiku.Folder(input_folder_name)
input_folder_path = input_folder.get_path()

output_dataset_name = get_output_names_for_role('output-dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

#==============================================================================
# RUN
#==============================================================================

client = get_client(connection_info)
rows = []
for filepath in os.listdir(input_folder_path):
    row = {}
    row["file_name"] = filepath
    if supported_image_format(filepath):
        path = os.path.join(input_folder_path, filepath)
        image = open(path, "rb")
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
        row["raw_results"] = json.dumps(response, default=lambda x: x.__dict__)
    else:
        logger.warn("Cannot score file (only JPEG, JPG and PNG extension are supported): " + filepath)
    rows.append(row)

output_dataset.write_with_schema(pd.DataFrame(rows))
