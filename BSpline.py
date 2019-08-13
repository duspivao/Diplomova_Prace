#!/usr/bin/env python
import SimpleITK as sitk
import time
import DataPreparation
import sed3

outputDirPath = 'C:/ZCU/Diplomka/Dataset/01/RESULTS/Res_BSpline'

# fixed = DataPreparation.readDICOMSerieToImage('C:/ZCU/DATA_FOR_TEST/MRI/TCGA-LIHC/TCGA-K7-AAU7/07-31-2001-MRI ABDOMEN WWO CONTRAST-59507/1201-C AX 3D LATE PHAS20CC MAGNEVISTE-50651')
# moving = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/PATIENT_DICOM')
#
# fixedR = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/PATIENT_DICOM')
# movingR = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.7/PATIENT_DICOM')
# fixMask = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/MASKS_DICOM/liver')
# movMas =  DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.7/MASKS_DICOM/liver')
#
# fixed = DataPreparation.maskToLivers(fixedR, fixMask)
# moving = DataPreparation.maskToLivers(movingR, movMas)


startTime = time.time()

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
reader = sitk.ImageFileReader()
reader.SetFileName(fixedRMHD)
fixed = reader.Execute()

movingRMHD = 'C:/ZCU/Diplomka/Dataset/01/october-massachusetts-helium-queen_ack-wyoming_7_ca45536493525b615615f4d703c108e994b2dc6ec8b33e58d64c5cd6a92a12f2_v0.mhd'
movingRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_7_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
movingRMHD = 'C:/ZCU/DATA_FOR_TEST/TCGA-LIHC/TCGA-BC-A10X/03-29-1993-CT ABDOMEN  WCONTRAST-43286/4-150cc OMNIPAQUE-36663'
movingRMHD = 'C:/ZCU/Diplomka/Dataset/02/summer-eight-blossom-table_diet-kitten_7_45280cdef17c50e470ef9f9990a3d6c9ed15c1e35e84bd43611cfa014abee817_v0.mhd'
# fixedR = DataPreparation.readNrrdToImage(fixedRMHD)
reader.SetFileName(movingRMHD)
moving = reader.Execute()

# moving = DataPreparation.readDICOMSerieToImage(movingRMHD)
# fixed = DataPreparation.readDICOMSerieToImage(fixedRMHD)
def observer(method) :
    print("{0:3} = {1:10.5f}".format(method.GetOptimizerIteration(),
                                     method.GetMetricValue()))

print("====Image registrion DICOM files====")
print 'Smoothing'
fixImgSmooth = sitk.CurvatureFlow(image1=fixed,
                                  timeStep=0.35,
                                  numberOfIterations=10)
movImgSmooth = sitk.CurvatureFlow(image1=moving,
                                  timeStep=0.35,
                                  numberOfIterations=10)
print 'Smoothing ENDED'
# fixImgSmooth = fixMask
# movImgSmooth = movMas
# ed = sed3.sed3(movMas)
# ed.show()
# print 'Translation transform'
# reg1 = sitk.ImageRegistrationMethod()
# reg1.SetInterpolator(sitk.sitkLinear)
# reg1.SetMetricAsMattesMutualInformation(numberOfHistogramBins=255)
# reg1.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-3,
#                        # numberOfIterations=50,
#                        maximumNumberOfCorrections=2,
#                        maximumNumberOfFunctionEvaluations=100,
#                        costFunctionConvergenceFactor=1e+7)
# reg1.SetInitialTransform(sitk.CenteredTransformInitializer(sitk.Cast(fixImgSmooth, movImgSmooth.GetPixelID()),
#                                                       movImgSmooth,
#                                                       sitk.Euler3DTransform(),
#                                                       sitk.CenteredTransformInitializerFilter.GEOMETRY),)
#
# init_transform_res = reg1.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
#                                                  sitk.Cast(movImgSmooth, sitk.sitkFloat32))
# res = sitk.ResampleImageFilter()
# res.SetReferenceImage(fixImgSmooth)
# res.SetInterpolator(sitk.sitkLinear)
# res.SetTransform(init_transform_res)
# resampledImage = res.Execute(movImgSmooth)
# ed = sed3.sed3(resampledImage)
# ed.show()
# print 'Translation transform ended'

print 'BSpline transform'
# initial_transform1 = sitk.CenteredTransformInitializer(sitk.Cast(fixImgSmooth, movImgSmooth.GetPixelID()),
#                                                       resampledImage,
#                                                       sitk.BSplineTransform,
#                                                       sitk.CenteredTransformInitializerFilter.GEOMETRY)
resampleFilter = sitk.ResampleImageFilter()
resampleFilter.SetReferenceImage(fixImgSmooth)

transformDomainMeshSize = [8]*fixImgSmooth.GetDimension()
initial_transform = sitk.BSplineTransformInitializer(fixImgSmooth,
                                      transformDomainMeshSize )
print("Initial Parameters:");
print(initial_transform.GetParameters())
registration_method = sitk.ImageRegistrationMethod()
# registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=255)
# registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
# registration_method.SetMetricSamplingPercentage(0.1)
registration_method.SetMetricAsCorrelation()
# registration_method.SetInterpolator(sitk.sitkGaussian)
registration_method.SetInterpolator(sitk.sitkLinear)

# registration_method.SetOptimizerAsGradientDescentLineSearch(learningRate=2.0, numberOfIterations=500)
# registration_method.SetOptimizerScalesFromPhysicalShift()
registration_method.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                       # numberOfIterations=100,
                       maximumNumberOfCorrections=5,
                       maximumNumberOfFunctionEvaluations=500,
                       costFunctionConvergenceFactor=1e+7)
# registration_method.SetOptimizerAsGradientDescentLineSearch(learningRate=2.0, numberOfIterations=100)
# registration_method.SetOptimizerScalesFromPhysicalShift()
registration_method.AddCommand( sitk.sitkIterationEvent, lambda: observer(registration_method) )

registration_method.SetInitialTransform(initial_transform, True)
final_transform_v1 = registration_method.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
                                                 sitk.Cast(movImgSmooth, sitk.sitkFloat32))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))

print(final_transform_v1)
print 'BSpline transform finished'
writer = sitk.ImageFileWriter()


writer.SetFileName(outputDirPath + 'BSpline_Fixed_Smoothed.nrrd')
writer.Execute(fixImgSmooth)
writer.SetFileName(outputDirPath + 'BSpline_Moving_Smoothed.nrrd')
# writer.Execute(movImgSmooth)

resample = sitk.ResampleImageFilter()
resample.SetReferenceImage(fixed)

# SimpleITK supports several interpolation options, we go with the simplest that gives reasonable results.
resample.SetInterpolator(sitk.sitkLinear)
resample.SetTransform(final_transform_v1)
sitk.WriteImage(resample.Execute(moving), outputDirPath+ 'BSpline_MovingAfterTransform' + '.nrrd')
sitk.WriteTransform(final_transform_v1, outputDirPath+ 'BSpline_transform' + '.tfm')

# writer.SetFileName(outputDirPath + '/' + '03.nrrd')
# writer.Execute(resample.Execute(moving))

simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
simg2 = sitk.Cast(sitk.RescaleIntensity(resample.Execute(moving)), sitk.sitkUInt8)
cimg = sitk.Compose(simg1, simg2, simg1 // 4. + simg2 // 4.)
# sitk.Show(cimg, "RESULT")

outFileName = 'BSpline_ResultOfRegistration.mha'

writer.SetFileName(outputDirPath + outFileName)
writer.Execute(cimg)

stopTime = time.time()
print stopTime-startTime

print "====END OF REGISTRATION====="