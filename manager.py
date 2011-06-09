##################################
#created by Daniel Chiles        #
#                                #
#AOS mod manager                 #
#allows users to easily swap mods#
#                                #
#Feel free to make this software #
#better, it is free to modify    #
##################################

#!/usr/bin/env python
#-*- coding: utf-8 -*-
from os.path import exists

import os
import wx

#global constants#
KV6 = ['BLOCK', 
       'CP', 
       'GRENADE', 
       'INTEL', 
       'PICKAXE', 
       'PLAYERARMS', 
       'PLAYERDEAD', 
       'PLAYERHEAD', 
       'PLAYERLEG', 
       'PLAYERLEGC', 
       'PLAYERTORSO', 
       'PLAYERTORSOC', 
       'SEMI', 
       'SPADE', 
       'TRACER']

KV6_PATH = ['\\kv6\\block.kv6',
            '\\kv6\\cp.kv6',
            '\\kv6\\grenade.kv6',
            '\\kv6\\intel.kv6',
            '\\kv6\\pickaxe.kv6',
            '\\kv6\\playerarms.kv6',
            '\\kv6\\playerdead.kv6',
            '\\kv6\\playerhead.kv6',
            '\\kv6\\playerleg.kv6',
            '\\kv6\\playerlegc.kv6',
            '\\kv6\\playertorso.kv6',
            '\\kv6\\playertorsoc.kv6',
            '\\kv6\\semi.kv6',
            '\\kv6\\spade.kv6',
            '\\kv6\\tracer.kv6']


PNG = ['ICON', 
       'KNUMB', 
       'SEMI', 
       'TARGET']

PNG_PATH = ['\\png\\icon.png',
            '\\png\\knumb.png',
            '\\png\\semi.png',
            '\\png\\target.png']
     
WAV = ['BOUNCE',
       'BUILD',
       'CHAT',
       'DEATH', 
       'DEBRIS',
       'EXPLODE',
       'FALLHURT',
       'FOOTSTEP1',
       'FOOTSTEP2',
       'FOOTSTEP3', 
       'FOOTSTEP4', 
       'HITGROUND', 
       'HITPLAYER', 
       'INTRO', 
       'JUMP', 
       'LAND', 
       'PICKUP',
       'PIN',
      'SEMIRELOAD',
      'SEMISHOOT',
      'SWITCH',
      'WADE1',
      'WADE2',
      'WADE3',
      'WADE4',
      'WATEREXPLODE',
      'WATERJUMP',
      'WATERLAND',
      'WOOSH']

WAV_PATH = ['\\wav\\bounce.wav',
            '\\wav\\build.wav',
            '\\wav\\chat.wav',
            '\\wav\\death.wav',
            '\\wav\\debris.wav',
            '\\wav\\explode.wav',
            '\\wav\\fallhurt.wav',
            '\\wav\\footstep1.wav',
            '\\wav\\footstep2.wav',
            '\\wav\\footstep3.wav',
            '\\wav\\footstep4.wav',
            '\\wav\\hitground.wav',
            '\\wav\\hitplayer.wav',
            '\\wav\\intro.wav',
            '\\wav\\jump.wav',
            '\\wav\\land.wav',
            '\\wav\\pickup.wav',
            '\\wav\\pin.wav',
            '\\wav\\semireload.wav',
            '\\wav\\semishoot.wav',
            '\\wav\\switch.wav',
            '\\wav\\wade1.wav',
            '\\wav\\wade2.wav',
            '\\wav\\wade3.wav',
            '\\wav\\wade4.wav',
            '\\wav\\waterexplode.wav',
            '\\wav\\waterjump.wav',
            '\\wav\\waterland.wav',
            '\\wav\\whoosh.wav']

#end global constants#

#current_output and input work with the OnLoad event handler
kv6_output =''
kv6_input = ''
png_output =''
png_input = ''
wav_output =''
wav_input = ''
game_path = ['C:\\Program Files (x86)\\Ace of Spades','C:\\Program Files\\Ace of Spades']
current_path = game_path[0]
tckv6 = 0
tcpng = 0
tcwav = 0

