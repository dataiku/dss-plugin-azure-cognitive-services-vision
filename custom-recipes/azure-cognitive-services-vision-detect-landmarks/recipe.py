import os
import json
import dataiku
from dataiku.customrecipe import *
from dku_azure_vision import *

#==============================================================================
# SETUP
#==============================================================================

connection_info = get_recipe_config().get('connection_info')
should_output_raw_results = get_recipe_config().get('should_output_raw_results')

input_folder_name = get_input_names_for_role('input_folder')[0]
input_folder = dataiku.Folder(input_folder_name)
input_folder_path = input_folder.get_path()

output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

client = get_client(connection_info)

#==============================================================================
# RUN
#==============================================================================

output_schema = [
    {"name": "file_path", "type": "string"},
    {"name": "landmarks", "type": "string"},
]
if should_output_raw_results:
    output_schema.append({"name": "raw_results", "type": "string"})
output_dataset.write_schema(output_schema)

writer = output_dataset.get_writer()
for filepath in os.listdir(input_folder.get_path()):
    if supported_image_format(filepath):
        with open(os.path.join(input_folder.get_path(), filepath), "rb") as image_file:
            row, response = detect_landmarks(image_file, client)
            if should_output_raw_results:
                row["raw_results"] = json.dumps(response, default=lambda x: x.__dict__)
    else:
        logging.warn("Cannot score file (only JPEG, JPG and PNG extension are supported): " + filepath)
        row = {}
    row["file_path"] = filepath
    writer.write_row_dict(row)

writer.close()
