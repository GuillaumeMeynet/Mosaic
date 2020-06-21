#-*- coding: utf-8 -*-
import sys
from Gatherer import Gatherer
from Builder import Builder
from pathlib import Path
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import shutil
from time import sleep

def main():

    # initialization of model image
    model = initModel()

    name = "Kaamelott"
    if (model == ""): model = "kaamlott2"
    segmentSize = 40
    grain = 4



    # initialization of classes
    GathererClass = Gatherer(name, model, segmentSize, grain)
    BuilderClass = Builder(name, model, segmentSize)

    # initialization of folder with Gatherer.initFolder function
    GathererClass.initFolder()

    # initialization of information gatherer on catalogue images
    GathererClass.smallColorDetector()

    # initialization of information gatherer on model image
    GathererClass.modelColorDetector()

    # now that we gathered all information we needed
    # we build the output image
    BuilderClass.outputImageBuilder()

def initModel():
    imageFolder = "../Images/"
    root = Tk()
    root.withdraw()
    root.update()
    filename = filedialog.askopenfilename(title="Select a png file", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    if(filename == ""): return ""
    originalPath = Path(filename)
    modelPath = Path(imageFolder + "/models/" + originalPath.stem + ".png")
    shutil.copy(str(originalPath), str(modelPath))
    return originalPath.stem

if __name__ == "__main__":
    main()
