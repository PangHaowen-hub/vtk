# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderWindow, vtkRenderWindowInteractor, \
    vtkRenderer
import vtkmodules.all as vtk


def display_mask(path):
    reader = vtk.vtkNIFTIImageReader()  # 实例化Reader对象
    reader.SetFileName(path)  # 指定所要读取的文件名
    reader.Update()  # 调用Update()方法促使管线执行

    mapper = vtk.vtkGPUVolumeRayCastMapper()
    mapper.SetInputData(reader.GetOutput())

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)

    opacity = vtk.vtkPiecewiseFunction()  # 透明度
    opacity.AddPoint(0, 0.0)
    opacity.AddPoint(1, 1.0)

    color = vtk.vtkColorTransferFunction()  # 颜色
    color.AddRGBPoint(1, 1, 0, 0)  # 红

    my_property = vtk.vtkVolumeProperty()
    my_property.SetInterpolationTypeToLinear()  # 设置插值方式
    my_property.SetColor(0, color)  # 设置颜色
    my_property.SetScalarOpacity(0, opacity)  # 设置透明度

    my_property.ShadeOn()  # 打开阴影效果
    my_property.SetDiffuse(0, 1)  # 散射光系数
    my_property.SetAmbient(0, 0)  # 环境光系数
    my_property.SetSpecular(0, 0)  # 反射光系数

    my_property.SetShade(0, 1)

    my_property.SetSpecularPower(0, 0.5)  # 高光强度,镜面反射强度
    my_property.SetComponentWeight(0, 1)
    my_property.SetDisableGradientOpacity(0, 1)
    my_property.DisableGradientOpacityOn()  # 禁用渐变不透明度
    my_property.SetScalarOpacityUnitDistance(0, 0.5)

    volume.SetProperty(my_property)

    myCamera = vtk.vtkCamera()  # 设置相机位置及方向
    myCamera.SetViewUp(0, 0, 1)
    myCamera.SetPosition(0, 1, 0)

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.SetActiveCamera(myCamera)

    ren.AddActor(volume)
    ren.SetBackground(1.0, 1.0, 1.0)
    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(2)
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    display_mask(r'G:\segment_registration\Registration\original_image\mask_airway\lobe512_000.nii.gz')
