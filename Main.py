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

# GetMaskForLiversSegmentation(DataPreparation.readNrrdToImage(folder=test0,saveImageToNrrd=False))
#
# inputImage1 = DataPreparation.readDICOMSerieToImage(folder=test, saveImageToNrrd=False)
#
# ed = sed3.sed3(inputImage1)
# ed.show()
inputImage2 = DataPreparation.readNrrdToImage(folder=test0,saveImageToNrrd=False)

rg = VesselSegmentation.RegionGrow(inputImage2)
writer=sitk.ImageFileWriter()
writer.SetFileName('C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/RegionGrow.nrrd')
writer.Execute(rg)

ff = VesselSegmentation.FrangiFilters(inputImage2)
writer.SetFileName('C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/FrangiFilters.nrrd')
writer.Execute(ff)

sm = VesselSegmentation.TresholdBySeedsMean(inputImage2)
writer.SetFileName('C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/MeanValueOfSeedsThreshold.nrrd')
writer.Execute(sm[1])

itkV = VesselSegmentation.GetVesselsFromITK(inputImage2)
writer.SetFileName('C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/ITKRegistrationHessian.nrrd')
writer.Execute(itkV)

# DataPreparation.saveImageAsNrrd(rg,'test',outputFolder='C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/', useTimeStampName=True)
# GetSeedForLiversSegmentation(inputImage1)
print '====END==='