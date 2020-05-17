#-*- coding: utf-8 -*-
import sys
from Gatherer import Gatherer
from Builder import Builder

def main():
    name = "wallpapers"
    model = "selfie"
    segmentSize = 50
    grain = 20

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



if __name__ == "__main__":
    main()
