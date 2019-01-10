############################################################################################################################
# The following is the GUI caller. Either a windows desktop version or a different one for the web site version
############################################################################################################################

# Revision 2017-04-18
# Major changes in Tkinter calls so no will run in Python 2.7 environment.


import Tkinter as tkinter
from Tkinter import Text
import ttk


import LH_Maths_20170418_R09
from LH_Maths_20170418_R09 import siteGUI
from LH_Maths_20170418_R09 import process_here


# When calling PS_Maths....py the following varibles in class siteGUI are used and their meanings   U = user input.  R = reports [back] to user
# These varibles are to keep track of instalation parameters.
"""class siteGUI:                              #   (U)ser input or (R)eport or both?        Description
    GUI_initial_data = int(1)               # R   Once turns a 0 then unlock rest of inputs
    GUI_process_option = str('basicdata')   # U   Contents is one of.... 'basicdata' 'pipe' 'pipeeff' 'pendiaLk' 'pendia' 'SetLkNumLHandJ' 'SetNumLHandJ' 'SetCableEff'  'NewCable' 'NewCableV' 'NewCableMaterial' 'NewCablesize' 'NewCableAWG'  'NewCablesize' 'CableLock' 
    GUI_revision = str('R09')               # R   Version number for this maths routine for GUI to display
    GUI_meas_sys = str('Metric')            # U   Units system to use  'Metric' or Imperial'
    GUI_LHtype = str('LH1500 and Pro')      # U   'LH1500 and Pro', 'LH1500 Pro +', 'LH1500 and Pro with SD PCB', 'LH1500 Pro + with SD PCB'
    GUI_avail_lps = str('')                 # U   either lps or gpm float.  eg '12 lps'  or '23 gpm'
    GUI_actual_lps = str('')                # R   either lps or gpm float.  eg '12 lps'  or '23 gpm'

    GUI_pipe_head = str('')                 # U   Pipe/Flume material
    GUI_pipe_head = str('')                 # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_pipe_len = str('')                  # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_water_depth = str('')               # R   mm depth of water in Flume/Pipe
    GUI_PipeFlume = str('')                 # UR  either 'Pipe' or 'Flume'
    GUI_PipeFlumeT1 = str('')               # R   Title for pipe diameter / flume width 
    GUI_PipeFlumeT2 = str('')               # R   Title for flume height or is blank
    GUI_pipe_mat = str('')                  # U   Either 'Drawn plastic tube','General steel','Asphalted iron','Galv. steel','Cast steel','Wood','Concrete','RivetedSteel'
  
    GUI_pipe_dia = str('')                  # UR  either mm or inch float  eg '34 mm' or '1.2 in'
    GUI_pipe_height = str('')               # UR  either mm or inch float  eg '34 mm' or '1.2 in'
    GUI_pipe_capacity = str('')             # R   either lps or gpm float.  eg '12 lps'  or '23 gpm'

    GUI_LH_head = str('')                   # UR  This is the actual head at the LH turbine. It is from flume top to river exit. It is the head the LH experiences.
    GUI_Num_LH = int(1)                     # UR  Number of turbines. Ranges from 1 to 10
    GUI_LockNumLH = int(0)                  # UR  A 0 or a 1. if 1 then number of LH hydros is locked

    GUI_LH_V_Opr = str('')                  # R   Generator output voltage at actual water throughput at max power point output
    GUI_LH_watts_Opr = str('')              # R   Generator output power at actual water throughput at max power point output
    GUI_LH_rpm_Opr = str('')                # R   Generator rpm at rated water capacity at max power point output
    GUI_LH_rpm_NL = str('')                 # R   Generator rpm at actual head with max. possible water throughput and no electrical load
    GUI_LH_Draft_T = str('')                # R   Draft tube diameter to be used for this head

    GUI_LH_V_NL = str('')                   # R   Generator output voltage at actual head with max. possible water throughput and no electrical load
    GUI_LH_pwr_tot = str('')                # R   eg '2562 W'

    GUI_cable_eff_target = str('')          # U   a string of int %.  eg '89 %'
    GUI_cable_len = str('')                 # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_Load_Vmax = str('')                 # UR  a united int string eg '56 V'   This is the maximum voltage the inverter/charge controller can handle.
    GUI_Load_Vmin = str('')                 # UR  a united int string eg '56 V'   This is the maimium working for the inverter/charge controller.
    GUI_Aload_V = str('')                   # R   a united int string eg '56 V'
    
    GUI_LockCable = int(0)                  # UR  A 0 or a 1. if 1 then cable size is locked
    GUI_cable_material = str('')            # U   'Copper', 'Aluminium' or 'Steel'
    GUI_cable_size = str('')                # UR  A 3 decimal place number or sqr mm  eg '2.256'
    GUI_cable_AWG = str('')                 # UR  AWG.  eg '0000' '0'  '13'
    GUI_cable_mm_AWG = str('mm')            #     Just needs to be set for maths routine to know if are in mm or AWG mode

    GUI_cable_mm_title = str('')            # R   Title for cables sqr mm size
    GUI_cable_AWG_title = str('')           # R   Title for cables AWG size
    GUI_cable_dia_mm_sld = str('')          # R   eg '2.23 mm'
    GUI_cable_dia_mm_str = str('')          # R   eg '2.23 mm'
    GUI_cable_dia_in_sld = str('')          # R   eg '0.213 in'
    GUI_cable_dia_in_str = str('')          # R   eg '0.213 in'

    GUI_cable_A = str('')                   # R   eg '34.3 A'
    GUI_actual_cable_eff = str('')          # R   eg '87 %'
    GUI_Load_pwr = str('')                  # R   eg '895 W'

    GUI_design_notes_hydro = str( '' )      # R   An empty string for design comments for the end user to read and understand
    GUI_design_notes_elec = str( '' )       # R   An empty string for design comments for the end user to read and understand
    GUI_design_notes_safety = str( '' )     # R   An empty string for design comments for the end user to read and understand

    GUI_revision = str('R09')               # R   Version number for this maths routine for GUI to display
    GUI_diag = str('')                      # R   All diagnostics go to here
    GUIcr = '<br>'                          # R   Carriage return with a line feed character
    GUI_diag_cr = str('\r\n')               # R   or '<br>'   # Carriage return with a line feed character"""


