#-*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image
import json

class Builder():

    def __init__(self, name, model, segmentSize):
        self.model = model
        self.segmentSize = segmentSize
        self.name = name
        self.Imagefolder = "../Catalogue/Images/" + name + "/"
        self.outputFolder = "../Output/" + model + "/"

    def colorComparator(color1, color2):
        red = ((255 - abs(int(color1[0])-(int(color2[0]))))/255)*100
        green = ((255 - abs(int(color1[1])-(int(color2[1]))))/255)*100
        blue = ((255 - abs(int(color1[2])-(int(color2[2]))))/255)*100
        return int((red + green + blue)/3) # indicates the correlation between the 2 images

    def outputImageBuilder(self):

        # creating paths
        outputPath = Path(self.outputFolder)
        if not outputPath.exists():
            print("Creating " + str(self.outputFolder) + "...")
            rootPath.mkdir()
        imagesInfoPath = Path("../Catalogue/ImagesInfo/" + self.name + "/")
        modelPath = Path("../Catalogue/Images/models/" + self.model + "/")
        modelInfoPath = Path("../Catalogue/ImagesInfo/" + self.model + "/")

        # inspecting information file of model
        jsonImages = None
        jsonModel = None
        with imagesInfoPath.open() as json_file:
            jsonImages = json.load(json_file)
        with modelInfoPath.open() as json_file:
            jsonModel = json.load(json_file)

        # creating the output image canvas
        canvasWidth = self.segmentSize*len(list(jsonModel[0].values())[0])
        canvasHeight = self.segmentSize*len(jsonModel)
        outputImage = Image.new('RGB', (canvasWidth, canvasHeight))

        # loopping over segments of model image to compare rgb values with images in catalogue
        x, y = 0, 0
        for raw in jsonModel:
            for segment in list(raw.values())[0]:
                modelRGB_value = list(segment.values())[0]
                bestImage = ""
                bestSimilar = 0
                # lopping over every image in the catalogue
                for image in jsonImages:
                    imageRGB_value = list(list(image.values())[0].values())[0]
                    similarity = colorComparator(modelRGB_value, imageRGB_value)
                    if similarity > bestSimilar:
                        bestImage = list(image.keys())[0]
                selectedImage = Image.open(self.Imagefolder + bestImage)
                outputImage.paste(selectedImage, (x, y))
                x += self.segmentSize
            x = 0
            y += self.segmentSize
        outputImage.save(self.outputFolder + str(model) + ".png")
        print("Process finished! Please go to output folder, file name is: " + str(model) + ".png")








pass
