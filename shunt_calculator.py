#!/usr/bin/env python

# Based on http://www3.rbht.nhs.uk/flowcalculations.asp

####################
# Standard Units to use:
   # Height - cms
   # Wt - kgs
   # Age - years
   # Sex - 0=male, 1=female
   # HR - bpm
   # Hb - g/dl
   # all sat - %

from __future__ import division

import wx
import math
from pprint import pprint

__author__ = 'Raja Selvaraj <rajajs@gmail.com>'
__version__ = '0.4'

ABOUT_MESSAGE = """
Shunt Calculator version %s

Author: %s
""" %(__version__, __author__)

ID_SAVE = wx.NewId()
ID_QUIT = wx.NewId()
ID_ABOUT = wx.NewId()

ID_CLEAR = wx.NewId()
ID_NORMAL = wx.NewId()
ID_L2R = wx.NewId()
ID_R2L = wx.NewId()
ID_BIDIRECTIONAL = wx.NewId()
    

class CalculatorGUI(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ShuntCalculator.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.mainpanel = wx.Panel(self, -1)
        self.lowerpanel = wx.Panel(self.mainpanel, -1,
                                   style=wx.RAISED_BORDER|wx.TAB_TRAVERSAL)
        self.middlepanel = wx.Panel(self.mainpanel, -1,
                                    style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.upperpanel = wx.Panel(self.mainpanel, -1,
                                   style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.titlelabel = wx.StaticText(self.upperpanel, -1,
                                     "Shunt Calculator", style=wx.ALIGN_CENTRE)
        self.subtitle = wx.StaticText(self.upperpanel, -1,
                 """Enter all the values in the left side.
                    Results are displayed in right side.
                    You can run the calculations in one go or step-by-step.""")
        self.namelabel = wx.StaticText(self.middlepanel, -1, "Name")
        self.namectrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.agelabel = wx.StaticText(self.middlepanel, -1, "Age (yrs)")
        self.agectrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.sexlabel = wx.StaticText(self.middlepanel, -1, "Sex")
        self.sexctrl = wx.ComboBox(self.middlepanel, -1,
                       choices=["Male", "Female"],
                       style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.htlabel = wx.StaticText(self.middlepanel, -1, "Height (cm)")
        self.htctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.wtlabel = wx.StaticText(self.middlepanel, -1, "Weight (kg)")
        self.wtctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.hrlabel = wx.StaticText(self.middlepanel, -1, "Heart rate (bpm)")
        self.hrctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.hblabel = wx.StaticText(self.middlepanel, -1, "Hemoglobin (g/dl)")
        self.hbctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.svcsatlabel = wx.StaticText(self.middlepanel, -1, "SVC sat")
        self.svcsatctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.ivcsatlabel = wx.StaticText(self.middlepanel, -1, "IVC sat")
        self.ivcsatctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.pasatlabel = wx.StaticText(self.middlepanel, -1, "PA sat")
        self.pasatctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.pvsatlabel = wx.StaticText(self.middlepanel, -1, "LA sat")
        self.pvsatctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.aosatlabel = wx.StaticText(self.middlepanel, -1, "Ao sat")
        self.aosatctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.rapresslabel = wx.StaticText(self.middlepanel, -1,
                                          "Mean RA press (mm Hg)")
        self.rapressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.lapresslabel = wx.StaticText(self.middlepanel, -1,
                                          "Mean LA press (mm Hg)")
        self.lapressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.papresslabel = wx.StaticText(self.middlepanel, -1,
                                          "mean PA press (mm Hg)")
        self.papressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.aopresslabel = wx.StaticText(self.middlepanel, -1,
                                          "Mean Ao press (mm Hg)")
        self.aopressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.bsalabel = wx.StaticText(self.middlepanel, -1, "BSA (m2)")
        self.bsadisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                      style=wx.TE_READONLY)
        self.vo2label = wx.StaticText(self.middlepanel, -1,
                                      "Estimated VO2 (ml/min)")
        self.vo2display = wx.TextCtrl(self.middlepanel, -1, "",
                                      style=wx.TE_READONLY)
        self.o2capacitylabel = wx.StaticText(self.middlepanel, -1,
                                             "O2 carrying cap (ml/L)")
        self.o2capacitydisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                             style=wx.TE_READONLY)
        self.mvsatlabel = wx.StaticText(self.middlepanel, -1,
                                        "Mixed venous sat")
        self.mvsatdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                        style=wx.TE_READONLY)
        self.qplabel = wx.StaticText(self.middlepanel, -1, "Q pulm (l/min)")
        self.qpdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                     style=wx.TE_READONLY)
        self.qslabel = wx.StaticText(self.middlepanel, -1, "Q syst (L/min)")
        self.qsdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                     style=wx.TE_READONLY)
        self.qelabel = wx.StaticText(self.middlepanel, -1, "Q eff (L/min)")
        self.qedisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                     style=wx.TE_READONLY)
        self.rt2ltlabel = wx.StaticText(self.middlepanel, -1, "Rt to Lt shunt (L/min)")
        self.rt2ltdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                        style=wx.TE_READONLY)
        self.lt2rtlabel = wx.StaticText(self.middlepanel, -1, "Lt to Rt shunt (L/min)")
        self.lt2rtdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                        style=wx.TE_READONLY)
        self.qratiolabel = wx.StaticText(self.middlepanel, -1, "Qp / Qs")
        self.qratiodisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                         style=wx.TE_READONLY)
        self.pvrlabel = wx.StaticText(self.middlepanel, -1, "PVR (Wood units)")
        self.pvrdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                      style=wx.TE_READONLY)
        self.svrlabel = wx.StaticText(self.middlepanel, -1, "SVR (Wood units)")
        self.svrdisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                      style=wx.TE_READONLY)
        self.pvrsvrratiolabel = wx.StaticText(self.middlepanel, -1, "PVR / SVR")
        self.pvrsvrratiodisplay = wx.TextCtrl(self.middlepanel, -1, "",
                                              style=wx.TE_READONLY)
        self.calculatebutton = wx.BitmapButton(self.lowerpanel, -1,
                                               wx.Bitmap("icons/calculate.png"))
        self.stepbeginningbutton = wx.BitmapButton(self.lowerpanel, 1003,
                                                   wx.Bitmap("icons/beginning.png"))
        self.stepforwardbutton = wx.BitmapButton(self.lowerpanel, 1001,
                                                 wx.Bitmap("icons/forward.png"))
        self.stepbackbutton = wx.BitmapButton(self.lowerpanel, 1002,
                                              wx.Bitmap("icons/back.png"))
        self.stependbutton = wx.BitmapButton(self.lowerpanel, 1004,
                                             wx.Bitmap("icons/end.png"))

        self.messagectrl = wx.TextCtrl(self.lowerpanel, -1, "",
                                      style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.CreateStatusBar()
        self.__set_properties()
        self.__build_menubar()
        self.__do_layout()
        self.__set_bindings()
        # end wxGlade
        self.calculator = ShuntCalculator()

        # for testing
        ##
        # some input value sets
        self.DEMO_NORMAL = [(self.namectrl, 'Normal'),
                            (self.agectrl, '50'),
                            (self.sexctrl, 'Female'),
                            (self.htctrl, '165'),
                            (self.wtctrl, '60'),
                            (self.hrctrl, '70'),
                            (self.hbctrl, '13'),
                            (self.svcsatctrl, '73'),
                            (self.ivcsatctrl, '77'),
                            (self.pasatctrl, '74'),
                            (self.pvsatctrl, '99'),
                            (self.aosatctrl, '99'),
                            (self.rapressctrl, '5'),
                            (self.lapressctrl, '7'),
                            (self.papressctrl, '20'),
                            (self.aopressctrl, '90')]

        self.DEMO_LT2RT = [(self.namectrl, 'Left to right'),
                            (self.agectrl, '50'),
                            (self.sexctrl, 'Female'),
                            (self.htctrl, '165'),
                            (self.wtctrl, '60'),
                            (self.hrctrl, '70'),
                            (self.hbctrl, '11'),
                            (self.svcsatctrl, '70'),
                            (self.ivcsatctrl, '75'),
                            (self.pasatctrl, '82'),
                            (self.pvsatctrl, '99'),
                            (self.aosatctrl, '99'),
                            (self.rapressctrl, '6'),
                            (self.lapressctrl, '9'),
                            (self.papressctrl, '56'),
                            (self.aopressctrl, '78')]

        self.DEMO_RT2LT = [(self.namectrl, 'Right to left'),
                            (self.agectrl, '50'),
                            (self.sexctrl, 'Female'),
                            (self.htctrl, '165'),
                            (self.wtctrl, '60'),
                            (self.hrctrl, '70'),
                            (self.hbctrl, '13'),
                            (self.svcsatctrl, '71'),
                            (self.ivcsatctrl, '71'),
                            (self.pasatctrl, '71'),
                            (self.pvsatctrl, '99'),
                            (self.aosatctrl, '91'),
                            (self.rapressctrl, '10'),
                            (self.lapressctrl, '11'),
                            (self.papressctrl, '72'),
                            (self.aopressctrl, '82')]

        self.DEMO_BIDIRECTIONAL = [(self.namectrl, 'Bidirectional'),
                            (self.agectrl, '50'),
                            (self.sexctrl, 'Female'),
                            (self.htctrl, '165'),
                            (self.wtctrl, '60'),
                            (self.hrctrl, '70'),
                            (self.hbctrl, '20'),
                            (self.svcsatctrl, '60'),
                            (self.ivcsatctrl, '67'),
                            (self.pasatctrl, '80'),
                            (self.pvsatctrl, '99'),
                            (self.aosatctrl, '85'),
                            (self.rapressctrl, '15'),
                            (self.lapressctrl, '18'),
                            (self.papressctrl, '89'),
                            (self.aopressctrl, '68')]

        self.DEFAULT = [(self.namectrl, ''),
                            (self.agectrl, ''),
                            (self.sexctrl, 'Male'),
                            (self.htctrl, ''),
                            (self.wtctrl, ''),
                            (self.hrctrl, ''),
                            (self.hbctrl, ''),
                            (self.svcsatctrl, ''),
                            (self.ivcsatctrl, ''),
                            (self.pasatctrl, ''),
                            (self.pvsatctrl, ''),
                            (self.aosatctrl, ''),
                            (self.rapressctrl, ''),
                            (self.lapressctrl, ''),
                            (self.papressctrl, ''),
                            (self.aopressctrl, '')]





        self.old_vals = {}
        self.frame_current_count = 0
        self.frame_total_count = 0

        self.input_controls = [self.namectrl, self.sexctrl, self.agectrl,
                               self.htctrl, self.wtctrl, self.hrctrl,
                               self.hbctrl, self.ivcsatctrl, self.svcsatctrl,
                               self.pasatctrl, self.pvsatctrl,
                               self.aosatctrl, self.lapressctrl, self.rapressctrl,
                               self.papressctrl, self.aopressctrl]
        
        self.output_controls = [self.bsadisplay, self.vo2display,
                         self.mvsatdisplay, self.o2capacitydisplay,
                         self.qpdisplay, self.qsdisplay, self.qedisplay,
                         self.rt2ltdisplay, self.lt2rtdisplay,
                         self.qratiodisplay, self.pvrdisplay, self.svrdisplay,
                                self.pvrsvrratiodisplay]


        
    def __set_properties(self):
        # begin wxGlade: ShuntCalculator.__set_properties
        self.SetTitle("Shunt Calculator")
        self.titlelabel.SetFont(wx.Font(14, wx.DEFAULT,
                                        wx.NORMAL, wx.BOLD, 0, ""))
        self.upperpanel.SetMinSize((400, 40))
        self.sexctrl.SetSelection(0)
        self.lowerpanel.SetMinSize((400, 40))
        # end wxGlade

    def __build_menubar(self):
        self.MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(ID_SAVE, "&Save", "Save the report")
        file_menu.Append(ID_QUIT, "&Quit","Quit the program")
   
        input_menu = wx.Menu()
        input_menu.Append(ID_CLEAR, "Clear", "Clear input values")
        input_menu.Append(ID_NORMAL, "Demo - Normal", "Fill normal values")
        input_menu.Append(ID_L2R, "Demo - left to right", "Fill values for left to right shunt")
        input_menu.Append(ID_R2L, "Demo - right to left", "Fill values for right to left shunt")
        input_menu.Append(ID_BIDIRECTIONAL, "Demo - bidirectional", "Fill values for bidirectional shunt")

        help_menu = wx.Menu()
        help_menu.Append(ID_ABOUT, "About", "About this application")
        
        self.MenuBar.Append(file_menu, "&File")
        self.MenuBar.Append(input_menu, "&Input")
        self.MenuBar.Append(help_menu, "&Help")

        
        self.SetMenuBar(self.MenuBar)
        
        
    def __do_layout(self):
        # begin wxGlade: ShuntCalculator.__do_layout
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainpanelsizer = wx.BoxSizer(wx.VERTICAL)
        lowerpanelsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        middlepanelsizer = wx.BoxSizer(wx.HORIZONTAL)
        outputsizer = wx.GridSizer(11, 2, 0, 0)
        inputsizer = wx.GridSizer(16, 2, 0, 0)
        upperpanelsizer = wx.BoxSizer(wx.VERTICAL)
        upperpanelsizer.Add(self.titlelabel, 2,
         wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        upperpanelsizer.Add(self.subtitle, 0,
                            wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.upperpanel.SetSizer(upperpanelsizer)
        mainpanelsizer.Add(self.upperpanel, 1,
                           wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
        inputsizer.Add(self.namelabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.namectrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.agelabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.agectrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.sexlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.sexctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.htlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.htctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.wtlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.wtctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.hrlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.hrctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.hblabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.hbctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.svcsatlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.svcsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.ivcsatlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.ivcsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.pasatlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.pasatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.pvsatlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.pvsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.aosatlabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.aosatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.rapresslabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.rapressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.lapresslabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.lapressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.papresslabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.papressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.aopresslabel, 0,
                       wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.aopressctrl, 0, wx.EXPAND, 0)
        middlepanelsizer.Add(inputsizer, 2, wx.RIGHT|wx.EXPAND, 10)
        outputsizer.Add(self.bsalabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.bsadisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.vo2label, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.vo2display, 0, wx.EXPAND, 0)
        outputsizer.Add(self.o2capacitylabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.o2capacitydisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.mvsatlabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.mvsatdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qplabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qpdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qslabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qsdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qelabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qedisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.rt2ltlabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.rt2ltdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.lt2rtlabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.lt2rtdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qratiolabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qratiodisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.pvrlabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.pvrdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.svrlabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.svrdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.pvrsvrratiolabel, 0,
                        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.pvrsvrratiodisplay, 0, wx.EXPAND, 0)
        middlepanelsizer.Add(outputsizer, 3, wx.LEFT|wx.EXPAND, 10)
        self.middlepanel.SetSizer(middlepanelsizer)
        mainpanelsizer.Add(self.middlepanel, 4,
           wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL,
                           5)
        sizer_1.Add(self.calculatebutton, 2, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_1.Add(self.stepbeginningbutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.stepbackbutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.stepforwardbutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.stependbutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        lowerpanelsizer.Add(sizer_1, 1, wx.EXPAND, 0)
        lowerpanelsizer.Add(self.messagectrl, 1, wx.ALL|wx.EXPAND, 2)
        self.lowerpanel.SetSizer(lowerpanelsizer)
        mainpanelsizer.Add(self.lowerpanel, 1,
                           wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
        self.mainpanel.SetSizer(mainpanelsizer)
        mainsizer.Add(self.mainpanel, 1, wx.EXPAND, 0)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Layout()
        # end wxGlade


    def __set_bindings(self):
        self.calculatebutton.Bind(wx.EVT_BUTTON, self.on_calculate)
        self.stepforwardbutton.Bind(wx.EVT_BUTTON, self.on_step)
        self.stepbackbutton.Bind(wx.EVT_BUTTON, self.on_step)
        self.stepbeginningbutton.Bind(wx.EVT_BUTTON, self.on_step)
        self.stependbutton.Bind(wx.EVT_BUTTON, self.on_step)

        self.Bind(wx.EVT_MENU, self.fill_demo_values, id=ID_NORMAL)
        self.Bind(wx.EVT_MENU, self.fill_demo_values, id = ID_L2R)
        self.Bind(wx.EVT_MENU, self.fill_demo_values, id = ID_R2L)
        self.Bind(wx.EVT_MENU, self.fill_demo_values, id = ID_BIDIRECTIONAL)
        self.Bind(wx.EVT_MENU, self.fill_default_values, id=ID_CLEAR)

        self.Bind(wx.EVT_MENU, self.display_about, id=ID_ABOUT)


    def display_about(self, event):
        """Display an about message"""
        dlg = wx.MessageDialog(self, ABOUT_MESSAGE, "About this app", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
             
        
    def getvalues(self):
        """read the input values into a dictionary"""
        vals = {}

        for key, ctrl in [('name', self.namectrl),
                          ('age', self.agectrl),
                          ('sex', self.sexctrl),
                          ('ht', self.htctrl),
                          ('wt', self.wtctrl),
                          ('hr', self.hrctrl),
                          ('hb', self.hbctrl),
                          ('svcsat', self.svcsatctrl),
                          ('ivcsat', self.ivcsatctrl),
                          ('pvsat', self.pvsatctrl),
                          ('pasat', self.pasatctrl),
                          ('aosat', self.aosatctrl),
                          ('rapress', self.rapressctrl),
                          ('lapress', self.lapressctrl),
                          ('papress', self.papressctrl),
                          ('aopress', self.aopressctrl)]:
            vals[key] = ctrl.GetValue()

        if vals['sex'] == 'Male':
            vals['sex'] = 0
        else:
            vals['sex'] = 1
            
        return vals


    def fill_demo_values(self, event):
        """Demo input values"""
        event_id = event.GetId()

        ids = [ID_NORMAL, ID_L2R, ID_R2L, ID_BIDIRECTIONAL]
        vals = [self.DEMO_NORMAL, self.DEMO_LT2RT,
                self.DEMO_RT2LT, self.DEMO_BIDIRECTIONAL]
        
        for ctrl, val in vals[ids.index(event_id)]:
            ctrl.SetValue(val)
    

    def fill_default_values(self, event):
        """Values that will be filled in initially
        and on clearing entered values"""
        for ctrl, val in self.DEFAULT:
            ctrl.SetValue(val)

        for ctrl in self.output_controls:
            ctrl.Clear()
            
            
    def on_calculate(self, event):
        """Run all the calculations and display the results"""
        vals = self.getvalues()
        vals, err_msg, warn_msg = self.calculator.process_entries(vals)

        for control in self.output_controls:
            control.Clear()
            
        if err_msg != '':
            self.messagectrl.SetValue(err_msg)
            return

        self.messagectrl.SetValue(warn_msg)
        self.frames = self.calculate_all(vals)
        self.frame_total_count = len(self.frames)
        
        if event != None:
            self.display_result_frame(self.frames[len(self.frames)-1])

            
    def calculate_all(self, vals):
        """Main calculations.
        Done in stages.
        Add the values to be displayed to a list
        """
        results_display = []
        
        # Body surface area
        bsa = self.calculator.calculate_bsa(vals['ht'], vals['wt'])

        if self.calculator.BSA == 'mosteller':
            results_display.append((self.bsadisplay, "Mosteller's formula"))
            results_display.append((self.bsadisplay, "sqrt(Height(cm) x Weight(kg) / 3600)"))
            results_display.append((self.bsadisplay, "sqrt(%d x %d / 3600)" %(vals['ht'], vals['wt'])))
            
        elif self.calculator.BSA == 'dubois':
            results_display.append((self.bsadisplay, "Dubois' formula"))
            results_display.append((self.bsadisplay,
                                    "0.20247 x height in metres ^ 0.725 x weight ^ 0.425"))
            results_display.append((self.bsadisplay,
                   "0.02047 x %0.2f ^ 0.725 x %d ^ 0.425" %(vals['ht']/100, vals['wt'])))
            results_display.append((self.bsadisplay,
                                    "0.02047 x %0.2f x %0.2f" %(vals['ht']**0.725,
                                                                vals['wt']**0.425)))
            
        results_display.append((self.bsadisplay, str(bsa)))
        
        # Estimated Vo2
        vo2 = self.calculator.calculate_vo2(vals['sex'], vals['age'],
                                 vals['hr'], bsa)

        if vals['sex'] == 0:
            results_display.append((self.vo2display,
                          "Male: BSA x (138.1 - (11.49 x log(age)) + (0.378 x Heart rate)))"))
            results_display.append((self.vo2display,
             "%0.2f x (138.1 - (11.49 x log(%d)) + (0.378 x %d)))" %(bsa, vals['age'], vals['hr'])))
            results_display.append((self.vo2display,
             "%0.2f x (138.1 - (11.49 x %d) + %d))" %(bsa, math.log(vals['age']), 0.378*vals['hr'])))
            
        elif vals['sex'] == 1:
            results_display.append((self.vo2display,
                       "Female: BSA x (138.1 - (11.49 x log(age)) + (0.378 x Heart rate)))"))
            results_display.append((self.vo2display,
              "%0.2f x (138.1 - (11.49 x log(%d)) + (0.378 x %d)))" %(bsa, vals['age'], vals['hr'])))
            results_display.append((self.vo2display,
              "%0.2f x (138.1 - (11.49 x %d) + %d))" %(bsa, math.log(vals['age']), 0.378*vals['hr'])))
        results_display.append((self.vo2display, str(vo2)))
                
        # Calculate MV saturation
        mvsat = self.calculator.calculate_mvsat(vals['svcsat'],
                                     vals['ivcsat'])
        if self.calculator.MVSAT == 'svc':
            results_display.append((self.mvsatdisplay, "= SVC saturation"))
        elif self.calculator.MVSAT == 'ivc':
            results_display.append((self.mvsatdisplay, "= IVC saturation"))
        elif self.calculator.MVSAT == 'combo1':
            results_display.append((self.mvsatdisplay, "(3 x SVC + IVC) / 4"))
            results_display.append((self.mvsatdisplay, "(3 x %d + %d) / 4" %(vals['svcsat'], vals['ivcsat'])))
            results_display.append((self.mvsatdisplay, "(%d + %d) / 4" %(3*vals['svcsat'], vals['ivcsat'])))
        elif self.calculator.MVSAT == 'combo2':
            results_display.append((self.mvsatdisplay, "(2 x SVC + 3 x IVC) / 5"))
            results_display.append((self.mvsatdisplay, "(2 x %d + 3 x %d) / 5" %(vals['svcsat'], vals['ivcsat'])))
            results_display.append((self.mvsatdisplay, "(%d + %d) / 5" %(2*vals['svcsat'], 3*vals['ivcsat'])))
        elif self.calculator.MVSAT == 'combo3':
            results_display.append((self.mvsatdisplay, "(SVC + 2 x IVC) / 3"))
            results_display.append((self.mvsatdisplay, "(%d + 2 x %d) / 3" %(vals['svcsat'], vals['ivcsat'])))
            results_display.append((self.mvsatdisplay, "(%d + %d) / 4" %(vals['svcsat'], 2*vals['ivcsat'])))
        results_display.append((self.mvsatdisplay, str(mvsat)))
        
        # O2 carrying capacity
        o2capacity = self.calculator.calculate_02capacity(vals['hb'])
        results_display.append((self.o2capacitydisplay, "Hb x 1.36 x 10"))
        results_display.append((self.o2capacitydisplay, str(o2capacity)))
        
        # Qp
        qp = self.calculator.calculate_Qp(vo2, o2capacity, vals['pvsat'],
                               vals['pasat'])

        results_display.append((self.qpdisplay, "O2 capacity x (PV sat - PA sat) / 100"))
        results_display.append((self.qpdisplay,
                  "%0.2f x (%d - %d) / 100" %(o2capacity, vals['pvsat'], vals['pasat'])))
        results_display.append((self.qpdisplay, str(qp)))

        # Qs
        qs = self.calculator.calculate_Qs(vo2, o2capacity, vals['aosat'],
                               mvsat)
        results_display.append((self.qsdisplay, "O2 capacity x (Ao sat - MV sat) / 100"))
        results_display.append((self.qsdisplay,
                  "%0.2f x (%d - %d) / 100" %(o2capacity, vals['aosat'], mvsat)))
        
        results_display.append((self.qsdisplay, str(qs)))

        # Qef
        qe = self.calculator.calculate_Qe(vo2, o2capacity, vals['pvsat'],
                                mvsat)
        results_display.append((self.qedisplay, "O2 capacity x (PV sat - MV sat) / 100"))
        results_display.append((self.qedisplay,
                  "%0.2f x (%d - %d) / 100" %(o2capacity, vals['pvsat'], mvsat)))
        results_display.append((self.qedisplay, str(qe)))

        # shunts
        rt2lt = qs - qe
        lt2rt = qp - qe
        results_display.append((self.rt2ltdisplay, "Qs - Qeff"))
        results_display.append((self.rt2ltdisplay, str(rt2lt)))
        results_display.append((self.lt2rtdisplay, "Qp - Qeff"))
        results_display.append((self.lt2rtdisplay, str(lt2rt)))
        
        # Qp / Qs
        qp_qs = qp / qs
        results_display.append((self.qratiodisplay, "Qp / Qs"))
        results_display.append((self.qratiodisplay, str(qp_qs)))
        
        # PVR
        pvr = (vals['papress'] - vals['lapress']) / qp
        results_display.append((self.pvrdisplay, "(PA press - LA pressure) / Qp"))
        results_display.append((self.pvrdisplay, "(%d - %d) / %0.2f" %(vals['papress'], vals['lapress'], qp)))
        results_display.append((self.pvrdisplay, str(pvr)))
        
        # SVR
        svr = (vals['aopress'] - vals['rapress']) / qs
        results_display.append((self.svrdisplay, "(Ao press - RA pressure) / Qs"))
        results_display.append((self.svrdisplay, "(%d - %d) / %0.2f" %(vals['aopress'], vals['rapress'], qs)))
        results_display.append((self.svrdisplay, str(svr)))

        # PVR / SVR
        pvrsvrratio = pvr / svr
        results_display.append((self.pvrsvrratiodisplay, "PVR / SVR"))
        results_display.append((self.pvrsvrratiodisplay, "%0.2f / %0.2f" %(pvr, svr)))
        results_display.append((self.pvrsvrratiodisplay, str(pvrsvrratio)))
        
        return self.build_frames(results_display)

        
    def build_frames(self, results_display):
        """Given the steps in the display of results, build
        the individual frames"""
        frames = {}
        framecounter = 0

        # first frame is empty
        frames[framecounter] = {}

        #
        for control, value in results_display:
            framecounter += 1
            frames[framecounter] = frames[framecounter-1].copy()
            control_index = self.output_controls.index(control)
            frames[framecounter][control_index] = value

        return frames

                
    def display_result_frame(self, frame):
        """Display one frame from the results.
        frame is a dict with keys being the control indices and
        values being the value to set"""
        for ctrl_index in frame:
            control = self.output_controls[ctrl_index]
            control.SetValue(frame[ctrl_index])            


    def on_step(self, event):
        """Any step button is pressed"""
        id = event.GetId()

        # validate entries, check for changes
        vals = self.getvalues()

        for control in self.output_controls:
            control.Clear()
            
        # if results have not been calculated, calculate them
        if vals != self.old_vals:
            vals, err_msg, warn_msg = self.calculator.process_entries(vals)
            self.old_vals = vals.copy()

            if err_msg != '':
                self.messagectrl.SetValue(err_msg)
                return
            self.messagectrl.SetValue(warn_msg)

            self.frames = self.calculate_all(vals)
            self.frame_total_count = len(self.frames)
            #self.calculate_all(vals)
        
        if id == 1001:
            self.frame_current_count += 1
            if self.frame_current_count == self.frame_total_count:
                self.frame_current_count -= 1
                return
            
        elif id == 1002:
            self.frame_current_count -= 1
            if self.frame_current_count < 0:
                self.frame_current_count = 0
                return

        elif id == 1003:
            if self.frame_current_count == 0:
                return
            self.frame_current_count = 0

        elif id == 1004:
            if self.frame_current_count == self.frame_total_count-1:
                return
            self.frame_current_count = self.frame_total_count -1

        self.display_result_frame(self.frames[self.frame_current_count])
                
        
        
class ShuntCalculator():
    """Calculate shunt flows and resistances from the pressure
    and saturation values"""
    def __init__(self):
        # initialize variables
        self.BSA = 'mosteller'
        self.MVSAT = 'combo1'
        
        self.WAITFORRESUME = False
        self.RESUME = False
        

    def calculate_bsa(self, ht, wt):
        """body surface area returned as sq m.
        ht is in cm and wt is in kg"""
        if self.BSA == 'mosteller':
            return (ht * wt / 3600) ** 0.5
        elif self.BSA == 'dubois':
            return 0.20247 * ((ht / 100) ** 0.725) * (wt ** 0.425)
        

    def calculate_vo2(self, sex, age, hr, bsa):
        """return vo2 as ml/min.
        sex is 0 for male and 1 for female.
        hr is in bpm"""
        if sex == 0:
            return bsa * (138.1 - (11.49 * math.log(age)) + (0.378 * hr))
        elif sex == 1:
            return bsa * (138.1 - (17.04 * math.log(age)) + (0.378 * hr))
        

    def calculate_02capacity(self, hb):
        """calculate oxygen carrying capacity as ml/L.
        1.36 is ml/g
        10 is for dl/L"""
        return hb * 1.36 * 10


    def calculate_Qp(self, vo2, o2capacity, pvsat, pasat):
        """calculate pulmonic flow"""
        return vo2 / (o2capacity * (pvsat - pasat) / 100)


    def calculate_Qs(self, vo2, o2capacity, aosat, mvsat):
        """calculate systemic flow"""
        return vo2 / (o2capacity * (aosat - mvsat) / 100)


    def calculate_Qe(self, vo2, o2capacity, pvsat, mvsat):
        """effective flow"""
        return vo2 / (o2capacity * (pvsat - mvsat) / 100)


    def calculate_mvsat(self, svcsat, ivcsat):
        """various methods to calculate mixed venous sat"""
        if self.MVSAT == 'svc':
            return svcsat
        elif self.MVSAT == 'ivc':
            return ivcsat
        elif self.MVSAT == 'combo1':
            return (3 * svcsat + ivcsat) / 4
        elif self.MVSAT == 'combo2':
            return (2 * svcsat + 3 * ivcsat) / 5
        elif self.MVSAT == 'combo3':
            return (svcsat + ivcsat * 2) / 3


    def process_entries(self, vals):
        """Process the input vals as a dictionary.
        keys:
        ht, wt, age, sex, hr, hb,
        svcsat, ivcsat, pasat, pvsat, aosat
        rapress, lapress, papress, aopress

        input vals may be as strings.
        sex should be 1,0
        returns error and warning msg.
        """
        self.vals = vals
        warn_msg = ''
        err_msg = ''

        # check all are valid numbers
        for key in vals:
            try:
                vals[key] = float(vals[key])
            except ValueError:
                if not key == 'name':
                    err_msg += ' '.join(['Error: Entry for', key, 'not valid\n'])

        if err_msg != '':
            return vals, err_msg, warn_msg
        
        # check some simple things

        assertions = [
            (50, 200, 'ht', 'height'),
            (3, 100, 'wt', 'weight'),
            (0.5, 100, 'age', 'age'),
            (30, 200, 'hr', 'heart rate'),
            (4, 20, 'hb', 'hemoglobin'),
            (1, 40, 'rapress', 'RA pressure'),
            (1, 40, 'lapress', 'LA pressure'),
            (5, 100, 'papress', 'PA pressure'),
            (20, 200, 'aopress', 'aortic pressure')]

        for min_val, max_val, k, parameter in assertions:
            if vals[k] > max_val or vals[k] < min_val:
                warn_msg += ' '.join(['Warning: Check value entered for', parameter, '\n'])
                
        sats = [('svcsat', 'SVC'),
                ('ivcsat', 'IVC'),
                ('pasat', 'PA'),
                ('pvsat', 'PV'),
                ('aosat', 'Ao')]

        for k, label in sats:
            if vals[k] > 100:
                err_msg += ' '.join(['Error:', label, 'saturation exceeds 100%'])

        return vals, err_msg, warn_msg

    
            
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    s = CalculatorGUI(None)
    app.SetTopWindow(s)
    s.Show()
    app.MainLoop()
                