def fetchGUI_data():
    siteGUI.GUI_meas_sys = dialouge.units.get()
    siteGUI.GUI_LHtype = dialouge.LHtype.get()
    siteGUI.GUI_avail_lps = dialouge.avail_lps.get()

    siteGUI.GUI_pipe_mat = dialouge.pipe_mat.get()
    siteGUI.GUI_pipe_head = dialouge.pipe_head.get()
    siteGUI.GUI_pipe_len = dialouge.pipe_len.get()

    siteGUI.GUI_PipeFlume = dialouge.PipeFlume.get()
    siteGUI.GUI_pipe_dia = dialouge.pipe_dia.get()
    siteGUI.GUI_pipe_height = dialouge.pipe_height.get()
    siteGUI.GUI_LH_head = dialouge.LH_head.get()
    siteGUI.GUI_Num_LH = dialouge.Num_LH.get()
    siteGUI.GUI_LockNumLH = dialouge.LockNumLH.get()

    siteGUI.GUI_cable_eff_target = dialouge.design_cable_eff.get()
    siteGUI.GUI_cable_len = dialouge.cable_len.get()
    siteGUI.GUI_Load_Vmax = dialouge.Load_Vmax.get()
    siteGUI.GUI_Load_Vmin = dialouge.Load_Vmin.get()
    siteGUI.GUI_LockCable = dialouge.LockCable.get()
    siteGUI.GUI_cable_material = dialouge.cable_material.get()
    siteGUI.GUI_cable_size = dialouge.cable_size.get()
    siteGUI.GUI_cable_AWG = dialouge.cable_AWG.get()



