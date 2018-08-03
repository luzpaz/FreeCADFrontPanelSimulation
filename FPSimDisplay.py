import FreeCAD
import FreeCADGui
#from PySide import QtGui
from pivy import coin
from random import randint
import generated.FPSimulation_pb2 as Proto
import FPPixelContainer


def _findNodeIn(classTypeId, rootNode):
    sa = coin.SoSearchAction()
    sa.setType( classTypeId )
    sa.setSearchingAll(True)
    sa.apply(rootNode)
    if(sa.isFound()):
        return sa.getPath().getTail() 
    else:
        return None

_pixelContainer = dict()

class FPSimDisplay:
    def __init__(self, obj):
        obj.addProperty('App::PropertyInteger', 'ResolutionX').ResolutionX = 10
        obj.addProperty('App::PropertyInteger', 'ResolutionY').ResolutionY = 10
        obj.Proxy = self

    def _reinitTexture(self, obj):
        if _pixelContainer.get(obj.Name):
            del _pixelContainer[obj.Name]
        _pixelContainer[obj.Name] = FPPixelContainer.PixelContainer(obj.ResolutionX, obj.ResolutionY)
        _pixelContainer[obj.Name].clear(Proto.ColorRGB(red = 0, green = 0, blue = 0))
        pixelStr = _pixelContainer[obj.Name].toString()
        resolution = coin.SbVec2s(obj.ResolutionX, obj.ResolutionY)

        for child in obj.Group:
            rootNode = child.ViewObject.RootNode

            # find texture node
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            if not tex:
                FreeCAD.Console.PrintMessage("inserting new texture\n")
                tex =  coin.SoTexture2()
                rootNode.insertChild(tex,1)
            tex.model = coin.SoTexture2.REPLACE
            # create the image for the texture
            image = coin.SoSFImage()
            #FreeCAD.Console.PrintMessage("Initial Texture begin:\n" + self._getTextureString(obj) + "\nTexture End")
            image.setValue(resolution, FPPixelContainer.PixelContainer.NUM_COLOR_COMPONENTS, pixelStr)
            tex.image = image

            # find complexity node
            complexity = _findNodeIn(coin.SoComplexity.getClassTypeId(), rootNode)
            if not complexity:
                FreeCAD.Console.PrintMessage("inserting new complexity\n")
                complexity = coin.SoComplexity()
                rootNode.insertChild(complexity,1)
            complexity.textureQuality = 0.00001

    def _removeTexture(self, obj):
        for child in obj.Group:
            rootNode = child.ViewObject.RootNode
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            if tex:
                rootNode.removeChild(tex)
            complexity = _findNodeIn(coin.SoComplexity.getClassTypeId(), rootNode)
            if complexity:
                rootNode.removeChild(complexity)
    
    def _updateObjectTexture(self, obj):
        pixelContainer = _pixelContainer[obj.Name]
        pixelStr = pixelContainer.toString()
        resolution = coin.SbVec2s(pixelContainer.image.width, pixelContainer.image.height)
        for child in obj.Group:
            rootNode = child.ViewObject.RootNode
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            image = tex.image 
            image.setValue(resolution, FPPixelContainer.PixelContainer.NUM_COLOR_COMPONENTS, pixelStr)

    def onChanged(self, obj, prop):
        if prop == 'Proxy':
            #newly created
            pass
        elif prop == 'Group':
            # Group modified
            pass
        elif prop == 'ResolutionX':
            if 'ResolutionY' in obj.PropertiesList:
                self._reinitTexture(obj)
        elif prop == 'ResolutionY':
            if 'ResolutionX' in obj.PropertiesList:
                self._reinitTexture(obj)

    def execute(self, obj):
        pass

    def setPixels(self, obj, pixelDataList):
        pixelContainer = _pixelContainer[obj.Name]
        for pixel in pixelDataList.pixelData:
            pixelContainer.setPixel(pixel)
        self._updateObjectTexture(obj)

    def setSubWindowPixels(self, obj, subWindowData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.setSubWindowPixels(subWindowData)
        self._updateObjectTexture(obj)

    def drawRectangle(self, obj, rectData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.drawRectangle(rectData)
        self._updateObjectTexture(obj)


    def drawLine(self, obj, lineData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.drawLine(lineData)
        self._updateObjectTexture(obj)


    def clearDisplay(self, obj, color):
        _pixelContainer[obj.Name].clear(color)
        self._updateObjectTexture(obj)


    def getResolution(self, obj):
        answ = Proto.DisplayResolutionAnswer(x = obj.ResolutionX,
                                             y = obj.ResolutionY)
        return answ

    

class FPSimDisplayViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/Display.svg'

def createFPSimDisplay():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimDisplay')
    FPSimDisplay(obj)
    FPSimDisplayViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelection()
    for selObj in selection:
        obj.addObject(selObj)
    obj.Proxy._reinitTexture(obj)
