# Microsoft Azure Cognitive Services - Vision


## Plugin information

This Dataiku DSS plugin provides several tools to interact with the Computer Vision API from [Microsoft Azure Cognitive Services API](https://azure.microsoft.com/en-us/services/cognitive-services/).

The Computer Vision API provides state-of-the-art algorithms to process images and return information.
For example, it can be used to determine if an image contains mature content, or it can be used to find all the faces in an image.
It also has other features like estimating dominant and accent colors, categorizing the content of images, and describing an image
with complete English sentences. Additionally, it can also intelligently generate images thumbnails for displaying large images effectively.
[Read the documentation](https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fc)
for more information.

## Prerequisites
In order to use the Plugin, you will need:

* an Azure account
* proper credentials (access tokens) to interact with the service:
	1. Sign in to [Azure portal](https://portal.azure.com/).
	2. In the left navigation pane, select **All services**.
	3. In Filter, type Cognitive Services. Add the **Computer Vision** service
	4. Select a plan
* make sure you know in **which Azure region the services are valid**, the Plugin will need this information to get authenticated

### Plugin components

* [Image Analysis](https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa):
this operation extracts a rich set of visual features based on the image content.
* [Image Description](https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fe):
this operation generates a description of an image in human readable language with complete sentences.
The description is based on a collection of content tags, which are also returned by the operation.
More than one description can be generated for each image. Descriptions are ordered by their confidence score. All descriptions are in English.
* [Image Tagging](https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1ff):
this operation generates a list of words, or tags, that are relevant to the content of the supplied image.
The Computer Vision API can return tags based on objects, living beings, scenery or actions found in images.
