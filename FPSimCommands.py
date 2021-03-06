# -*- coding: utf-8 -*-
# FreeCAD init script of Front Panel Simulation module  

#***************************************************************************
#*   (c) Daniel Zicsi-Liess liessdaniel415@gmail.com 2018                  *   
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/

import FreeCAD
import FreeCADGui
import FPSimDir
import FPSimulation


class CreateDisplay:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/Display.svg',
                'MenuText': 'Create Display',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimDisplay
        FPSimDisplay.createFPSimDisplay()

class CreateLED:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/LED.svg',
                'MenuText': 'Create LED',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimLED
        FPSimLED.createFPSimLED()

class CreateTouchSurface:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/TouchSurface.svg',
                'MenuText': 'Create Touch Surface',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimTouchSurface
        FPSimTouchSurface.createFPSimTouchSurface()

class CreateLinButton:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/CreateLinButton.svg',
                'MenuText': 'Create linear press button',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimButton
        FPSimButton.createFPSimLinButton()

class CreateRotButton:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/CreateRotButton.svg',
                'MenuText': 'Create rotational press button',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimButton
        FPSimButton.createFPSimRotButton()

class CreateRotaryEncoder:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/RotEncoder.svg',
                'MenuText': 'Create rotary encoder',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimRotaryEncoder
        FPSimRotaryEncoder.createFPSimRotaryEncoder()

class CreateRotaryPotentiometer:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/RotPotentiometer.svg',
                'MenuText': 'Create rotary potentiometer',
                'ToolTip': 'Create rotary potentiometer'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimRotaryPotentiometer
        FPSimRotaryPotentiometer.createFPSimRotaryPotentiometer()

class CreateLinearPotentiometer:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/LinearPotentiometer.svg',
                'MenuText': 'Create a linear potentiometer',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPSimLinearPotentiometer
        FPSimLinearPotentiometer.createFPSimLinearPotentiometer()

    

class StartSimulation:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/StartSimulation.svg',
                'MenuText': 'Start Simulation',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        FPSimulation.startSimulation()



class StopSimulation:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/StopSimulation.svg',
                'MenuText': 'Stop Simulation',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        FPSimulation.stopSimulation()

class ExportWidgetInfo:
    def GetResources(self):
        return {'Pixmap': FPSimDir.__dir__ + '/icons/ExportWidgetInfo.svg',
                'MenuText': 'Export Topology',
                'ToolTip': ''}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and not FPSimulation.simulationRunning:
            return True
        else:
            return False

    def Activated(self):
        import FPWidgetInfoExporter
        FPWidgetInfoExporter.exportWidgetInfo(FreeCAD.ActiveDocument.Name)


FreeCAD.Gui.addCommand('CreateDisplay', CreateDisplay())
FreeCAD.Gui.addCommand('CreateLED', CreateLED())
FreeCAD.Gui.addCommand('CreateTouchSurface', CreateTouchSurface())
FreeCAD.Gui.addCommand('CreateLinButton', CreateLinButton())
FreeCAD.Gui.addCommand('CreateRotButton', CreateRotButton())
FreeCAD.Gui.addCommand('CreateRotaryEncoder', CreateRotaryEncoder())
FreeCAD.Gui.addCommand('CreateRotaryPotentiometer', CreateRotaryPotentiometer())
FreeCAD.Gui.addCommand('CreateLinearPotentiometer', CreateLinearPotentiometer())
FreeCAD.Gui.addCommand('StartSimulation', StartSimulation())
FreeCAD.Gui.addCommand('StopSimulation', StopSimulation())
FreeCAD.Gui.addCommand('ExportWidgetInfo', ExportWidgetInfo())

