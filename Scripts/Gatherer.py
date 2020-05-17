#-*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image
import json
import statistics
import os

class Gatherer():

    def __init__(self, name, model, segmentSize, pixelSize):
        self.name = name
        self.segmentSize = segmentSize
        self.pixelSize = pixelSize
        self.imageFolder = "../Catalogue/Images/"
        self.folder = "../Catalogue/Images/" + name + "/"
        rootPath = Path(self.folder)
        self.model = model
        if not rootPath.exists():
            print("Creating " + str(self.folder) + "...")
            rootPath.mkdir()

    def initFolder(self):
        originalPath = Path(self.folder + "/Originals/")
        print(str(originalPath))
        croppedPath = Path(self.folder + "/Resized/")

        # create folder if doesn't exist
        if not originalPath.exists():
            print("Creating " + str(originalPath) + "...")
            originalPath.mkdir()

        if not croppedPath.exists():
            print("Creating " + str(croppedPath) + "...")
            croppedPath.mkdir()

        # check if directory is empty
        try:
            if not list(originalPath.glob('*')):
                raise ValueError("The directory is empty or has just been created.")
        except ValueError:
            exit(str(ValueError))

        # get a list of all JPG and convert them to PNG
        jpgList = list(originalPath.glob('*.jpg'))
        if(jpgList != []):
            for jpg in jpgList:
                image = Image.open(str(jpg))
                print("saving " + jpg.stem + ".png !")
                image.save(str(originalPath) + "/" + jpg.stem + ".png")
                print("deleting " + jpg.stem + ".jpg !")
                os.remove(jpg)

        # resize all images to widthSize x heightSize px
        pngList = list(originalPath.glob('*.png'))
        widthSize = heightSize = self.segmentSize
        for png in pngList:
            print("cropping " + png.stem + " to " + str(self.segmentSize) + " px...")
            resizedImage = self.cropImage(png, widthSize, heightSize)

            # the image now has a resolution of self.segmentSize x self.segmentSize px
            resizedImage.save(str(croppedPath) + "/" + png.stem + ".png")

    def cropImage(self, png, widthSize, heightSize):
        image = Image.open(png)
        resizedImage = None
        if (image.size[0] > image.size[1]):
            heightPercent = heightSize/image.size[1]
            widthSize = int(heightPercent*image.size[0])
            resizedImage = image.resize((widthSize,heightSize), Image.ANTIALIAS)
            left = (resizedImage.size[0] - heightSize)/2
            top = 0
            right = (resizedImage.size[0] - heightSize)/2 + heightSize
            bottom = resizedImage.size[1]
            resizedImage = resizedImage.crop((left, top, right, bottom))
        else:
            widthPercent = widthSize/image.size[0]
            heightSize = int(widthPercent*image.size[1])
            resizedImage = image.resize((widthSize,heightSize), Image.ANTIALIAS)
            left = 0
            top = (resizedImage.size[1] - widthSize)/2
            right = resizedImage.size[0]
            bottom = (resizedImage.size[1] - widthSize)/2 + widthSize
            resizedImage = resizedImage.crop((left, top, right, bottom))
        return resizedImage

    def colorDetector(self, rgb_im, jsonImage, scale, size = None, x = 0, y = 0):
        if size is None:
            size = rgb_im.size[0]
        red = []
        blue = []
        green = []
        jsonImage["RGB"] = []
        for raw in range(y, y + size, scale):
            for column in range(x, x + size, scale):
                rgbValues = rgb_im.getpixel((column, raw))
                red.append(rgbValues[0])
                blue.append(rgbValues[1])
                green.append(rgbValues[2])
        jsonImage["RGB"].append(str(int(statistics.mean(red))))
        jsonImage["RGB"].append(str(int(statistics.mean(green))))
        jsonImage["RGB"].append(str(int(statistics.mean(blue))))
        return jsonImage # type of JSON : {'RGB': ['255', '0', '0']}

    def resizeMiddle(self, rgb_image, pixelSize):
        deltaWidth = rgb_image.size[0] % pixelSize
        deltaHeight = rgb_image.size[1] % pixelSize

        # resize image to fit pixelSize x pixelSize cutting
        if deltaWidth % 2:
            rgb_image = rgb_image.crop((int(deltaWidth/2) + 1, 0, rgb_image.size[0] - int(deltaWidth/2), rgb_image.size[1]))
            print("new:", rgb_image.size[0])
        else:
            rgb_image = rgb_image.crop((deltaWidth/2, 0, rgb_image.size[0] - deltaWidth/2, rgb_image.size[1]))
        if deltaHeight % 2:
            rgb_image = rgb_image.crop((0, int(deltaHeight/2) + 1, rgb_image.size[0], rgb_image.size[1] - int(deltaHeight/2)))
        else:
            rgb_image = rgb_image.crop((0, deltaHeight/2, rgb_image.size[0], rgb_image.size[1] - deltaHeight/2))

        return rgb_image



    def smallColorDetector(self):
        imagesPath = Path(self.folder + "/Resized/")
        ImagesInfoPath = Path(self.imageFolder + "/imagesInfo/")
        if not ImagesInfoPath.exists():
            print("Creating " + str(ImagesInfoPath) + "...")
            ImagesInfoPath.mkdir()
        imagesList = list(imagesPath.glob('*.png'))

        imagesInfoJson = json.loads('[]') # gloal JSON


        for image in imagesList:
            im = Image.open(image)
            rgb_im = im.convert('RGB')
            imageInfoJson = json.loads('{}') # focus JSON
            imageInfoJson[str(image.stem) + ".png"] = str(self.colorDetector(rgb_im, json.loads('{}'), 5))
            imagesInfoJson.append(imageInfoJson)

        # JSON at this point : [{'image1': {'RGB': ['255', '0', '0']}},
        #                       {'image2': {'RGB': ['0', '255', '0']}}]

        # storage of json in ImagesInfo json file
        with open(str(ImagesInfoPath) + "/" + str(self.name) + ".json", "w") as outfile:
            json.dump(imagesInfoJson, outfile)

    def modelColorDetector(self):
        modelPath = Path(self.imageFolder + "/models/")
        ImagesInfoPath = Path(self.imageFolder + "/imagesInfo/")

        if not ImagesInfoPath.exists():
            print("Creating " + str(ImagesInfoPath) + "...")
            ImagesInfoPath.mkdir()
        if not modelPath.exists():
            print("Creating " + str(modelPath) + "...")
            modelPath.mkdir()
        modelImagePath = Path(self.imageFolder + "/models/" + self.model + ".png")
        try:
            if not modelImagePath.is_file():
                raise ValueError("The model image does not exist, exiting...")
        except ValueError:
            exit(str(ValueError))

        pixelSize = self.pixelSize
        image = Image.open(modelImagePath)
        rgb_image = self.resizeMiddle(image.convert('RGB'), pixelSize)
        jsonImages = json.loads('[]') # global JSON
        rawNbr = 1
        for raw in range(0, rgb_image.size[1], pixelSize):
            jsonRaw = json.loads('{}')
            jsonRaw["raw" + str(rawNbr)] = []
            for column in range(0, rgb_image.size[0], pixelSize):
                jsonRaw["raw" + str(rawNbr)].append(self.colorDetector(rgb_image, json.loads('{}'), 2, pixelSize, column, raw))
            rawNbr+=1
            jsonImages.append(jsonRaw) # append each raw in the global JSON

        with open(str(ImagesInfoPath) + "/" + self.model + ".json", "w") as outfile:
            json.dump(jsonImages, outfile)
