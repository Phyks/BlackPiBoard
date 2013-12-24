#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Written by: QuantumPhysics
# http://compsci.ca/v3/viewtopic.php?t=32343
# Date Written: 10/06/12

import wx

class PaintWindow(wx.Window):
    # array of colors available to draw
    colours = ['Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple',
        'Brown', 'Aquamarine', 'Forest Green', 'Light Blue', 'Goldenrod',
        'Cyan', 'Orange', 'Navy', 'Light Grey', 'ClearScreen']
    # color quantity
    thicknesses = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128]

    def __init__(self, parent):
        # creates paint window
        super(PaintWindow, self).__init__(parent,
            style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.initDrawing()
        self.makeMenu()
        # binds key_down and up events
        self.bindEvents()
        self.initBuffer()

    def initDrawing(self):
        self.SetBackgroundColour('WHITE')
        self.currentThickness = self.thicknesses[0]
        self.currentColour = self.colours[0]
        self.lines = []
        self.previousPosition = (0, 0)

    def bindEvents(self):
        for event, handler in [
                # creates bind event for left button down
                (wx.EVT_LEFT_DOWN, self.onLeftDown),
                # creates bind event once left button is released
                (wx.EVT_LEFT_UP, self.onLeftUp),
                # creates bind event for drawing (moving cursor)
                (wx.EVT_MOTION, self.onMotion),
                # creates bind event for right button up
                (wx.EVT_RIGHT_UP, self.onRightUp),
                (wx.EVT_SIZE, self.onSize),       
                (wx.EVT_IDLE, self.onIdle),       
                (wx.EVT_PAINT, self.onPaint),
                # creates event to close window after 'x' is selected
                (wx.EVT_WINDOW_DESTROY, self.cleanup)]:
            self.Bind(event, handler)

    def initBuffer(self):
        # gets size of window
        size = self.GetClientSize()
        # sets window to empty canvas .bmp x-width, y-height
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.drawLines(dc, *self.lines)
        self.reInitBuffer = False

    def makeMenu(self):
        # creates menu on right click
        self.menu = wx.Menu()
        # sets selection for items (colors) in the runtime window on right click
        self.idToColourMap = self.addCheckableMenuItems(self.menu,
            self.colours)
        # updates screen once a new color is selected
        self.bindMenuEvents(menuHandler=self.onMenuSetColour,
            updateUIHandler=self.onCheckMenuColours,
            ids=self.idToColourMap.keys())
        self.menu.Break()
        self.idToThicknessMap = self.addCheckableMenuItems(self.menu,
            self.thicknesses)
        self.bindMenuEvents(menuHandler=self.onMenuSetThickness,
            updateUIHandler=self.onCheckMenuThickness,
            ids=self.idToThicknessMap.keys())

    # adds a static surpressor to conditions
    @staticmethod
    def addCheckableMenuItems(menu, items):
       
        idToItemMapping = {}
        for item in items:
            menuId = wx.NewId()
            idToItemMapping[menuId] = item
            menu.Append(menuId, str(item), kind=wx.ITEM_CHECK)
        return idToItemMapping

    def bindMenuEvents(self, menuHandler, updateUIHandler, ids):
       
        sortedIds = sorted(ids)
        firstId, lastId = sortedIds[0], sortedIds[-1]
        for event, handler in \
                [(wx.EVT_MENU_RANGE, menuHandler),
                 (wx.EVT_UPDATE_UI_RANGE, updateUIHandler)]:
            self.Bind(event, handler, id=firstId, id2=lastId)

    def onLeftDown(self, event):
        # draw line
        self.currentLine = []
        self.previousPosition = event.GetPositionTuple()
        self.CaptureMouse()

    def onLeftUp(self, event):
        # close motion, stop drawing, wait for event
        if self.HasCapture():
            self.lines.append((self.currentColour, self.currentThickness,
                self.currentLine))
            self.currentLine = []
            self.ReleaseMouse()

    def onRightUp(self, event):
        # if right button is clicked then make wx.menu to select colors
        self.PopupMenu(self.menu)

    def onMotion(self, event):

        if event.Dragging() and event.LeftIsDown():
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            currentPosition = event.GetPositionTuple()
            lineSegment = self.previousPosition + currentPosition
            self.drawLines(dc, (self.currentColour, self.currentThickness,
                [lineSegment]))
            self.currentLine.append(lineSegment)
            self.previousPosition = currentPosition

    def onSize(self, event):
       
        self.reInitBuffer = True

    def onIdle(self, event):

        if self.reInitBuffer:
            self.initBuffer()
            self.Refresh(False)

    def onPaint(self, event):
       

        dc = wx.BufferedPaintDC(self, self.buffer)

    def cleanup(self, event):
        if hasattr(self, "menu"):
            self.menu.Destroy()
            del self.menu

    def onCheckMenuColours(self, event):
        colour = self.idToColourMap[event.GetId()]
        event.Check(colour == self.currentColour)

    def onCheckMenuThickness(self, event):
        thickness = self.idToThicknessMap[event.GetId()]
        event.Check(thickness == self.currentThickness)

    def onMenuSetColour(self, event):
        self.currentColour = self.idToColourMap[event.GetId()]

    def onMenuSetThickness(self, event):
        self.currentThickness = self.idToThicknessMap[event.GetId()]

    @staticmethod
    def drawLines(dc, *lines):
        dc.BeginDrawing()
        for colour, thickness, lineSegments in lines:
            pen = wx.Pen(wx.NamedColour(colour), thickness, wx.SOLID)
            dc.SetPen(pen)
            for lineSegment in lineSegments:
                dc.DrawLine(*lineSegment)
        dc.EndDrawing()


class PaintFrame(wx.Frame):
    def __init__(self, parent=None):
        size = wx.GetDisplaySize()
        super(PaintFrame, self).__init__(parent, title="Black PiBoard",
            size=size,
            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        doodle = PaintWindow(self)


if __name__ == '__main__':
    app = wx.App()
    frame = PaintFrame()
    frame.ShowFullScreen(True, wx.FULLSCREEN_ALL)
    app.MainLoop() 
