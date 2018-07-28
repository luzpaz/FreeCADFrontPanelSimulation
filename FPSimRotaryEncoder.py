import FreeCAD
import FPEventDispatcher
from FPInitialPlacement import InitialPlacements
import FPSimServer

lastRotationIncrementsAtAquire = {}


class FPSimRotaryEncoder(InitialPlacements):
    def __init__(self, obj):
        InitialPlacements.__init__(self, obj)
        obj.addProperty('App::PropertyPythonObject', 'PressEventLocationXY').PressEventLocationXY = []
        obj.addProperty('App::PropertyPythonObject', 'RotationAngleAtPress').RotationAngleAtPress = 0
        obj.addProperty('App::PropertyPythonObject', 'RotationAngle').RotationAngle = 0
        obj.addProperty('App::PropertyInteger', 'IncrementsPerRev').IncrementsPerRev = 64
        obj.addProperty('App::PropertyFloat', 'MouseSensitivity').MouseSensitivity = 1.0

        obj.addProperty('App::PropertyVector', 'RotationAxis').RotationAxis = (0,0,0)
        obj.addProperty('App::PropertyVector', 'RotationCenter').RotationCenter = (0,0,0)

        obj.Proxy = self

    def _registerEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.registerForButtonEvent(objName, self.onButtonEvent)

    def _unregisterEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.unregisterForButtonEvent(objName)

    def onChanged(self, obj, prop):
        #FreeCAD.Console.PrintMessage("in onChanged obj.Name: " + str(obj.Name) + " obj.Label: " + str(obj.Label) + " prop: " + str(prop) + "\n")
        if prop == 'Proxy':
            # Called at loading existing object on first place(Placement is not valid yet )
            # Called at creation on first place(ToCheck: I think Placement is not valid here yet)
            self._registerEventCallbacks(obj.Name)
        elif prop == 'Group':
            # Always called when the group changes(new group member inserted or removed) 
            # or gets created :
            #    - called after 'proxy'-cb
            #    - Placement is valid
            #    - strange thing is at this point there is no child object inside
            if not obj.Group:
                # Called when Removing all objects from group or when group-obj gets deleted
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has no Group attribute\n")
                self._unregisterEventCallbacks(obj.Name)
            elif self.hasNoChilds(obj):
                # Called at object creation
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has Group attribute but no childs\n")
                self._registerEventCallbacks(obj.Name)
            else:
                # Called When object gets added to a group that already has at least one child
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has Group attribute and childs\n")
                pass
            self.saveInitialPlacements(obj) 
        elif prop == 'ExpressionEngine':
            # Called at loading existing object at last cb(Placement is valid now)
            try:
                obj.RotationAngle = 0
                self.moveToInitialPlacement(obj)
            except KeyError:
                self.saveInitialPlacements(obj)
        #elif prop == a parameter of the object
            # Called on parameter change (followed by execute-cb when it gets applied)

    def execute(self, fp):
        #FreeCAD.Console.PrintMessage("in execute fp: " + str(fp.Label) + "\n")
        # Called when group-obj parameter change or child-objects parameter change gets applied
        pass

    def onButtonEvent(self, objName, state, pointerPos):
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            obj = FreeCAD.ActiveDocument.getObject(objName)
            obj.PressEventLocationXY = pointerPos
            obj.RotationAngleAtPress = obj.RotationAngle
            FPEventDispatcher.eventDispatcher.registerForLocation(objName, self.onDragged)
        else:
            FPEventDispatcher.eventDispatcher.unregisterForLocation(objName, self.onDragged)

    def onDragged(self, objName, pointerPos):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        obj.RotationAngle = obj.RotationAngleAtPress + (pointerPos[1] - obj.PressEventLocationXY[1]) * obj.MouseSensitivity
        rot = FreeCAD.Rotation(obj.RotationAxis, obj.RotationAngle)
        for child in obj.Group:
            initPlc = self.getInitialPlacement(obj, child.Name)
            rotPlacement = FreeCAD.Placement(initPlc.Base, rot, obj.RotationCenter - initPlc.Base)
            newRot = rotPlacement.Rotation.multiply( initPlc.Rotation )
            newBase = rotPlacement.Base
            child.Placement.Base = newBase
            child.Placement.Rotation = newRot
        FPSimServer.dataAquisitionCBHolder.setEncoderCB(objName, self.getIncrements)
        

    def getIncrements(self, objName):
        FPSimServer.dataAquisitionCBHolder.clearEncoderCB(objName)
        obj = FreeCAD.ActiveDocument.getObject(objName)
        # take a sample of rot angle because of thread concurrency
        actRotIncr = int( (float(obj.RotationAngle) / 360.0) * float(obj.IncrementsPerRev) )
        if not lastRotationIncrementsAtAquire.get(objName):
            lastRotationIncrementsAtAquire[objName] = actRotIncr
        ret = actRotIncr - lastRotationIncrementsAtAquire[objName]
        lastRotationIncrementsAtAquire[objName] = actRotIncr
        return ret


class FPSimRotaryEncoderViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/RotEncoder.svg'

def createFPSimRotaryEncoder():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimRotaryEncoder')
    FPSimRotaryEncoder(obj)
    FPSimRotaryEncoderViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    try:
        obj.RotationAxis = selection[-1].SubObjects[-1].normalAt(0,0)
        obj.RotationCenter = selection[-1].SubObjects[-1].CenterOfMass
        for sel_obj in selection:
            obj.addObject(sel_obj.Object)
    except IndexError:
        FreeCAD.Console.PrintError("Usage Error, select objects and a rotation surface\n")
        