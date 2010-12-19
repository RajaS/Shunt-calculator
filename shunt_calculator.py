#!/usr/bin/env python

# Author: Raja Selvaraj <rajajs@gmail.com>

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



class CalculatorGUI(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ShuntCalculator.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.mainpanel = wx.Panel(self, -1)
        self.lowerpanel = wx.Panel(self.mainpanel, -1,
                                   style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        self.middlepanel = wx.Panel(self.mainpanel, -1,
                                    style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        self.upperpanel = wx.Panel(self.mainpanel, -1,
                                   style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
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
                                          "RA press (mm Hg)")
        self.rapressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.lapresslabel = wx.StaticText(self.middlepanel, -1,
                                          "LA press (mm Hg)")
        self.lapressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.papresslabel = wx.StaticText(self.middlepanel, -1,
                                          "PA press (mm Hg)")
        self.papressctrl = wx.TextCtrl(self.middlepanel, -1, "")
        self.aopresslabel = wx.StaticText(self.middlepanel, -1,
                                          "Ao press (mm Hg)")
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
        self.calculatebutton = wx.Button(self.lowerpanel, -1, "Calculate")
        self.stepbutton = wx.Button(self.lowerpanel, -1, "Step")
        self.resultctrl = wx.TextCtrl(self.lowerpanel, -1, "",
                                      style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()
        self.__set_bindings()
        # end wxGlade
        self.calculator = ShuntCalculator()

        # for testing
        self.fill_demo_values()
        
        
    def __set_properties(self):
        # begin wxGlade: ShuntCalculator.__set_properties
        self.SetTitle("Shunt Calculator")
        self.titlelabel.SetFont(wx.Font(14, wx.DEFAULT,
                                        wx.NORMAL, wx.BOLD, 0, ""))
        self.upperpanel.SetMinSize((400, 40))
        self.sexctrl.SetSelection(0)
        self.lowerpanel.SetMinSize((400, 40))
        # end wxGlade

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
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.namectrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.agelabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.agectrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.sexlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.sexctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.htlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.htctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.wtlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.wtctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.hrlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.hrctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.hblabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.hbctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.svcsatlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.svcsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.ivcsatlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.ivcsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.pasatlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.pasatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.pvsatlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.pvsatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.aosatlabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.aosatctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.rapresslabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.rapressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.lapresslabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.lapressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.papresslabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.papressctrl, 0, wx.EXPAND, 0)
        inputsizer.Add(self.aopresslabel, 0,
                       wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        inputsizer.Add(self.aopressctrl, 0, wx.EXPAND, 0)
        middlepanelsizer.Add(inputsizer, 1, wx.RIGHT|wx.EXPAND, 5)
        outputsizer.Add(self.bsalabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.bsadisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.vo2label, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.vo2display, 0, wx.EXPAND, 0)
        outputsizer.Add(self.o2capacitylabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.o2capacitydisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.mvsatlabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.mvsatdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qplabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qpdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qslabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qsdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qelabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qedisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.qratiolabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.qratiodisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.pvrlabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.pvrdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.svrlabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.svrdisplay, 0, wx.EXPAND, 0)
        outputsizer.Add(self.pvrsvrratiolabel, 0,
                        wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        outputsizer.Add(self.pvrsvrratiodisplay, 0, wx.EXPAND, 0)
        middlepanelsizer.Add(outputsizer, 1, wx.LEFT|wx.EXPAND, 5)
        self.middlepanel.SetSizer(middlepanelsizer)
        mainpanelsizer.Add(self.middlepanel, 4,
           wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL,
                           5)
        sizer_1.Add(self.calculatebutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.stepbutton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        lowerpanelsizer.Add(sizer_1, 1, wx.EXPAND, 0)
        lowerpanelsizer.Add(self.resultctrl, 1, wx.ALL|wx.EXPAND, 2)
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


    def fill_demo_values(self):
        for ctrl, val in [(self.namectrl, 'John Doe'),
                          (self.agectrl, '36'),
                          (self.sexctrl, 'Male'),
                          (self.htctrl, '170'),
                          (self.wtctrl, '78'),
                          (self.hrctrl, '72'),
                          (self.hbctrl, '14'),
                          (self.svcsatctrl, '64'),
                          (self.ivcsatctrl, '56'),
                          (self.pvsatctrl, '99'),
                          (self.pasatctrl, '80'),
                          (self.aosatctrl, '99'),
                          (self.rapressctrl, '6'),
                          (self.lapressctrl, '8'),
                          (self.papressctrl, '20'),
                          (self.aopressctrl, '90')]:
            ctrl.SetValue(val)
    
        
    def on_calculate(self, event):
        """Run all the calculations and display the results"""
        vals = self.getvalues()
        print vals
        vals, err_msg, warn_msg = self.calculator.process_entries(vals)
        
        self.calculate_all(vals)

        
    def calculate_all(self, vals):
        """Main calculations.
        Done in stages.
        WAITFORRESUME flag determines if they will be run with or without break.
        """
        # Body surface area
        bsa = self.calculator.calculate_bsa(vals['ht'], vals['wt'])
        self.bsadisplay.SetValue(str(bsa))
        
        # Estimated Vo2
        print vals['sex'], vals['age'], vals['hr'], bsa
        
        vo2 = self.calculator.calculate_vo2(vals['sex'], vals['age'],
                                 vals['hr'], bsa)

        print vo2
        self.vo2display.SetValue(str(vo2))
                
        # Calculate MV saturation
        mvsat = self.calculator.calculate_mvsat(vals['svcsat'],
                                     vals['ivcsat'])
        self.mvsatdisplay.SetValue(str(mvsat))
        
        # O2 carrying capacity
        o2capacity = self.calculator.calculate_02capacity(vals['hb'])
        self.o2capacitydisplay.SetValue(str(o2capacity))
        
        # Qp
        qp = self.calculator.calculate_Qp(vo2, o2capacity, vals['pvsat'],
                               vals['pasat'])
        self.qpdisplay.SetValue(str(qp))

        # Qs
        qs = self.calculator.calculate_Qs(vo2, o2capacity, vals['aosat'],
                               mvsat)
        self.qsdisplay.SetValue(str(qs))

        # Qef
        qe = self.calculator.calculate_Qe(vo2, o2capacity, vals['pvsat'],
                                mvsat)
        self.qedisplay.SetValue(str(qe))
        
        # Qp / Qs
        qp_qs = qp / qs
        self.qratiodisplay.SetValue(str(qp_qs))
        
        # PVR
        pvr = (vals['papress'] - vals['lapress']) / qp
        self.pvrdisplay.SetValue(str(pvr))
        
        # SVR
        svr = (vals['aopress'] - vals['rapress']) / qs
        self.svrdisplay.SetValue(str(svr))
        


        
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
            if min_val > vals[k] > max_val:
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
                

