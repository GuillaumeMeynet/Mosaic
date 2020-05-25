#-*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image
import json
import ast
import progressbar

class Builder():

    def __init__(self, name, model, segmentSize):
        self.model = model
        self.segmentSize = segmentSize
        self.name = name
        self.imagesInfoFolder = "../Catalogue/Images/imagesInfo/"
        self.modelFolder = "../Catalogue/Images/models/"
        self.folder300px = "../Catalogue/Images/" + name + "/Resized/"
        self.imagesFolder = "../Catalogue/Images/"
        self.outputFolder = "../Output/"

    def colorComparator(self, color1, color2):
        red = ((255 - abs(int(color1[0])-(int(color2[0]))))/255)*100
        green = ((255 - abs(int(color1[1])-(int(color2[1]))))/255)*100
        blue = ((255 - abs(int(color1[2])-(int(color2[2]))))/255)*100
        return int((red + green + blue)/3) # indicates the correlation between the 2 images

    def outputImageBuilder(self):

        # creating paths
        outputPath = Path(self.outputFolder)
        imagesInfoPath = Path(self.imagesInfoFolder + self.name + ".json")
        modelPath = Path(self.modelFolder + self.model + "/")
        modelInfoPath = Path(self.imagesInfoFolder + self.model + ".json")

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
        maxValue = len(jsonModel)*len(list(jsonModel[0].values())[0])
        bar = progressbar.ProgressBar(maxval=maxValue, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        print("Creating output image...")
        bar.start()
        i=0
        for raw in jsonModel:
            for segment in list(raw.values())[0]:
                modelRGB_value = list(segment.values())[0]
                bestImage = ""
                bestSimilar = 0
                # lopping over every image in the catalogue
                for image in jsonImages:
                    imageRGB_value = list(ast.literal_eval(list(image.values())[0]).values())[0]
                    similarity = self.colorComparator(modelRGB_value, imageRGB_value)
                    if (similarity > bestSimilar):
                        bestSimilar = similarity
                        bestImage = list(image.keys())[0]
                selectedImage = Image.open(self.folder300px + bestImage)
                outputImage.paste(selectedImage, (x, y))
                x += self.segmentSize
                i+=1
                bar.update(i)
            x = 0
            y += self.segmentSize
        bar.finish()
        print("Saving output image... Please wait.")
        outputImage.save(self.outputFolder + str(self.model) + ".png")
        print("Process finished! Please go to output folder, file name is: " + str(self.model) + ".png")








pass
