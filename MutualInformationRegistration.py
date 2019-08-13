#!/usr/bin/env python
import SimpleITK as sitk
import time
import DataPreparation
import sed3
import cv2
import numpy as np
from skimage.measure import compare_ssim
import scipy

def resample(image, transform):
    reference_image = image
    interpolator = sitk.sitkCosineWindowedSinc
    default_value = 100.0
    return sitk.Resample(image, reference_image, transform,
                         interpolator, default_value)
def main():
    startTime = time.time()
    outputDirPath = 'C:/ZCU/Diplomka/Dataset/04/RESULTS/Res_Conv'
    writer = sitk.ImageFileWriter()
    # moving = DataPreparation.readDICOMSerieToImage('C:/ZCU/DATA_FOR_TEST/MRI/TCGA-LIHC/TCGA-K7-AAU7/07-31-2001-MRI ABDOMEN WWO CONTRAST-59507/1201-C AX 3D LATE PHAS20CC MAGNEVISTE-50651')
    # fixedR = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/PATIENT_DICOM')
    # movingR = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.7/PATIENT_DICOM')
    # fixMask = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/MASKS_DICOM/liver')
    # movMas =  DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.7/MASKS_DICOM/liver')

    fixedRMHD = 'C:/ZCU/Diplomka/Dataset/01/october-massachusetts-helium-queen_ack-wyoming_4_ca45536493525b615615f4d703c108e994b2dc6ec8b33e58d64c5cd6a92a12f2_v0.mhd'
    fixedRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_4_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
    fixedRMHD = 'C:/ZCU/DATA_FOR_TEST/TCGA-LIHC/TCGA-BC-A10X/11-22-1992-MRI ABD WWO CONT-49239/11-LIVER-GAD-ENHANCEMENTT1F-68307'
    fixedRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_4_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
    fixedRMHD = 'C:/ZCU/Diplomka/Dataset/04/hamper-carpet-earth-jersey_lake-fanta_601_447041836b6cf9ef3b328041cf99cac6c8308e90c46d437db62f6c8689fa6b58_v0.mhd'
    reader = sitk.ImageFileReader()
    reader.SetFileName(fixedRMHD)
    fixed = reader.Execute()

    movingRMHD = 'C:/ZCU/Diplomka/Dataset/01/october-massachusetts-helium-queen_ack-wyoming_7_ca45536493525b615615f4d703c108e994b2dc6ec8b33e58d64c5cd6a92a12f2_v0.mhd'
    movingRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_7_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
    movingRMHD = 'C:/ZCU/DATA_FOR_TEST/TCGA-LIHC/TCGA-BC-A10X/03-29-1993-CT ABDOMEN  WCONTRAST-43286/4-150cc OMNIPAQUE-36663'
    movingRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_7_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
    movingRMHD = 'C:/ZCU/Diplomka/Dataset/04/hamper-carpet-earth-jersey_lake-fanta_501_447041836b6cf9ef3b328041cf99cac6c8308e90c46d437db62f6c8689fa6b58_v0.mhd'
    # fixedR = DataPreparation.readNrrdToImage(fixedRMHD)
    # fixedR = DataPreparation.readNrrdToImage(fixedRMHD)
    reader.SetFileName(movingRMHD)
    moving = reader.Execute()
    # print movingBR.GetSize()
    # size = [512,512,101]
    # movingAr = sitk.GetArrayFromImage(movingBR)
    # M = cv2.getRotationMatrix2D((512./2.,512./2.), -7., 1.)
    # moving = movingAr.copy()
    #
    #
    # for slice in range(size[2]):
    #     moving[slice][:][:] = cv2.warpAffine(movingAr[slice][:][:], M, (movingAr.shape[1], movingAr.shape[2]))
    # moving = sitk.GetImageFromArray(moving)
    # ed = sed3.sed3(moving)
    # ed.show()
    # X = compare_ssim(sitk.GetArrayFromImage(fixed), sitk.GetArrayFromImage(moving), full=True)
    # # ed = sed3.sed3(sitk.GetImageFromArray(X[1]))
    # # ed.show()
    # print 'Difference Score BEFORE:'+str(X[0])
    # writer.SetFileName(outputDirPath + 'DifferenceBefore.nrrd')
    # writer.Execute(sitk.GetImageFromArray(X[1]))


    # fixed = DataPreparation.maskToLivers(fixedR, fixMask)
    # moving = DataPreparation.maskToLivers(movingR, movMas)
    def observer(method) :
        print("{0:3} = {1:10.5f} : {2}".format(method.GetOptimizerIteration(),
                                               method.GetMetricValue(),
                                               method.GetOptimizerPosition()))




    print("====Image registrion DICOM files====")
    #
    # resampleFilter = sitk.ResampleImageFilter()
    # resampleFilter.SetSize(fixed.GetSize()*(1/3))
    # resampleFilter.SetInterpolator(sitk.sitkGaussian)
    # resampleFilter.SetOutputSpacing([1,1,1])
    # fixedResampled = resampleFilter.Execute(fixed)
    # resampleFilter.SetSize(moving.GetSize()/3)
    # movingResampled = resampleFilter.Execute(moving)




    print 'Smoothing'
    fixImgSmooth = sitk.CurvatureFlow(image1=fixed,
                                      timeStep=0.35,
                                      numberOfIterations=10)
    movImgSmooth = sitk.CurvatureFlow(image1=fixed,
                                      timeStep=0.35,
                                      numberOfIterations=10)

    print 'Smoothing ENDED'
    # movImgSmooth = moving
    # fixImgSmooth = fixed
    resample = sitk.ResampleImageFilter()
    resample.SetReferenceImage(fixImgSmooth)
    initial_transform = sitk.CenteredTransformInitializer(sitk.Cast(fixImgSmooth, movImgSmooth.GetPixelID()),
                                                          movImgSmooth,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)

    registration_method = sitk.ImageRegistrationMethod()

    # registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=255)
    # registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    # registration_method.SetMetricSamplingPercentage(0.01)
    registration_method.SetMetricAsCorrelation()


    registration_method.SetInterpolator(sitk.sitkGaussian)
    # registration_method.SetInterpolator(sitk.sitkLinear)

    registration_method.SetOptimizerAsGradientDescentLineSearch(learningRate=2.0, numberOfIterations=100)
    registration_method.SetOptimizerScalesFromPhysicalShift()
    # registration_method.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
    #                        numberOfIterations=100,
    #                        maximumNumberOfCorrections=5,
    #                        maximumNumberOfFunctionEvaluations=1000,
    #                        costFunctionConvergenceFactor=1e+7)
    registration_method.AddCommand( sitk.sitkIterationEvent, lambda: observer(registration_method) )

    registration_method.SetInitialTransform(initial_transform, inPlace=False)
    final_transform_v1 = registration_method.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
                                                     sitk.Cast(movImgSmooth, sitk.sitkFloat32))

    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
    print('Final metric value: {0}'.format(registration_method.GetMetricValue()))

    print(final_transform_v1)



    writer.SetFileName(outputDirPath + 'Fixed_Smoothed.nrrd')
    writer.Execute(fixImgSmooth)
    writer.SetFileName(outputDirPath + 'Moving_Smoothed.nrrd')
    writer.Execute(fixImgSmooth)

    resample = sitk.ResampleImageFilter()
    resample.SetReferenceImage(fixed)

    # SimpleITK supports several interpolation options, we go with the simplest that gives reasonable results.
    resample.SetInterpolator(sitk.sitkLinear)
    resample.SetTransform(final_transform_v1)
    movingAfterTransform = resample.Execute(moving)
    sitk.WriteImage(movingAfterTransform, outputDirPath +'MovingAfterTransform' + '.nrrd')
    sitk.WriteTransform(final_transform_v1, outputDirPath+ 'transform' + '.tfm')


    X = compare_ssim(sitk.GetArrayFromImage(fixed), sitk.GetArrayFromImage(movingAfterTransform), full=True)
    # ed = sed3.sed3(sitk.GetImageFromArray(X[1]))
    # ed.show()
    # print 'Difference Score AFTER:'+str(X[0])
    # writer.SetFileName(outputDirPath + 'DifferenceAfter.nrrd')
    # writer.Execute(sitk.GetImageFromArray(X[1]))


    # writer.SetFileName(outputDirPath + '/' + '03.nrrd')
    # writer.Execute(resample.Execute(moving))

    simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(resample.Execute(moving)), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
    # sitk.Show(cimg, "RESULT")

    outFileName = 'ResultOfRegistration.nrrd'

    writer.SetFileName(outputDirPath + outFileName)
    writer.Execute(cimg)

    stopTime = time.time()
    print stopTime-startTime

    print "====END OF REGISTRATION====="