def putGUI_data():
    dialouge.avail_lps.set( siteGUI.GUI_avail_lps )
    dialouge.actual_lps.set( siteGUI.GUI_actual_lps )
    dialouge.pipe_head.set( siteGUI.GUI_pipe_head )
    dialouge.pipe_len.set( siteGUI.GUI_pipe_len )

    if siteGUI.GUI_PipeFlume == "Pipe":
        siteGUI.GUI_pipe_width = ""
        dialouge.pipe_height_entry.config(state='DISABLED')
        
    if siteGUI.GUI_PipeFlume == "Flume":
        dialouge.pipe_height_entry.config(state='NORMAL')

    if siteGUI.GUI_PipeFlume == "PS_pipe":
        siteGUI.GUI_pipe_width = ""
        dialouge.pipe_height_entry.config(state='DISABLED')

    dialouge.PipeFlumeT1.set( siteGUI.GUI_PipeFlumeT1 )
    dialouge.PipeFlumeT2.set( siteGUI.GUI_PipeFlumeT2 )
    dialouge.water_depth.set( siteGUI.GUI_water_depth )

    dialouge.pipe_dia.set( siteGUI.GUI_pipe_dia )
    dialouge.pipe_height.set( siteGUI.GUI_pipe_height )

    dialouge.LH_head.set( siteGUI.GUI_LH_head )
    dialouge.Num_LH.set( siteGUI.GUI_Num_LH )
    dialouge.LockNumLH.set( siteGUI.GUI_LockNumLH )
    dialouge.LH_Draft_T.set( siteGUI.GUI_LH_Draft_T )

    dialouge.pipe_capacity.set( siteGUI.GUI_pipe_capacity )
    dialouge.LH_rpm_Opr.set( siteGUI.GUI_LH_rpm_Opr )
    dialouge.LH_rpm_NL.set( siteGUI.GUI_LH_rpm_NL )
    dialouge.LH_watts_Opr.set( siteGUI.GUI_LH_watts_Opr )
    dialouge.LH_pwr_tot.set( siteGUI.GUI_LH_pwr_tot )
    dialouge.LH_V_Opr.set( siteGUI.GUI_LH_V_Opr )
    dialouge.LH_V_NL.set( siteGUI.GUI_LH_V_NL )

    dialouge.design_cable_eff.set( siteGUI.GUI_cable_eff_target )
    dialouge.cable_len.set( siteGUI.GUI_cable_len )
    dialouge.Load_Vmax.set( siteGUI.GUI_Load_Vmax )
    dialouge.Load_Vmin.set( siteGUI.GUI_Load_Vmin )
    dialouge.Aload_V.set( siteGUI.GUI_Aload_V )
    dialouge.LockCable.set( siteGUI.GUI_LockCable )
    dialouge.cable_size.set( siteGUI.GUI_cable_size )
    dialouge.cable_AWG.set( siteGUI.GUI_cable_AWG )

    dialouge.cable_material.set( siteGUI.GUI_cable_material )
    dialouge.cable_mm_title.set( siteGUI.GUI_cable_mm_title )
    dialouge.cable_AWG_title.set( siteGUI.GUI_cable_AWG_title )

    dialouge.cable_dia_mm_sld.set( siteGUI.GUI_cable_dia_mm_sld )
    dialouge.cable_dia_mm_str.set( siteGUI.GUI_cable_dia_mm_str )
    dialouge.cable_dia_in_sld.set( siteGUI.GUI_cable_dia_in_sld )
    dialouge.cable_dia_in_str.set( siteGUI.GUI_cable_dia_in_str )

    dialouge.cable_A.set( siteGUI.GUI_cable_A )
    dialouge.actual_cable_eff.set( siteGUI.GUI_actual_cable_eff )
    dialouge.Load_pwr.set( siteGUI.GUI_Load_pwr )

    dialouge.revision.set( 'Maths version ' + siteGUI.GUI_revision )

    dialouge.diag.delete(1.0, 'end')
    dialouge.diag.insert('1.0', siteGUI.GUI_diag )

    dialouge.design_noted.delete(1.0, 'end')
    dialouge.design_noted.insert('1.0', ( 'Hydro design notes..........................................\n' + siteGUI.GUI_design_notes_hydro + '\nElectrical design notes.....................................\n' + siteGUI.GUI_design_notes_elec + '\nSafety warnings.............................................\n' + siteGUI.GUI_design_notes_safety ) )





