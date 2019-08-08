#!/usr/bin/env python
import SimpleITK as sitk
import time
import DataPreparation

outputDirPath = 'C:/Users/duso/PycharmProjects/Semestralni_Prace/Registration/Frangis/RegistrationTests/test/Registration_Mutual_'

fixed = DataPreparation.readDICOMSerieToImage('C:/ZCU/DATA_FOR_TEST/MRI/TCGA-LIHC/TCGA-K7-AAU7/07-31-2001-MRI ABDOMEN WWO CONTRAST-59507/1201-C AX 3D LATE PHAS20CC MAGNEVISTE-50651')
moving = DataPreparation.readDICOMSerieToImage('C:/ZCU/3Dircadb1/3Dircadb1.1/PATIENT_DICOM')

def observer(method) :
    print("{0:3} = {1:10.5f} : {2}".format(method.GetOptimizerIteration(),
                                           method.GetMetricValue(),
                                           method.GetOptimizerPosition()))




print("====Image registrion DICOM files====")
print 'Smoothing'
fixImgSmooth = sitk.CurvatureFlow(image1=fixed,
                                  timeStep=0.25,
                                  numberOfIterations=20)
movImgSmooth = sitk.CurvatureFlow(image1=fixed,
                                  timeStep=0.25,
                                  numberOfIterations=20)
print 'Smoothing ENDED'
resample = sitk.ResampleImageFilter()
resample.SetReferenceImage(fixImgSmooth)

initial_transform = sitk.CenteredTransformInitializer(sitk.Cast(fixImgSmooth, movImgSmooth.GetPixelID()),
                                                      movImgSmooth,
                                                      sitk.Euler3DTransform(),
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

registration_method = sitk.ImageRegistrationMethod()

registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=255)
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.01)

registration_method.SetInterpolator(sitk.sitkGaussian)
# registration_method.SetInterpolator(sitk.sitkLinear)

# registration_method.SetOptimizerAsGradientDescentLineSearch(learningRate=2.0, numberOfIterations=500)
# registration_method.SetOptimizerScalesFromPhysicalShift()
registration_method.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                       numberOfIterations=100,
                       maximumNumberOfCorrections=5,
                       maximumNumberOfFunctionEvaluations=1000,
                       costFunctionConvergenceFactor=1e+7)
registration_method.AddCommand( sitk.sitkIterationEvent, lambda: observer(registration_method) )

registration_method.SetInitialTransform(initial_transform, inPlace=False)
final_transform_v1 = registration_method.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
                                                 sitk.Cast(movImgSmooth, sitk.sitkFloat32))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))

print(final_transform_v1)
writer = sitk.ImageFileWriter()


writer.SetFileName(outputDirPath + 'Fixed_Smoothed.nrrd')
writer.Execute(fixImgSmooth)
writer.SetFileName(outputDirPath + 'Moving_Smoothed.nrrd')
writer.Execute(fixImgSmooth)

resample = sitk.ResampleImageFilter()
resample.SetReferenceImage(fixed)

# SimpleITK supports several interpolation options, we go with the simplest that gives reasonable results.
resample.SetInterpolator(sitk.sitkLinear)
resample.SetTransform(final_transform_v1)
sitk.WriteImage(resample.Execute(moving), outputDirPath+ '/' +'MovingAfterTransform' + '.nrrd')
sitk.WriteTransform(final_transform_v1, outputDirPath+ 'transform' + '.tfm')

# writer.SetFileName(outputDirPath + '/' + '03.nrrd')
# writer.Execute(resample.Execute(moving))

simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
simg2 = sitk.Cast(sitk.RescaleIntensity(resample.Execute(moving)), sitk.sitkUInt8)
cimg = sitk.Compose(simg1, simg2, simg1 // 4. + simg2 // 4.)
# sitk.Show(cimg, "RESULT")

outFileName = 'ResultOfRegistration.nrrd'

writer.SetFileName(outputDirPath + '/' + outFileName)
writer.Execute(cimg)



print "====END OF REGISTRATION====="