# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer
import vtkmodules.all as vtk
import os


def get_listdir(path):  # 获取目录下所有gz格式文件的地址，返回地址list
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def display_mask(path, save_path, Angle):
    reader = vtk.vtkNIFTIImageReader()  # 实例化Reader对象
    reader.SetFileName(path)  # 所要读取的文件名
    reader.Update()  # 调用Update()方法执行

    mapper = vtk.vtkGPUVolumeRayCastMapper()

    mapper.SetInputData(reader.GetOutput())

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)

    opacity = vtk.vtkPiecewiseFunction()  # 透明度
    opacity.AddPoint(0, 0.0)
    opacity.AddPoint(1, 1.0)

    color = vtk.vtkColorTransferFunction()  # 颜色
    color.AddRGBPoint(1, 0, 1, 0)  # TODO:(X,R,G,B) 颜色改RGB

    my_property = vtk.vtkVolumeProperty()
    my_property.SetInterpolationTypeToLinear()  # 设置插值方式
    my_property.SetColor(0, color)  # 设置颜色
    my_property.SetScalarOpacity(0, opacity)  # 设置透明度

    my_property.ShadeOn()  # 打开阴影效果
    my_property.SetAmbient(0, 0.5)  # 环境光系数
    my_property.SetDiffuse(0, 1)  # 散射光系数
    my_property.SetSpecular(0, 0)  # 反射光系数
    # 当环境光系数占主导时，阴影效果不明显。
    # 当散射光系数占主导时，显示效果会比较粗燥。
    # 当反射光系数占主导时，显示效果会比较光滑。
    my_property.SetSpecularPower(0, 0.0)  # 高光强度

    my_property.SetShade(0, 1)

    # my_property.SetComponentWeight(0, 1)
    # my_property.SetDisableGradientOpacity(0, 1)
    # my_property.DisableGradientOpacityOn()
    # my_property.SetScalarOpacityUnitDistance(0, 0.5)

    volume.SetProperty(my_property)

    myCamera = vtk.vtkCamera()  # 设置相机位置及方向
    myCamera.SetViewUp(0, 0, 1)
    myCamera.SetPosition(Angle)

    myLight = vtk.vtkLight()  # 设置光源颜色、位置、焦点
    myLight.SetColor(1, 1, 1)
    myLight.SetPosition(0, 1, 1)
    myLight.SetFocalPoint(myCamera.GetFocalPoint())

    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.SetSize(256, 256)  # 窗口尺寸
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.SetActiveCamera(myCamera)
    ren.AddLight(myLight)
    ren.AddActor(volume)
    ren.SetBackground(1.0, 1.0, 1.0)
    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
    # iren.Start()

    writer = vtk.vtkBMPWriter()
    windowto_image_filter = vtk.vtkWindowToImageFilter()
    windowto_image_filter.SetInput(renWin)  # renWin为vtk.vtkRenderWindow()
    windowto_image_filter.SetScale(1)
    windowto_image_filter.SetInputBufferTypeToRGB()
    windowto_image_filter.ReadFrontBufferOff()
    windowto_image_filter.Update()
    writer.SetFileName(save_path)
    writer.SetInputConnection(windowto_image_filter.GetOutputPort())
    writer.Write()


if __name__ == '__main__':
    img_list = get_listdir(r'C:\Users\user\Desktop\copd\0')
    save_path = r'C:\Users\user\Desktop\copd\0_png'
    for img_path in img_list:
        _, fullflname = os.path.split(img_path)
        save_dir = os.path.join(save_path, fullflname[:-7])
        os.makedirs(save_dir, exist_ok=True)
        display_mask(img_path, os.path.join(save_dir, '1.png'), (0, -1, 0))
        display_mask(img_path, os.path.join(save_dir, '2.png'), (0, 1, 0))
        display_mask(img_path, os.path.join(save_dir, '3.png'), (0, -1, 0.5))
