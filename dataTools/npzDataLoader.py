import glob
import numpy as np
import time
import cv2
from PIL import Image
from scipy.io import loadmat
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from torchvision.utils import save_image
from utilities.customUtils import *
from dataTools.dataNormalization import *
from dataTools.customTransform import *
import os
class npzDatasetReader(Dataset):
    def __init__(self, image_list, imagePathGT, height, width, transformation=True):
        self.image_list = image_list
        self.imagePathGT = imagePathGT
        self.transformLR = transforms
        self.imageH = height
        self.imageW = width
        self.normalize1 = transforms.Normalize(normMean(1), normStd(1))
        self.normalize12 = transforms.Normalize(normMean(12), normStd(12))

        self.transformHRGT = transforms.Compose([
						])

    
        self.transformRI = transforms.Compose([
                                                AddGaussianNoise(0, 0.02, pov=1),
                                            ])

    def __len__(self):
        return (len(self.image_list))
    
    def __getitem__(self, i):
        # Read Images
        #print ("print i",i, i+1)
        npz = np.load(self.image_list[i])
        raw = torch.tensor(npz["raw"]).float() / 255.0
        gt = torch.tensor(npz["gt"]).float() / 255.0

        self.inputImage = self.normalize1(self.transformRI(raw))
        self.gtImageHR = self.normalize12(gt) #self.gtImage #self.transformHRGT(self.gtImage)

        #print (self.gtImageHR.max(), self.gtImageHR.min(), self.inputImage.max(), self.inputImage.min())

        return self.inputImage, self.gtImageHR