#Class MainWindow#
class MainWindow(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (650,200))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.sb = self.CreateStatusBar()# status bar at the bottom of the window

        #set up the menu
        filemenu = wx.Menu()

        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provide by wxWidgets
         #menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
         #menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File") # adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)

        # setting up the Box sizer
        vbox    = wx.BoxSizer(wx.VERTICAL)
        pathbox = wx.BoxSizer(wx.HORIZONTAL)
        kv6box  = wx.BoxSizer(wx.HORIZONTAL)
        pngbox  = wx.BoxSizer(wx.HORIZONTAL)
        wavbox  = wx.BoxSizer(wx.HORIZONTAL)
        
        global current_path
        global game_path
        global tckv6
        global tcpng
        global tcwav
        global KV6
        global PNG
        global WAV
        
        panel = wx.Panel(self,-1,style=wx.SUNKEN_BORDER)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        
        stpath = wx.StaticText(panel, -1, "Path to game...", style=wx.ALIGN_CENTER,size=(-1,-1))
        stpath.SetFont(font)

        cbpath = wx.ComboBox(panel, -1, size = (-1, -1), choices = game_path, style=wx.CB_READONLY)
        
        pathbox.Add(stpath, 1,wx.TOP, 5)
        pathbox.Add(cbpath, 1,wx.TOP, 5)
        vbox.Add(pathbox)

        stkv6 = wx.StaticText(panel, -1, "KV6", style=wx.ALIGN_CENTER,size=(-1,-1))
        cbkv6 = wx.ComboBox(panel, -1, size = (100, -1), choices = KV6, style=wx.CB_READONLY)
        tckv6 = wx.TextCtrl(panel,-1,"none selected")
        browsekv6 = wx.Button(panel, -1,"Browse", (-1,-1))
        swapkv6 = wx.Button(panel, -1,"Swap", (-1,-1))

        kv6box.Add(stkv6, 1, wx.TOP, 5)
        kv6box.Add(cbkv6, 1, wx.TOP, 5)
        kv6box.Add(tckv6, 1, wx.TOP, 5)
        kv6box.Add(browsekv6, 1, wx.TOP, 5)
        kv6box.Add(swapkv6, 1, wx.TOP, 5)
        vbox.Add(kv6box)

        stpng = wx.StaticText(panel, -1, "PNG", style=wx.ALIGN_CENTER,size=(-1,-1))
        cbpng = wx.ComboBox(panel, -1, size = (100, -1), choices = PNG, style=wx.CB_READONLY)
        tcpng = wx.TextCtrl(panel,-1,"none selected")
        browsepng = wx.Button(panel, -1,"Browse", (-1,-1))
        swappng = wx.Button(panel, -1,"Swap", (-1,-1))

        pngbox.Add(stpng, 1, wx.TOP, 5)
        pngbox.Add(cbpng, 1, wx.TOP, 5)
        pngbox.Add(tcpng, 1, wx.TOP, 5)
        pngbox.Add(browsepng, 1, wx.TOP, 5)
        pngbox.Add(swappng, 1, wx.TOP, 5)
        vbox.Add(pngbox)

        stwav = wx.StaticText(panel, -1, "WAV", style=wx.ALIGN_CENTER,size=(-1,-1))
        cbwav = wx.ComboBox(panel, -1, size = (100, -1), choices = WAV, style=wx.CB_READONLY)
        tcwav = wx.TextCtrl(panel,-1,"none selected")
        browsewav = wx.Button(panel, -1,"Browse", (-1,-1))
        swapwav = wx.Button(panel, -1,"Swap", (-1,-1))

        wavbox.Add(stwav, 1, wx.TOP, 5)
        wavbox.Add(cbwav, 1, wx.TOP, 5)
        wavbox.Add(tcwav, 1, wx.TOP, 5)
        wavbox.Add(browsewav, 1, wx.TOP, 5)
        wavbox.Add(swapwav, 1, wx.TOP, 5)
        vbox.Add(wavbox)
        
        panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

        #event handling
         #self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
         #self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Bind(wx.EVT_COMBOBOX, self.OnPathSelect, cbpath)
        self.Bind(wx.EVT_COMBOBOX, self.OnKV6Select, cbkv6)
        self.Bind(wx.EVT_COMBOBOX, self.OnPNGSelect, cbpng)
        self.Bind(wx.EVT_COMBOBOX, self.OnWAVSelect, cbwav)

        self.Bind(wx.EVT_BUTTON, self.OnKV6Browse, browsekv6)
        self.Bind(wx.EVT_BUTTON, self.OnPNGBrowse, browsepng)
        self.Bind(wx.EVT_BUTTON, self.OnWAVBrowse, browsewav)

        self.Bind(wx.EVT_BUTTON, self.OnKV6Swap, swapkv6)
        self.Bind(wx.EVT_BUTTON, self.OnPNGSwap, swappng)
        self.Bind(wx.EVT_BUTTON, self.OnWAVSwap, swapwav)
        
        self.Centre()
        self.Show(True)

        
    #EVENT HANDLERS#

    #OnPathSelect#
    
    def OnPathSelect(self, event):
        global current_path
        item = event.GetSelection()
        current_path = game_path[item]
        self.sb.SetStatusText(current_path)
    #End OnPathSelect#

    #OnKV6Select#
    def OnKV6Select(self, event):
        global KV6_PATH
        global kv6_output
        global current_path
        item = event.GetSelection()
        kv6_output = current_path + KV6_PATH[item]
        self.sb.SetStatusText(kv6_output)
    #End OnKV6Select#

    #OnPNGSelect#
    def OnPNGSelect(self, event):
        global PNG_PATH
        global png_output
        global current_path
        item = event.GetSelection()
        png_output = current_path + PNG_PATH[item]
        self.sb.SetStatusText(png_output)
    #End OnPNGSelect#

    #OnWAVSelect#
    def OnWAVSelect(self, event):
        global WAV_PATH
        global wav_output
        global current_path
        item = event.GetSelection()
        wav_output = current_path + WAV_PATH[item]
        self.sb.SetStatusText(wav_output)
    #End OnWAVSelect#
    
    #OnAbout#
    def OnAbout(self,e):
        #dialog box with a hidden easteregg maybe :)
        dlg = QuizDlg(None, -1, 'About AOS Mod Manager')
        dlg.ShowModal() 
        dlg.Destroy()
    #end OnAbout#
        
    #close application event
    def OnExit(self,e):
        self.Close(True)
    #end OnExit
    
    #open file event#
    def OnOpen(self,e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            stuff = dlg.GetDirectory() + "\\" + dlg.GetFilename()+"\n"
            global current_output 
            current_output = stuff
        dlg.Destroy()
    #end OnOpen#

    #OnKV6Browse#
    def OnKV6Browse(self,e):
        global kv6_input
        global tckv6

        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a KV6 model", self.dirname, "", "*.kv6", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            
            self.sb.SetStatusText(dlg.GetDirectory() + "\\" + dlg.GetFilename())
            kv6_input = dlg.GetDirectory() + "\\" + dlg.GetFilename()
            tckv6.SetValue(dlg.GetFilename())
            
    #End OnKV6Browse#

    #OnPNGBrowse#
    def OnPNGBrowse(self,e):
        global png_input
        global tcpng

        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a PNG file", self.dirname, "", "*.png", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            
            self.sb.SetStatusText(dlg.GetDirectory() + "\\" + dlg.GetFilename())
            png_input = dlg.GetDirectory() + "\\" + dlg.GetFilename()
            tcpng.SetValue(dlg.GetFilename())
            
    #End OnPNGBrowse#

    #OnWAVBrowse#
    def OnWAVBrowse(self,e):
        global wav_input
        global tcwav

        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a WAV sound", self.dirname, "", "*.wav", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            
            self.sb.SetStatusText(dlg.GetDirectory() + "\\" + dlg.GetFilename())
            wav_input = dlg.GetDirectory() + "\\" + dlg.GetFilename()
            tcwav.SetValue(dlg.GetFilename())
            
    #End OnWAVBrowse#

    #Load file from current_input to current_ouput
    def OnLoad(self,e): 

        if exists(current_input):
            input = open(current_input)
            indata = input.read()
            
            if exists(current_output):
                o = open(current_output, 'w')
                o.write(indata)
            else:
                print "%s is not a valid file name" % current_output
        else:
            print "%s is not a valid file name" % current_input
    #End OnLoad#
    
    #OnKV6Swap#
    def OnKV6Swap(self,e): 
        global kv6_input
        global kv6_output

        if exists(kv6_input):
            input = open(kv6_input, 'rb')
            indata = input.read()
            
            if exists(kv6_output):
                o = open(kv6_output, 'wb')
                o.write(indata)
                self.sb.SetStatusText("SUCCESS!!")
            else:
                self.sb.SetStatusText("Please Select a KV6 model type")  
        else:
            self.sb.SetStatusText("a KV6 file has not been selected or is not a valid file name")
    #EndOnKV6Swap#

    #OnPNGSwap#
    def OnPNGSwap(self,e): 
        global png_input
        global png_output

        if exists(png_input):
            input = open(png_input, 'rb')
            indata = input.read()
            
            if exists(png_output):
                o = open(png_output, 'wb')
                o.write(indata)
                self.sb.SetStatusText("SUCCESS!!")
            else:
                self.sb.SetStatusText("Please Select a PNG image type")  
        else:
            self.sb.SetStatusText("a PNG file has not been selected or is not a valid file name")
    #EndOnPNGSwap#

    #OnWAVSwap#
    def OnWAVSwap(self,e): 
        global wav_input
        global wav_output

        if exists(wav_input):
            input = open(wav_input, 'rb')
            indata = input.read()
            
            if exists(wav_output):
                o = open(wav_output, 'wb')
                o.write(indata)
                self.sb.SetStatusText("SUCCESS!!")
            else:
                self.sb.SetStatusText("Please Select a WAV sound type")  
        else:
            self.sb.SetStatusText("a WAV file has not been selected or is not a valid file name")
    #EndOnWAVSwap#
    
    
    #END OF EVENT HANDLERS#

    
    
    
#END OF CLASS MainWindow#

#Class QuizDlg#
class QuizDlg(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size = (315,220))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'AOS Mod Manager', (5, 5), (300, 150))
        self.quizText = wx.StaticText(panel, -1, "AOS Mod Manager is a utility that allows users to \neasily modify game assets for Ace of Spades\n\nQuiz:\n\nWhat item explodes?\nWhich side is the better race?\nWhat item do you use to remove up to 3 blocks at once?", style=wx.ALIGN_LEFT,pos=(25,20),size=(-1,-1))
        self.answerbox = wx.TextCtrl(panel, -1, '', (55, 130))
        okButton = wx.Button(panel, -1,"Submit", (165,130))
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        closeButton = wx.Button(self, -1, 'Close', size=(70, 30))
        #hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
#End Class QuizDlg#

#GUI INI
app = wx.App(False)

frame = MainWindow(None,'AOS Mod Manager')    

app.MainLoop()
