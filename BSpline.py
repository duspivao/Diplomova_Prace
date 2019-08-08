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

print 'Translation transform'
reg1 = sitk.ImageRegistrationMethod()
reg1.SetInterpolator(sitk.sitkLinear)
reg1.SetMetricAsMattesMutualInformation(numberOfHistogramBins=120)
reg1.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-4,
                       numberOfIterations=50,
                       maximumNumberOfCorrections=2,
                       maximumNumberOfFunctionEvaluations=100,
                       costFunctionConvergenceFactor=1e+7)

init_transform_res = reg1.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
                                                 sitk.Cast(movImgSmooth, sitk.sitkFloat32))
res = sitk.ResampleImageFilter()
res.SetReferenceImage(fixImgSmooth)
res.SetInterpolator(sitk.sitkLinear)
res.SetTransform(init_transform_res)
resampledImage = res.Execute(movImgSmooth)
print 'Translation transform ended'

print 'BSpline transform'
initial_transform1 = sitk.CenteredTransformInitializer(sitk.Cast(fixImgSmooth, movImgSmooth.GetPixelID()),
                                                      resampledImage,
                                                      sitk.BSplineTransform,
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)
resampleFilter = sitk.ResampleImageFilter()
resampleFilter.SetReferenceImage(fixImgSmooth)

transformDomainMeshSize = [6]*resampledImage.GetDimension()
initial_transform = sitk.BSplineTransformInitializer(fixImgSmooth,
                                      transformDomainMeshSize )

registration_method = sitk.ImageRegistrationMethod()
registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.1)

# registration_method.SetInterpolator(sitk.sitkGaussian)
registration_method.SetInterpolator(sitk.sitkLinear)

# registration_method.SetOptimizerAsGradientDescentLineSearch(learningRate=2.0, numberOfIterations=500)
# registration_method.SetOptimizerScalesFromPhysicalShift()
registration_method.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                       numberOfIterations=100,
                       maximumNumberOfCorrections=5,
                       maximumNumberOfFunctionEvaluations=500,
                       costFunctionConvergenceFactor=1e+7)
registration_method.AddCommand( sitk.sitkIterationEvent, lambda: observer(registration_method) )

registration_method.SetInitialTransform(initial_transform, inPlace=False)
final_transform_v1 = registration_method.Execute(sitk.Cast(fixImgSmooth, sitk.sitkFloat32),
                                                 sitk.Cast(movImgSmooth, sitk.sitkFloat32))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))

print(final_transform_v1)
print 'BSpline transform finished'
writer = sitk.ImageFileWriter()


writer.SetFileName(outputDirPath + 'Affine_Fixed_Smoothed.nrrd')
writer.Execute(fixImgSmooth)
writer.SetFileName(outputDirPath + 'Affine_Moving_Smoothed.nrrd')
writer.Execute(fixImgSmooth)

resample = sitk.ResampleImageFilter()
resample.SetReferenceImage(fixed)

# SimpleITK supports several interpolation options, we go with the simplest that gives reasonable results.
resample.SetInterpolator(sitk.sitkLinear)
resample.SetTransform(final_transform_v1)
sitk.WriteImage(resample.Execute(moving), outputDirPath+ 'Affine_MovingAfterTransform' + '.nrrd')
sitk.WriteTransform(final_transform_v1, outputDirPath+ 'Affine_transform' + '.tfm')

# writer.SetFileName(outputDirPath + '/' + '03.nrrd')
# writer.Execute(resample.Execute(moving))

simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
simg2 = sitk.Cast(sitk.RescaleIntensity(resample.Execute(moving)), sitk.sitkUInt8)
cimg = sitk.Compose(simg1, simg2, simg1 // 4. + simg2 // 4.)
# sitk.Show(cimg, "RESULT")

outFileName = 'Affine_ResultOfRegistration.nrrd'

writer.SetFileName(outputDirPath + '/' + outFileName)
writer.Execute(cimg)



print "====END OF REGISTRATION====="