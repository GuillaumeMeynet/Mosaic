#-*- coding: utf-8 -*-
import sys
from Gatherer import Gatherer
from Builder import Builder

def main():
    name = "wallpapers"
    model = "Kappa"
    segmentSize = 200

    # initialization of classes
    GathererClass = Gatherer(name, model, segmentSize)
    BuilderClass = Builder(name, model, segmentSize)

    # initialization of folder with Gatherer.initFolder function
    GathererClass.initFolder()

    



if __name__ == "__main__":
    main()
