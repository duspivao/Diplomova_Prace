#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import DataPreparation
import VesselSegmentation
import types
import sed3
import SimpleITK as sitk
import numpy as np
import sys
from mayavi import mlab

# moving = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/PATIENT_DICOM')
# ed = sed3.sed3(moving)
# ed.show()

test0 = 'C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/Reg_8_GaborliversSmall.nrrd'
test = 'test/4-150cc OMNIPAQUE-36663'
test = 'C:/ZCU/DATA_FOR_TEST/MRI/TCGA-LIHC/TCGA-DD-A1EF/07-23-2000-MRI Abd wo-63516/9-Ax spgr-30793'

def GetMaskForLiversSegmentation(image):
        # arrayImage = np.array(sitk.GetArrayFromImage(image))
        caster = sitk.CastImageFilter()
        caster.SetOutputPixelType(sitk.sitkUInt8)
        image = caster.Execute(image)

        ed = sed3.sed3(image)
        ed.show()

        allSeeds = np.where(ed.seeds>0)
        seeds = []

        for i in range(len(allSeeds[0])):
                p = (int(allSeeds[0][i]),int(allSeeds[1][i]),int(allSeeds[2][i]))
                seeds.append(p)

        # print image.GetSize()
        # max1 = 0
        # min1 = image.GetSize()[0]
        # max2 = 0
        # min2 = image.GetSize()[1]
        # max3 = 0
        # min3 = image.GetSize()[2]
        # for seed in allSeeds:
        #         if seed[0] > max1:
        #                 max1 = seed[0]
        #         if seed[0] < min1:
        #                 min1 = seed[0]
        #         if seed[1] > max2:
        #                 max2 = seed[1]
        #         if seed[1] < min2:
        #                 min2 = seed[1]
        #         if seed[2] > max3:
        #                 max3 = seed[2]
        #         if seed[2] < min3:
        #                 min3 = seed[2]
        # imgRes = sitk.GetImageFromArray(sitk.Cast(image, sitk.sitkUInt32))[min1:max1][min2:max2][min3:max3]
        print 'Region grow segmentation'

        regionGrow = sitk.ConnectedThreshold(image, seedList=seeds,
                                lower=50, upper=220)
        # regionGrow = sitk.ConnectedThreshold(sitk.Cast(image,sitk.sitkUInt8),
        #                                      seedList=seeds,
        #                                      lower=50, upper=220)
        writer = sitk.ImageFileWriter()
        outputDirPath = 'C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/Filters_'

        writer.SetFileName(outputDirPath +'liversMaskTest.nrrd')
        writer.Execute(regionGrow)
        print 'Region grow segmentation done'
        ed = sed3.sed3(sitk.RescaleIntensity(regionGrow))
        ed.show()

outPutFolder = 'C:/ZCU/Diplomka/Dataset/01/RESULTS/VesselSegmentation/'

# GetMaskForLiversSegmentation(DataPreparation.readNrrdToImage(folder=test0,saveImageToNrrd=False))
#
# inputImage1 = DataPreparation.readDICOMSerieToImage(folder=test, saveImageToNrrd=False)
#
# ed = sed3.sed3(inputImage1)
# ed.show()
inputImage2 = DataPreparation.readNrrdToImage(folder=test0,saveImageToNrrd=False)

# fixedRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_4_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
# reader = sitk.ImageFileReader()
# reader.SetFileName(fixedRMHD)
# inputImage2 = reader.Execute()

# rg = VesselSegmentation.RegionGrow(inputImage2)
writer=sitk.ImageFileWriter()
# writer.SetFileName(outPutFolder+'RegionGrow.nrrd')
# writer.Execute(rg)
# DataPreparation.showImageInPerspektive(rg)
#
#
#
# ff = VesselSegmentation.FrangiFilters(inputImage2)
# writer.SetFileName(outPutFolder+'FrangiFilters.nrrd')
# writer.Execute(ff)
# DataPreparation.showImageInPerspektive(ff)

sm = VesselSegmentation.TresholdBySeedsMean(inputImage2)
writer.SetFileName(outPutFolder+'MeanValueOfSeedsThreshold.nrrd')
writer.Execute(sitk.RescaleIntensity(sitk.GetImageFromArray(sm[1])))
DataPreparation.showImageInPerspektive(sm[1])

# itkV = VesselSegmentation.GetVesselsFromITK(inputImage2)
# writer.SetFileName(outPutFolder+'ITKRegistrationHessian.nrrd')
# writer.Execute(itkV)
# DataPreparation.showImageInPerspektive(itkV)

# DataPreparation.saveImageAsNrrd(rg,'test',outputFolder='C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/', useTimeStampName=True)
# GetSeedForLiversSegmentation(inputImage1)
print '====END==='