##############################################################
# The following defines are the actions for all widgets in gui
##############################################################

def units(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'basicdata'
    process_here()
    putGUI_data()

def BasicData(*args):        # For entering of lps, head, PS type and produce rest or an update of just one of these
    fetchGUI_data()
    # This is the only widget call permissable untill there is enough data to work with. See site.initial_data permits unlocking rest of widgets
    siteGUI.GUI_process_option = 'basicdata'
    process_here()
    if( siteGUI.GUI_initial_data == 0 ):
        # Now unblock rest of gui dialouge for user to update with own site data
        dialouge.pipe_head_entry.config(state='NORMAL')
        dialouge.pipe_len_entry.config(state='NORMAL')
        dialouge.pipe_dia_entry.config(state='NORMAL')
        dialouge.pipe_height_entry.config(state='NORMAL')
        dialouge.Num_LH_entry.config(state='NORMAL')
        dialouge.load_Vmin_entry.config(state='NORMAL')
        dialouge.design_cable_eff_entry.config(state='NORMAL')
        dialouge.cable_len_entry.config(state='NORMAL')
        dialouge.cable_material_entry.config(state='NORMAL')
        dialouge.cable_size_entry.config(state='NORMAL')
        dialouge.cable_AWG_entry.config(state='NORMAL')

        #dialouge.Lock_pipe_entry.config( state=NORMAL)
        #dialouge.LockNumLH_entry.config( state=NORMAL)
        #dialouge.LockCable_entry.config( state=NORMAL)

    putGUI_data()

    
def newpipelen(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'pipelen'
    process_here()
    putGUI_data()

def newpendia(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'pipe_dia'
    process_here()
    putGUI_data()

def newpendia(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'pipe_dia'
    process_here()
    putGUI_data()

def PipeFlume_sel(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'pipe_dia'
    process_here()
    putGUI_data()

def newNoPS(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'SetNumLH'
    process_here()
    putGUI_data()

def LockNumLH(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'SetLockNumLH'
    process_here()
    putGUI_data()

def newcableeff(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'SetCableEff'
    process_here()
    putGUI_data()

def newcablecond(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'NewCable'
    process_here()
    putGUI_data()

def newcablevolts(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'NewCableV'
    process_here()
    putGUI_data()

def LockCable(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'CableLock'
    process_here()
    putGUI_data()

def newcablematerial(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'NewCableMaterial'
    process_here()
    putGUI_data()

def newcablesize(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'NewCablesize'
    process_here()
    putGUI_data()

def newAWG(*args):
    fetchGUI_data()
    siteGUI.GUI_process_option = 'NewCableAWG'
    process_here()
    putGUI_data()



##############################################################
#  GUI layout
##############################################################    
root = tkinter.Tk()
root.title("Structured interface for LH hydro calculator maths from www use")

mainframe = ttk.Frame(root, padding="12 3 12 12")
mainframe.grid(column=0, row=0)    # , padx=66 , sticky=(N, W, E, S)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Setup two frames. Right hand one for entry space and the left hand one for user information and design comments
frame_1 = ttk.Frame( mainframe, width=1000, height=200)
frame_1.grid(row=0, column=1, sticky='nesw')        # put frame1 in row 0 to make it resize
frame_1.grid_propagate(0)                           # needed for width and height
frame_1.columnconfigure(0, weight=1)                # need for button to stick 'w'


frame_2 = ttk.Frame(mainframe, width=300, height=500)   # put frame2 in row 1 to make it resize bg='white', 
frame_2.grid(row=0, column=0, sticky='nesw')
# needed for width and height
frame_2.grid_propagate(0)
# need for button to stick 'e'
frame_2.columnconfigure(0, weight=1)




##############################################################
#  GUI variables
##############################################################    

class dialouge:       # This class contains all items displayed in the gui
    units = tkinter.StringVar()
    LHtype = tkinter.StringVar()

    avail_lps = tkinter.StringVar()
    actual_lps = tkinter.StringVar()
    pipe_mat = tkinter.StringVar()
    pipe_head = tkinter.StringVar()

    pipe_len = tkinter.StringVar()
    PipeFlume = tkinter.StringVar()             # U User selects either "Pipe" or "Flume"
    PipeFlumeT1 = tkinter.StringVar()           # R Title for pipe diameter / flume width
    PipeFlumeT2 = tkinter.StringVar()           # R Title for flume height or is blank
    pipe_dia = tkinter.StringVar()              # UR Content for pipe diameter or flume width
    pipe_height = tkinter.StringVar()            # UR Content for flume height or is blank
    water_depth = tkinter.StringVar()           # R  Water depth in fume/pipe in mm
    pipe_capacity = tkinter.StringVar()         # R  lps/gpm for hydro delivery

    Num_LH = tkinter.IntVar()                   # UR  Number of turbines. Ranges from 1 to 10
    LockNumLH = tkinter.IntVar()                # UR  A 0 or a 1. if 1 then number of LH hydros is locked
    LH_head = tkinter.StringVar()               # UR  This is the actual head at the LH turbine. It is from flume top to river exit. It is the head the LH experiences.
    LH_Draft_T = tkinter.StringVar()            # R  Draft tube inside diameter
    LH_lps_Opr = tkinter.StringVar()            # R  Generator actual water usage at this site head
    LH_watts_Opr = tkinter.StringVar()          # R  Generator output power at actual water throughput at max power point output
    LH_rpm_Opr = tkinter.StringVar()            # R  Generator rpm at rated water capacity at max power point output
    LH_rpm_cap = tkinter.StringVar()            # R  Generator rpm at actual water throughput at max power point output
    LH_rpm_NL = tkinter.StringVar()             # R  Generator rpm at actual head with max. possible water throughput and no electrical load
    LH_Draft_T = tkinter.StringVar()            # R  Draft tube diameter to be used for this head

    LHstator = tkinter.StringVar()              # R  Description string for the selected stator
    LH_V_Opr = tkinter.StringVar()              # R  Generator output voltage at actual water throughput at max power point output
    LH_V_NL = tkinter.StringVar()               # R  Generator output voltage at actual head with max. possible water throughput and no electrical load
    LH_pwr_tot = tkinter.StringVar()            # R


    LH_total_pwr = tkinter.StringVar()
    Load_Vmax = tkinter.StringVar()
    Load_Vmin = tkinter.StringVar()
    
    cable_len = tkinter.StringVar()
    Aload_V = tkinter.StringVar()
    design_cable_eff = tkinter.StringVar()
    cable_material = tkinter.StringVar()
    cable_size = tkinter.StringVar()
    cable_AWG = tkinter.StringVar()
    cable_A = tkinter.StringVar()
    actual_cable_eff = tkinter.StringVar()
    Load_pwr = tkinter.StringVar()
    designcheck = tkinter.StringVar()
    cable_mm_title = tkinter.StringVar() # 'Cable cross section mm^2')
    cable_AWG_title = tkinter.StringVar() # 'Next size up cable AWG')
    LockCable = tkinter.IntVar()
    design_notes = tkinter.StringVar() # Design notes becomes a big long string in here
    cable_dia_mm_sld = tkinter.StringVar()
    cable_dia_mm_str = tkinter.StringVar()
    cable_dia_in_sld = tkinter.StringVar()
    cable_dia_in_str = tkinter.StringVar()
    revision = tkinter.StringVar()


##############################################################
# All the widgets
##############################################################    



ttk.Label(frame_1, text="Metric or imperial units?").grid(column=0, row=4, sticky='E') 
dialouge.units_entry = ttk.Combobox(frame_1, textvariable=dialouge.units)
dialouge.units_entry.grid(column=1, row=4, sticky='ew' )
dialouge.units_entry['values'] = ('Metric', 'Imperial')
dialouge.units_entry.bind('<<ComboboxSelected>>', units)

ttk.Label(frame_1, textvariable=dialouge.revision).grid(column=2, row=4, columnspan=2, sticky='E' )

ttk.Label(frame_1, text="Which LH hydro").grid(column=0, row=10, sticky='E')
dialouge.PStype_entry = ttk.Combobox(frame_1, textvariable=dialouge.LHtype)
dialouge.PStype_entry.grid(column=1, row=10, sticky='EW' )
dialouge.PStype_entry['values'] = ('LH/LH Pro', 'LH mini')
dialouge.PStype_entry.bind('<<ComboboxSelected>>', BasicData)        # This command is chosen just to make calculator check numbers

ttk.Label(frame_1, text="Water supply system").grid(column=0, row=15, sticky='W')

ttk.Label(frame_1, text="Available water flow").grid(column=0, row=16, sticky='E')
dialouge.avail_lps_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.avail_lps)
dialouge.avail_lps_entry.grid(column=1, row=16, sticky='WE')
dialouge.avail_lps_entry.bind('<Return>', BasicData)

ttk.Label(frame_1, text="Used water flow").grid(column=0, row=17, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.actual_lps).grid(column=1, row=17, sticky='WE')

ttk.Label(frame_1, text="Pipe/Flume fall").grid(column=0, row=18, sticky='E')
dialouge.pipe_head_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.pipe_head, state='DISABLED')
dialouge.pipe_head_entry.grid(column=1, row=18, sticky='WE')
dialouge.pipe_head_entry.bind('<Return>', BasicData)

ttk.Label(frame_1, text="Pipe/Flume material").grid(column=2, row=18, sticky='E')
dialouge.pipe_mat_entry = ttk.Combobox(frame_1, textvariable=dialouge.pipe_mat)
dialouge.pipe_mat_entry.grid(column=2, row=19, sticky='EW' )
dialouge.pipe_mat_entry['values'] = ('Drawn plastic tube','General steel','Asphalted iron','Galv. steel','Cast steel','Wood','Concrete','RivetedSteel')
dialouge.pipe_mat_entry.bind('<<ComboboxSelected>>', BasicData)        # This command is chosen just to make calculator check numbers



ttk.Label(frame_1, text="Pipe/Flume length").grid(column=0, row=19, sticky='E' )
dialouge.pipe_len_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.pipe_len, state='DISABLED')
dialouge.pipe_len_entry.grid(column=1, row=19, sticky='WE')
dialouge.pipe_len_entry.bind('<Return>', newpipelen)

ttk.Label(frame_1, text="Using a Flume or Pipe?").grid(column=0, row=25, sticky='E')
dialouge.PipeFlume_entry = ttk.Combobox(frame_1, textvariable=dialouge.PipeFlume)
dialouge.PipeFlume_entry.grid(column=1, row=25, sticky='E' )
dialouge.PipeFlume_entry['values'] = ('Flume', 'Pipe', 'PS_pipe')
dialouge.PipeFlume_entry.bind('<<ComboboxSelected>>', PipeFlume_sel)

ttk.Label(frame_1, textvariable=dialouge.PipeFlumeT1).grid(column=0, row=26, sticky='E')
dialouge.pipe_dia_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.pipe_dia, state='DISABLED')
dialouge.pipe_dia_entry.grid(column=1, row=26, sticky='WE')
dialouge.pipe_dia_entry.bind('<Return>', newpendia)

ttk.Label(frame_1, textvariable=dialouge.PipeFlumeT2).grid(column=0, row=27, sticky='E')
dialouge.pipe_height_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.pipe_height, state='DISABLED')
dialouge.pipe_height_entry.grid(column=1, row=27, sticky='WE')
dialouge.pipe_height_entry.bind('<Return>', newpendia)

ttk.Label(frame_1, text="Water depth in pipe/flume").grid(column=2, row=26, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.water_depth).grid(column=2, row=27, sticky='WE')

ttk.Label(frame_1, text="Pipe/Flume capacity").grid(column=0, row=28, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.pipe_capacity).grid(column=1, row=28, sticky='WE')

ttk.Label(frame_1, text="LH Hydro parameters").grid(column=0, row=35, sticky='W')

ttk.Label(frame_1, text="Head of water at LH hydro").grid(column=0, row=36, sticky='E')
dialouge.LH_head_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.LH_head)
dialouge.LH_head_entry.grid(column=1, row=36, sticky='WE')
dialouge.LH_head_entry.bind('<Return>', BasicData)

ttk.Label(frame_1, text="Number of LH hydros").grid(column=0, row=37, sticky='E')
dialouge.Num_LH_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.Num_LH, state='DISABLED')
dialouge.Num_LH_entry.grid(column=1, row=37, sticky='WE')
dialouge.Num_LH_entry.bind('<Return>', newNoPS)
dialouge.LockNumLH_entry = ttk.Checkbutton(frame_1, text="Lock \"Number of LH hydros\"", variable = dialouge.LockNumLH, command = LockNumLH ).grid(column=2, row=37, columnspan=2, sticky='EW')     # , state = DISABLED

ttk.Label(frame_1, text="Draft tube diameter").grid(column=0, row=38, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_Draft_T).grid(column=1, row=38, sticky='W')

ttk.Label(frame_1, text="SD operating speed").grid(column=0, row=40, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_rpm_Opr).grid(column=1, row=40, sticky='W')
ttk.Label(frame_1, text="SD no load speed").grid(column=0, row=41, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_rpm_NL).grid(column=1, row=41, sticky='W')

ttk.Label(frame_1, text="Output of each LH hydro").grid(column=0, row=42, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_watts_Opr).grid(column=1, row=42, sticky='W')

ttk.Label(frame_1, text="Total LH hydro output").grid(column=0, row=43, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_pwr_tot).grid(column=1, row=43, sticky='WE')

ttk.Label(frame_1, text="LH hydro output voltage").grid(column=0, row=44, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_V_Opr).grid(column=1, row=44, sticky='WE')
ttk.Label(frame_1, text="LH hydro no load output voltage").grid(column=0, row=45, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.LH_V_NL).grid(column=1, row=45, sticky='WE')

ttk.Label(frame_1, text="Electrical parameters").grid(column=0, row=51, sticky='W')

ttk.Label(frame_1, text="Target cable efficiency").grid(column=0, row=52, sticky='E')
dialouge.design_cable_eff_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.design_cable_eff, state='DISABLED')
dialouge.design_cable_eff_entry.grid(column=1, row=52, sticky='WE')
dialouge.design_cable_eff_entry.bind('<FocusIn>', newcableeff)
dialouge.design_cable_eff_entry.bind('<Return>', newcableeff)

ttk.Label(frame_1, text="Length of cable").grid(column=0, row=53, sticky='E')
dialouge.cable_len_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.cable_len, state='DISABLED')
dialouge.cable_len_entry.grid(column=1, row=53, sticky='WE')
dialouge.cable_len_entry.bind('<Return>', newcablecond)

ttk.Label(frame_1, text="Max Voltage rating of inverter/charge controller").grid(column=0, row=54, sticky='E')
dialouge.load_Vmax_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.Load_Vmax)
dialouge.load_Vmax_entry.grid(column=1, row=54, sticky='WE')
dialouge.load_Vmax_entry.bind('<Return>', BasicData)

ttk.Label(frame_1, text="Min Voltage rating of inverter/charge controller").grid(column=0, row=55, sticky='E')
dialouge.load_Vmin_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.Load_Vmin, state='DISABLED')
dialouge.load_Vmin_entry.grid(column=1, row=55, sticky='WE')
dialouge.load_Vmin_entry.bind('<Return>', BasicData)

ttk.Label(frame_1, text="Actual load voltage").grid(column=0, row=56, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.Aload_V).grid(column=1, row=56, sticky='WE')

ttk.Label(frame_1, text="Cable material").grid(column=0, row=57, sticky='E')
dialouge.cable_material_entry = ttk.Combobox(frame_1, textvariable=dialouge.cable_material, state='DISABLED')
dialouge.cable_material_entry.grid(column=1, row=57, sticky='EW' )
dialouge.cable_material_entry['values'] = ('Copper', 'Aluminium', 'Steel')
dialouge.cable_material_entry.bind('<<ComboboxSelected>>', newcablematerial)

dialouge.LockCable_entry = ttk.Checkbutton(frame_1, text="Lock cable size", variable = dialouge.LockCable, command = LockCable ).grid(column=2, row=57, columnspan=2, sticky='')     # , state = DISABLED

ttk.Label(frame_1, text="Solid wire dia." ).grid(column=2, row=65, sticky='')
ttk.Label(frame_1, text="Approx stranded dia." ).grid(column=3, row=65, sticky='')
ttk.Label(frame_1, textvariable=dialouge.cable_dia_mm_sld).grid(column=2, row=66, sticky='' )
ttk.Label(frame_1, textvariable=dialouge.cable_dia_mm_str).grid(column=3, row=66, sticky='' )
ttk.Label(frame_1, textvariable=dialouge.cable_dia_in_sld).grid(column=2, row=67, sticky='' )
ttk.Label(frame_1, textvariable=dialouge.cable_dia_in_str).grid(column=3, row=67, sticky='' )

ttk.Label(frame_1, textvariable=dialouge.cable_mm_title).grid(column=0, row=65, sticky='E')
dialouge.cable_size_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.cable_size, state='DISABLED')
dialouge.cable_size_entry.grid(column=1, row=65, sticky='WE')
dialouge.cable_size_entry.bind('<FocusIn>', newcablesize)
dialouge.cable_size_entry.bind('<Return>', newcablesize)

ttk.Label(frame_1, textvariable=dialouge.cable_AWG_title).grid(column=0, row=66, sticky='E')
dialouge.cable_AWG_entry = ttk.Entry(frame_1, width=7, textvariable=dialouge.cable_AWG, state='DISABLED')
dialouge.cable_AWG_entry.grid(column=1, row=66, sticky='WE')
dialouge.cable_AWG_entry.bind('<FocusIn>', newAWG)
dialouge.cable_AWG_entry.bind('<Return>', newAWG)

ttk.Label(frame_1, text="Cable current").grid(column=0, row=67, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.cable_A).grid(column=1, row=67, sticky='WE')

ttk.Label(frame_1, text="Actual cable efficiency").grid(column=0, row=68, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.actual_cable_eff).grid(column=1, row=68, sticky='W')

ttk.Label(frame_1, text="Power at your powershed").grid(column=0, row=69, sticky='E')
ttk.Label(frame_1, textvariable=dialouge.Load_pwr).grid(column=1, row=69, sticky='WE')

dialouge.diag = Text(frame_1, state='normal', width=250, height=14, wrap='char')
dialouge.diag.grid(column=0, row=80, sticky='E', columnspan=8)


dialouge.design_noted = Text(frame_2, state='normal', width=60, height=50, wrap='char')
dialouge.design_noted.grid(column=0, row=46, sticky='E', columnspan=8)
dialouge.design_noted.pack()



##############################################################
# Provide initial descriptions for starters. Only runs once!
##############################################################    
siteGUI.GUI_cable_mm_AWG = "mm"
siteGUI.GUI_initial_data = 1

siteGUI.GUIcr = '\r\n'                    # Carriage return with a line feed character
siteGUI.GUI_diag_cr = '\r\n'


dialouge.units.set( 'Metric' )
dialouge.LHtype.set( 'LH/LH Pro' )
dialouge.pipe_mat.set('Wood')
dialouge.cable_mm_title.set('Cable cross section mm^2')
dialouge.cable_AWG_title.set('Next size up cable AWG')
dialouge.PipeFlume.set('Flume')
dialouge.PipeFlumeT1.set('T1')
dialouge.PipeFlumeT1.set('T2')
dialouge.Num_LH.set(0)
dialouge.LockCable.set( 0 )
dialouge.cable_material.set( 'Copper' )
units()


##############################################################
# Enter the event loop
##############################################################    
root.mainloop()     # Tells Tk to enter its event loop, makes everything run
