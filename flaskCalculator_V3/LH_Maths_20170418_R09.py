#!/usr/bin/python
# -*- coding: cp1252 -*-
from math import pi, log10, log, sqrt, acos, sin
import sys      # Needed to find out what platform are using.  sys.platform = win32 or win64? or linux2 or????

# Designed and developed by Smithies Technology Ltd
# Email andrew.smithies@paradise.net.nz


# Revision History

# R09   Addition of LH mini turbine. Additional turbine data and now support for 'LH/LH Pro' and 'LH mini' turbines
#       Added in new comment for no output to reccomend user to use LH mini or PLT turbine as an option.
#       Supressed SD codes from displaying when LH mini selected

# R08   Removed cutdowns from automatic SD selector in favour of packing the rotor out to reduce magnetisim.
#           New suffix in SD code (0) for packers
#           Changed columns in list of suggested SD codes to now be Vo, Voc, and stators V/rpm for table in EcoInnovation workshop
#       Major replacement of SD lookup table. Removed unused parameters
#       Revised weighting factors for which SD codes to show first
#           Removed "Magic7"
#           Added in a weighting factor for packers. n = number of packers. use 1+(n*0.02)^2
#           Added in a weighting factor for optimal fitness. There is a max efficiency point which gives a 1
#               As power per finger approaches max weighting increases by 2 using square law
#               As power per finger reduces max weighting factor increases to 2 at 50% W/finger, then to 5 at 0% W/finger


# R07   Changed default units for fall in flume/pipe to be mm and in. Set default fall to 28mm to reduce intake water velocity
#       Added an alarm warning for excessive flume velocity ( >1ms ) as it causes turbulence at the turbine and water slosh
#       Flume/pipe water depth also reports water velocity.


# R06   Bug found in SD code generator added in version R05. Cutdowns codes where given when the loading operating point was for
#       more than the cutdown number of fingersets. Would result in designs where the cutdown was unable to load the
#       pelton wheel properly


# R05   Migrated SD calculator routine from latest update in PLT/TRG tool into this routine. SDs are now
#       determined from the electrical watts output in Michaels lookup table / 80% to give shaft power as well
#       using the rpm figures in the same table. rpm figures are sqr proportional to head and are obviously
#       theory based relationship to some field data. Should be close enough...
#       The nominal 80% eff is true within 1% for plain SDs 0.3W per rpm. { 0.148W:74%, 0.2:76, 0.254:78, 0.302:79, 0.5:80, 0.8+:80 }
#       At below 0.302 W/rpm are less than 1.4m head and manually reduced power figures are in product data.


# R04   Added in table info in electrical user notes so users understand what to enter
#       into their inverter/charge controller


# R03   Minimim load voltage reduced to 50V


# R02   Minor tweak to comments section to remove UTF coded characters that Python 2.7 could not handle. No code changes
#       Minor changes to alarm strings to suit html usage as well as Python GUI caller.
#       siteGUI.GUI_LockNumLH replaced with siteGUI.GUI_LockNumLH as used everywhere else
#       LH_W_forNumLH(LHcount) routine now ok for 0 LHcount
#       Issue in Manning formula for flow calc with ^(2/3) should be ^(2.0/3.0) to use float maths as needed
#       In CalcCable() cable loss is calculated for existing cable size at begining of routine to
#           remove reliance on data coming back fromm caller 


# R01   First of LH calculator. This is a design fork from Pelton Powerspout maths version R10.
#       Major rewrite of nearly all of it apart from some of cable loss calculations and Moody water flow calcs kept for reference.


# These varibles are to keep track of instalation parameters.
class siteGUI:                              #   (U)ser input or (R)eport or both?        Description
    GUI_initial_data = int(1)               # R   Once turns a 0 then unlock rest of inputs
    GUI_process_option = str('basicdata')   # U   Contents is one of.... 'basicdata' 'pipe' 'pipeeff' 'pendiaLk' 'pendia' 'SetLkNumLHandJ' 'SetNumLHandJ' 'SetCableEff'  'NewCable' 'NewCableV' 'NewCableMaterial' 'NewCablesize' 'NewCableAWG'  'NewCablesize' 'CableLock' 
    GUI_revision = str('R01')               # R   Version number for this maths routine for GUI to display
    GUI_meas_sys = str('Metric')            # U   Units system to use  'Metric' or Imperial'
    GUI_LHtype = str('LH/LH Pro')           # U   'LH1500 and Pro', 'LH1500 Pro +', 'LH1500 and Pro with SD PCB', 'LH1500 Pro + with SD PCB'
    GUI_avail_lps = str('')                 # U   either lps or gpm float.  eg '12 lps'  or '23 gpm'
    GUI_actual_lps = str('')                # R   either lps or gpm float.  eg '12 lps'  or '23 gpm'

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

    # GUI_LH_lps_Opr = str('')              # R   Generator actual water usage at this site head
    GUI_LH_V_Opr = str('')                  # R   Generator output voltage at actual water throughput at max power point output
    GUI_LH_watts_Opr = str('')              # R   Generator output power at actual water throughput at max power point output
    GUI_LH_rpm_Opr = str('')                # R   Generator rpm at rated water capacity at max power point output
    # GUI_LH_rpm_cap = str('')              # R   Generator rpm at actual water throughput at max power point output
    GUI_LH_rpm_NL = str('')                 # R   Generator rpm at actual head with max. possible water throughput and no electrical load
    GUI_LH_Draft_T = str('')                # R   Draft tube diameter to be used for this head

    # GUI_LHstator = str()                  # R   Description string for the selected stator
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
    GUI_design_notes_SD = str( '' )         # R   An empty string for design comments for the end user to read and understand

    GUI_revision = str('R09')               # R   Version number for this maths routine for GUI to display
    GUI_diag = str('')                      # R   All diagnostics go to here
    GUIcr = '<br>'                          # R   Carriage return with a line feed character
    GUI_diag_cr = str('\r\n')               # R   or '<br>'   # Carriage return with a line feed character



class site:    
    SD_types = ('100--S','100--D','80--S','80--D','60--S','60--D','60dc--S','60dc--D')
    SD_types += ('100-HP-S','100-HP-D','80-HP-S','80-HP-D','60-HP-S','60-HP-D','60dc-HP-S','60dc-HP-D',)
    SD_types += ('60R85-HP-S','60R85-HP-D','60R90-HP-S','60R90-HP-D','60R100-HP-S','60R100-HP-D','60R110-HP-S','60R110-HP-D','60R120-HP-S','60R120-HP-D',)

    SD_finger_sets           = { '100--S': 1.400000E+01,'100--D': 1.400000E+01,'80--S': 1.400000E+01,'80--D': 1.400000E+01,'60--S': 1.400000E+01,'60--D': 1.400000E+01,'60dc--S': 1.200000E+01,'60dc--D': 1.200000E+01 } # How many fingers on stator for each phase
    SD_mV4rpm4set            = { '100--S': 1.900000E+01,'100--D': 1.085714E+01,'80--S': 4.992857E+01,'80--D': 2.842857E+01,'60--S': 7.271429E+01,'60--D': 4.142857E+01,'60dc--S': 8.347987E+01,'60dc--D': 4.755371E+01 } # Open circuit volts per rpm per finger
    Stator_mV4rpm4set        = { '100--S': 1.900000E+01,'100--D': 1.085714E+01,'80--S': 4.992857E+01,'80--D': 2.842857E+01,'60--S': 7.271429E+01,'60--D': 4.142857E+01,'60dc--S': 9.333333E+01,'60dc--D': 5.316667E+01 } # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA     = { '100--S': 0.000000E+00,'100--D': 0.000000E+00,'80--S': 0.000000E+00,'80--D': 0.000000E+00,'60--S': 0.000000E+00,'60--D': 0.000000E+00,'60dc--S': 0.000000E+00,'60dc--D': 0.000000E+00 } # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB     = { '100--S': 0.000000E+00,'100--D': 0.000000E+00,'80--S': 0.000000E+00,'80--D': 0.000000E+00,'60--S': 0.000000E+00,'60--D': 0.000000E+00,'60dc--S': 0.000000E+00,'60dc--D': 0.000000E+00 } # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC     = { '100--S': 5.357143E+01,'100--D': 5.357143E+01,'80--S': 5.357143E+01,'80--D': 5.357143E+01,'60--S': 5.357143E+01,'60--D': 5.357143E+01,'60dc--S': 6.250000E+01,'60dc--D': 6.250000E+01 } # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking              = { '100--S': 1.500000E+00,'100--D': 3.000000E+00,'80--S': 1.100000E+00,'80--D': 2.200000E+00,'60--S': 1.000000E+00,'60--D': 2.000000E+00,'60dc--S': 1.200000E+00,'60dc--D': 2.400000E+00 } # Rating of build effort and value of generator value to EcoInnovation

    SD_finger_sets.update         ( { '100-HP-S': 1.400000E+01,'100-HP-D': 1.400000E+01,'80-HP-S': 1.400000E+01,'80-HP-D': 1.400000E+01,'60-HP-S': 1.400000E+01,'60-HP-D': 1.400000E+01,'60dc-HP-S': 1.200000E+01,'60dc-HP-D': 1.200000E+01 } ) # How many fingers on stator for each phase
    SD_mV4rpm4set.update          ( { '100-HP-S': 2.124265E+01,'100-HP-D': 1.213865E+01,'80-HP-S': 5.582184E+01,'80-HP-D': 3.178411E+01,'60-HP-S': 8.129704E+01,'60-HP-D': 4.631855E+01,'60dc-HP-S': 9.333333E+01,'60dc-HP-D': 5.316667E+01 } ) # Open circuit volts per rpm per finger
    Stator_mV4rpm4set.update      ( { '100-HP-S': 1.900000E+01,'100-HP-D': 1.085714E+01,'80-HP-S': 4.992857E+01,'80-HP-D': 2.842857E+01,'60-HP-S': 7.271429E+01,'60-HP-D': 4.142857E+01,'60dc-HP-S': 9.333333E+01,'60dc-HP-D': 5.316667E+01 } ) # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA.update   ( { '100-HP-S': 0.000000E+00,'100-HP-D': 0.000000E+00,'80-HP-S': 0.000000E+00,'80-HP-D': 0.000000E+00,'60-HP-S': 0.000000E+00,'60-HP-D': 0.000000E+00,'60dc-HP-S': 0.000000E+00,'60dc-HP-D': 0.000000E+00 } ) # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB.update   ( { '100-HP-S': 0.000000E+00,'100-HP-D': 0.000000E+00,'80-HP-S': 0.000000E+00,'80-HP-D': 0.000000E+00,'60-HP-S': 0.000000E+00,'60-HP-D': 0.000000E+00,'60dc-HP-S': 0.000000E+00,'60dc-HP-D': 0.000000E+00 } ) # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC.update   ( { '100-HP-S': 7.142857E+01,'100-HP-D': 7.142857E+01,'80-HP-S': 7.142857E+01,'80-HP-D': 7.142857E+01,'60-HP-S': 7.142857E+01,'60-HP-D': 7.142857E+01,'60dc-HP-S': 8.333333E+01,'60dc-HP-D': 8.333333E+01 } ) # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking.update            ( { '100-HP-S': 3.000000E+00,'100-HP-D': 3.500000E+00,'80-HP-S': 3.000000E+00,'80-HP-D': 3.500000E+00,'60-HP-S': 3.000000E+00,'60-HP-D': 3.500000E+00,'60dc-HP-S': 1.600000E+00,'60dc-HP-D': 3.200000E+00 } ) # Rating of build effort and value of generator value to EcoInnovation

    SD_finger_sets.update         ( { '60R85-HP-S': 1.200000E+01,'60R85-HP-D': 1.200000E+01,'60R90-HP-S': 1.200000E+01,'60R90-HP-D': 1.200000E+01,'60R100-HP-S': 1.200000E+01,'60R100-HP-D': 1.200000E+01,'60R110-HP-S': 1.200000E+01,'60R110-HP-D': 1.200000E+01,'60R120-HP-S': 1.200000E+01,'60R120-HP-D': 1.200000E+01 } ) # How many fingers on stator for each phase
    SD_mV4rpm4set.update          ( { '60R85-HP-S': 4.033333E+01,'60R85-HP-D': 2.300000E+01,'60R90-HP-S': 4.316667E+01,'60R90-HP-D': 2.458333E+01,'60R100-HP-S': 4.791667E+01,'60R100-HP-D': 2.733333E+01,'60R110-HP-S': 5.275000E+01,'60R110-HP-D': 3.008333E+01,'60R120-HP-S': 5.750000E+01,'60R120-HP-D': 3.275000E+01 } ) # Open circuit volts per rpm per finger
    Stator_mV4rpm4set.update      ( { '60R85-HP-S': 4.033333E+01,'60R85-HP-D': 2.300000E+01,'60R90-HP-S': 4.316667E+01,'60R90-HP-D': 2.458333E+01,'60R100-HP-S': 4.791667E+01,'60R100-HP-D': 2.733333E+01,'60R110-HP-S': 5.275000E+01,'60R110-HP-D': 3.008333E+01,'60R120-HP-S': 5.750000E+01,'60R120-HP-D': 3.275000E+01 } ) # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA.update   ( { '60R85-HP-S': 0.000000E+00,'60R85-HP-D': 0.000000E+00,'60R90-HP-S': 0.000000E+00,'60R90-HP-D': 0.000000E+00,'60R100-HP-S': 0.000000E+00,'60R100-HP-D': 0.000000E+00,'60R110-HP-S': 0.000000E+00,'60R110-HP-D': 0.000000E+00,'60R120-HP-S': 0.000000E+00,'60R120-HP-D': 0.000000E+00 } ) # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB.update   ( { '60R85-HP-S': 0.000000E+00,'60R85-HP-D': 0.000000E+00,'60R90-HP-S': 0.000000E+00,'60R90-HP-D': 0.000000E+00,'60R100-HP-S': 0.000000E+00,'60R100-HP-D': 0.000000E+00,'60R110-HP-S': 0.000000E+00,'60R110-HP-D': 0.000000E+00,'60R120-HP-S': 0.000000E+00,'60R120-HP-D': 0.000000E+00 } ) # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC.update   ( { '60R85-HP-S': 8.333333E+01,'60R85-HP-D': 8.333333E+01,'60R90-HP-S': 8.333333E+01,'60R90-HP-D': 8.333333E+01,'60R100-HP-S': 8.333333E+01,'60R100-HP-D': 8.333333E+01,'60R110-HP-S': 8.333333E+01,'60R110-HP-D': 8.333333E+01,'60R120-HP-S': 8.333333E+01,'60R120-HP-D': 8.333333E+01 } ) # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking.update            ( { '60R85-HP-S': 5.000000E+00,'60R85-HP-D': 5.833333E+00,'60R90-HP-S': 5.050000E+00,'60R90-HP-D': 5.891667E+00,'60R100-HP-S': 5.100500E+00,'60R100-HP-D': 5.950583E+00,'60R110-HP-S': 5.151505E+00,'60R110-HP-D': 6.010089E+00,'60R120-HP-S': 5.203020E+00,'60R120-HP-D': 6.070190E+00 } ) # Rating of build effort and value of generator value to EcoInnovation



    magic7 = { '60R85-12S1P-S':0.5, '60R110-12S1P-D':0.5, '60R100-12S1P-D':0.5, '60R85-12S1P-D':0.5, '60R85-6S2P-S':0.5, '60R110-4S3P-S':0.5, '60R110-6S2P-D':1, \
               '60R100-3S4P-S':0.6, '60R90-3S4P-S':0.6, '60R100-4S3P-D':0.6, '60R100-2S6P-S':0.6, '60R90-3S4P-D':0.6, '60R90-2S6P-S':0.6 }


    Sscore = { '14-1':4, '14-2':3, '14-3':5, '14-4':5, '14-5':5, '14-6':5, '14-7':2, \
               '14-8':5, '14-9':5, '14-10':5, '14-11':5,  '14-12':5,  '14-13':5,  '14-14':1, \
               '12-1':5, '12-2':3.5, '12-3':3, '12-4':2.5,  '12-5':5,  '12-6':2,  '12-7':5, \
               '12-8':5, '12-9':5, '12-10':5, '12-11':5,  '12-12':1 }
               
    Pscore = { '14-1':1, '14-2':2, '14-3':5, '14-4':5, '14-5':5, '14-6':5, '14-7':3, \
               '14-8':5, '14-9':5, '14-10':5, '14-11':5,  '14-12':5,  '14-13':5,  '14-14':4, \
               '12-1':1, '12-2':2, '12-3':2.5, '12-4':3,  '12-5':5,  '12-6':3.5,  '12-7':5, \
               '12-8':5, '12-9':5, '12-10':5, '12-11':5,  '12-12':5 }

    SDsearch = str('')
    SDdiffConEff = 0.85     # Basic efficiency although not used now
    SDmargin = 1.02         # The amount of SD rating oversize required to keep the LH hydro from speed surging. MPPT must always be in control of rpm  1.18 typ
    
    # This is a complex curve to relate Vo/Vl ratio called Vr to normalized output per fingerset per rpm.
    # Input power to the SD follows this curve at all given rpms
    # The table above has the mW per finger set per rpm for each SD type   
    # The table above has the Vr above 1 scalar also as MPP is not always at Vr of 2
   
    pwr4Vr = { -5:-.0001, \
               0:0, \
               1:0.00001, \
        1.004341:0.013055,  \
        1.233832:0.416688,  \
        1.325629:0.567330,  \
        1.371527:0.639718,  \
        1.417425:0.705019,  \
        1.463324:0.762368,  \
        1.509222:0.812648,  \
        1.555120:0.855258,  \
        1.601018:0.891995,  \
        1.646917:0.922566,  \
        1.692815:0.946355,  \
        1.738713:0.964218,  \
        1.784611:0.977666,  \
        1.830510:0.987121,  \
        1.876408:0.993923,  \
        1.922306:0.998037,  \
        2.000000:1.000000 }

    SDcloseness = 15    # Percentage range for SD choice to match requirement.  was 15







    #diag = open('diag.txt','w')
    #diag2 = open('diag2.txt','w')
    LHtype = str('')

    avail_lps = float(0)                # litres per second
    usable_water = float(0)             # litres per second
    actual_lps = float(0)               # litres per second
    
    lps = float(0)                      # litres per second
    pipe_head = float(0.028)            # metres
    pipe_len = float(1)                 # metres
    pipe_dia = float(2)                 # metres
    pipe_height = float(0.4)            # metres
    water_depth = float()

    pipe_flow_roughness = 0.00015       # in cm. for Moody water calcs
    pipe_capacity = float()

    pipe_iterations = 0                 # Counts number of times pipe calc done to solve pipe diameter

    LH_head = float(2)                  # OPerating head for the turbine itself

    LH_lps_cap = float()                # Generator rated water capacity at this site head
    LH_lps_Opr = float()                # Generator actual water usage at this site head

    LH_watts_cap = float()              # Generator output power at rated water capacity at max power point output
    LH_watts_Opr = float()              # Generator output power at actual water throughput at max power point output

    LH_V_cap = float()                  # Generator output voltage at rated water capacity at max power point output
    LH_V_Opr = float()                  # Generator output voltage at actual water throughput at max power point output
    LH_V_Opr_guide = float()            # Copy of generator output voltage at actual water throughput at max power point output for alarm reporting
    LH_V_NL = float()                   # Generator output voltage at actual head with max. possible water throughput and no electrical load

    LH_rpm_Opr = float()                # Generator rpm at rated water capacity at max power point output
    LH_rpm_cap = float()                # Generator rpm at actual water throughput at max power point output
    LH_rpm_NL = float()                 # Generator rpm at actual head with max. possible water throughput and no electrical load

    LH_Draft_T = float()                # Draft tube diameter to be used for this head
    percent_LHutilize = float()         # Percentage of units capacity in use as a lps ratio

    SDchoice = str()                    # A pointer to which SD is used in lookup table
    LHstator = str()                    # Description string for the selected stator
    vmax_req = float()                  # Vmax of inverter required to find a stator to suit
    LH_Vmax_guide = float()             # Next step up Vmax for inverter for user to try when voltag problems
    eps = 1.25e-5                       # Used in pipe loss calc
    Num_LH = 1                          # Number of turbines
    maxWnumLH = 0                       # Number of turbines for max watts
    indexbase = str()                   # base to make up index to LH hydro lookup table

    SDs2show = int(20)                  # How many SD codes to list to user
    
    # This table maps out the efficiency degradation at low power levels.
    # Fraction of maximum of lps in to fraction of V, I, R.rpm output
    # Software uses straight line interpolation between points and level above top point
    eff = {0:0, 0.4:0.05, 0.5:0.4, 0.6:0.95, 1:1, 10:10 }

    cable_len = float(20)
    cable_voltage = float(48)
    cable_A = float()
    cable_eff_target = 0.90             # Proportion of electricity to be delivered to the power shed
    cable_material = 'Copper'
    cableR = 1
    cableR_req = 1
    Load_Vmax = 0                       # Max volts the inverter/charge controller can handle
    Load_Vmin = 0                       # Min volts the inverter/charge controller can use
    cable_Vdrop = float()
    viscosity = 1.32E-03                #   kg/m-sec
    density = 999.4                     #   kg/m^3
    gravity = 9.81	                #   m/sec^2
    mmm_lps = 1000.00                   #   lps/m^3/sec

    LH_pwr_tot = float(0)
    Load_pwr = float(0)
    cable_size = float(1)
    cable_gauge = float(1)
    cable_AWGn = int(0)
    cableLock = int(0)
    itteratorCount = float(0)
 
    alarms = []     # Empty list for alarms to be .append(  )ed to as alarm numbers. Valid entries are ints.
                    # Final running of prog may give a list like   [ 2, 5, 10 ]

    # Dictionary of conversion coeffecients. Enter all units here as lower case. All indexing is done via .lower() string function
    convert = { 'ft-m':3.28083989501312,  'in-m':39.3700787401575,  'gpm-lps':15.8704967465482,  'awg- awg':1,  \
                'm-ft':0.3048,  'm-in':0.0254,  'm-cm':0.01,  'm-m':1,  'm-mm':0.001,  'm-mile':1609.344,  'm-kpa':0.102,  'm-LHi':0.703,  'm-bar':10.197,  'm-atm':10.33211,  \
                'mm-ft':304.8,  'mm-in':25.4,  'mm-cm':10,  'mm-m':1000,  'mm-mm':1,  'mm-mile':1609344,  'mm-kpa':102,  'mm-LHi':703,  'mm-bar':10197,  'mm-atm':10332.11,  \
                'lps-lps':1,  'lps-lpm':60,  'lps-lph':3600,  'lps-gpm':0.06301,  'lps-cfs':28.316846592,  'lps-cfm':0.4719474432,  'lps-cfh':0.00786579072,  'lps-cfd':0.00032774128,  'lps-cumecs':1000,\
                'mps-mps':1,  'fps-mps':3.28084 }
    
    material = { 'Copper': 1.78e-8, 'Aluminium': 3.21e-8, 'Steel': 11.78e-8 }
                            # Reference ohms per metre for a block of metel for cable amp carring ability calcs at 20deg C with typical wire grade material
                            # Steel is from http://www.kencove.com/fence/100_Fence+Construction_resource.php  (Electric fence info)
    LHeff = float(0)
    MaxLH = 20


    Aspace = ' '
    monospace_on = ''
    monospace_off = ''
    debug = ''

    LH_type = { 'LH/LH Pro':1, 'LH mini':2 }

    LHdata = {}     # This is the performance data lookup tables for all low head turbines. See Michael L spreadsheet for filling this in!
    LHdata.update( {'1_1.0m_l/s':25, '1_1.0m_Watts':91, '1_1.0m_Efficiency':38, '1_1.0m_RPM':688, '1_1.0m_R.RPM':1032, '1_1.0m_W.RPM':0, '1_1.0m_DT':0.19, '1_1.0m_DT W':9, '1_1.0m_A.Stator':'100-7s-2p- star', '1_1.0m_A.OC V':137, '1_1.0m_A.R V':69, '1_1.0m_B.Stator':'80-7s-2p-delta', '1_1.0m_B.OC V':205, '1_1.0m_B.R V':103, '1_1.0m_C.Stator':'80-7s-2p-star', '1_1.0m_C.OC V':361, '1_1.0m_C.R V':181, '1_1.0m_D.Stator':'80-14s-1p-delta', '1_1.0m_D.OC V':411, '1_1.0m_D.R V':205,  } )
    LHdata.update( {'1_1.1m_l/s':26, '1_1.1m_Watts':107, '1_1.1m_Efficiency':38, '1_1.1m_RPM':722, '1_1.1m_R.RPM':1083, '1_1.1m_W.RPM':0, '1_1.1m_DT':0.19, '1_1.1m_DT W':11, '1_1.1m_A.Stator':'100-7s-2p- star', '1_1.1m_A.OC V':144, '1_1.1m_A.R V':72, '1_1.1m_B.Stator':'80-7s-2p-delta', '1_1.1m_B.OC V':215, '1_1.1m_B.R V':108, '1_1.1m_C.Stator':'80-7s-2p-star', '1_1.1m_C.OC V':379, '1_1.1m_C.R V':189, '1_1.1m_D.Stator':'80-14s-1p-delta', '1_1.1m_D.OC V':431, '1_1.1m_D.R V':215,  } )
    LHdata.update( {'1_1.2m_l/s':27, '1_1.2m_Watts':123, '1_1.2m_Efficiency':39, '1_1.2m_RPM':754, '1_1.2m_R.RPM':1131, '1_1.2m_W.RPM':0, '1_1.2m_DT':0.19, '1_1.2m_DT W':12, '1_1.2m_A.Stator':'100-7s-2p- star', '1_1.2m_A.OC V':150, '1_1.2m_A.R V':75, '1_1.2m_B.Stator':'80-7s-2p-delta', '1_1.2m_B.OC V':225, '1_1.2m_B.R V':113, '1_1.2m_C.Stator':'80-7s-2p-star', '1_1.2m_C.OC V':396, '1_1.2m_C.R V':198, '1_1.2m_D.Stator':'80-14s-1p-delta', '1_1.2m_D.OC V':450, '1_1.2m_D.R V':225,  } )
    LHdata.update( {'1_1.3m_l/s':28, '1_1.3m_Watts':176, '1_1.3m_Efficiency':49, '1_1.3m_RPM':785, '1_1.3m_R.RPM':1177, '1_1.3m_W.RPM':0, '1_1.3m_DT':0.19, '1_1.3m_DT W':14, '1_1.3m_A.Stator':'80-2s-7p-star', '1_1.3m_A.OC V':118, '1_1.3m_A.R V':59, '1_1.3m_B.Stator':'80-7s-2p-delta', '1_1.3m_B.OC V':234, '1_1.3m_B.R V':117, '1_1.3m_C.Stator':'100-14s-1p-star', '1_1.3m_C.OC V':313, '1_1.3m_C.R V':157, '1_1.3m_D.Stator':'80-14s-1p-delta', '1_1.3m_D.OC V':468, '1_1.3m_D.R V':234,  } )
    LHdata.update( {'1_1.4m_l/s':29, '1_1.4m_Watts':199, '1_1.4m_Efficiency':50, '1_1.4m_RPM':814, '1_1.4m_R.RPM':1221, '1_1.4m_W.RPM':0, '1_1.4m_DT':0.19, '1_1.4m_DT W':16, '1_1.4m_A.Stator':'80-2s-7p-star', '1_1.4m_A.OC V':122, '1_1.4m_A.R V':61, '1_1.4m_B.Stator':'80-7s-2p-delta', '1_1.4m_B.OC V':243, '1_1.4m_B.R V':122, '1_1.4m_C.Stator':'100-14s-1p-star', '1_1.4m_C.OC V':325, '1_1.4m_C.R V':162, '1_1.4m_D.Stator':'80-14s-1p-delta', '1_1.4m_D.OC V':486, '1_1.4m_D.R V':243,  } )
    LHdata.update( {'1_1.5m_l/s':30, '1_1.5m_Watts':223, '1_1.5m_Efficiency':50, '1_1.5m_RPM':843, '1_1.5m_R.RPM':1264, '1_1.5m_W.RPM':0, '1_1.5m_DT':0.19, '1_1.5m_DT W':17, '1_1.5m_A.Stator':'80-2s-7p-star', '1_1.5m_A.OC V':126, '1_1.5m_A.R V':63, '1_1.5m_B.Stator':'100-14s-1p-delta', '1_1.5m_B.OC V':192, '1_1.5m_B.R V':96, '1_1.5m_C.Stator':'100-14s-1p-star', '1_1.5m_C.OC V':336, '1_1.5m_C.R V':168, '1_1.5m_D.Stator':'80-7s-2p-star', '1_1.5m_D.OC V':442, '1_1.5m_D.R V':221,  } )
    LHdata.update( {'1_1.6m_l/s':31, '1_1.6m_Watts':248, '1_1.6m_Efficiency':50, '1_1.6m_RPM':870, '1_1.6m_R.RPM':1306, '1_1.6m_W.RPM':0, '1_1.6m_DT':0.19, '1_1.6m_DT W':19, '1_1.6m_A.Stator':'80-2s-7p-star', '1_1.6m_A.OC V':130, '1_1.6m_A.R V':65, '1_1.6m_B.Stator':'100-14s-1p-delta', '1_1.6m_B.OC V':198, '1_1.6m_B.R V':99, '1_1.6m_C.Stator':'100-14s-1p-star', '1_1.6m_C.OC V':347, '1_1.6m_C.R V':174, '1_1.6m_D.Stator':'80-7s-2p-star', '1_1.6m_D.OC V':457, '1_1.6m_D.R V':228,  } )
    LHdata.update( {'1_1.7m_l/s':32, '1_1.7m_Watts':272, '1_1.7m_Efficiency':51, '1_1.7m_RPM':897, '1_1.7m_R.RPM':1346, '1_1.7m_W.RPM':0, '1_1.7m_DT':0.19, '1_1.7m_DT W':21, '1_1.7m_A.Stator':'80-2s-7p-star', '1_1.7m_A.OC V':134, '1_1.7m_A.R V':67, '1_1.7m_B.Stator':'100-14s-1p-delta', '1_1.7m_B.OC V':205, '1_1.7m_B.R V':102, '1_1.7m_C.Stator':'100-14s-1p-star', '1_1.7m_C.OC V':358, '1_1.7m_C.R V':179, '1_1.7m_D.Stator':'80-7s-2p-star', '1_1.7m_D.OC V':471, '1_1.7m_D.R V':236,  } )
    LHdata.update( {'1_1.8m_l/s':33, '1_1.8m_Watts':297, '1_1.8m_Efficiency':51, '1_1.8m_RPM':923, '1_1.8m_R.RPM':1385, '1_1.8m_W.RPM':0, '1_1.8m_DT':0.19, '1_1.8m_DT W':23, '1_1.8m_A.Stator':'80-2s-7p-star', '1_1.8m_A.OC V':138, '1_1.8m_A.R V':69, '1_1.8m_B.Stator':'100-14s-1p-delta', '1_1.8m_B.OC V':211, '1_1.8m_B.R V':105, '1_1.8m_C.Stator':'100-14s-1p-star', '1_1.8m_C.OC V':368, '1_1.8m_C.R V':184, '1_1.8m_D.Stator':'80-7s-2p-star', '1_1.8m_D.OC V':485, '1_1.8m_D.R V':242,  } )
    LHdata.update( {'1_1.9m_l/s':34, '1_1.9m_Watts':323, '1_1.9m_Efficiency':51, '1_1.9m_RPM':949, '1_1.9m_R.RPM':1423, '1_1.9m_W.RPM':0, '1_1.9m_DT':0.19, '1_1.9m_DT W':25, '1_1.9m_A.Stator':'80-2s-7p-star', '1_1.9m_A.OC V':142, '1_1.9m_A.R V':71, '1_1.9m_B.Stator':'100-14s-1p-delta', '1_1.9m_B.OC V':216, '1_1.9m_B.R V':108, '1_1.9m_C.Stator':'100-14s-1p-star', '1_1.9m_C.OC V':378, '1_1.9m_C.R V':189, '1_1.9m_D.Stator':'60-7s-2p-delta', '1_1.9m_D.OC V':413, '1_1.9m_D.R V':206,  } )
    LHdata.update( {'1_2.0m_l/s':35, '1_2.0m_Watts':349, '1_2.0m_Efficiency':51, '1_2.0m_RPM':973, '1_2.0m_R.RPM':1460, '1_2.0m_W.RPM':0, '1_2.0m_DT':0.19, '1_2.0m_DT W':27, '1_2.0m_A.Stator':'80-2s-7p-star', '1_2.0m_A.OC V':146, '1_2.0m_A.R V':73, '1_2.0m_B.Stator':'100-14s-1p-delta', '1_2.0m_B.OC V':222, '1_2.0m_B.R V':111, '1_2.0m_C.Stator':'100-14s-1p-star', '1_2.0m_C.OC V':388, '1_2.0m_C.R V':194, '1_2.0m_D.Stator':'60-7s-2p-delta', '1_2.0m_D.OC V':423, '1_2.0m_D.R V':212,  } )
    LHdata.update( {'1_2.1m_l/s':36, '1_2.1m_Watts':376, '1_2.1m_Efficiency':51, '1_2.1m_RPM':997, '1_2.1m_R.RPM':1496, '1_2.1m_W.RPM':0, '1_2.1m_DT':0.19, '1_2.1m_DT W':29, '1_2.1m_A.Stator':'80-2s-7p-star', '1_2.1m_A.OC V':149, '1_2.1m_A.R V':75, '1_2.1m_B.Stator':'100-14s-1p-delta', '1_2.1m_B.OC V':227, '1_2.1m_B.R V':114, '1_2.1m_C.Stator':'100-14s-1p-star', '1_2.1m_C.OC V':398, '1_2.1m_C.R V':199, '1_2.1m_D.Stator':'60-7s-2p-delta', '1_2.1m_D.OC V':434, '1_2.1m_D.R V':217,  } )
    LHdata.update( {'1_2.2m_l/s':37, '1_2.2m_Watts':404, '1_2.2m_Efficiency':51, '1_2.2m_RPM':1021, '1_2.2m_R.RPM':1531, '1_2.2m_W.RPM':0, '1_2.2m_DT':0.19, '1_2.2m_DT W':31, '1_2.2m_A.Stator':'80-2s-7p-star', '1_2.2m_A.OC V':153, '1_2.2m_A.R V':76, '1_2.2m_B.Stator':'100-14s-1p-delta', '1_2.2m_B.OC V':233, '1_2.2m_B.R V':116, '1_2.2m_C.Stator':'80-7s-2p-delta', '1_2.2m_C.OC V':305, '1_2.2m_C.R V':152, '1_2.2m_D.Stator':'60-7s-2p-delta', '1_2.2m_D.OC V':444, '1_2.2m_D.R V':222,  } )
    LHdata.update( {'1_2.3m_l/s':38, '1_2.3m_Watts':433, '1_2.3m_Efficiency':51, '1_2.3m_RPM':1044, '1_2.3m_R.RPM':1565, '1_2.3m_W.RPM':0, '1_2.3m_DT':0.19, '1_2.3m_DT W':33, '1_2.3m_A.Stator':'100-7s-2p-delta', '1_2.3m_A.OC V':119, '1_2.3m_A.R V':59, '1_2.3m_B.Stator':'100-14s-1p-delta', '1_2.3m_B.OC V':238, '1_2.3m_B.R V':119, '1_2.3m_C.Stator':'80-7s-2p-delta', '1_2.3m_C.OC V':312, '1_2.3m_C.R V':156, '1_2.3m_D.Stator':'60-7s-2p-delta', '1_2.3m_D.OC V':454, '1_2.3m_D.R V':227,  } )
    LHdata.update( {'1_2.4m_l/s':38, '1_2.4m_Watts':463, '1_2.4m_Efficiency':51, '1_2.4m_RPM':1066, '1_2.4m_R.RPM':1599, '1_2.4m_W.RPM':0, '1_2.4m_DT':0.19, '1_2.4m_DT W':35, '1_2.4m_A.Stator':'100-7s-2p-delta', '1_2.4m_A.OC V':122, '1_2.4m_A.R V':61, '1_2.4m_B.Stator':'100-14s-1p-delta', '1_2.4m_B.OC V':243, '1_2.4m_B.R V':122, '1_2.4m_C.Stator':'80-7s-2p-delta', '1_2.4m_C.OC V':318, '1_2.4m_C.R V':159, '1_2.4m_D.Stator':'60-7s-2p-delta', '1_2.4m_D.OC V':464, '1_2.4m_D.R V':232,  } )
    LHdata.update( {'1_2.5m_l/s':39, '1_2.5m_Watts':493, '1_2.5m_Efficiency':51, '1_2.5m_RPM':1088, '1_2.5m_R.RPM':1632, '1_2.5m_W.RPM':0, '1_2.5m_DT':0.19, '1_2.5m_DT W':37, '1_2.5m_A.Stator':'100-7s-2p-delta', '1_2.5m_A.OC V':124, '1_2.5m_A.R V':62, '1_2.5m_B.Stator':'100-7s-2p-star', '1_2.5m_B.OC V':217, '1_2.5m_B.R V':109, '1_2.5m_C.Stator':'80-7s-2p-delta', '1_2.5m_C.OC V':325, '1_2.5m_C.R V':162, '1_2.5m_D.Stator':'60-7s-2p-delta', '1_2.5m_D.OC V':473, '1_2.5m_D.R V':237,  } )
    LHdata.update( {'1_2.6m_l/s':40, '1_2.6m_Watts':524, '1_2.6m_Efficiency':51, '1_2.6m_RPM':1110, '1_2.6m_R.RPM':1664, '1_2.6m_W.RPM':0, '1_2.6m_DT':0.19, '1_2.6m_DT W':40, '1_2.6m_A.Stator':'100-7s-2p-delta', '1_2.6m_A.OC V':126, '1_2.6m_A.R V':63, '1_2.6m_B.Stator':'100-7s-2p-star', '1_2.6m_B.OC V':221, '1_2.6m_B.R V':111, '1_2.6m_C.Stator':'80-7s-2p-delta', '1_2.6m_C.OC V':331, '1_2.6m_C.R V':166, '1_2.6m_D.Stator':'60-7s-2p-delta', '1_2.6m_D.OC V':483, '1_2.6m_D.R V':241,  } )
    LHdata.update( {'1_2.7m_l/s':41, '1_2.7m_Watts':555, '1_2.7m_Efficiency':52, '1_2.7m_RPM':1131, '1_2.7m_R.RPM':1696, '1_2.7m_W.RPM':0, '1_2.7m_DT':0.24, '1_2.7m_DT W':16, '1_2.7m_A.Stator':'100-7s-2p-delta', '1_2.7m_A.OC V':129, '1_2.7m_A.R V':64, '1_2.7m_B.Stator':'100-7s-2p-star', '1_2.7m_B.OC V':226, '1_2.7m_B.R V':113, '1_2.7m_C.Stator':'80-7s-2p-delta', '1_2.7m_C.OC V':338, '1_2.7m_C.R V':169, '1_2.7m_D.Stator':'60-7s-2p-delta', '1_2.7m_D.OC V':492, '1_2.7m_D.R V':246,  } )
    LHdata.update( {'1_2.8m_l/s':41, '1_2.8m_Watts':587, '1_2.8m_Efficiency':52, '1_2.8m_RPM':1151, '1_2.8m_R.RPM':1727, '1_2.8m_W.RPM':1, '1_2.8m_DT':0.24, '1_2.8m_DT W':17, '1_2.8m_A.Stator':'100-7s-2p-delta', '1_2.8m_A.OC V':131, '1_2.8m_A.R V':66, '1_2.8m_B.Stator':'100-7s-2p-star', '1_2.8m_B.OC V':230, '1_2.8m_B.R V':115, '1_2.8m_C.Stator':'80-7s-2p-delta', '1_2.8m_C.OC V':344, '1_2.8m_C.R V':172, '1_2.8m_D.Stator':'80-7s-2p-delta', '1_2.8m_D.OC V':344, '1_2.8m_D.R V':172,  } )
    LHdata.update( {'1_2.9m_l/s':42, '1_2.9m_Watts':620, '1_2.9m_Efficiency':52, '1_2.9m_RPM':1172, '1_2.9m_R.RPM':1758, '1_2.9m_W.RPM':1, '1_2.9m_DT':0.24, '1_2.9m_DT W':18, '1_2.9m_A.Stator':'100-7s-2p-delta', '1_2.9m_A.OC V':134, '1_2.9m_A.R V':67, '1_2.9m_B.Stator':'100-7s-2p-star', '1_2.9m_B.OC V':234, '1_2.9m_B.R V':117, '1_2.9m_C.Stator':'80-7s-2p-delta', '1_2.9m_C.OC V':350, '1_2.9m_C.R V':175, '1_2.9m_D.Stator':'80-7s-2p-delta', '1_2.9m_D.OC V':350, '1_2.9m_D.R V':175,  } )
    LHdata.update( {'1_3.0m_l/s':43, '1_3.0m_Watts':654, '1_3.0m_Efficiency':52, '1_3.0m_RPM':1192, '1_3.0m_R.RPM':1788, '1_3.0m_W.RPM':1, '1_3.0m_DT':0.24, '1_3.0m_DT W':19, '1_3.0m_A.Stator':'100-7s-2p-delta', '1_3.0m_A.OC V':136, '1_3.0m_A.R V':68, '1_3.0m_B.Stator':'100-7s-2p-star', '1_3.0m_B.OC V':238, '1_3.0m_B.R V':119, '1_3.0m_C.Stator':'80-7s-2p-delta', '1_3.0m_C.OC V':356, '1_3.0m_C.R V':178, '1_3.0m_D.Stator':'80-7s-2p-delta', '1_3.0m_D.OC V':356, '1_3.0m_D.R V':178,  } )
    LHdata.update( {'1_3.1m_l/s':44, '1_3.1m_Watts':688, '1_3.1m_Efficiency':52, '1_3.1m_RPM':1212, '1_3.1m_R.RPM':1817, '1_3.1m_W.RPM':1, '1_3.1m_DT':0.24, '1_3.1m_DT W':20, '1_3.1m_A.Stator':'100-7s-2p-delta', '1_3.1m_A.OC V':138, '1_3.1m_A.R V':69, '1_3.1m_B.Stator':'100-7s-2p-star', '1_3.1m_B.OC V':242, '1_3.1m_B.R V':121, '1_3.1m_C.Stator':'80-7s-2p-delta', '1_3.1m_C.OC V':362, '1_3.1m_C.R V':181, '1_3.1m_D.Stator':'80-7s-2p-delta', '1_3.1m_D.OC V':362, '1_3.1m_D.R V':181,  } )
    LHdata.update( {'1_3.2m_l/s':44, '1_3.2m_Watts':723, '1_3.2m_Efficiency':52, '1_3.2m_RPM':1231, '1_3.2m_R.RPM':1846, '1_3.2m_W.RPM':1, '1_3.2m_DT':0.24, '1_3.2m_DT W':21, '1_3.2m_A.Stator':'100-7s-2p-delta', '1_3.2m_A.OC V':140, '1_3.2m_A.R V':70, '1_3.2m_B.Stator':'100-7s-2p-star', '1_3.2m_B.OC V':246, '1_3.2m_B.R V':123, '1_3.2m_C.Stator':'80-7s-2p-delta', '1_3.2m_C.OC V':367, '1_3.2m_C.R V':184, '1_3.2m_D.Stator':'80-7s-2p-delta', '1_3.2m_D.OC V':367, '1_3.2m_D.R V':184,  } )
    LHdata.update( {'1_3.3m_l/s':45, '1_3.3m_Watts':759, '1_3.3m_Efficiency':52, '1_3.3m_RPM':1250, '1_3.3m_R.RPM':1875, '1_3.3m_W.RPM':1, '1_3.3m_DT':0.24, '1_3.3m_DT W':22, '1_3.3m_A.Stator':'100-7s-2p-delta', '1_3.3m_A.OC V':143, '1_3.3m_A.R V':71, '1_3.3m_B.Stator':'80-2s-7p-star', '1_3.3m_B.OC V':187, '1_3.3m_B.R V':94, '1_3.3m_C.Stator':'80-7s-2p-delta', '1_3.3m_C.OC V':373, '1_3.3m_C.R V':187, '1_3.3m_D.Stator':'80-7s-2p-delta', '1_3.3m_D.OC V':373, '1_3.3m_D.R V':187,  } )
    LHdata.update( {'1_3.4m_l/s':46, '1_3.4m_Watts':795, '1_3.4m_Efficiency':52, '1_3.4m_RPM':1269, '1_3.4m_R.RPM':1903, '1_3.4m_W.RPM':1, '1_3.4m_DT':0.24, '1_3.4m_DT W':23, '1_3.4m_A.Stator':'100-7s-2p-delta', '1_3.4m_A.OC V':145, '1_3.4m_A.R V':72, '1_3.4m_B.Stator':'80-2s-7p-star', '1_3.4m_B.OC V':190, '1_3.4m_B.R V':95, '1_3.4m_C.Stator':'80-7s-2p-delta', '1_3.4m_C.OC V':379, '1_3.4m_C.R V':189, '1_3.4m_D.Stator':'80-7s-2p-delta', '1_3.4m_D.OC V':379, '1_3.4m_D.R V':189,  } )
    LHdata.update( {'1_3.5m_l/s':46, '1_3.5m_Watts':832, '1_3.5m_Efficiency':52, '1_3.5m_RPM':1287, '1_3.5m_R.RPM':1931, '1_3.5m_W.RPM':1, '1_3.5m_DT':0.24, '1_3.5m_DT W':24, '1_3.5m_A.Stator':'100-7s-2p-delta', '1_3.5m_A.OC V':147, '1_3.5m_A.R V':73, '1_3.5m_B.Stator':'80-2s-7p-star', '1_3.5m_B.OC V':193, '1_3.5m_B.R V':96, '1_3.5m_C.Stator':'80-7s-2p-delta', '1_3.5m_C.OC V':384, '1_3.5m_C.R V':192, '1_3.5m_D.Stator':'80-7s-2p-delta', '1_3.5m_D.OC V':384, '1_3.5m_D.R V':192,  } )
    LHdata.update( {'1_3.6m_l/s':47, '1_3.6m_Watts':870, '1_3.6m_Efficiency':52, '1_3.6m_RPM':1306, '1_3.6m_R.RPM':1959, '1_3.6m_W.RPM':1, '1_3.6m_DT':0.24, '1_3.6m_DT W':25, '1_3.6m_A.Stator':'100-7s-2p-delta', '1_3.6m_A.OC V':149, '1_3.6m_A.R V':74, '1_3.6m_B.Stator':'80-2s-7p-star', '1_3.6m_B.OC V':196, '1_3.6m_B.R V':98, '1_3.6m_C.Stator':'80-7s-2p-delta', '1_3.6m_C.OC V':390, '1_3.6m_C.R V':195, '1_3.6m_D.Stator':'80-7s-2p-delta', '1_3.6m_D.OC V':390, '1_3.6m_D.R V':195,  } )
    LHdata.update( {'1_3.7m_l/s':48, '1_3.7m_Watts':908, '1_3.7m_Efficiency':53, '1_3.7m_RPM':1324, '1_3.7m_R.RPM':1986, '1_3.7m_W.RPM':1, '1_3.7m_DT':0.24, '1_3.7m_DT W':26, '1_3.7m_A.Stator':' Not possible. Use 250 vdc regulator', '1_3.7m_A.OC V':0, '1_3.7m_A.R V':0, '1_3.7m_B.Stator':'60dcHP-1s-12p-star', '1_3.7m_B.OC V':185, '1_3.7m_B.R V':92, '1_3.7m_C.Stator':'60dc-2s-6p-S-HP', '1_3.7m_C.OC V':371, '1_3.7m_C.R V':186, '1_3.7m_D.Stator':'60dcHP-2s-6p-star', '1_3.7m_D.OC V':371, '1_3.7m_D.R V':186,  } )
    LHdata.update( {'1_3.8m_l/s':48, '1_3.8m_Watts':947, '1_3.8m_Efficiency':53, '1_3.8m_RPM':1341, '1_3.8m_R.RPM':2012, '1_3.8m_W.RPM':1, '1_3.8m_DT':0.24, '1_3.8m_DT W':28, '1_3.8m_A.Stator':' Not possible. Use 250 vdc regulator', '1_3.8m_A.OC V':0, '1_3.8m_A.R V':0, '1_3.8m_B.Stator':'60dcHP-1s-12p-star', '1_3.8m_B.OC V':187, '1_3.8m_B.R V':94, '1_3.8m_C.Stator':'60dc-2s-6p-S-HP', '1_3.8m_C.OC V':376, '1_3.8m_C.R V':188, '1_3.8m_D.Stator':'60dcHP-2s-6p-star', '1_3.8m_D.OC V':376, '1_3.8m_D.R V':188,  } )
    LHdata.update( {'1_3.9m_l/s':49, '1_3.9m_Watts':986, '1_3.9m_Efficiency':53, '1_3.9m_RPM':1359, '1_3.9m_R.RPM':2038, '1_3.9m_W.RPM':1, '1_3.9m_DT':0.24, '1_3.9m_DT W':29, '1_3.9m_A.Stator':' Not possible. Use 250 vdc regulator', '1_3.9m_A.OC V':0, '1_3.9m_A.R V':0, '1_3.9m_B.Stator':'60dcHP-1s-12p-star', '1_3.9m_B.OC V':190, '1_3.9m_B.R V':95, '1_3.9m_C.Stator':'60dcHP-2s-6p-star', '1_3.9m_C.OC V':381, '1_3.9m_C.R V':191, '1_3.9m_D.Stator':'60dcHP-2s-6p-star', '1_3.9m_D.OC V':381, '1_3.9m_D.R V':191,  } )
    LHdata.update( {'1_4.0m_l/s':50, '1_4.0m_Watts':1026, '1_4.0m_Efficiency':53, '1_4.0m_RPM':1376, '1_4.0m_R.RPM':2064, '1_4.0m_W.RPM':1, '1_4.0m_DT':0.24, '1_4.0m_DT W':30, '1_4.0m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.0m_A.OC V':0, '1_4.0m_A.R V':0, '1_4.0m_B.Stator':'60dcHP-1s-12p-star', '1_4.0m_B.OC V':192, '1_4.0m_B.R V':96, '1_4.0m_C.Stator':'60dcHP-2s-6p-star', '1_4.0m_C.OC V':386, '1_4.0m_C.R V':193, '1_4.0m_D.Stator':'60dcHP-2s-6p-star', '1_4.0m_D.OC V':386, '1_4.0m_D.R V':193,  } )
    LHdata.update( {'1_4.1m_l/s':50, '1_4.1m_Watts':1067, '1_4.1m_Efficiency':53, '1_4.1m_RPM':1393, '1_4.1m_R.RPM':2090, '1_4.1m_W.RPM':1, '1_4.1m_DT':0.24, '1_4.1m_DT W':31, '1_4.1m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.1m_A.OC V':0, '1_4.1m_A.R V':0, '1_4.1m_B.Stator':'60dcHP-1s-12p-star', '1_4.1m_B.OC V':194, '1_4.1m_B.R V':97, '1_4.1m_C.Stator':'60dcHP-2s-6p-star', '1_4.1m_C.OC V':391, '1_4.1m_C.R V':195, '1_4.1m_D.Stator':'60dcHP-2s-6p-star', '1_4.1m_D.OC V':391, '1_4.1m_D.R V':195,  } )
    LHdata.update( {'1_4.2m_l/s':51, '1_4.2m_Watts':1109, '1_4.2m_Efficiency':53, '1_4.2m_RPM':1410, '1_4.2m_R.RPM':2115, '1_4.2m_W.RPM':1, '1_4.2m_DT':0.24, '1_4.2m_DT W':32, '1_4.2m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.2m_A.OC V':0, '1_4.2m_A.R V':0, '1_4.2m_B.Stator':'60dcHP-1s-12p-star', '1_4.2m_B.OC V':197, '1_4.2m_B.R V':98, '1_4.2m_C.Stator':'60dcHP-2s-6p-star', '1_4.2m_C.OC V':396, '1_4.2m_C.R V':198, '1_4.2m_D.Stator':'60dcHP-2s-6p-star', '1_4.2m_D.OC V':396, '1_4.2m_D.R V':198,  } )
    LHdata.update( {'1_4.3m_l/s':51, '1_4.3m_Watts':1151, '1_4.3m_Efficiency':53, '1_4.3m_RPM':1427, '1_4.3m_R.RPM':2140, '1_4.3m_W.RPM':1, '1_4.3m_DT':0.24, '1_4.3m_DT W':33, '1_4.3m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.3m_A.OC V':0, '1_4.3m_A.R V':0, '1_4.3m_B.Stator':'60dcHP-1s-12p-star', '1_4.3m_B.OC V':199, '1_4.3m_B.R V':100, '1_4.3m_C.Stator':'60dcHP-3s-4p-delta', '1_4.3m_C.OC V':342, '1_4.3m_C.R V':171, '1_4.3m_D.Stator':'60dcHP-2s-6p-star', '1_4.3m_D.OC V':400, '1_4.3m_D.R V':200,  } )
    LHdata.update( {'1_4.4m_l/s':52, '1_4.4m_Watts':1193, '1_4.4m_Efficiency':53, '1_4.4m_RPM':1443, '1_4.4m_R.RPM':2165, '1_4.4m_W.RPM':1, '1_4.4m_DT':0.24, '1_4.4m_DT W':34, '1_4.4m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.4m_A.OC V':0, '1_4.4m_A.R V':0, '1_4.4m_B.Stator':'60dcHP-1s-12p-star', '1_4.4m_B.OC V':201, '1_4.4m_B.R V':101, '1_4.4m_C.Stator':'60dcHP-3s-4p-delta', '1_4.4m_C.OC V':346, '1_4.4m_C.R V':173, '1_4.4m_D.Stator':'60dcHP-2s-6p-star', '1_4.4m_D.OC V':405, '1_4.4m_D.R V':202,  } )
    LHdata.update( {'1_4.5m_l/s':53, '1_4.5m_Watts':1236, '1_4.5m_Efficiency':53, '1_4.5m_RPM':1460, '1_4.5m_R.RPM':2190, '1_4.5m_W.RPM':1, '1_4.5m_DT':0.24, '1_4.5m_DT W':35, '1_4.5m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.5m_A.OC V':0, '1_4.5m_A.R V':0, '1_4.5m_B.Stator':'60dcHP-1s-12p-star', '1_4.5m_B.OC V':204, '1_4.5m_B.R V':102, '1_4.5m_C.Stator':'60dcHP-3s-4p-delta', '1_4.5m_C.OC V':350, '1_4.5m_C.R V':175, '1_4.5m_D.Stator':'60dcHP-2s-6p-star', '1_4.5m_D.OC V':409, '1_4.5m_D.R V':205,  } )
    LHdata.update( {'1_4.6m_l/s':53, '1_4.6m_Watts':1280, '1_4.6m_Efficiency':53, '1_4.6m_RPM':1476, '1_4.6m_R.RPM':2214, '1_4.6m_W.RPM':1, '1_4.6m_DT':0.24, '1_4.6m_DT W':37, '1_4.6m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.6m_A.OC V':0, '1_4.6m_A.R V':0, '1_4.6m_B.Stator':'60dcHP-1s-12p-star', '1_4.6m_B.OC V':206, '1_4.6m_B.R V':103, '1_4.6m_C.Stator':'60dcHP-3s-4p-delta', '1_4.6m_C.OC V':354, '1_4.6m_C.R V':177, '1_4.6m_D.Stator':'60dcHP-2s-6p-star', '1_4.6m_D.OC V':414, '1_4.6m_D.R V':207,  } )
    LHdata.update( {'1_4.7m_l/s':54, '1_4.7m_Watts':1325, '1_4.7m_Efficiency':54, '1_4.7m_RPM':1492, '1_4.7m_R.RPM':2238, '1_4.7m_W.RPM':1, '1_4.7m_DT':0.24, '1_4.7m_DT W':38, '1_4.7m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.7m_A.OC V':0, '1_4.7m_A.R V':0, '1_4.7m_B.Stator':'60dcHP-1s-12p-star', '1_4.7m_B.OC V':208, '1_4.7m_B.R V':104, '1_4.7m_C.Stator':'60dcHP-3s-4p-delta', '1_4.7m_C.OC V':358, '1_4.7m_C.R V':179, '1_4.7m_D.Stator':'60dcHP-2s-6p-star', '1_4.7m_D.OC V':418, '1_4.7m_D.R V':209,  } )
    LHdata.update( {'1_4.8m_l/s':54, '1_4.8m_Watts':1370, '1_4.8m_Efficiency':54, '1_4.8m_RPM':1508, '1_4.8m_R.RPM':2261, '1_4.8m_W.RPM':1, '1_4.8m_DT':0.24, '1_4.8m_DT W':39, '1_4.8m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.8m_A.OC V':0, '1_4.8m_A.R V':0, '1_4.8m_B.Stator':'60dcHP-1s-12p-star', '1_4.8m_B.OC V':210, '1_4.8m_B.R V':105, '1_4.8m_C.Stator':'60dcHP-3s-4p-delta', '1_4.8m_C.OC V':362, '1_4.8m_C.R V':181, '1_4.8m_D.Stator':'60dcHP-2s-6p-star', '1_4.8m_D.OC V':423, '1_4.8m_D.R V':211,  } )
    LHdata.update( {'1_4.9m_l/s':55, '1_4.9m_Watts':1415, '1_4.9m_Efficiency':54, '1_4.9m_RPM':1523, '1_4.9m_R.RPM':2285, '1_4.9m_W.RPM':1, '1_4.9m_DT':0.24, '1_4.9m_DT W':40, '1_4.9m_A.Stator':' Not possible. Use 250 vdc regulator', '1_4.9m_A.OC V':0, '1_4.9m_A.R V':0, '1_4.9m_B.Stator':'60dcHP-1s-12p-star', '1_4.9m_B.OC V':212, '1_4.9m_B.R V':106, '1_4.9m_C.Stator':'60dcHP-3s-4p-delta', '1_4.9m_C.OC V':366, '1_4.9m_C.R V':183, '1_4.9m_D.Stator':'60dcHP-2s-6p-star', '1_4.9m_D.OC V':427, '1_4.9m_D.R V':214,  } )
    LHdata.update( {'1_5.0m_l/s':55, '1_5.0m_Watts':1462, '1_5.0m_Efficiency':54, '1_5.0m_RPM':1539, '1_5.0m_R.RPM':2308, '1_5.0m_W.RPM':1, '1_5.0m_DT':0.24, '1_5.0m_DT W':42, '1_5.0m_A.Stator':' Not possible. Use 250 vdc regulator', '1_5.0m_A.OC V':0, '1_5.0m_A.R V':0, '1_5.0m_B.Stator':'60dcHP-1s-12p-star', '1_5.0m_B.OC V':215, '1_5.0m_B.R V':107, '1_5.0m_C.Stator':'60dcHP-3s-4p-delta', '1_5.0m_C.OC V':369, '1_5.0m_C.R V':185, '1_5.0m_D.Stator':'60dcHP-2s-6p-star', '1_5.0m_D.OC V':432, '1_5.0m_D.R V':216,  } )


    LHdata.update( {'2_1.0m_l/s':14, '2_1.0m_Watts':68, '2_1.0m_Efficiency':49, '2_1.0m_RPM':1202, '2_1.0m_R.RPM':2260, '2_1.0m_W.RPM':0, '2_1.0m_DT':0.15, '2_1.0m_DT W':5, '2_1.0m_A.Stator':'LHM70-2s-3p-D', '2_1.0m_A.OC V':54, '2_1.0m_A.R V':27, '2_1.0m_B.Stator':'LHM70-3s-2p-D', '2_1.0m_B.OC V':81, '2_1.0m_B.R V':41, '2_1.0m_C.Stator':'LHM70-2s-3p-S', '2_1.0m_C.OC V':99, '2_1.0m_C.R V':50, '2_1.0m_D.Stator':'LHM70-3s-2p-S', '2_1.0m_D.OC V':151, '2_1.0m_D.R V':76, '2_1.0m_E.Stator':'LHM70-6s-1p-D', '2_1.0m_E.OC V':160, '2_1.0m_E.R V':80, '2_1.0m_F.Stator':'LHM70-6s-1p-S', '2_1.0m_F.OC V':301, '2_1.0m_F.R V':150,  } )																															
    LHdata.update( {'2_1.1m_l/s':15, '2_1.1m_Watts':79, '2_1.1m_Efficiency':49, '2_1.1m_RPM':1261, '2_1.1m_R.RPM':2370, '2_1.1m_W.RPM':0, '2_1.1m_DT':0.15, '2_1.1m_DT W':5, '2_1.1m_A.Stator':'LHM70-2s-3p-D', '2_1.1m_A.OC V':57, '2_1.1m_A.R V':28, '2_1.1m_B.Stator':'LHM70-3s-2p-D', '2_1.1m_B.OC V':85, '2_1.1m_B.R V':43, '2_1.1m_C.Stator':'LHM70-2s-3p-S', '2_1.1m_C.OC V':104, '2_1.1m_C.R V':52, '2_1.1m_D.Stator':'LHM70-3s-2p-S', '2_1.1m_D.OC V':159, '2_1.1m_D.R V':79, '2_1.1m_E.Stator':'LHM70-6s-1p-D', '2_1.1m_E.OC V':168, '2_1.1m_E.R V':84, '2_1.1m_F.Stator':'LHM70-6s-1p-S', '2_1.1m_F.OC V':315, '2_1.1m_F.R V':158,  } )																															
    LHdata.update( {'2_1.2m_l/s':15, '2_1.2m_Watts':90, '2_1.2m_Efficiency':49, '2_1.2m_RPM':1317, '2_1.2m_R.RPM':2476, '2_1.2m_W.RPM':0, '2_1.2m_DT':0.15, '2_1.2m_DT W':6, '2_1.2m_A.Stator':'LHM70-2s-3p-D', '2_1.2m_A.OC V':59, '2_1.2m_A.R V':30, '2_1.2m_B.Stator':'LHM70-3s-2p-D', '2_1.2m_B.OC V':89, '2_1.2m_B.R V':45, '2_1.2m_C.Stator':'LHM70-2s-3p-S', '2_1.2m_C.OC V':109, '2_1.2m_C.R V':54, '2_1.2m_D.Stator':'LHM70-3s-2p-S', '2_1.2m_D.OC V':166, '2_1.2m_D.R V':83, '2_1.2m_E.Stator':'LHM70-6s-1p-D', '2_1.2m_E.OC V':176, '2_1.2m_E.R V':88, '2_1.2m_F.Stator':'LHM70-6s-1p-S', '2_1.2m_F.OC V':329, '2_1.2m_F.R V':165,  } )																															
    LHdata.update( {'2_1.3m_l/s':16, '2_1.3m_Watts':101, '2_1.3m_Efficiency':49, '2_1.3m_RPM':1371, '2_1.3m_R.RPM':2577, '2_1.3m_W.RPM':0, '2_1.3m_DT':0.15, '2_1.3m_DT W':7, '2_1.3m_A.Stator':'LHM70-2s-3p-D', '2_1.3m_A.OC V':62, '2_1.3m_A.R V':31, '2_1.3m_B.Stator':'LHM70-3s-2p-D', '2_1.3m_B.OC V':93, '2_1.3m_B.R V':46, '2_1.3m_C.Stator':'LHM70-2s-3p-S', '2_1.3m_C.OC V':113, '2_1.3m_C.R V':57, '2_1.3m_D.Stator':'LHM70-3s-2p-S', '2_1.3m_D.OC V':173, '2_1.3m_D.R V':86, '2_1.3m_E.Stator':'LHM70-6s-1p-D', '2_1.3m_E.OC V':183, '2_1.3m_E.R V':91, '2_1.3m_F.Stator':'LHM70-6s-1p-S', '2_1.3m_F.OC V':343, '2_1.3m_F.R V':171,  } )																															
    LHdata.update( {'2_1.4m_l/s':17, '2_1.4m_Watts':114, '2_1.4m_Efficiency':49, '2_1.4m_RPM':1422, '2_1.4m_R.RPM':2674, '2_1.4m_W.RPM':0, '2_1.4m_DT':0.15, '2_1.4m_DT W':8, '2_1.4m_A.Stator':'LHM70-2s-3p-D', '2_1.4m_A.OC V':64, '2_1.4m_A.R V':32, '2_1.4m_B.Stator':'LHM70-3s-2p-D', '2_1.4m_B.OC V':96, '2_1.4m_B.R V':48, '2_1.4m_C.Stator':'LHM70-2s-3p-S', '2_1.4m_C.OC V':118, '2_1.4m_C.R V':59, '2_1.4m_D.Stator':'LHM70-3s-2p-S', '2_1.4m_D.OC V':179, '2_1.4m_D.R V':90, '2_1.4m_E.Stator':'LHM70-6s-1p-D', '2_1.4m_E.OC V':190, '2_1.4m_E.R V':95, '2_1.4m_F.Stator':'LHM70-6s-1p-S', '2_1.4m_F.OC V':356, '2_1.4m_F.R V':178,  } )																															
    LHdata.update( {'2_1.5m_l/s':17, '2_1.5m_Watts':126, '2_1.5m_Efficiency':50, '2_1.5m_RPM':1472, '2_1.5m_R.RPM':2768, '2_1.5m_W.RPM':0, '2_1.5m_DT':0.15, '2_1.5m_DT W':8, '2_1.5m_A.Stator':'LHM70-2s-3p-D', '2_1.5m_A.OC V':66, '2_1.5m_A.R V':33, '2_1.5m_B.Stator':'LHM70-3s-2p-D', '2_1.5m_B.OC V':100, '2_1.5m_B.R V':50, '2_1.5m_C.Stator':'LHM70-2s-3p-S', '2_1.5m_C.OC V':122, '2_1.5m_C.R V':61, '2_1.5m_D.Stator':'LHM70-3s-2p-S', '2_1.5m_D.OC V':185, '2_1.5m_D.R V':93, '2_1.5m_E.Stator':'LHM70-6s-1p-D', '2_1.5m_E.OC V':197, '2_1.5m_E.R V':98, '2_1.5m_F.Stator':'LHM70-6s-1p-S', '2_1.5m_F.OC V':368, '2_1.5m_F.R V':184,  } )																															
    LHdata.update( {'2_1.6m_l/s':18, '2_1.6m_Watts':139, '2_1.6m_Efficiency':50, '2_1.6m_RPM':1521, '2_1.6m_R.RPM':2859, '2_1.6m_W.RPM':0, '2_1.6m_DT':0.15, '2_1.6m_DT W':9, '2_1.6m_A.Stator':'LHM70-2s-3p-D', '2_1.6m_A.OC V':69, '2_1.6m_A.R V':34, '2_1.6m_B.Stator':'LHM70-3s-2p-D', '2_1.6m_B.OC V':103, '2_1.6m_B.R V':51, '2_1.6m_C.Stator':'LHM70-2s-3p-S', '2_1.6m_C.OC V':126, '2_1.6m_C.R V':63, '2_1.6m_D.Stator':'LHM70-3s-2p-S', '2_1.6m_D.OC V':192, '2_1.6m_D.R V':96, '2_1.6m_E.Stator':'LHM70-6s-1p-D', '2_1.6m_E.OC V':203, '2_1.6m_E.R V':101, '2_1.6m_F.Stator':'LHM70-6s-1p-S', '2_1.6m_F.OC V':380, '2_1.6m_F.R V':190,  } )																															
    LHdata.update( {'2_1.7m_l/s':18, '2_1.7m_Watts':153, '2_1.7m_Efficiency':50, '2_1.7m_RPM':1567, '2_1.7m_R.RPM':2947, '2_1.7m_W.RPM':0, '2_1.7m_DT':0.15, '2_1.7m_DT W':10, '2_1.7m_A.Stator':'LHM70-2s-3p-D', '2_1.7m_A.OC V':71, '2_1.7m_A.R V':35, '2_1.7m_B.Stator':'LHM70-3s-2p-D', '2_1.7m_B.OC V':106, '2_1.7m_B.R V':53, '2_1.7m_C.Stator':'LHM70-2s-3p-S', '2_1.7m_C.OC V':130, '2_1.7m_C.R V':65, '2_1.7m_D.Stator':'LHM70-3s-2p-S', '2_1.7m_D.OC V':197, '2_1.7m_D.R V':99, '2_1.7m_E.Stator':'LHM70-6s-1p-D', '2_1.7m_E.OC V':209, '2_1.7m_E.R V':105, '2_1.7m_F.Stator':'LHM70-6s-1p-S', '2_1.7m_F.OC V':392, '2_1.7m_F.R V':196,  } )																															
    LHdata.update( {'2_1.8m_l/s':19, '2_1.8m_Watts':167, '2_1.8m_Efficiency':50, '2_1.8m_RPM':1613, '2_1.8m_R.RPM':3032, '2_1.8m_W.RPM':0, '2_1.8m_DT':0.15, '2_1.8m_DT W':11, '2_1.8m_A.Stator':'LHM70-2s-3p-D', '2_1.8m_A.OC V':73, '2_1.8m_A.R V':36, '2_1.8m_B.Stator':'LHM70-3s-2p-D', '2_1.8m_B.OC V':109, '2_1.8m_B.R V':55, '2_1.8m_C.Stator':'LHM70-2s-3p-S', '2_1.8m_C.OC V':133, '2_1.8m_C.R V':67, '2_1.8m_D.Stator':'LHM70-3s-2p-S', '2_1.8m_D.OC V':203, '2_1.8m_D.R V':102, '2_1.8m_E.Stator':'LHM70-6s-1p-D', '2_1.8m_E.OC V':215, '2_1.8m_E.R V':108, '2_1.8m_F.Stator':'LHM70-6s-1p-S', '2_1.8m_F.OC V':403, '2_1.8m_F.R V':202,  } )																															
    LHdata.update( {'2_1.9m_l/s':19, '2_1.9m_Watts':181, '2_1.9m_Efficiency':50, '2_1.9m_RPM':1657, '2_1.9m_R.RPM':3115, '2_1.9m_W.RPM':0, '2_1.9m_DT':0.15, '2_1.9m_DT W':12, '2_1.9m_A.Stator':'LHM70-2s-3p-D', '2_1.9m_A.OC V':75, '2_1.9m_A.R V':37, '2_1.9m_B.Stator':'LHM70-3s-2p-D', '2_1.9m_B.OC V':112, '2_1.9m_B.R V':56, '2_1.9m_C.Stator':'LHM70-2s-3p-S', '2_1.9m_C.OC V':137, '2_1.9m_C.R V':69, '2_1.9m_D.Stator':'LHM70-3s-2p-S', '2_1.9m_D.OC V':209, '2_1.9m_D.R V':104, '2_1.9m_E.Stator':'LHM70-6s-1p-D', '2_1.9m_E.OC V':221, '2_1.9m_E.R V':111, '2_1.9m_F.Stator':'LHM70-6s-1p-S', '2_1.9m_F.OC V':414, '2_1.9m_F.R V':207,  } )																															
    LHdata.update( {'2_2.0m_l/s':20, '2_2.0m_Watts':196, '2_2.0m_Efficiency':50, '2_2.0m_RPM':1700, '2_2.0m_R.RPM':3196, '2_2.0m_W.RPM':0, '2_2.0m_DT':0.15, '2_2.0m_DT W':13, '2_2.0m_A.Stator':'LHM70-2s-3p-D', '2_2.0m_A.OC V':77, '2_2.0m_A.R V':38, '2_2.0m_B.Stator':'LHM70-3s-2p-D', '2_2.0m_B.OC V':115, '2_2.0m_B.R V':58, '2_2.0m_C.Stator':'LHM70-2s-3p-S', '2_2.0m_C.OC V':141, '2_2.0m_C.R V':70, '2_2.0m_D.Stator':'LHM70-3s-2p-S', '2_2.0m_D.OC V':214, '2_2.0m_D.R V':107, '2_2.0m_E.Stator':'LHM70-6s-1p-D', '2_2.0m_E.OC V':227, '2_2.0m_E.R V':113, '2_2.0m_F.Stator':'LHM70-6s-1p-S', '2_2.0m_F.OC V':425, '2_2.0m_F.R V':213,  } )																															
    LHdata.update( {'2_2.1m_l/s':20, '2_2.1m_Watts':212, '2_2.1m_Efficiency':50, '2_2.1m_RPM':1742, '2_2.1m_R.RPM':3275, '2_2.1m_W.RPM':0, '2_2.1m_DT':0.15, '2_2.1m_DT W':14, '2_2.1m_A.Stator':'LHM70-2s-3p-D', '2_2.1m_A.OC V':79, '2_2.1m_A.R V':39, '2_2.1m_B.Stator':'LHM70-3s-2p-D', '2_2.1m_B.OC V':118, '2_2.1m_B.R V':59, '2_2.1m_C.Stator':'LHM70-2s-3p-S', '2_2.1m_C.OC V':144, '2_2.1m_C.R V':72, '2_2.1m_D.Stator':'LHM70-3s-2p-S', '2_2.1m_D.OC V':219, '2_2.1m_D.R V':110, '2_2.1m_E.Stator':'LHM70-6s-1p-D', '2_2.1m_E.OC V':233, '2_2.1m_E.R V':116, '2_2.1m_F.Stator':'LHM70-6s-1p-S', '2_2.1m_F.OC V':436, '2_2.1m_F.R V':218,  } )																															
    LHdata.update( {'2_2.2m_l/s':21, '2_2.2m_Watts':227, '2_2.2m_Efficiency':50, '2_2.2m_RPM':1783, '2_2.2m_R.RPM':3352, '2_2.2m_W.RPM':0, '2_2.2m_DT':0.15, '2_2.2m_DT W':15, '2_2.2m_A.Stator':'LHM70-2s-3p-D', '2_2.2m_A.OC V':80, '2_2.2m_A.R V':40, '2_2.2m_B.Stator':'LHM70-3s-2p-D', '2_2.2m_B.OC V':121, '2_2.2m_B.R V':60, '2_2.2m_C.Stator':'LHM70-2s-3p-S', '2_2.2m_C.OC V':147, '2_2.2m_C.R V':74, '2_2.2m_D.Stator':'LHM70-3s-2p-S', '2_2.2m_D.OC V':225, '2_2.2m_D.R V':112, '2_2.2m_E.Stator':'LHM70-6s-1p-D', '2_2.2m_E.OC V':238, '2_2.2m_E.R V':119, '2_2.2m_F.Stator':'LHM70-6s-1p-S', '2_2.2m_F.OC V':446, '2_2.2m_F.R V':223,  } )																															
    LHdata.update( {'2_2.3m_l/s':21, '2_2.3m_Watts':243, '2_2.3m_Efficiency':50, '2_2.3m_RPM':1823, '2_2.3m_R.RPM':3427, '2_2.3m_W.RPM':0, '2_2.3m_DT':0.15, '2_2.3m_DT W':16, '2_2.3m_A.Stator':'LHM70-2s-3p-D', '2_2.3m_A.OC V':82, '2_2.3m_A.R V':41, '2_2.3m_B.Stator':'LHM70-3s-2p-D', '2_2.3m_B.OC V':123, '2_2.3m_B.R V':62, '2_2.3m_C.Stator':'LHM70-2s-3p-S', '2_2.3m_C.OC V':151, '2_2.3m_C.R V':75, '2_2.3m_D.Stator':'LHM70-3s-2p-S', '2_2.3m_D.OC V':230, '2_2.3m_D.R V':115, '2_2.3m_E.Stator':'LHM70-6s-1p-D', '2_2.3m_E.OC V':243, '2_2.3m_E.R V':122, '2_2.3m_F.Stator':'LHM70-6s-1p-S', '2_2.3m_F.OC V':456, '2_2.3m_F.R V':228,  } )																															
    LHdata.update( {'2_2.4m_l/s':22, '2_2.4m_Watts':260, '2_2.4m_Efficiency':50, '2_2.4m_RPM':1862, '2_2.4m_R.RPM':3501, '2_2.4m_W.RPM':0, '2_2.4m_DT':0.15, '2_2.4m_DT W':17, '2_2.4m_A.Stator':'LHM70-2s-3p-D', '2_2.4m_A.OC V':84, '2_2.4m_A.R V':42, '2_2.4m_B.Stator':'LHM70-3s-2p-D', '2_2.4m_B.OC V':126, '2_2.4m_B.R V':63, '2_2.4m_C.Stator':'LHM70-2s-3p-S', '2_2.4m_C.OC V':154, '2_2.4m_C.R V':77, '2_2.4m_D.Stator':'LHM70-3s-2p-S', '2_2.4m_D.OC V':235, '2_2.4m_D.R V':117, '2_2.4m_E.Stator':'LHM70-6s-1p-D', '2_2.4m_E.OC V':249, '2_2.4m_E.R V':124, '2_2.4m_F.Stator':'LHM70-6s-1p-S', '2_2.4m_F.OC V':466, '2_2.4m_F.R V':233,  } )																															
    LHdata.update( {'2_2.5m_l/s':22, '2_2.5m_Watts':277, '2_2.5m_Efficiency':51, '2_2.5m_RPM':1901, '2_2.5m_R.RPM':3573, '2_2.5m_W.RPM':0, '2_2.5m_DT':0.15, '2_2.5m_DT W':18, '2_2.5m_A.Stator':'LHM70-2s-3p-D', '2_2.5m_A.OC V':86, '2_2.5m_A.R V':43, '2_2.5m_B.Stator':'LHM70-3s-2p-D', '2_2.5m_B.OC V':129, '2_2.5m_B.R V':64, '2_2.5m_C.Stator':'LHM70-2s-3p-S', '2_2.5m_C.OC V':157, '2_2.5m_C.R V':79, '2_2.5m_D.Stator':'LHM70-3s-2p-S', '2_2.5m_D.OC V':239, '2_2.5m_D.R V':120, '2_2.5m_E.Stator':'LHM70-6s-1p-D', '2_2.5m_E.OC V':254, '2_2.5m_E.R V':127, '2_2.5m_F.Stator':'LHM70-6s-1p-S', '2_2.5m_F.OC V':475, '2_2.5m_F.R V':238,  } )																															
    LHdata.update( {'2_2.6m_l/s':23, '2_2.6m_Watts':294, '2_2.6m_Efficiency':51, '2_2.6m_RPM':1938, '2_2.6m_R.RPM':3644, '2_2.6m_W.RPM':0, '2_2.6m_DT':0.15, '2_2.6m_DT W':19, '2_2.6m_A.Stator':'LHM70-2s-3p-D', '2_2.6m_A.OC V':87, '2_2.6m_A.R V':44, '2_2.6m_B.Stator':'LHM70-3s-2p-D', '2_2.6m_B.OC V':131, '2_2.6m_B.R V':66, '2_2.6m_C.Stator':'LHM70-2s-3p-S', '2_2.6m_C.OC V':160, '2_2.6m_C.R V':80, '2_2.6m_D.Stator':'LHM70-3s-2p-S', '2_2.6m_D.OC V':244, '2_2.6m_D.R V':122, '2_2.6m_E.Stator':'LHM70-6s-1p-D', '2_2.6m_E.OC V':259, '2_2.6m_E.R V':129, '2_2.6m_F.Stator':'LHM70-6s-1p-S', '2_2.6m_F.OC V':485, '2_2.6m_F.R V':242,  } )																															
    LHdata.update( {'2_2.7m_l/s':23, '2_2.7m_Watts':312, '2_2.7m_Efficiency':51, '2_2.7m_RPM':1975, '2_2.7m_R.RPM':3713, '2_2.7m_W.RPM':0, '2_2.7m_DT':0.15, '2_2.7m_DT W':20, '2_2.7m_A.Stator':'LHM70-2s-3p-D', '2_2.7m_A.OC V':89, '2_2.7m_A.R V':45, '2_2.7m_B.Stator':'LHM70-3s-2p-D', '2_2.7m_B.OC V':134, '2_2.7m_B.R V':67, '2_2.7m_C.Stator':'LHM70-2s-3p-S', '2_2.7m_C.OC V':163, '2_2.7m_C.R V':82, '2_2.7m_D.Stator':'LHM70-3s-2p-S', '2_2.7m_D.OC V':249, '2_2.7m_D.R V':124, '2_2.7m_E.Stator':'LHM70-6s-1p-D', '2_2.7m_E.OC V':264, '2_2.7m_E.R V':132, '2_2.7m_F.Stator':'LHM70-6s-1p-S', '2_2.7m_F.OC V':494, '2_2.7m_F.R V':247,  } )																															
    LHdata.update( {'2_2.8m_l/s':24, '2_2.8m_Watts':330, '2_2.8m_Efficiency':51, '2_2.8m_RPM':2011, '2_2.8m_R.RPM':3782, '2_2.8m_W.RPM':0, '2_2.8m_DT':0.15, '2_2.8m_DT W':21, '2_2.8m_A.Stator':'LHM70-2s-3p-D', '2_2.8m_A.OC V':91, '2_2.8m_A.R V':45, '2_2.8m_B.Stator':'LHM70-3s-2p-D', '2_2.8m_B.OC V':136, '2_2.8m_B.R V':68, '2_2.8m_C.Stator':'LHM70-2s-3p-S', '2_2.8m_C.OC V':166, '2_2.8m_C.R V':83, '2_2.8m_D.Stator':'LHM70-3s-2p-S', '2_2.8m_D.OC V':253, '2_2.8m_D.R V':127, '2_2.8m_E.Stator':'LHM70-6s-1p-D', '2_2.8m_E.OC V':268, '2_2.8m_E.R V':134, '2_2.8m_F.Stator':'LHM70-6s-1p-S', '2_2.8m_F.OC V':503, '2_2.8m_F.R V':251,  } )																															
    LHdata.update( {'2_2.9m_l/s':24, '2_2.9m_Watts':349, '2_2.9m_Efficiency':51, '2_2.9m_RPM':2047, '2_2.9m_R.RPM':3848, '2_2.9m_W.RPM':0, '2_2.9m_DT':0.15, '2_2.9m_DT W':22, '2_2.9m_A.Stator':'LHM70-2s-3p-D', '2_2.9m_A.OC V':92, '2_2.9m_A.R V':46, '2_2.9m_B.Stator':'LHM70-3s-2p-D', '2_2.9m_B.OC V':139, '2_2.9m_B.R V':69, '2_2.9m_C.Stator':'LHM70-2s-3p-S', '2_2.9m_C.OC V':169, '2_2.9m_C.R V':85, '2_2.9m_D.Stator':'LHM70-3s-2p-S', '2_2.9m_D.OC V':258, '2_2.9m_D.R V':129, '2_2.9m_E.Stator':'LHM70-6s-1p-D', '2_2.9m_E.OC V':273, '2_2.9m_E.R V':137, '2_2.9m_F.Stator':'LHM70-6s-1p-S', '2_2.9m_F.OC V':512, '2_2.9m_F.R V':256,  } )																															
    LHdata.update( {'2_3.0m_l/s':24, '2_3.0m_Watts':368, '2_3.0m_Efficiency':51, '2_3.0m_RPM':2082, '2_3.0m_R.RPM':3914, '2_3.0m_W.RPM':0, '2_3.0m_DT':0.15, '2_3.0m_DT W':24, '2_3.0m_A.Stator':'LHM70-2s-3p-D', '2_3.0m_A.OC V':94, '2_3.0m_A.R V':47, '2_3.0m_B.Stator':'LHM70-3s-2p-D', '2_3.0m_B.OC V':141, '2_3.0m_B.R V':70, '2_3.0m_C.Stator':'LHM70-2s-3p-S', '2_3.0m_C.OC V':172, '2_3.0m_C.R V':86, '2_3.0m_D.Stator':'LHM70-3s-2p-S', '2_3.0m_D.OC V':262, '2_3.0m_D.R V':131, '2_3.0m_E.Stator':'LHM70-6s-1p-D', '2_3.0m_E.OC V':278, '2_3.0m_E.R V':139, '2_3.0m_F.Stator':'LHM70-6s-1p-S', '2_3.0m_F.OC V':521, '2_3.0m_F.R V':260,  } )																															
    LHdata.update( {'2_3.1m_l/s':25, '2_3.1m_Watts':387, '2_3.1m_Efficiency':51, '2_3.1m_RPM':2116, '2_3.1m_R.RPM':3979, '2_3.1m_W.RPM':0, '2_3.1m_DT':0.15, '2_3.1m_DT W':25, '2_3.1m_A.Stator':'LHM70-2s-3p-D', '2_3.1m_A.OC V':95, '2_3.1m_A.R V':48, '2_3.1m_B.Stator':'LHM70-3s-2p-D', '2_3.1m_B.OC V':143, '2_3.1m_B.R V':72, '2_3.1m_C.Stator':'LHM70-2s-3p-S', '2_3.1m_C.OC V':175, '2_3.1m_C.R V':88, '2_3.1m_D.Stator':'LHM70-3s-2p-S', '2_3.1m_D.OC V':267, '2_3.1m_D.R V':133, '2_3.1m_E.Stator':'LHM70-6s-1p-D', '2_3.1m_E.OC V':283, '2_3.1m_E.R V':141, '2_3.1m_F.Stator':'LHM70-6s-1p-S', '2_3.1m_F.OC V':529, '2_3.1m_F.R V':265,  } )																															
    LHdata.update( {'2_3.2m_l/s':25, '2_3.2m_Watts':406, '2_3.2m_Efficiency':51, '2_3.2m_RPM':2150, '2_3.2m_R.RPM':4043, '2_3.2m_W.RPM':0, '2_3.2m_DT':0.15, '2_3.2m_DT W':26, '2_3.2m_A.Stator':'LHM70-2s-3p-D', '2_3.2m_A.OC V':97, '2_3.2m_A.R V':49, '2_3.2m_B.Stator':'LHM70-3s-2p-D', '2_3.2m_B.OC V':146, '2_3.2m_B.R V':73, '2_3.2m_C.Stator':'LHM70-2s-3p-S', '2_3.2m_C.OC V':178, '2_3.2m_C.R V':89, '2_3.2m_D.Stator':'LHM70-3s-2p-S', '2_3.2m_D.OC V':271, '2_3.2m_D.R V':135, '2_3.2m_E.Stator':'LHM70-6s-1p-D', '2_3.2m_E.OC V':287, '2_3.2m_E.R V':144, '2_3.2m_F.Stator':'LHM70-6s-1p-S', '2_3.2m_F.OC V':538, '2_3.2m_F.R V':269,  } )																															
    LHdata.update( {'2_3.3m_l/s':26, '2_3.3m_Watts':425, '2_3.3m_Efficiency':51, '2_3.3m_RPM':2184, '2_3.3m_R.RPM':4105, '2_3.3m_W.RPM':0, '2_3.3m_DT':0.15, '2_3.3m_DT W':27, '2_3.3m_A.Stator':'LHM70-2s-3p-D', '2_3.3m_A.OC V':99, '2_3.3m_A.R V':49, '2_3.3m_B.Stator':'LHM70-3s-2p-D', '2_3.3m_B.OC V':148, '2_3.3m_B.R V':74, '2_3.3m_C.Stator':'LHM70-2s-3p-S', '2_3.3m_C.OC V':181, '2_3.3m_C.R V':90, '2_3.3m_D.Stator':'LHM70-3s-2p-S', '2_3.3m_D.OC V':275, '2_3.3m_D.R V':138, '2_3.3m_E.Stator':'LHM70-6s-1p-D', '2_3.3m_E.OC V':291, '2_3.3m_E.R V':146, '2_3.3m_F.Stator':'LHM70-6s-1p-S', '2_3.3m_F.OC V':546, '2_3.3m_F.R V':273,  } )																															
    LHdata.update( {'2_3.4m_l/s':26, '2_3.4m_Watts':445, '2_3.4m_Efficiency':51, '2_3.4m_RPM':2217, '2_3.4m_R.RPM':4167, '2_3.4m_W.RPM':0, '2_3.4m_DT':0.15, '2_3.4m_DT W':28, '2_3.4m_A.Stator':'LHM70-2s-3p-D', '2_3.4m_A.OC V':100, '2_3.4m_A.R V':50, '2_3.4m_B.Stator':'LHM70-3s-2p-D', '2_3.4m_B.OC V':150, '2_3.4m_B.R V':75, '2_3.4m_C.Stator':'LHM70-2s-3p-S', '2_3.4m_C.OC V':183, '2_3.4m_C.R V':92, '2_3.4m_D.Stator':'LHM70-3s-2p-S', '2_3.4m_D.OC V':279, '2_3.4m_D.R V':140, '2_3.4m_E.Stator':'LHM70-6s-1p-D', '2_3.4m_E.OC V':296, '2_3.4m_E.R V':148, '2_3.4m_F.Stator':'LHM70-6s-1p-S', '2_3.4m_F.OC V':554, '2_3.4m_F.R V':277,  } )																															
    LHdata.update( {'2_3.5m_l/s':26, '2_3.5m_Watts':466, '2_3.5m_Efficiency':51, '2_3.5m_RPM':2249, '2_3.5m_R.RPM':4228, '2_3.5m_W.RPM':0, '2_3.5m_DT':0.15, '2_3.5m_DT W':30, '2_3.5m_A.Stator':'LHM70-2s-3p-D', '2_3.5m_A.OC V':101, '2_3.5m_A.R V':51, '2_3.5m_B.Stator':'LHM70-3s-2p-D', '2_3.5m_B.OC V':152, '2_3.5m_B.R V':76, '2_3.5m_C.Stator':'LHM70-2s-3p-S', '2_3.5m_C.OC V':186, '2_3.5m_C.R V':93, '2_3.5m_D.Stator':'LHM70-3s-2p-S', '2_3.5m_D.OC V':283, '2_3.5m_D.R V':142, '2_3.5m_E.Stator':'LHM70-6s-1p-D', '2_3.5m_E.OC V':300, '2_3.5m_E.R V':150, '2_3.5m_F.Stator':'LHM70-6s-1p-S', '2_3.5m_F.OC V':562, '2_3.5m_F.R V':281,  } )																															
    LHdata.update( {'2_3.6m_l/s':27, '2_3.6m_Watts':486, '2_3.6m_Efficiency':51, '2_3.6m_RPM':2281, '2_3.6m_R.RPM':4288, '2_3.6m_W.RPM':0, '2_3.6m_DT':0.15, '2_3.6m_DT W':31, '2_3.6m_A.Stator':'LHM70-2s-3p-D', '2_3.6m_A.OC V':103, '2_3.6m_A.R V':51, '2_3.6m_B.Stator':'LHM70-3s-2p-D', '2_3.6m_B.OC V':154, '2_3.6m_B.R V':77, '2_3.6m_C.Stator':'LHM70-2s-3p-S', '2_3.6m_C.OC V':189, '2_3.6m_C.R V':94, '2_3.6m_D.Stator':'LHM70-3s-2p-S', '2_3.6m_D.OC V':287, '2_3.6m_D.R V':144, '2_3.6m_E.Stator':'LHM70-6s-1p-D', '2_3.6m_E.OC V':304, '2_3.6m_E.R V':152, '2_3.6m_F.Stator':'LHM70-6s-1p-S', '2_3.6m_F.OC V':570, '2_3.6m_F.R V':285,  } )																															
    LHdata.update( {'2_3.7m_l/s':27, '2_3.7m_Watts':507, '2_3.7m_Efficiency':51, '2_3.7m_RPM':2312, '2_3.7m_R.RPM':4347, '2_3.7m_W.RPM':0, '2_3.7m_DT':0.15, '2_3.7m_DT W':32, '2_3.7m_A.Stator':'LHM70-2s-3p-D', '2_3.7m_A.OC V':104, '2_3.7m_A.R V':52, '2_3.7m_B.Stator':'LHM70-3s-2p-D', '2_3.7m_B.OC V':156, '2_3.7m_B.R V':78, '2_3.7m_C.Stator':'LHM70-2s-3p-S', '2_3.7m_C.OC V':191, '2_3.7m_C.R V':96, '2_3.7m_D.Stator':'LHM70-3s-2p-S', '2_3.7m_D.OC V':291, '2_3.7m_D.R V':146, '2_3.7m_E.Stator':'LHM70-6s-1p-D', '2_3.7m_E.OC V':309, '2_3.7m_E.R V':154, '2_3.7m_F.Stator':'LHM70-6s-1p-S', '2_3.7m_F.OC V':578, '2_3.7m_F.R V':289,  } )																															
    LHdata.update( {'2_3.8m_l/s':28, '2_3.8m_Watts':528, '2_3.8m_Efficiency':51, '2_3.8m_RPM':2343, '2_3.8m_R.RPM':4405, '2_3.8m_W.RPM':0, '2_3.8m_DT':0.15, '2_3.8m_DT W':34, '2_3.8m_A.Stator':'LHM70-2s-3p-D', '2_3.8m_A.OC V':106, '2_3.8m_A.R V':53, '2_3.8m_B.Stator':'LHM70-3s-2p-D', '2_3.8m_B.OC V':159, '2_3.8m_B.R V':79, '2_3.8m_C.Stator':'LHM70-2s-3p-S', '2_3.8m_C.OC V':194, '2_3.8m_C.R V':97, '2_3.8m_D.Stator':'LHM70-3s-2p-S', '2_3.8m_D.OC V':295, '2_3.8m_D.R V':148, '2_3.8m_E.Stator':'LHM70-6s-1p-D', '2_3.8m_E.OC V':313, '2_3.8m_E.R V':156, '2_3.8m_F.Stator':'LHM70-6s-1p-S', '2_3.8m_F.OC V':586, '2_3.8m_F.R V':293,  } )																															
    LHdata.update( {'2_3.9m_l/s':28, '2_3.9m_Watts':550, '2_3.9m_Efficiency':51, '2_3.9m_RPM':2374, '2_3.9m_R.RPM':4463, '2_3.9m_W.RPM':0, '2_3.9m_DT':0.15, '2_3.9m_DT W':35, '2_3.9m_A.Stator':'LHM70-2s-3p-D', '2_3.9m_A.OC V':107, '2_3.9m_A.R V':54, '2_3.9m_B.Stator':'LHM70-3s-2p-D', '2_3.9m_B.OC V':161, '2_3.9m_B.R V':80, '2_3.9m_C.Stator':'LHM70-2s-3p-S', '2_3.9m_C.OC V':196, '2_3.9m_C.R V':98, '2_3.9m_D.Stator':'LHM70-3s-2p-S', '2_3.9m_D.OC V':299, '2_3.9m_D.R V':150, '2_3.9m_E.Stator':'LHM70-6s-1p-D', '2_3.9m_E.OC V':317, '2_3.9m_E.R V':158, '2_3.9m_F.Stator':'LHM70-6s-1p-S', '2_3.9m_F.OC V':594, '2_3.9m_F.R V':297,  } )																															
    LHdata.update( {'2_4.0m_l/s':28, '2_4.0m_Watts':572, '2_4.0m_Efficiency':51, '2_4.0m_RPM':2404, '2_4.0m_R.RPM':4520, '2_4.0m_W.RPM':0, '2_4.0m_DT':0.15, '2_4.0m_DT W':36, '2_4.0m_A.Stator':'LHM70-2s-3p-D', '2_4.0m_A.OC V':108, '2_4.0m_A.R V':54, '2_4.0m_B.Stator':'LHM70-3s-2p-D', '2_4.0m_B.OC V':163, '2_4.0m_B.R V':81, '2_4.0m_C.Stator':'LHM70-2s-3p-S', '2_4.0m_C.OC V':199, '2_4.0m_C.R V':99, '2_4.0m_D.Stator':'LHM70-3s-2p-S', '2_4.0m_D.OC V':303, '2_4.0m_D.R V':151, '2_4.0m_E.Stator':'LHM70-6s-1p-D', '2_4.0m_E.OC V':321, '2_4.0m_E.R V':160, '2_4.0m_F.Stator':'LHM70-6s-1p-S', '2_4.0m_F.OC V':601, '2_4.0m_F.R V':301,  } )																															
    LHdata.update( {'2_4.1m_l/s':29, '2_4.1m_Watts':594, '2_4.1m_Efficiency':52, '2_4.1m_RPM':2434, '2_4.1m_R.RPM':4576, '2_4.1m_W.RPM':0, '2_4.1m_DT':0.15, '2_4.1m_DT W':38, '2_4.1m_A.Stator':'LHM70-2s-3p-D', '2_4.1m_A.OC V':110, '2_4.1m_A.R V':55, '2_4.1m_B.Stator':'LHM70-3s-2p-D', '2_4.1m_B.OC V':165, '2_4.1m_B.R V':82, '2_4.1m_C.Stator':'LHM70-2s-3p-S', '2_4.1m_C.OC V':201, '2_4.1m_C.R V':101, '2_4.1m_D.Stator':'LHM70-3s-2p-S', '2_4.1m_D.OC V':307, '2_4.1m_D.R V':153, '2_4.1m_E.Stator':'LHM70-6s-1p-D', '2_4.1m_E.OC V':325, '2_4.1m_E.R V':162, '2_4.1m_F.Stator':'LHM70-6s-1p-S', '2_4.1m_F.OC V':609, '2_4.1m_F.R V':304,  } )																															
    LHdata.update( {'2_4.2m_l/s':29, '2_4.2m_Watts':616, '2_4.2m_Efficiency':52, '2_4.2m_RPM':2464, '2_4.2m_R.RPM':4631, '2_4.2m_W.RPM':0, '2_4.2m_DT':0.15, '2_4.2m_DT W':39, '2_4.2m_A.Stator':'LHM70-2s-3p-D', '2_4.2m_A.OC V':111, '2_4.2m_A.R V':56, '2_4.2m_B.Stator':'LHM70-3s-2p-D', '2_4.2m_B.OC V':167, '2_4.2m_B.R V':83, '2_4.2m_C.Stator':'LHM70-2s-3p-S', '2_4.2m_C.OC V':204, '2_4.2m_C.R V':102, '2_4.2m_D.Stator':'LHM70-3s-2p-S', '2_4.2m_D.OC V':310, '2_4.2m_D.R V':155, '2_4.2m_E.Stator':'LHM70-6s-1p-D', '2_4.2m_E.OC V':329, '2_4.2m_E.R V':164, '2_4.2m_F.Stator':'LHM70-6s-1p-S', '2_4.2m_F.OC V':616, '2_4.2m_F.R V':308,  } )																															
    LHdata.update( {'2_4.3m_l/s':29, '2_4.3m_Watts':639, '2_4.3m_Efficiency':52, '2_4.3m_RPM':2493, '2_4.3m_R.RPM':4686, '2_4.3m_W.RPM':0, '2_4.3m_DT':0.15, '2_4.3m_DT W':40, '2_4.3m_A.Stator':'LHM70-2s-3p-D', '2_4.3m_A.OC V':112, '2_4.3m_A.R V':56, '2_4.3m_B.Stator':'LHM70-3s-2p-D', '2_4.3m_B.OC V':169, '2_4.3m_B.R V':84, '2_4.3m_C.Stator':'LHM70-2s-3p-S', '2_4.3m_C.OC V':206, '2_4.3m_C.R V':103, '2_4.3m_D.Stator':'LHM70-3s-2p-S', '2_4.3m_D.OC V':314, '2_4.3m_D.R V':157, '2_4.3m_E.Stator':'LHM70-6s-1p-D', '2_4.3m_E.OC V':333, '2_4.3m_E.R V':166, '2_4.3m_F.Stator':'LHM70-6s-1p-S', '2_4.3m_F.OC V':623, '2_4.3m_F.R V':312,  } )																															
    LHdata.update( {'2_4.4m_l/s':30, '2_4.4m_Watts':662, '2_4.4m_Efficiency':52, '2_4.4m_RPM':2522, '2_4.4m_R.RPM':4740, '2_4.4m_W.RPM':0, '2_4.4m_DT':0.15, '2_4.4m_DT W':42, '2_4.4m_A.Stator':'LHM70-2s-3p-D', '2_4.4m_A.OC V':114, '2_4.4m_A.R V':57, '2_4.4m_B.Stator':'LHM70-3s-2p-D', '2_4.4m_B.OC V':171, '2_4.4m_B.R V':85, '2_4.4m_C.Stator':'LHM70-2s-3p-S', '2_4.4m_C.OC V':209, '2_4.4m_C.R V':104, '2_4.4m_D.Stator':'LHM70-3s-2p-S', '2_4.4m_D.OC V':318, '2_4.4m_D.R V':159, '2_4.4m_E.Stator':'LHM70-6s-1p-D', '2_4.4m_E.OC V':337, '2_4.4m_E.R V':168, '2_4.4m_F.Stator':'LHM70-6s-1p-S', '2_4.4m_F.OC V':630, '2_4.4m_F.R V':315,  } )																															
    LHdata.update( {'2_4.5m_l/s':30, '2_4.5m_Watts':685, '2_4.5m_Efficiency':52, '2_4.5m_RPM':2550, '2_4.5m_R.RPM':4794, '2_4.5m_W.RPM':0, '2_4.5m_DT':0.15, '2_4.5m_DT W':43, '2_4.5m_A.Stator':'LHM70-2s-3p-D', '2_4.5m_A.OC V':115, '2_4.5m_A.R V':58, '2_4.5m_B.Stator':'LHM70-3s-2p-D', '2_4.5m_B.OC V':173, '2_4.5m_B.R V':86, '2_4.5m_C.Stator':'LHM70-2s-3p-S', '2_4.5m_C.OC V':211, '2_4.5m_C.R V':105, '2_4.5m_D.Stator':'LHM70-3s-2p-S', '2_4.5m_D.OC V':321, '2_4.5m_D.R V':161, '2_4.5m_E.Stator':'LHM70-6s-1p-D', '2_4.5m_E.OC V':340, '2_4.5m_E.R V':170, '2_4.5m_F.Stator':'LHM70-6s-1p-S', '2_4.5m_F.OC V':638, '2_4.5m_F.R V':319,  } )																															
    LHdata.update( {'2_4.6m_l/s':30, '2_4.6m_Watts':709, '2_4.6m_Efficiency':52, '2_4.6m_RPM':2578, '2_4.6m_R.RPM':4847, '2_4.6m_W.RPM':0, '2_4.6m_DT':0.15, '2_4.6m_DT W':45, '2_4.6m_A.Stator':'LHM70-2s-3p-D', '2_4.6m_A.OC V':116, '2_4.6m_A.R V':58, '2_4.6m_B.Stator':'LHM70-3s-2p-D', '2_4.6m_B.OC V':174, '2_4.6m_B.R V':87, '2_4.6m_C.Stator':'LHM70-2s-3p-S', '2_4.6m_C.OC V':213, '2_4.6m_C.R V':107, '2_4.6m_D.Stator':'LHM70-3s-2p-S', '2_4.6m_D.OC V':325, '2_4.6m_D.R V':162, '2_4.6m_E.Stator':'LHM70-6s-1p-D', '2_4.6m_E.OC V':344, '2_4.6m_E.R V':172, '2_4.6m_F.Stator':'LHM70-6s-1p-S', '2_4.6m_F.OC V':645, '2_4.6m_F.R V':322,  } )																															
    LHdata.update( {'2_4.7m_l/s':31, '2_4.7m_Watts':733, '2_4.7m_Efficiency':52, '2_4.7m_RPM':2606, '2_4.7m_R.RPM':4899, '2_4.7m_W.RPM':0, '2_4.7m_DT':0.15, '2_4.7m_DT W':46, '2_4.7m_A.Stator':'LHM70-2s-3p-D', '2_4.7m_A.OC V':118, '2_4.7m_A.R V':59, '2_4.7m_B.Stator':'LHM70-3s-2p-D', '2_4.7m_B.OC V':176, '2_4.7m_B.R V':88, '2_4.7m_C.Stator':'LHM70-2s-3p-S', '2_4.7m_C.OC V':216, '2_4.7m_C.R V':108, '2_4.7m_D.Stator':'LHM70-3s-2p-S', '2_4.7m_D.OC V':328, '2_4.7m_D.R V':164, '2_4.7m_E.Stator':'LHM70-6s-1p-D', '2_4.7m_E.OC V':348, '2_4.7m_E.R V':174, '2_4.7m_F.Stator':'LHM70-6s-1p-S', '2_4.7m_F.OC V':652, '2_4.7m_F.R V':326,  } )																															
    LHdata.update( {'2_4.8m_l/s':31, '2_4.8m_Watts':757, '2_4.8m_Efficiency':52, '2_4.8m_RPM':2634, '2_4.8m_R.RPM':4951, '2_4.8m_W.RPM':0, '2_4.8m_DT':0.15, '2_4.8m_DT W':48, '2_4.8m_A.Stator':'LHM70-2s-3p-D', '2_4.8m_A.OC V':119, '2_4.8m_A.R V':59, '2_4.8m_B.Stator':'LHM70-3s-2p-D', '2_4.8m_B.OC V':178, '2_4.8m_B.R V':89, '2_4.8m_C.Stator':'LHM70-2s-3p-S', '2_4.8m_C.OC V':218, '2_4.8m_C.R V':109, '2_4.8m_D.Stator':'LHM70-3s-2p-S', '2_4.8m_D.OC V':332, '2_4.8m_D.R V':166, '2_4.8m_E.Stator':'LHM70-6s-1p-D', '2_4.8m_E.OC V':352, '2_4.8m_E.R V':176, '2_4.8m_F.Stator':'LHM70-6s-1p-S', '2_4.8m_F.OC V':659, '2_4.8m_F.R V':329,  } )																															
    LHdata.update( {'2_4.9m_l/s':31, '2_4.9m_Watts':782, '2_4.9m_Efficiency':52, '2_4.9m_RPM':2661, '2_4.9m_R.RPM':5003, '2_4.9m_W.RPM':0, '2_4.9m_DT':0.15, '2_4.9m_DT W':49, '2_4.9m_A.Stator':'LHM70-2s-3p-D', '2_4.9m_A.OC V':120, '2_4.9m_A.R V':60, '2_4.9m_B.Stator':'LHM70-3s-2p-D', '2_4.9m_B.OC V':180, '2_4.9m_B.R V':90, '2_4.9m_C.Stator':'LHM70-2s-3p-S', '2_4.9m_C.OC V':220, '2_4.9m_C.R V':110, '2_4.9m_D.Stator':'LHM70-3s-2p-S', '2_4.9m_D.OC V':335, '2_4.9m_D.R V':168, '2_4.9m_E.Stator':'LHM70-6s-1p-D', '2_4.9m_E.OC V':355, '2_4.9m_E.R V':178, '2_4.9m_F.Stator':'LHM70-6s-1p-S', '2_4.9m_F.OC V':665, '2_4.9m_F.R V':333,  } )																															
    LHdata.update( {'2_5.0m_l/s':32, '2_5.0m_Watts':807, '2_5.0m_Efficiency':52, '2_5.0m_RPM':2688, '2_5.0m_R.RPM':5053, '2_5.0m_W.RPM':0, '2_5.0m_DT':0.15, '2_5.0m_DT W':51, '2_5.0m_A.Stator':'LHM70-2s-3p-D', '2_5.0m_A.OC V':121, '2_5.0m_A.R V':61, '2_5.0m_B.Stator':'LHM70-3s-2p-D', '2_5.0m_B.OC V':182, '2_5.0m_B.R V':91, '2_5.0m_C.Stator':'LHM70-2s-3p-S', '2_5.0m_C.OC V':222, '2_5.0m_C.R V':111, '2_5.0m_D.Stator':'LHM70-3s-2p-S', '2_5.0m_D.OC V':339, '2_5.0m_D.R V':169, '2_5.0m_E.Stator':'LHM70-6s-1p-D', '2_5.0m_E.OC V':359, '2_5.0m_E.R V':179, '2_5.0m_F.Stator':'LHM70-6s-1p-S', '2_5.0m_F.OC V':672, '2_5.0m_F.R V':336,  } )																															






    # Moody roughness figures from M Lawley as used in his spreadsheet for pipe loss calculations prior to Advanced Calculator
    Moody_pipe_material = { \
        'Drawn plastic tube':   0.00015, \
        'General steel':        0.00457, \
        'Asphalted iron':       0.01219, \
        'Galv. steel':          0.01524, \
        'Cast steel':           0.02540, \
        'Wood':                 0.09, \
        'Concrete':             0.3, \
        'RivetedSteel':         0.9 }

    # See origin of these figures below
    Manning_pipe_material = { \
        'Drawn plastic tube':   0.009, \
        'General steel':        0.011, \
        'Asphalted iron':       0.01, \
        'Galv. steel':          0.016, \
        'Cast steel':           0.014, \
        'Wood':                 0.012, \
        'Concrete':             0.015, \
        'RivetedSteel':         0.022 }



    """   This is from http://www.engineeringtoolbox.com/mannings-roughness-d_799.html
    Manning's Roughness
    Coefficient         Surface Material
    0.011		Asbestos cement
    0.016		Asphalt
    0.011		Brass
    0.015		Brickwork
    0.012		Cast-iron, new
    0.014		Clay tile
    0.011		Concrete - steel forms
    0.012		Concrete - finished
    0.015		Concrete - wooden forms
    0.013		Concrete - centrifugally spun
    0.011		Copper
    0.022		Corrugated metal
    0.025		Earth
    0.022		Earth channel - clean
    0.025		Earth channel - gravelly
    0.03		Earth channel - weedy
    0.035		Earth channel - stony, cobbles
    0.035		Floodplains - pasture, farmland
    0.05		Floodplains - light brush
    0.075		Floodplains - heavy brush
    0.15		Floodplains - trees
    0.016		Galvanized iron
    0.01		Glass
    0.029		Gravel
    0.011		Lead
    0.025		Masonry
    0.022		Metal - corrugated
    0.03		Natural streams - clean and straight
    0.035		Natural streams - major rivers
    0.04		Natural streams - sluggish with deep pools
    0.009		Plastic
    0.009 - 0.015	Polyethylene PE - Corrugated with smooth inner walls		
    0.018 - 0.025	Polyethylene PE - Corrugated with corrugated inner walls		
    0.009 - 0.011	Polyvinyl Chloride PVC - with smooth inner walls		
    0.01		Steel - Coal-tar enamel
    0.012		Steel - smooth
    0.011		Steel - New unlined
    0.019		Steel - Riveted
    0.012		Wood - planed
    0.013		Wood - unplaned
    0.012		Wood stave
    """




def VIpacked(n):    # This equates number of packers in a ratio of Volt or Current output relative to 0 packers
    return(-0.00025224 *n*n - 0.05304074 *n + 1) 

def PackersPref(n): # This provides a multiplier for the preference rating based on the number of packers
    if n == 0: return(1)
    return(3.5)

def loadingPref(portion): # This provides a multiplier for the preference rating based on normalised loading per finger
    # portion is the per finger load as a fraction of 1. 1 == max possible power
    if portion > 0.8:
        return ((portion - 0.8) *5 )**2.0 + 1
    return ((0.8 - portion ) * 8 )**2.0 + 1


def VPref(maxV, actV): # This provides a multiplier for the preference rating based loading per finger
    # maxld is the maximum possible per finger load
    # effld is the load per finger for max effeciency
    # actld is the actual load per finger
    ratio = 0.9
    gap = 1-ratio
    bestV = maxV * ratio
    if actV >= bestV:
        return ((actV - bestV) / (maxV * gap ) *2 )**2.0 + 1
    else:
        return ((bestV - actV ) / bestV *4 )**2.0 + 1

    
    

def computeSDtype(ElectOP_W, ShaftRPM, NLshaftRPM, vmax, vmin):
    #return():
    siteGUI.GUI_design_notes_SD = ''
    site.debug += 'Are in compute SD type with'+ str(ElectOP_W) +","+ str(ShaftRPM) +","+ str(NLshaftRPM) +","+ str(vmax) +","+ str(vmin) 
    ShaftRPM *= (0.1081 * site.LH_head + 0.7021)    # Correction to Michaels rmp figures to get voltages right  * (0.1081 * site.LH_head + 0.7021)
    site.debug += 'and shaft speed adj ' + str(ShaftRPM) +'rpm' + siteGUI.GUIcr
       
    if sys.platform[:5] == 'linux':
        site.monospace_on = '<span style=\'font-family:monospace;\'><span style=\'font-size:x-small;\'>'
        site.monospace_off = '</span></span></span>'
        site.Aspace = '&nbsp;'

    # Make a list of the SD versions including a finger set count that have acceptable w/rpm/fset
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(ShaftRPM) + 'rpm    at ' + str( ShaftPwr4SD ) + 'W convertable shaft power' + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr
    SD_size_list_ptr = 0
    SD_size_listA = {}
    SD_size_listB = {}
    SD_size_listC = {}
    SD_size_listD = {}
    SD_size_listE = {}
    SD_size_listF = {}
    SD_size_listG = {}

    #print ( 'Have ' + str(round( ElectOP_W )) + 'W output power to make' )
    site.SDsearch = site.SDsearch + 'Searching through all SD options with enough fingers for this power level' + siteGUI.GUI_diag_cr
    for SDchk in site.SD_types:      # Iterates over { '100--S','100--D','80--S','80--D','60--S','60--D','60dc--S','60dc--D','60dc-HPS','60dc-HP-D'.......}
        site.debug += ' Here I am 1.' + SDchk + siteGUI.GUIcr  #####################

        for packers in range(0,10):    # Itterate through all the packer sizes
            site.debug += ' Here I am 1.2 ' + str(packers) + siteGUI.GUIcr  #####################
            # Figure out the max power possible from this trial SD and the best efficency power for this SD
            MaxWmake  = (VIpacked(packers))* (VIpacked(packers)) \
                        * (site.SD_Max_e_mW4rpm4setA[SDchk] * ShaftRPM**2.0 \
                        + site.SD_Max_e_mW4rpm4setB[SDchk] * ShaftRPM \
                        + site.SD_Max_e_mW4rpm4setC[SDchk]) # MaxWuse = electrical watts out at MPP of this SD in mW per finger set

            if ShaftRPM <= 0 or MaxWmake <= 0: return
            site.debug += ' Here I am 1.post'  + siteGUI.GUIcr  #####################
            minfsets = int(ElectOP_W / ShaftRPM / MaxWmake * site.SDmargin * 1000 )+1
            maxfsets = int(site.SD_finger_sets[ SDchk ])
                                           
            if 1 > minfsets:
                minfsets = 1

            #print 'Def W/rpm   ElectOP_W ', ElectOP_W, '  ShaftRPM ', ShaftRPM, '  MaxWmake ', MaxWmake,\ '  BestWmake ', BestWmake, ' minfsets ', minfsets, '  maxfsets ', maxfsets,'   packers',packers
            if minfsets > site.SD_finger_sets[ SDchk ]: #maxfsets:  
                continue
            

            #  site.SDsearch = site.SDsearch + str(SDchk) + ' SDchk    ' + str(BestWuse) + ' BestWuse    ' + str(MaxWuse) + ' MaxWuse    ' + str(minfsets) + ' minfsets      ' + str( maxfsets ) + ' maxfsets    '  + siteGUI.GUI_diag_cr
            for fsets in range( int(minfsets), maxfsets+1 ):   # Iterate through possible number of finger sets to determine if within range
                site.debug += ' Here I am 1.3 ' + str(fsets) + siteGUI.GUIcr  #####################
                #print fsets
                for series in range (1,fsets+1): # Iterate through number of ok finger sets to factorize and make list of series/parallel possibilities
                    parallel = int(fsets / series)
                    if fsets != parallel * series: continue  # Only consider combinations that use all fsets!

                    if parallel * series < site.SD_finger_sets[ SDchk ]:    # Detect a cutdown and goto next lap
                        #print 'Cutdown alert'
                        continue

                    # Have a factorized version of this number of finger sets. Now determine power per finger set and Vo
                    mWperfset    = ElectOP_W / fsets / ShaftRPM * 1000 / site.Num_LH  # 1000x is from MaxWmake is in mW    Actual per fset power in mW
                    WnormPERfset = mWperfset / MaxWmake   # 1000x is from MaxWmake is in mW                                Per fset pwer as a portion of max possible
                    VoutNoLoad    = VIpacked(packers) * series * site.SD_mV4rpm4set[SDchk] * ShaftRPM  /1000  # Note that the table is in mV!
                    VoutNoLoadmax = VIpacked(packers) * series * site.SD_mV4rpm4set[SDchk] * NLshaftRPM /1000  # Note that the table is in mV!
    

                    # Use normalized sampled parameters in dictionary pwr4Vr[ Vr ] to determine Vr required for this power level (WnormPERfset).
                    # Samples are in Vr,Pwr samples in asscending order of Vr. Scan through and find above and below points
                    #  site.SDsearch = site.SDsearch + "     Looking for Vr for Pwr of " + str(WnormPERfset) + siteGUI.GUI_diag_cr
                    xl = 2
                    yl = 1
                    xh = 0
                    yh = 0
                    for key in site.pwr4Vr:
                        if( ( site.pwr4Vr[key] > WnormPERfset ) and ( site.pwr4Vr[key] <= yl) ):
                            xl = key
                            yl = site.pwr4Vr[key]
                            
                        if( ( site.pwr4Vr[key] < WnormPERfset ) and ( site.pwr4Vr[key] >= yh) ):
                            xh = key
                            yh = site.pwr4Vr[key]
                            

                    VrRequired = (WnormPERfset - yl) / (yh - yl) * (xh - xl) + xl          # Straight line interpolate between Xn,Yn points
                    TargetLdV = VoutNoLoad / VrRequired         # Expected output voltage at load

                    site.debug += ' Here I am 1.4 ' + str(TargetLdV) + siteGUI.GUIcr  #####################

                    Vo_diag = (' ' + str(round(VoutNoLoad,1)) + 'Voc @opr rpm               ')
                    Vl_diag = (' ' + str(round(TargetLdV,1))  + 'Vopr                         ')

                    
                    site.SDsearch = site.SDsearch + (SDchk + '        ')[:11] +  (str(series) + 'S' + str(parallel) + 'P  ' +'   ')[:8] \
                                    + (str(round(VrRequired,3)) + 'Vr         ')[:9]\
                                    + Vo_diag[len(Vo_diag)-16:]     +     Vl_diag[len(Vl_diag)-16:]  \
                                    + '  ' + (str(round(VoutNoLoad,1)) + ' SD nl V          ' )[:15] \
                                    + ' at ' + str(round(WnormPERfset*100,1)) + '% of MPP  ' + str(VoutNoLoadmax) + 'V no load free spinning'  + siteGUI.GUI_diag_cr
                    ###########################################
                    ###########################################
                    ###########################################
                    #print (SDchk + '        ')[:11] \
                    #      + (str(series) + 'S' + str(parallel) + 'P' + str(packers) + '   ')[:8] \
                    #      + (str(round(VrRequired,3)) + 'Vr         ')[:9] \
                    #      + Vo_diag[:18] \
                    #      + Vl_diag[:15] \
                    #      + (str(round(VoutNoLoad,1)) + ' Voc @opr          ' )[:15] \
                    #      + (str(round(MaxWmake,1)) + ' MaxWmake       ' )[:15] \
                    #      + (str(round(mWperfset,1)) + ' mWperfset       ' )[:15] \
                    #      + (str(round(ShaftRPM,1)) + ' ShaftRPM       ' )[:15] \
                    #      + ' at ' + str(round(WnormPERfset*100,1)) + '% of MPP  ' + str(VoutNoLoadmax) + 'Voc'\
                    #      ,'packer r=',VIpacked(packers), ' at SD finger pwr', site.SD_Max_e_mW4rpm4setC[ SDchk ]



                    
                    
                    if TargetLdV > vmin and VoutNoLoadmax < vmax:             # abs(TargetLdV / site.cable_Vgen - 1.0 ) < ( site.SDcloseness / 100.0 ) :        # Have found a SD type that is close enough. Create the SD code!
                        site.debug += ' Here I am 1.4 ' + str(TargetLdV) + siteGUI.GUIcr  #####################
                        site.SDsearch = site.SDsearch + 'This SD selected ' + siteGUI.GUI_diag_cr
                        SD_codes = SDchk.split('-')
                        ThisSD = SD_codes[0] + '-' + str(series) + 'S' + str(parallel) + 'P' + '-' + SD_codes[2] + '(' + str(int(packers)) + ')'
                        if ( SD_codes[1] != '' ):
                            ThisSD = ThisSD + '-' + SD_codes[1]

                        # Determine build effort rating for this SD
                        # 'ThisSD' is the code with 'series' and 'parallel' connections and operating at 'TargetLdV' load voltage and fractional possible power load of 'WnormPERfset'
                        # It also has site.SD_finger_sets[ SDchk ] possible finger sets
                        indexSscore = str(int(site.SD_finger_sets[ SDchk ])) + '-' + str(int(series))
                        indexPscore = str(int(site.SD_finger_sets[ SDchk ])) + '-' + str(int(parallel))
                        BuildChoice = site.Bld_ranking [SDchk] * site.Sscore[indexSscore] * site.Pscore[indexPscore]

                        # Check for magic 7. Although now removed in ver8
                        #if ThisSD in site.magic7:
                        #    BuildChoice = site.magic7[ThisSD]

                        BuildChoice = BuildChoice * PackersPref(packers) * loadingPref(WnormPERfset) * VPref(vmax, VoutNoLoadmax)
                        #print 'Found ', ThisSD, ' pref.',BuildChoice,',  maxW ', MaxWmake, ',  effW', BestWmake, ', act', ',   %lding', WnormPERfset * 100  # mWperfset / MaxWmake * 1000
                     
                        SD_size_list_ptr += 1                                                   # Vo, Voc, Vo/rpm, V/rpm, %ld
                        SD_size_listA[SD_size_list_ptr] = BuildChoice
                        SD_size_listB[SD_size_list_ptr] = ThisSD
                        SD_size_listC[SD_size_list_ptr] = str(int(round(TargetLdV,0)))          # Operating voltage this SD at this shaft speed
                        SD_size_listD[SD_size_list_ptr] = str(int(round(VoutNoLoadmax,0)))      # Open circuit voltage at runaway rpm
                        SD_size_listE[SD_size_list_ptr] = ''  #str(round(TargetLdV / ShaftRPM,3))    # Operating V/rpm for this install
                        SD_size_listF[SD_size_list_ptr] = str(round(series * site.Stator_mV4rpm4set[SDchk] / 1000,3))  # no load V/rpm for this stator
                        SD_size_listG[SD_size_list_ptr] = str(int(round( WnormPERfset * 100,0)))# % loading of this stator
                        



    site.debug += ' Here I am 2.' + siteGUI.GUIcr
    
    if siteGUI.GUI_LHtype == 'LH/LH Pro':
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'The following are other SD type code options and may be more suitable for your site.' + siteGUI.GUIcr
        if SD_size_list_ptr > 100:
            siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'These are the most useful SD stator/rotors of the '
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD +                    str(SD_size_list_ptr) + ' options found.' + siteGUI.GUIcr
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'Operating at ' + str(round(ElectOP_W / ShaftRPM,3)) + ' W/rpm' + siteGUI.GUIcr + siteGUI.GUIcr

        if ElectOP_W / ShaftRPM > 0.7:
            siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'Operating at greater than 0.7W per rpm requires the purchase ' \
                                          + 'of the high power option. Please check your order' + siteGUI.GUIcr + siteGUI.GUIcr

        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + site.monospace_on
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD \
                                      + ( ' SD code               ')[:20].replace(' ',site.Aspace) \
                                      + '        Vo'[-3:].replace(' ',site.Aspace) \
                                      + '       Voc'[-5:].replace(' ',site.Aspace) \
                                      + ' V/rpm    '[:6].replace(' ',site.Aspace) \
                                      + siteGUI.GUIcr

        siteGUI.GUI_diag = siteGUI.GUI_diag + str(SD_size_list_ptr) + ' SD stator/rotor diag options found.' + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr
        siteGUI.GUI_diag = siteGUI.GUI_diag \
                           + ('Pref.' + '       ')[:6] \
                           + ( ' SD code               ')[:20] \
                           + '        Vo'[-3:] \
                           + '       Voc'[-5:] \
                           + ' V/rpm    '[:6] \
                           + '      %ld '[-6:] \
                           + siteGUI.GUI_diag_cr

        outputlines = 0
        SD_types_done = []  # stores already displayed cores as 60R100-2S-6P-S(3) and 60R100-2S-6P-S(

        #print 'SD_size_list_ptr', SD_size_list_ptr, '  outputlines', outputlines, '  site.SDs2show', site.SDs2show
        while( SD_size_list_ptr >= 1 ):
            
            Whichrating = 1E50
            Whichchoice = 0
            for indexer in SD_size_listA:
                if( SD_size_listA[indexer] < Whichrating):
                    Whichchoice = indexer
                    Whichrating = SD_size_listA[indexer]
            if Whichchoice == 0: break


            
            #print Whichchoice, round(SD_size_listA[Whichchoice],3), SD_size_listB[Whichchoice], SD_size_listC[Whichchoice], SD_size_listD[Whichchoice]

            foundthis = SD_size_listB[Whichchoice].split('(')
            if foundthis[1] == '0)' or foundthis[0] not in SD_types_done:  # If a rotor not packed then include in list. Or if never displayed any packed version then display it
                #if 1 == 1:  foundthis[1] == '0)' or 

                if foundthis[1][:2] == '0)':    # If the SD code has no packers then remove the packers reference
                    this = SD_size_listB[Whichchoice].split('(0)')
                    SD_size_listB[Whichchoice] = this[0] + this[1]
                    
                if outputlines < site.SDs2show:
                    siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD \
                                   + (SD_size_listB[Whichchoice] + '                   ')[:20].replace(' ',site.Aspace) \
                                   + ( '     ' + SD_size_listC[Whichchoice] + ' ')[-4:].replace(' ',site.Aspace) \
                                   + ( '      ' + SD_size_listD[Whichchoice] + ' ')[-5:].replace(' ',site.Aspace) \
                                   + ( SD_size_listF[Whichchoice] + '     ')[:6].replace(' ',site.Aspace) \
                                   + siteGUI.GUIcr
                
                siteGUI.GUI_diag = siteGUI.GUI_diag \
                                   + ('         ' + str(int(round(SD_size_listA[Whichchoice],0))) +' ')[-6:] \
                                   + (SD_size_listB[Whichchoice] + '                   ')[:20] \
                                   + ( '     ' + SD_size_listC[Whichchoice] + ' ')[-4:] \
                                   + ( '      ' + SD_size_listD[Whichchoice] + ' ')[-5:] \
                                   + ( SD_size_listF[Whichchoice] + '     ')[:6] \
                                   + ( '     ' + SD_size_listG[Whichchoice])[-4:] \
                                   + siteGUI.GUIcr
                outputlines+= 1
            


            if foundthis[1] != '0)': SD_types_done.append(foundthis[0])
            SD_types_done.append(SD_size_listB[Whichchoice])
            
            del SD_size_listA[Whichchoice]
            del SD_size_listB[Whichchoice]
            del SD_size_listC[Whichchoice]
            del SD_size_listD[Whichchoice]
            del SD_size_listE[Whichchoice]
            del SD_size_listF[Whichchoice]
            del SD_size_listG[Whichchoice]
            
            if( SD_size_listA == {} or SD_size_listB == {} or SD_size_listC == {} or SD_size_listD == {} or SD_size_listE == {} ):
                break

    else:
        #print siteGUI.GUI_design_notes_SD
        #print "######################################"
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'The following are other LH mini code options and may show a more suitable option for your site.' + siteGUI.GUIcr
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + 'Operating at ' + str(round(ElectOP_W / ShaftRPM,3)) + ' W/rpm' + siteGUI.GUIcr + siteGUI.GUIcr

        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + site.monospace_on
        siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD \
                                      + ( ' SD code               ')[:20].replace(' ',site.Aspace) \
                                      + '        Vo'[-3:].replace(' ',site.Aspace) \
                                      + '       Voc'[-5:].replace(' ',site.Aspace) \
                                      + ' V/rpm    '[:6].replace(' ',site.Aspace) \
                                      + siteGUI.GUIcr


        site.indexbase = str(site.LH_type[ site.LHtype ]) + '_' + "%3.1f" % round(site.LH_head,1) + 'm_'
        site.LH_watts_cap = site.LHdata[ ( site.indexbase + 'Watts' ) ]
        thisStator = ''
        laststator = ''
        for SDoption in [ 'A.', 'B.', 'C.', 'D.', 'E.', 'F.' ]:
            #print( SDoption )
            laststator = thisStator
            thisStator = site.LHdata[ ( site.indexbase + SDoption + 'Stator' ) ]                            # Stator code
            thisVmax = str(int(round(   site.LHdata[ ( site.indexbase + SDoption + 'OC V' ) ]    ,0)))      # Open circuit voltage at runaway rpm
            thisVopr = str(int(round(   site.LHdata[ ( site.indexbase + SDoption + 'R V' ) ]     ,0)))      # Operating voltage this SD at this shaft speed
            thisrpm =  str(int(round(   site.LHdata[ ( site.indexbase + 'R.RPM' ) ]              ,0)))      # OPerating rpm 
            thisvrpm = str(round( (float(eval(thisVopr)) / float(eval(thisrpm))),6 )) # Operating V/rpm  "2_4.0m_R.RPM"
            #print eval(thisVopr),
            #print eval(thisrpm),
            #rint float(eval(thisVopr) / eval(thisrpm))

            #if laststator != thisStator and site.LHstator != thisStator:
            siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD \
                                     + (thisStator + '                   ')[:20].replace(' ',site.Aspace) \
                                     + ( '     ' + thisVopr + ' ')[-4:].replace(' ',site.Aspace) \
                                     + ( '      ' + thisVmax )[-4:].replace(' ',site.Aspace) \
                                     + ( ' ' + thisvrpm + '    ')[:6].replace(' ',site.Aspace) \
                                     + siteGUI.GUIcr

        #print siteGUI.GUI_design_notes_SD
        #print "######################################"

    siteGUI.GUI_design_notes_SD = siteGUI.GUI_design_notes_SD + site.monospace_off + siteGUI.GUIcr
    site.debug += ' Here I am 3.' + siteGUI.GUIcr









def FigureManningFlume(height):    # Determine possible flow in flume of passed height
    if height < 0.001: height = 0.001
    Mann = site.Manning_pipe_material[ siteGUI.GUI_pipe_mat ]
    # print( "Flume Manning", Mann)
    area = site.pipe_dia * height
    wetP = site.pipe_dia + 2 * height
    R = area / wetP
    site.pipeV = R**(2.0/3.0) * (site.pipe_head / site.pipe_len)**0.5 / Mann
    lps = area * site.pipeV * 1000
    return(lps)


def LH_Flume():  # Determine capacity of flume when full
    site.pipe_capacity = FigureManningFlume(site.pipe_height)   # Full height of flume capacity please
    if ( site.pipe_capacity < site.avail_lps ):
        site.usable_water = site.pipe_capacity
        site.alarms.append( 11 )    # Advise user of reduced water use due to pipe/flume losses
    else:
        site.usable_water = site.avail_lps




    
def LH_Flumedepth(): # Determine water depth in flume at site.actual_lps by trying different flume heights to determine flow capacity in N.R. S.A. approach 
    # Use site.pipe_head, site.pipe_len, site.pipe_dia, site.pipe_height, site.actual_lps
    # to work out site.water_depth and count convergance in site.pipe_iterations = 0
    # Pipe flow ranges from 0 to max over portion of depth full from 0 to 0.9382. At 0.8196 are same flow as at 1
    #   Start by determining max flow and then scale to actual flow using sucsseive approximation based on slope
    #   determined from last/previous result
    if FigureManningFlume(0.001) > site.actual_lps:
        site.water_depth = 0
        site.alarms.append( 14 )    # Tiny water for pipe size. Advise user
        return

    site.pipe_iterations = 0
    last_depth = 0.001
    last_lps = FigureManningPipe(last_depth)
    # r_tried_lps = 0
    depth_try = site.pipe_height

    while(1):
        tried_lps = FigureManningFlume(depth_try)
        #print( "Llps, Lr, Tlps, Tr, itrs", last_lps, last_depth, tried_lps, depth_try, site.pipe_iterations)
        if abs(site.actual_lps - tried_lps) < 0.1:  # See if found answer.... Are lps close enough?
            site.water_depth = depth_try
            break
        new = depth_try + ( depth_try - last_depth ) / (tried_lps - last_lps) * (site.actual_lps - tried_lps) 
        last_depth = depth_try
        last_lps = tried_lps
        depth_try = new
        site.pipe_iterations += 1
        if( site.pipe_iterations > 29):
            break

    # print(" PD exit ", site.pipe_iterations)
    if( site.pipe_iterations > 29):
        site.alarms.append( 10 )    # Opps. Flume calc failure. Advise user
            
            
    if site.pipe_capacity == site.actual_lps:
        site.water_depth = site.pipe_height
        site.alarms.append( 16 )    # Flume is at max capacity so probably full. Advise user

    if site.water_depth / site.pipe_height > 0.7:
        site.alarms.append( 13 )    # Flume is near capacity and this is a design guideline only. Advise user
        



def Manning_pipe_adj(height_ratio):  # Implements stepwise equation used for modifying Manning numbers for partially full pipes. See table below from Section 8, Partially Full Pipe Flow Calculations.pdf, http://www.google.co.nz/url?sa=t&rct=j&q=although%20the%20%E2%80%9Cflow%20in%20partially%20full%20pipes%E2%80%9D%20graph%20can%20be&source=web&cd=1&ved=0CFQQFjAA&url=http%3A%2F%2Fwww.cedengineering.com%2Fupload%2FPartially%2520Full%2520Pipe%2520Flow%2520Calculations.pdf&ei=eyjNT9-7L8SziQeD_9XmBg&usg=AFQjCNFMz3c-FLncq66Xlp0-dQZXWnHutw&cad=rja
    ratio = 1
    if height_ratio <= 0.03:                        ratio = 1 + height_ratio / 0.3
    if height_ratio >0.03 and height_ratio <= 0.1:  ratio = 1.1 + (height_ratio - 0.03)*(12/7)
    if height_ratio >0.1 and height_ratio <= 0.2:   ratio = 1.22 + (height_ratio - 0.1)*(0.6)
    if height_ratio >0.2 and height_ratio <= 0.3:   ratio = 1.29
    if height_ratio >0.3 and height_ratio <= 0.5:   ratio = 1.29 - (height_ratio - 0.3)*(0.2)
    if height_ratio >0.5 :                          ratio = 1.25 - (height_ratio - 0.5)*(0.5)
    return ( ratio )

    #The table as given in pdf as
    """
    0 < y/D < 0.03: n/nfull = 1 + (y/D)/(0.3) (3)
    0.03 < y/D < 0.1: n/nfull = 1.1 + (y/D  0.03)(12/7) (4)
    0.1 < y/D < 0.2: n/nfull = 1.22 + (y/D  0.1)(0.6) (5)
    0.2 < y/D < 0.3: n/nfull = 1.29 (6)
    0.3 < y/D < 0.5: n/nfull = 1.29 - (y/D  0.3)(0.2) (7)
    0.5 < y/D < 1: n/nfull = 1.25 - (y/D  0.5)(0.5) (8)
    """




def FigureManningPipe(percent_H):    # Input is portion of pipe fullness in terms of vertical height
    if percent_H < 0.01: percent_H = 0.01
    #percent_H = float(input("percent_H? ->"))
    Mod_Mann = site.Manning_pipe_material[ siteGUI.GUI_pipe_mat ]  *  Manning_pipe_adj(percent_H) 
    #print "Pipe Manning", site.Manning_pipe_material[ siteGUI.GUI_pipe_mat ], Manning_pipe_adj(percent_H) , Mod_Mann
    y = percent_H * site.pipe_dia
    theta = 2 * acos(1-2*y/site.pipe_dia)
    area = site.pipe_dia**2 /8*(theta - sin(theta))
    wetP = theta / 2 * site.pipe_dia
    R = area / wetP
    site.pipeV = R**(2.0/3.0) * (site.pipe_head / site.pipe_len)**0.5 / Mod_Mann
    lps = area * site.pipeV * 1000
    #print "pipe head="+str(site.pipe_head), "pip len="+str(site.pipe_len), "Mod_Mann="+str(Mod_Mann), \
    #      "dia="+str(site.pipe_dia), "Y="+str(y),"theta="+str(theta), "area="+str(area), \
    #      "wet"+str(wetP), "R="+str(R), "v="+str(site.pipeV), "lps="+str(lps)
    return(lps)



def LH_Pipe():  # Determine capacity of a Manning pipe at 81.96 & 100% full by height
    #print "Figure pipe cap at 81.96% full optimum"
    site.pipe_capacity = FigureManningPipe(0.8196)   # 81.96% full by height is same capacity as 100% full but less than at 93.82% which is in surging range.
    if ( site.pipe_capacity < site.avail_lps ):
        site.usable_water = site.pipe_capacity
        site.alarms.append( 11 )    # Advise user of reduced water use due to pipe losses
    else:
        site.usable_water = site.avail_lps


def PS_pipecalcdepth():     # Update that the pipe fullness is 100% for a PS pipe calculation
    site.water_depth = site.pipe_dia



def LH_Pipedepth(): # Determine depth of water in a Manning pipe
    # Use site.pipe_head, site.pipe_len, site.pipe_dia, site.pipe_height, site.actual_lps
    # to work out site.water_depth and count convergance in site.pipe_iterations = 0
    # Pipe flow ranges from 0 to max over portion of depth full from 0 to 0.9382. At 0.8196 are same flow as at 1
    #   Start by determining max flow and then scale to actual flow using sucsseive approximation based on slope
    #   determined from last/previous result
    #print "Test Manning pipe for very empty"
    if FigureManningPipe(0.01) > site.actual_lps:
        site.water_depth = 0
        site.alarms.append( 14 )    # Tiny water for pipe size. Advise user
        return

    site.pipe_iterations = 0
    last_depth_r = 0.01
    #print "Check last Manning depth"
    last_lps = FigureManningPipe(last_depth_r)
    # r_tried_lps = 0
    depth_r_try = 0.9382
    while(1):
        #print "Figure Manning depth"
        r_tried_lps = FigureManningPipe(depth_r_try)
        if abs(site.actual_lps - r_tried_lps) < 0.1:  # See if found answer.... Are lps close enough?
            site.water_depth = site.pipe_dia * depth_r_try
            break
        new_r = depth_r_try + ( depth_r_try - last_depth_r ) / (r_tried_lps - last_lps) * (site.actual_lps - r_tried_lps) 
        last_depth_r = depth_r_try
        last_lps = r_tried_lps
        depth_r_try = new_r
        site.pipe_iterations += 1
        if( site.pipe_iterations > 29):
            break

    if( site.pipe_iterations > 29):
        site.alarms.append( 10 )    # Opps. Pipe calc failure. Advise user
            
            
    if site.pipe_capacity == site.actual_lps:
        site.water_depth = site.pipe_dia
        site.alarms.append( 15 )    # Pipe is at max capacity so probably full and potential for surging. Advise user

    if site.water_depth / site.pipe_dia > 0.7:
        site.alarms.append( 12 )    # Pipe is near capacity and this is a design guideline only. Advise user
 
    


def PSpipe_hydro(this_lps):  # Calc pipe pressure loss based on Moody calcs
    site.pipe_flow_roughness = site.Moody_pipe_material[ siteGUI.GUI_pipe_mat ]  # But this is never used.....!!!!!
    #print( "PS material, roughness", siteGUI.GUI_pipe_mat, site.pipe_flow_roughness )


    site.pipe_area = pi * (site.pipe_dia / 2 )*(site.pipe_dia / 2 )
    site.pipeV = this_lps / site.mmm_lps / site.pipe_area
    site.Qm = 0.5 * site.pipeV * site.pipeV / site.gravity
    site.Re = site.density * site.pipeV * site.pipe_dia / site.viscosity
    # print ( "Pipe_hydro ", this_lps, " ", site.density, " ", site.pipeV, " ", site.pipe_dia, " ", site.viscosity, " ", site.pipe_len )
    if site.Re < 2100:
        site.Re_consider = 16 / site.Re
    else:
        site.Re_consider = -1


    if site.Re_consider == -1:
        site.x1 = -log10( site.eps / 3.7 -4.52 / site.Re * log( 7 / site.Re + site.eps / 7 ,10)  )
    else:
        site.x1 = -1

    if ( site.eps / 3.7 + 5.02 * site.x1 / site.Re) > 0:
        site.x2 = -log10( site.eps / 3.7 + 5.02 * site.x1 / site.Re)
    else:
        site.x2 = -1
        site.alarms.append( 10 )    # Opps. Pipe coefficients calculation failure. Advise user

    if ( site.eps / 3.7 + 5.02 * site.x2 / site.Re) > 0:    
        site.x3 = -log10( site.eps / 3.7 + 5.02 * site.x2 / site.Re)
    else:
        site.x3 = -1
        site.alarms.append( 10 )    # Opps. Pipe coefficients calculation failure. Advise user
    
    if ( site.eps / 3.7 + 5.02 * site.x3 / site.Re) > 0:
        site.x4 = -log10( site.eps / 3.7 + 5.02 * site.x3 / site.Re)
    else:
        site.x4 = -1
        site.alarms.append( 10 )    # Opps. Pipe coefficients calculation failure. Advise user
        
    site.Moodyfff = 1/ (16 * site.x4 * site.x4 )

    if site.x1 == -1:
        site.f = site.Re_consider
    else:
        site.f = site.Moodyfff

    site.dp_m = (4 * site.f * site.pipe_len / site.pipe_dia ) * site.Qm      # + site.pipe_Kf
    return(site.dp_m)


def PS_pipecalc(): # Determine pipe capacity calc based on Moody calcs
    """
    Evaluate the hydro parameters of pipe lenght, head and diameter and determine the pipes capacity.
    If capacity is less than the available then set used lps to pipe capacity lps otherwise used lps = available lps.

    This is based on hydro losses used for PowerSpout calculator
    """

    last_lps = 0
    last_dpm = 0
    this_lps = site.avail_lps
    this_dpm = PSpipe_hydro( this_lps )
    site.pipe_iterations = 0
    
    while( (abs(this_dpm - site.pipe_head) > 0.01) and (site.pipe_iterations < 30) ):
        dpm_slope = (this_lps - last_lps) / (this_dpm - last_dpm )
        last_lps = this_lps
        last_dpm = this_dpm
        this_lps = this_lps + dpm_slope * (site.pipe_head - this_dpm)
        this_dpm = PSpipe_hydro( this_lps )
        # print ( site.pipe_iterations, last_lps, last_dpm, dpm_slope, this_dpm, site.pipe_head, this_lps, "\r\n")
        site.pipe_iterations = site.pipe_iterations + 1
    site.pipe_capacity = this_lps
    # print( " pipe capacity is ", site.pipe_capacity )
    if( site.pipe_iterations > 29):
        site.alarms.append( 10 )    # Opps. Pipe calc failure. Advise user

    if ( site.pipe_capacity < site.avail_lps ):
        site.usable_water = site.pipe_capacity
        site.alarms.append( 11 )    # Advise user of reduced water use due to pipe losses

    else:
        site.usable_water = site.avail_lps

    if site.avail_lps / site.pipe_capacity > 0.7:
        site.alarms.append( 12 )    # Pipe is near capacity and this is a design guideline only. Advise user
  



def Determine_waterdepth(): # Consider pipe/flume to determine available water by user selected method
    """
    Evaluate the hydro parameters of pipe lenght, head and diameter and determine the pipes capacity.
    If capacity is less than the available then set used lps to pipe capacity lps otherwise used lps = available lps.
    """
    #print "Determine water depth", siteGUI.GUI_PipeFlume
    if siteGUI.GUI_PipeFlume == 'PS_pipe':  PS_pipecalcdepth()
    if siteGUI.GUI_PipeFlume == 'Pipe':     LH_Pipedepth()
    if siteGUI.GUI_PipeFlume == 'Flume':    LH_Flumedepth()




def Determine_water(): # Consider pipe to determine available water by user selected method
    """
    Evaluate the hydro parameters of pipe lenght, head and diameter and determine the pipes capacity.
    If capacity is less than the available then set used lps to pipe capacity lps otherwise used lps = available lps.
    """
    #print ""
    #print ""
    #print "Determine water available", siteGUI.GUI_PipeFlume
    if siteGUI.GUI_PipeFlume == 'PS_pipe':  PS_pipecalc()
    if siteGUI.GUI_PipeFlume == 'Pipe':     LH_Pipe()
    if siteGUI.GUI_PipeFlume == 'Flume':    LH_Flume()





def eff2use(frac):  # What turbine efficiency to use as eff drops at lower than ideal water flow? Lookup dictionary site.eff[ ] and straight line interpolate
        # siteGUI.GUI_diag = siteGUI.GUI_diag + str(water_frac) + siteGUI.GUI_diag_cr

        # Dictionary eff{} has water power: % efficiency points in asscending order. Scan through and find above and below points
        x1 = 0
        y1 = 0
        x2 = 1000000
        y2 = 52
        for key in site.eff:
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "key is " + str(key) + ' ' + str(site.eff[key]) + siteGUI.GUI_diag_cr
            if( (float(key) > float(x1) ) and ( float(key) <= float(frac))   ):
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new higher x1' + siteGUI.GUI_diag_cr
                x1 = key
                y1 = float(site.eff[key])
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x1,y1 is now' + str(x1) + ',' + str(y1) + siteGUI.GUI_diag_cr

            if( (float(key) < float(x2) ) and ( float(key) > float(frac))   ):
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new lower x2' + siteGUI.GUI_diag_cr
                x2 = key
                y2 = float(site.eff[key])
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x2,y2 is now' + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr

        # siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
        # siteGUI.GUI_diag = siteGUI.GUI_diag + '  x1,y1  x2,y2    finalizes at ' + str(x1) + ',' + str(y1)  + '    '   + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr
        # siteGUI.GUI_diag = siteGUI.GUI_diag + "WaterPwr/LH = " + str(water_frac) + "  x1 " + str(x1) + "  y1 " + str(y1) + "  x2 " + str(x2) + "  y2 " + str(y2) + siteGUI.GUI_diag_cr
        # print( "eff ing ", frac, x1, x2, y1, y2)
        if x2 == x1:
            return (0)
        else:
            site.LHeff = ( frac - x1) / (x2 - x1) * (y2 - y1) + y1          # Straight line interpolate between Xn,Yn points
            return(site.LHeff)



def Fetch_LH_parameters():  # Read dictionary site.LHdata[] and fetch base data for selected turbine head
    """
    LH_type = { 'LH1500 and Pro':1, 'LH1500 Pro +':2, 'LH1500 and Pro with SD PCB':3, 'LH1500 Pro + with SD PCB':4 }

    LHdata.update( {'1_1.0m_l/s':25, '1_1.0m_Watts':91, '1_1.0m_Efficiency':38, '1_1.0m_RPM':688, '1_1.0m_R.RPM':1032, '1_1.0m_W.RPM':0, '1_1.0m_DT':190, '1_1.0m_DT W':9, '1_1.0m_A.Stator':'100-7s-2p- star', '1_1.0m_A.OC V':137, '1_1.0m_A.R V':69, '1_1.0m_B.Stator':'80-7s-2p-delta', '1_1.0m_B.OC V':205, '1_1.0m_B.R V':103, '1_1.0m_C.Stator':'80-7s-2p-star', '1_1.0m_C.OC V':361, '1_1.0m_C.R V':181, '1_1.0m_D.Stator':'80-14s-1p-delta', '1_1.0m_D.OC V':411, '1_1.0m_D.R V':205,  } )
    LHdata.update( {'1_1.1m_l/s':26, '1_1.1m_Watts':107, '1_1.1m_Efficiency':38, '1_1.1m_RPM':722, '1_1.1m_R.RPM':1083, '1_1.1m_W.RPM':0, '1_1.1m_DT':190, '1_1.1m_DT W':11, '1_1.1m_A.Stator':'100-7s-2p- star', '1_1.1m_A.OC V':144, '1_1.1m_A.R V':72, '1_1.1m_B.Stator':'80-7s-2p-delta', '1_1.1m_B.OC V':215, '1_1.1m_B.R V':108, '1_1.1m_C.Stator':'80-7s-2p-star', '1_1.1m_C.OC V':379, '1_1.1m_C.R V':189, '1_1.1m_D.Stator':'80-14s-1p-delta', '1_1.1m_D.OC V':431, '1_1.1m_D.R V':215,  } )
    LHdata.update( {'1_1.2m_l/s':27, '1_1.2m_Watts':123, '1_1.2m_Efficiency':39, '1_1.2m_RPM':754, '1_1.2m_R.RPM':1131, '1_1.2m_W.RPM':0, '1_1.2m_DT':190, '1_1.2m_DT W':12, '1_1.2m_A.Stator':'100-7s-2p- star', '1_1.2m_A.OC V':150, '1_1.2m_A.R V':75, '1_1.2m_B.Stator':'80-7s-2p-delta', '1_1.2m_B.OC V':225, '1_1.2m_B.R V':113, '1_1.2m_C.Stator':'80-7s-2p-star', '1_1.2m_C.OC V':396, '1_1.2m_C.R V':198, '1_1.2m_D.Stator':'80-14s-1p-delta', '1_1.2m_D.OC V':450, '1_1.2m_D.R V':225,  } )
    LHdata.update( {'1_1.3m_l/s':28, '1_1.3m_Watts':176, '1_1.3m_Efficiency':49, '1_1.3m_RPM':785, '1_1.3m_R.RPM':1177, '1_1.3m_W.RPM':0, '1_1.3m_DT':190, '1_1.3m_DT W':14, '1_1.3m_A.Stator':'80-2s-7p-star', '1_1.3m_A.OC V':118, '1_1.3m_A.R V':59, '1_1.3m_B.Stator':'80-7s-2p-delta', '1_1.3m_B.OC V':234, '1_1.3m_B.R V':117, '1_1.3m_C.Stator':'100-14s-1p-star', '1_1.3m_C.OC V':313, '1_1.3m_C.R V':157, '1_1.3m_D.Stator':'80-14s-1p-delta', '1_1.3m_D.OC V':468, '1_1.3m_D.R V':234,  } )
            etc    """
    # Determine which index base to use.
    site.indexbase = str(site.LH_type[ site.LHtype ]) + '_' + "%3.1f" % round(site.LH_head,1) + 'm_'
    
    # And fetch parameters for this turbine
    site.LH_lps_cap = site.LHdata[ ( site.indexbase + 'l/s' ) ]
    site.LH_rpm_cap = site.LHdata[ ( site.indexbase + 'RPM' ) ]
    site.LH_watts_cap = site.LHdata[ ( site.indexbase + 'Watts' ) ]
    site.LH_rpm_NL = site.LHdata[ ( site.indexbase + 'R.RPM' ) ]
    site.LH_Draft_T = site.LHdata[ ( site.indexbase + 'DT' ) ]
    
    # print ( site.indexbase, site.LH_lps_cap, site.LH_rpm_cap, site.LH_rpm_NL, site.LH_watts_cap, site.LH_Draft_T )


    # Need to figure out which stator. Stator is the one with the biggest voltage that is under the Vmax limit in site.Load_Vmax
    vmax = 0
    site.vmax_req = 600
    thisVmax = 0
    thisVopr = 0
    site.SDchoice = ''
    for SDoption in [ 'A.', 'B.', 'C.', 'D.', 'E.', 'F.' ]:
        # print( SDoption )
        try:
            thisVmax = site.LHdata[ ( site.indexbase + SDoption + 'OC V' ) ]
            thisVopr = site.LHdata[ ( site.indexbase + SDoption + 'R V' ) ]
        except:
            continue
        if( thisVmax > vmax and thisVmax < site.Load_Vmax ):
            site.SDchoice = SDoption
        if thisVmax < site.vmax_req and thisVmax > 0:
            site.vmax_req = float(thisVmax) + 1
            
    if (site.SDchoice != '' ):
        site.LHstator = site.LHdata[ ( site.indexbase + site.SDchoice + 'Stator' ) ]
        site.LH_V_NL = site.LHdata[ ( site.indexbase + site.SDchoice + 'OC V' ) ]
        site.LH_V_cap = site.LHdata[ ( site.indexbase + site.SDchoice + 'R V' ) ]

    else:
        # print( "There are no generators appropiate.   Over V with no load or over W/rpm")
        site.alarms.append( 50 )    # Advise user of over voltage problem
        site.LH_V_NL = 0
        site.LH_V_Opr = 0
        site.LH_V_cap = 0
        site.LHstator = ''
        site.LH_W_Opr = 0





def Fetch_LH_4_next_Vmin(Vmax_min):     # Search SD gens to find the next up Vmax option after the current site.SDchoice selected SD
    vmax = Vmax_min + 1  # Only search up from current V no load
    vmax_most = 600
    thisVmax = 0
    thisVopr = 0
    SDchoice = ''
    for SDoption in [ 'A.', 'B.', 'C.', 'D.', 'E.', 'F.' ]:
        # print( SDoption )
        try:
            thisVmax = site.LHdata[ ( site.indexbase + SDoption + 'OC V' ) ]
            thisVopr = site.LHdata[ ( site.indexbase + SDoption + 'R V' ) ]
        except:
            continue
        # print( 'thisVmax upping  SDoption and V NL', SDoption, thisVmax )
        if( thisVmax > Vmax_min and thisVmax < vmax_most and thisVopr > site.Load_Vmin ):
            # print( '                       Have chosen', SDoption, thisVmax )
            vmax_most = thisVmax
            SDchoice = SDoption
                    
    if (SDchoice != '' ):
        siteLH_V_NL = site.LHdata[ ( site.indexbase + SDchoice + 'OC V' ) ] + 1
    else:
        siteLH_V_NL = 0

    return(siteLH_V_NL)











def LH_W_forNumLH(LHcount):     # For a given number of LH hydros what is the power output in watts
    # Determine Watts for this LHcount
    # Scale for water volume
    # If have 70% of the water then operating rpm, power out, and output voltage are reduced to 70% of rating also and
    # output current, no load rpm and voltage do not change
    if LHcount == 0:
        site.LH_lps_Opr = 0
        site.percent_LHutilize = 0
        site.actual_lps = 0
        site.LH_rpm_Opr = 0
        site.LH_watts_Opr = 0
        site.LH_V_Opr = 0
        Eff_scalar = 0
        site.LH_pwr_tot = 0
        return(0)
    
    else:
        site.LH_lps_Opr = site.actual_lps / LHcount
        site.percent_LHutilize = site.LH_lps_Opr / site.LH_lps_cap
        if site.percent_LHutilize > 1:
            site.percent_LHutilize = 1
            site.LH_lps_Opr = site.LH_lps_cap
        site.actual_lps = site.LH_lps_Opr * LHcount
        site.LH_rpm_Opr = site.percent_LHutilize * site.LH_rpm_cap
        site.LH_watts_Opr = site.percent_LHutilize * site.LH_watts_cap
        site.LH_V_Opr = site.percent_LHutilize * site.LH_V_cap

        # print ( "%%%", site.LH_lps_Opr, site.percent_LHutilize, site.LH_rpm_Opr, site.LH_watts_Opr, site.LH_watts_cap, site.LH_V_cap )
        # Scale for efficiency drop at lower water volume
        # With reduced water volume then operating rpm, power out, output voltage, output current need further scaling to account for hydro performance fall off.
        Eff_scalar = eff2use( site.percent_LHutilize )
        site.LH_rpm_Opr = Eff_scalar * site.LH_rpm_Opr
        site.LH_watts_Opr = Eff_scalar * Eff_scalar * site.LH_watts_Opr
        site.LH_V_Opr = Eff_scalar * site.LH_V_Opr


        site.LH_pwr_tot = site.LH_watts_Opr * LHcount
        # print( site.percent_LHutilize, Eff_scalar, ('LH_lps_cap each =' + str(site.LH_lps_cap)), ('LH_lps_Opr each =' + str(site.LH_lps_Opr)),\
        #       ('LH_rpm_Opr =' + str(site.LH_rpm_Opr)), ('LH_watts_Opr each =' + str(site.LH_watts_Opr)), ('LH_V_Opr each =' + str(site.LH_V_Opr)) )


        """site.diag.write( 'Eff calcs  lps=' + str(site.actual_lps) + \
                         '  W cap=' + str(site.LH_watts_cap) + '  V cap=' + str(site.LH_V_cap) + \
                         '  % cap=' + str(site.percent_LHutilize) + '  eff scale=' + str(Eff_scalar) + \
                         '  V Opr=' + str(site.LH_V_Opr) + '  W Opr=' + str(site.LH_watts_Opr) + '\n\n\n')
        """

        #site.diag2.write( '\t' + str(site.LH_pwr_tot) )

        return(site.LH_lps_Opr * LHcount)



def LH_hydro_calc(): # Compute output power for selected number of LH hydros. And select best LH hydro if not locked
    Fetch_LH_parameters()

    # Itterate through each number of LH hydros till find peak. Result always inc to peak then drops. Check all anyhow
    # Need to assess if design has optimum number of hydros so can advise user
    lasttestW = 0
    maxWnumLH = 1
    lpsputback = site.actual_lps
    #site.diag2.write( str(site.actual_lps) )
    for count in range(1,21):
        site.actual_lps = lpsputback
        Fetch_LH_parameters()
        test_lps = LH_W_forNumLH( count )  # site.LH_pwr_tot has W for this count
        #site.diag.write( 'Num_LH=' + str(count) + '  lps2use=' + str(lpsputback) + '  lps used=' + str(site.actual_lps) + '  W=' + str(site.LH_pwr_tot) + '  Wea=' + str(site.LH_pwr_tot/count) + '  lps ea=' + str(site.LH_lps_Opr) + '\n')
        if site.LH_pwr_tot > lasttestW:
            lasttestW = site.LH_pwr_tot
            site.maxWnumLH = count

    # Use result from above according to if GUI_LockNumLH is true                                 Check and adjust number of LH hydros installed
    if( siteGUI.GUI_LockNumLH == 0 ):  # Test if number of LH hydros is not locked
        test_lps = LH_W_forNumLH( site.maxWnumLH )  # Recompute the best result to update site.    
        site.Num_LH = site.maxWnumLH
        site.actual_lps = LH_W_forNumLH( site.Num_LH )
    else:       # Number of LH hydros is locked so figure if an optimum power design and tell the user
        site.actual_lps = LH_W_forNumLH( site.Num_LH )  # Update water figures
        #if site.Num_LH == site.maxWnumLH and abs(site.usable_water - site.actual_lps) < 0.2:
        #    site.alarms.append( 1x )    # Advise user that have an ideal match between water delivered by flume and number of LH hydro 

        if site.Num_LH < site.maxWnumLH:
            site.alarms.append( 21 )    # Advise user that more LH hydro units would make more power

        if site.Num_LH > site.maxWnumLH and site.maxWnumLH > 1:
            site.alarms.append( 22 )    # Advise user that less LH hydro units would make more power
        if site.Num_LH > site.maxWnumLH and site.maxWnumLH == 1:
            site.alarms.append( 23 )    # Advise user that 1 LH hydro unit would make more power


    # This call uses site data to determine which SD to use.
    #print 'Off to computeSDtype( )'
    site.debug += ' LH_hydro_calc() calls computeSDtype ' \
                 + str(site.LH_watts_Opr) \
                 + " " + str(site.LH_rpm_Opr) \
                 + " " + str(site.LH_rpm_NL) \
                 + " " + str(site.Load_Vmax) \
                 + " " + str(site.Load_Vmin) \
                 + siteGUI.GUIcr  #####################
    computeSDtype( site.LH_watts_Opr, site.LH_rpm_Opr, site.LH_rpm_NL, site.Load_Vmax, site.Load_Vmin)  

    if site.Num_LH == site.maxWnumLH and site.usable_water - site.actual_lps > 0.1:
        site.alarms.append( 19 )    # Advise user that have correct Num LH for max power even though not all water is used

   



def CalcCable():  # Work out cable performance. Select cable size if needed.
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Entering CalcCable' + siteGUI.GUI_diag_cr
    #print 'Entering CalcCable', str(site.LH_pwr_tot) + ' of hydro watts, ', str(site.cable_size) + 'mm^2 cable'
    if(site.LH_V_NL == 0 or site.LH_V_Opr < site.Load_Vmin - 1 ):
        site.cable_voltage = 0
        site.cable_A = 0
        site.LH_pwr_tot = 0.001
        site.Load_pwr = 0
        site.LH_V_Opr = 0
        site.LH_W_Opr = 0
    else:
        #print 'Have a valid power level to compute cable results', site.cable_A, site.LH_pwr_tot, site.LH_V_Opr
        site.cable_A = site.LH_pwr_tot / site.LH_V_Opr            # amps in cable
        #print 'Have a valid power level to compute cable results', site.cable_A, site.LH_pwr_tot, site.LH_V_Opr
        # Update cable losses based on current cable size in site.cable_size
        # Find loss in current cable size. Gives resultant load watts. Ignores under volts delivered
        site.cableR = float(site.material[ site.cable_material ] * float(1e6) / site.cable_size * site.cable_len * float(2))
        site.cable_Vdrop = site.cable_A * site.cableR
        site.cable_voltage = site.LH_V_Opr - site.cable_Vdrop
        site.Load_pwr = site.cable_A * site.cable_voltage


        # See is cable size is to be calculated from scratch and if then calc it.
        if int(site.cableLock) == int(0):      # If no user lock on cable size And not initial data then go pick a cable size for the target cable loss     and siteGUI.GUI_initial_data == 0 
            #print 'calc cable from scratch'
            site.Load_pwr = site.cable_eff_target * site.LH_pwr_tot        # Power to load
            site.cable_Vdrop = site.LH_V_Opr * ( 1-site.cable_eff_target )       # total volts lost accross cable in both directions
            site.cable_voltage = site.LH_V_Opr - site.cable_Vdrop
            site.cableR_req = site.cable_Vdrop / site.cable_A / site.cable_len / 2          # Cable resistance in ohm/m for each direction
            site.cable_size = round(site.material[ site.cable_material ] * 1e6 / site.cableR_req, 1)  # Sqr mm needed


        #print  'Pre check cable voltage and load Vmin ', site.cable_voltage, site.Load_Vmin

        # Determine minimum cable size for amps and if selected cable is less than this then up cable size as needed and notify user.
        previous_cablesize = site.cable_size   # temp store of cable size while do min cable size calculation
        MinCable4Amps()    # Choose cable based on amps carrying ability. Rating for this cable just " + str(site.cable_amp_spec) )
        #print 'site.cable_size, previous_cablesize', site.cable_size, previous_cablesize
        if site.cable_size > previous_cablesize:
            #print 'Need bigger cable'
            if int(site.cableLock) == int(1): # Test if cable size locked cause then is a user size being adjusted.
                site.alarms.append( 53 )    # Note to alm reporting section that users cable size was increased to handle current
            else:                             # And as is a resistance loss based size then need a different message to user
                site.alarms.append( 54 )    # Note to alm reporting section that cable size was increased to handle current
        else:
            site.cable_size = previous_cablesize

        site.cable_amp_spec = cable_amps_rate( site.cable_size )


        #print  ' from cable voltage and load Vmin ', site.cable_voltage, site.Load_Vmin
        # See if voltage drop is excessive for inverter and selected SD and increase cable size to suit. Notify user
        if site.cable_voltage < site.Load_Vmin:     # If true voltage drop is too much so must increase cable size and tell user
            #print 'Excessive V drop on cable at cable size ' + str(site.cable_size)
            site.cable_Vdrop = site.LH_V_Opr - site.Load_Vmin       # total volts lost accross cable in both directions
            site.cable_voltage = site.LH_V_Opr - site.cable_Vdrop
            site.cableR_req = site.cable_Vdrop / site.cable_A / site.cable_len / 2          # Cable resistance in ohm/m for each direction
            site.cable_size = round(site.material[ site.cable_material ] * 1e6 / site.cableR_req, 1)  # Sqr mm needed
            site.alarms.append( 55 )    # Note to alm reporting section that cable size was increased to cover match Vmin of inverter



        # Provide AWG sizing
        createAWG()
        # If are working in AWG cable sizes then need to create a whole round AWG size (roundup) in metric for final computation.
        if siteGUI.GUI_cable_mm_AWG == 'AWG':
            create_mm_4_AWG(site.cable_gauge)

        # Find loss in current cable size. Gives resultant load watts. Ignores under volts delivered
        site.cableR = float(site.material[ site.cable_material ] * float(1e6) / site.cable_size * site.cable_len * float(2))
        site.cable_Vdrop = site.cable_A * site.cableR
        site.cable_voltage = site.LH_V_Opr - site.cable_Vdrop
        site.Load_pwr = site.cable_A * site.cable_voltage

    #print str(site.cable_size), 'mm^2 at exit'






def computeALL():       # Do the calculation of inputs to create outputs following all design limits
    Determine_water()
    site.actual_lps = site.usable_water
    LH_hydro_calc()
    #if site.actual_lps < site.usable_water:
    #    site.alarms.append( xx )    # Advise user of ......

    #print "Original", site.LHeff, site.Load_pwr, siteGUI.GUI_LHtype

    if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH/LH Pro':
        site.alarms.append( 25 )
    if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH mini':
        site.alarms.append( 24 )
    if siteGUI.GUI_LHtype == 'LH mini' and site.Num_LH > 2:
        site.alarms.append( 26 )

    # Sort out under and over voltage issues and report to user
    if site.LH_V_Opr < site.Load_Vmin:   # Check if under Vmin of inverter, Over Vmin LHh, and that do not have a Vmax problem     and 1-(50 in site.alarms)
        # print( "There are no generators appropiate   Under V with load", site.Num_LH, site.LH_V_Opr, site.Load_Vmin )
        if 1-(50 in site.alarms):
            if site.LH_V_Opr > 75:
                site.alarms.append( 51 )    # Advise user of under voltage problem and to use a lower Vmin or increase Vmax to ...?????
            else:
                site.alarms.append( 52 )    # Advise user of under voltage problem and to increaseVmax to ...?????

        if site.LH_V_cap > 0:   # Check to avoid divide by zero
            if site.LH_V_Opr / site.LH_V_cap and site.Num_LH > 1:   # Check to see if are at maximum lps per turbine and >1 of LH cause less LH turbines may be enough
                site.alarms.append( 60 )    # Fewer turbines may do the trick to increase V operate as are at less than max lps per turbine

        site.LH_V_Opr_guide = site.LH_V_Opr
        site.LH_Vmax_guide = Fetch_LH_4_next_Vmin(site.LH_V_NL)
        # print( 'Vmax guide is ', site.LH_Vmax_guide, ' based on value ', site.LH_V_NL, ' and operating at ', site.LH_V_Opr)
        site.cable_voltage = 0
        site.cable_A = 0
        site.LH_pwr_tot = 0
        site.Load_pwr = 0
        site.LH_W_Opr = 0
        site.LHstator = ''

        #print "2nd", site.LHeff, site.Load_pwr, siteGUI.GUI_LHtype
        if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH/LH Pro':
            site.alarms.append( 25 )
        if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH mini':
            site.alarms.append( 24 )
        if siteGUI.GUI_LHtype == 'LH mini' and site.Num_LH > 2:
            site.alarms.append( 26 )
        return


    CalcCable()

    #print "3rd", site.LHeff, site.Load_pwr, siteGUI.GUI_LHtype

    if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH/LH Pro':
        site.alarms.append( 25 )
    if site.LHeff< 0.5 and site.Load_pwr == 0 and siteGUI.GUI_LHtype == 'LH mini':
        site.alarms.append( 24 )
    if siteGUI.GUI_LHtype == 'LH mini' and site.Num_LH > 2:
        site.alarms.append( 26 )




       
    # Put in checks here for design issues not resolved elsewhere
    #################################################################################################################################################################################
    #################################################################################################################################################################################
    # Check cable for current rating as is close to typical ratings
    if( site.cable_A > 0 and site.cable_amp_spec / site.cable_A < 1.5):
        site.alarms.append( 56 )        # Cable size within 50% of likely current rating. Please check with your cable supplier for suitability. Amps temp rise etc

    #################################################################################################################################################################################
    # Check cable oversize expense
    if site.LH_V_Opr > 0:
        if 1-(52 in site.alarms or 53 in site.alarms or 54 in site.alarms or 55 in site.alarms or 56 in site.alarms) and site.cable_voltage / site.LH_V_Opr > 0.98 and site.cable_len > 30:
            site.alarms.append( 57 )        # Cable size within 50% of likely current rating. Please check with your cable supplier for suitability. Amps temp rise etc

    #################################################################################################################################################################################
    # Check voltage margins
    if abs( site.LH_V_Opr - site.Load_Vmin) < 20:
        site.alarms.append( 58 )        # Operating voltages are close to Vmin limits of your inverter.
    if abs( site.LH_V_NL - site.Load_Vmax ) < 40:
        site.alarms.append( 59 )        # Operating voltages are close to limits of your inverter. Be careful




def cable_amps_rate( smm ):     # Convert cable square mm into a nominal amps rating
    #print ( "smm", smm)
    amp_limit1 = float(smm * 10)                    / (  site.material[ site.cable_material ] / site.material[ 'Copper' ])**0.5
    amp_limit2 = float(smm * 10 * pow(smm,0.74))    / (  site.material[ site.cable_material ] / site.material[ 'Copper' ])**0.5
    
    if( amp_limit1 > amp_limit2 ):
        return(amp_limit2)
    else:
        return(amp_limit1)


def cable_smm4amps( amps ):  # Determine sqr mm cable needed for given current
    smm = 2
    site.cable_amp_spec = cable_amps_rate( smm )
    while(1):        
        site.itteratorCount = site.itteratorCount + 1
        smm_slope = cable_amps_rate( smm + 0.01 ) - site.cable_amp_spec
        smm = smm + ( amps - site.cable_amp_spec ) / smm_slope / float(100)
        site.cable_amp_spec = cable_amps_rate( smm )
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "amps " + str(amps) + "  Sqr mm" + str(smm) + " & rating" + str(site.cable_amp_spec) + "    at slope of " +str(smm_slope) + siteGUI.GUI_diag_cr
        if( abs(site.cable_amp_spec / amps - 1 ) < 0.001 ):
            break
    return(smm)


def MinCable4Amps():    # Choose cable based on amps carrying ability. Rating for this cable just " + str(site.cable_amp_spec) )
    # print( "Choosing min cable size for this number of amps.  Was " + str(site.cable_size) )
    while(1):
        temp_holder = site.cable_size
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.cable_size) + siteGUI.GUI_diag_cr
        site.cable_size = cable_smm4amps( site.cable_A )
        if( abs( temp_holder / site.cable_size - 1 ) < 0.001):
            break

    #print(' and now is ' + str(site.cable_size) )
    createAWG()


    
def createAWG():  # Convert sqr mm into next size up AWG
    cable_gauge_tmp = -39 * log( 2 * sqrt( site.cable_size * 0.99 / pi) /0.127 ,92) +36
    if cable_gauge_tmp < 0:
        cable_gauge_tmp = -int(cable_gauge_tmp - 1)
        string = ""
        site.cable_gauge = string.zfill(cable_gauge_tmp+1)
    else:
        site.cable_gauge = str(int(cable_gauge_tmp))



def create_mm_4_AWG(AWG):  # Convert AWG into sqr mm
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Arrived at create_mm_4_AWG ' + str(site.cable_size) + siteGUI.GUI_diag_cr
    temp = site.cable_size
    try:
        if( eval( AWG ) == 0 ):
            site.cable_AWGn = -AWG.count("0")+1
        else:
            site.cable_AWGn = textread( AWG, 'AWG', 'AWG' )

        if( site.cable_AWGn > 20 ):
            site.cable_AWGn = 20
        if( site.cable_AWGn < -6 ):
            site.cable_AWGn = -6

        #siteGUI.GUI_diag = siteGUI.GUI_diag + str(pi * pow(0.127/2 * pow(92, (36-site.cable_AWGn) / 39 ) ,2)) + siteGUI.GUI_diag_cr
        site.cable_size = pi * pow(float(0.127/2) * pow(92, float(36-site.cable_AWGn) / 39 ) ,2)
    except:
        site.cable_size = temp

    #  siteGUI.GUI_diag = siteGUI.GUI_diag + '   Leaving create_mm_4_AWG ' + str(site.cable_size) + siteGUI.GUI_diag_cr
    return()        # Result is an updated site.cable_size





def reportAll():        # Report all results to user gui. This is the only place where gui values get updated for the user to see
    Determine_waterdepth()

    if( site.cable_material == 'Steel'):
        site.alarms.append( 58 )
        

    put_lps()
    put_lpsused()
    put_pipehead()
    put_LHhead()
    put_PenLen()
    put_Pipe_Cap()
    put_PenDia()
    put_PenHeight()
    put_waterD()
    put_Num_LH()
    put_draftT()
    put_LH_rpm_Opr()
    put_LH_rpm_NL()
    put_eaLH_W()
    put_allps_W()
    put_Opr_V()
    put_NL_V()
    put_cableEff_targ()
    put_CableLen()
    put_Load_Vmax()
    put_Load_Vmin()
    put_ActLdV()
    put_CableSize()
    put_CableAWG() 
    put_CableDetails()

    if site.LH_V_Opr == 0:
        blank_OP()  # Blank output values to be empty strings

    if site.pipeV > 1: site.alarms.append( 17 )    # Advise user of high flume/pipe velocity

    # Create alarm string for hydro issues
    # example of list is.....     alarms = [ 10, 12, 20]
    #print ('Site alarm codes', site.alarms)
    siteGUI.GUI_design_notes_hydro = ''  # An empty string for design comments for the end user to read and understand
    siteGUI.GUI_design_notes_elec = ''   # An empty string for design comments for the end user to read and understand
    siteGUI.GUI_design_notes_safety = ''  # An empty string for design comments for the end user to read and understand

    #
    if 10 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Pipe loss calculations failed and pipe flow limit ignored. ' +\
        'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr
    #
    if 11 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your chosen pipe/flume limits water flow. With a larger pipe/flume more water ' + \
        'will yield more power, although extra flow cannot always be utilised.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 12 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your pipe is at least 70% full. Note that this calculator is provided as a guide only. ' +\
        'Adequate design margin is your responsibility and you are recommended to obtain independent engineering advice ' +\
        'if you are committing significant money into your installation.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 13 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your flume is at least 70% full. Note that this calculator is provided as a guide only. ' +\
        'Adequate design margin is your responsibility and you are recommended to obtain independent engineering advice ' +\
        'if you are committing significant money into your installation.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 14 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your chosen pipe/flume is much, much larger than is required. Water flow is insignificant' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 15 in site.alarms: 
        if( siteGUI.GUI_meas_sys == 'Metric' ):
            text1 = str(int(round(site.pipe_dia * 0.9382 * site.convert[ 'mm-m' ],0) )) + ' mm'
        if( siteGUI.GUI_meas_sys == 'Imperial' ):
            text1 = str(round(site.pipe_dia * 0.9382 * site.convert[ 'in-m' ] ,2) )  + ' in'
        if( siteGUI.GUI_meas_sys == 'Metric' ):
            text2 = str(round(FigureManningPipe(0.9382),3-int(log10(site.pipe_capacity)) )  ) + ' lps'  
        if( siteGUI.GUI_meas_sys == 'Imperial' ):    
            text2 = str(int(round(FigureManningPipe(0.9382) * site.convert[ 'gpm-lps' ],3-int(log10(site.pipe_capacity * site.convert[ 'gpm-lps' ])) )  )) + ' gpm'
        siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your chosen pipe is operating at capacity. If there was an air gap at ' + text1 + ' water depth the pipe can transport ' + \
        text2 + '. Increased flow is not expected as surging likely to limit performance so pipe is assumed to be full.' + siteGUI.GUIcr + siteGUI.GUIcr


    #
    if 16 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your chosen flume is completely full. Overflow water can cause erosion issues.' + siteGUI.GUIcr + siteGUI.GUIcr

    if 17 in site.alarms:
        supplier = '???'
        if siteGUI.GUI_PipeFlume == 'Pipe': supplier = 'pipe'
        if siteGUI.GUI_PipeFlume == 'PS_pipe': supplier = 'pipe'
        if siteGUI.GUI_PipeFlume == 'Flume': supplier = 'flume'
        siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Your ' + supplier + ' has high water velocity. High water velocity causes turbulance at the turbine and poor performance. Reduce ' +\
        supplier + ' steepness with less fall or increased length.' + siteGUI.GUIcr + siteGUI.GUIcr

    # 19 = Plateau region operation detected
    if 19 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'More LH hydros could use more of your available water ' + \
        'but you would then get less power. This design ' + \
        'provides the most power as it will operate at the highest efficiency as the LH hydro(s) are fully ' + \
        'utilised' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 21 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'More LH hydro units would use more of your available water ' + \
        'and provide more power. ' + str(int(site.maxWnumLH)) + ' LH hydro units is best.' + siteGUI.GUIcr + siteGUI.GUIcr
    #
    if 22 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Fewer LH hydro units would provide more efficient use of your available water ' + \
        'and provide more power. ' + str(int(site.Num_LH)) + ' LH hydro units is best.' + siteGUI.GUIcr + siteGUI.GUIcr
    #
    if 23 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Just 1 LH hydro unit would provide more efficient use of your available water ' + \
        'and provide more power. ' + siteGUI.GUIcr + siteGUI.GUIcr

    if 24 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Flow is too low. Try a TRG turbine.' + siteGUI.GUIcr + siteGUI.GUIcr

    if 25 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'Flow is too low. Try LH mini or TRG turbine options. ' + siteGUI.GUIcr + siteGUI.GUIcr

    if 26 in site.alarms: siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
        'LH/LH Pro turbines are usually a better option than many LH-mini turbines.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 50 in site.alarms:
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
            'Sorry. There are no standard generators to suit your design. ' + \
            'Select an inverter/charge controller with a Vmax input of at least ' + \
            str(site.vmax_req)+ 'V.' + siteGUI.GUIcr + siteGUI.GUIcr
        blank_OP()  # Blank output values to be empty strings
   
    #
    if 60 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'The operating on load voltage from the LH Hydro increases with increased water flow in each turbine. ' +\
        'Try less LH hydro units or more water to increase operating voltage and you might achieve your inverter/charge controllers Vmin specification. ' +\
        siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 51 in site.alarms: # site.cable_voltage < site.Load_Vmin AND site.cable_voltage > 75 (LH hydro is 75Vout min)
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
            'There is no SD generator suitable for your site. Under load the voltage output of the LH hydro is less ' + \
            'than your inverter can operate with. ' + \
            'Use an inverter with a Vmin input less than ' + str(int(site.LH_V_Opr_guide)) + 'V. '
        if site.LH_Vmax_guide > 0:
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                'An inverter with a higher Vmax of over ' + str(int(site.LH_Vmax_guide)) + ' may help.' + siteGUI.GUIcr + siteGUI.GUIcr
        else:
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUIcr + siteGUI.GUIcr
            
        blank_OP()  # Blank output values to be empty strings"""

    #
    if 52 in site.alarms: # site.cable_voltage < site.Load_Vmin AND site.cable_voltage < 75 (LH hydro is 75Vout min)
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
            'There is no SD generator suitable for your site. Under load the voltage output of the LH hydro would end up less ' + \
            'than the LH hydro is designed for. '
        if site.LH_Vmax_guide > 0:
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                'An inverter with a higher Vmax of over ' + str(int(site.LH_Vmax_guide)) + ' may help.' + siteGUI.GUIcr + siteGUI.GUIcr
        else:
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUIcr + siteGUI.GUIcr

        blank_OP()  # Blank output values to be empty strings"""

    #
    if 53 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Your cable efficiency target and cable size selection has been ignored and a larger cable size calculated to carry the ' +\
        'current from the LH hydro unit(s). ' + \
        'If you only have a smaller sized cable to use then either increase ' +\
        'the operating voltage or reduce the number of LH hydro units' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 54 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Your cable efficiency target has been ignored and a larger cable size calculated to carry the ' +\
        'current from the LH hydro unit(s). ' + \
        'If you only have a smaller sized cable to use then either increase ' +\
        'the operating voltage or reduce the number of LH hydro units.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 55 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Your cable efficiency target has been ignored and a larger cable size calculated to reduce ' +\
        'the cable voltage drop to meet the inverter/charge controller\'s minimum operating voltage. ' +\
        'An inverter/charge controller with a higher Vmax and/or lower Vmin may reduce the required cable size. ' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 56 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Cable size is within 50% of likely current rating. ' +\
        'Cable loss calculations are based on a ' +\
        '20 deg C (68 deg F) conductor temperature. Please check ' +\
        'with your cable supplier for suitability for current ' +\
        'handling, temperature rise and loss at this current.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 57 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Cable efficiency is very high. While this is good the cost of cable can be ' +\
        'a problem. You might want to reduce cable size, loose some efficiency and save money?' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 58 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'The operating voltage is close to the Vmin of your inverter/charge controller will operate at. ' +\
        'There is a possibility of less than expected power if the operating point is actually lower than the Vmin. ' +\
        'A, lower than Vmin, operating point will not damage your equipment, although some inverters and charge controllers ' +\
        'are confused by this situation.' + siteGUI.GUIcr + siteGUI.GUIcr

    #
    if 59 in site.alarms: siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'The no load voltage from the LH Hydro is close to the Vmax of your inverter/charge controller will accept. ' +\
        'Exceeding Vmax for a charge controller/inverter is usually destructive. Failure to follow documented commissioning ' +\
        'procedures may result in the damage of your inverter/charge controller at your expense! ' +\
        'No warranty is provided for failure to follow instructions.' + siteGUI.GUIcr + siteGUI.GUIcr


    rounds = { }
    values = { }
    
    values['-2a'] = site.cable_voltage * 0.8
    rounds['-2a'] = -len(str(int(values['-2a']))) +3
    values['-2b'] = site.Load_pwr * 0.25
    rounds['-2b'] = -len(str(int(values['-2b']))) +3

    values['-1a'] = site.cable_voltage * 0.9
    rounds['-1a'] = -len(str(int(values['-1a']))) +3
    values['-1b'] = site.Load_pwr * 0.5
    rounds['-1b'] = -len(str(int(values['-1b']))) +3

    values['0a'] = site.cable_voltage
    rounds['0a'] = -len(str(int(values['0a']))) +3
    values['0b'] = site.Load_pwr
    rounds['0b'] = -len(str(int(values['0b']))) +3

    values['+1a'] = site.cable_voltage * 1.1
    rounds['+1a'] = -len(str(int(values['+1a']))) +3
    values['+1b'] = site.Load_pwr * 1.5
    rounds['+1b'] = -len(str(int(values['+1b']))) +3

    values['+2a'] = site.cable_voltage * 1.2
    rounds['+2a'] = -len(str(int(values['+2a']))) +3
    values['+2b'] = site.Load_pwr * 2
    rounds['+2b'] = -len(str(int(values['+2b']))) +3

    for items in rounds:
        if rounds[items] > 0: rounds[items] = 0


    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
        'Table mode ( in some inverters) can be used to resolve MPPT tracking stability issues. ' +\
        'Below is a suggested table that will help in getting you started. ' +\
        'On site adjustment (by trial and error) will be needed to get the best result when using table mode. ' +\
        'Only Power-One, EnaSolar and Ginlong inverters have a table mode setting. ' +\
        'Some off grid MPPT regulators also have table modes. ' +\
        siteGUI.GUIcr + 'Suggested table' + siteGUI.GUIcr +\
        'min voltage setting, min power setting'  + siteGUI.GUIcr +\
        str(int(round(values['-2a'],rounds['-2a']))) + ', ' + str(int(round(values['-2b'],rounds['-2b']))) + siteGUI.GUIcr +\
        str(int(round(values['-1a'],rounds['-1a']))) + ', ' + str(int(round(values['-1b'],rounds['-1b']))) + siteGUI.GUIcr +\
        str(int(round(values['0a'],rounds['0a']))) + ', ' + str(int(round(values['0b'],rounds['0b']))) + siteGUI.GUIcr +\
        str(int(round(values['+1a'],rounds['+1a']))) + ', ' + str(int(round(values['+1b'],rounds['+1b']))) + siteGUI.GUIcr +\
        str(int(round(values['+2a'],rounds['+2a']))) + ', ' + str(int(round(values['+2b'],rounds['+2b']))) + siteGUI.GUIcr +\
        'max voltage setting, max power setting'  + siteGUI.GUIcr + siteGUI.GUIcr



    if site.LHstator != '':
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + 'Recommended SD stator is ' + site.LHstator + '(provisional)' + siteGUI.GUIcr
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + '(This code is copyright of EcoInnovation)' + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr

    
    #if siteGUI.GUI_LHtype == 'LH/LH Pro':
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUI_design_notes_SD  # Add lookuped SD codes to report


    siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + \
        'Operation of the LH hydro generates voltages that exceeds the ELV (Extra Low Voltage) limits for non electrical workers to maintain.' + siteGUI.GUIcr +\
        'Please ensure you hire a registered electrical worker.' + siteGUI.GUIcr + siteGUI.GUIcr +\
        'Please note' + siteGUI.GUIcr +\
        'Only the performance of the LH Hydro turbine is warranted to meet the predictions made in this tool. ' +\
        'The losses calculated in the flow of water through the flume/pipe to ' +\
        'your LH Hydro(s) is your responsibility and are provided here free of charge for your guidance only. ' +\
        'If you require guaranteed performance for your flume/pipe then please obtain independent engineering advice.' + siteGUI.GUIcr + siteGUI.GUIcr


    
    if sys.platform[:5] == 'linux':
        siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr
    if sys.platform[:5] == 'linux':
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr
    if sys.platform[:5] == 'linux':
        siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr



    siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "  Calculation process" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     It took " + str(site.pipe_iterations) + " iterations to solve pipe flow rate" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                         eps " + str(site.eps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               Pipe velocity " + str(site.pipeV) + "m/s" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "       Turbine operating rpm " + str(site.LH_rpm_Opr) + "rpm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                 runaway_rpm " + str(site.LH_rpm_NL) + "rpm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + " Some constants" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     density " + str(site.density) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     gravity " + str(site.gravity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     mmm_lps " + str(site.mmm_lps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   viscosity " + str(site.viscosity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "         pipe_flow_roughness " + str(site.pipe_flow_roughness) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              cable_material " + str(site.cable_material) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  cableR_req " + str(site.cableR_req) + "ohm/m" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "      Cable ohms (ret. trip) " + str(site.cableR) + "ohm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "           Cable voltage drop" + str(site.cable_Vdrop) + " V"  + siteGUI.GUI_diag_cr

    siteGUI.GUI_diag = siteGUI.GUI_diag + "           Itterator counter " + str(site.itteratorCount) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "      siteGUI.GUI_LockNumLH " + str(siteGUI.GUI_LockNumLH) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "    siteGUI.GUI_initial_data " + str(siteGUI.GUI_initial_data) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr


    siteGUI.GUI_diag = siteGUI.GUI_diag_cr + siteGUI.GUI_diag + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr + 'After' + siteGUI.GUI_diag_cr 
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'Electrical notes here ' + siteGUI.GUI_design_notes_elec + siteGUI.GUI_diag_cr 



def blank_OP():
    siteGUI.GUI_LH_watts_Opr = ''
    siteGUI.GUI_LH_pwr_tot = ''
    siteGUI.GUI_LH_V_Opr = ''
    siteGUI.GUI_LH_V_NL = ''
    siteGUI.GUI_Aload_V = ''
    siteGUI.GUI_cable_A = ''
    siteGUI.GUI_actual_cable_eff = ''
    siteGUI.GUI_Load_pwr = '' 







def put_lps():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_avail_lps = str(round(site.avail_lps,1)) + ' lps'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_avail_lps = str(round(site.avail_lps * site.convert[ 'gpm-lps' ]  ,1)) + ' gpm'

def put_lpsused():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_actual_lps = str(round(site.actual_lps,1)) + ' lps'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_actual_lps = str(round(site.actual_lps * site.convert[ 'gpm-lps' ] ,1)) + ' gpm'

def put_pipehead():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_pipe_head = str( int(round(site.pipe_head * site.convert[ 'mm-m' ] ,0 ))) + ' mm'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_pipe_head = str( round(site.pipe_head * site.convert[ 'in-m' ] ,2 )) + ' in'

def put_LHhead():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_LH_head = str( round(site.LH_head,1 )) + ' m'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_LH_head = str( round(site.LH_head * site.convert[ 'ft-m' ] ,1 )) + ' ft'

def put_PenLen():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_pipe_len = str(round(site.pipe_len,1) ) + ' m'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_pipe_len = str(round(site.pipe_len * site.convert[ 'ft-m' ] ,1))  + ' ft'

def put_Pipe_Cap():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_pipe_capacity = str(round(site.pipe_capacity,3-int(log10(site.pipe_capacity)) )  ) + ' lps'  
    if( siteGUI.GUI_meas_sys == 'Imperial' ):    
        siteGUI.GUI_pipe_capacity = str(int(round(site.pipe_capacity * site.convert[ 'gpm-lps' ],3-int(log10(site.pipe_capacity * site.convert[ 'gpm-lps' ])) )  )) + ' gpm'

def put_PenDia():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_pipe_dia = str(int(round(site.pipe_dia * site.convert[ 'mm-m' ],0) )) + ' mm'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_pipe_dia = str(round(site.pipe_dia * site.convert[ 'in-m' ] ,2) )  + ' in'

def put_PenHeight():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_pipe_height = str(int(round(site.pipe_height * site.convert[ 'mm-m' ],0) )) + ' mm'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_pipe_height = str(round(site.pipe_height * site.convert[ 'in-m' ] ,2) )  + 'in'

def put_waterD():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_water_depth = str(int(round(site.water_depth * site.convert[ 'mm-m' ],0) )) + ' mm  at '  +\
                                  str(round(site.pipeV * site.convert[ 'mps-mps' ] ,1) ) + 'm/s'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_water_depth = str(round(site.water_depth * site.convert[ 'in-m' ] ,1) )  + 'in  at '  +\
                                  str(round(site.pipeV * site.convert[ 'fps-mps' ] ,1) )  + 'ft/s'
    if siteGUI.GUI_PipeFlume == 'PS_pipe':  siteGUI.GUI_water_depth = ''


def put_Num_LH():
    siteGUI.GUI_Num_LH = int( site.Num_LH )

def put_draftT():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_LH_Draft_T = str(int(round(site.LH_Draft_T * site.convert[ 'mm-m' ],0) )) + ' mm'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_LH_Draft_T = str(int(round(site.LH_Draft_T * site.convert[ 'in-m' ],2) ))  + ' in'

def put_LH_rpm_Opr():
    siteGUI.GUI_LH_rpm_Opr = str(int(site.LH_rpm_Opr )) + ' rpm'

def put_LH_rpm_NL():
    siteGUI.GUI_LH_rpm_NL = str(int(site.LH_rpm_NL )) + ' rpm'

def put_eaLH_W():
    siteGUI.GUI_LH_watts_Opr = str(int(site.LH_watts_Opr ) ) + ' W'
    
def put_allps_W():
    siteGUI.GUI_LH_pwr_tot = str(int(site.LH_watts_Opr * site.Num_LH) ) + ' W'

def put_Load_Vmax():
    siteGUI.GUI_Load_Vmax = str(int(site.Load_Vmax + 0.5)) + ' V'

def put_Load_Vmin():
    siteGUI.GUI_Load_Vmin = str(int(site.Load_Vmin + 0.5)) + ' V'

def put_Opr_V():
    siteGUI.GUI_LH_V_Opr = str(int(site.LH_V_Opr + 0.5)) + ' V'

def put_NL_V():
    siteGUI.GUI_LH_V_NL = str(int(site.LH_V_NL + 0.5)) + ' V'

def put_cableEff_targ():
    siteGUI.GUI_cable_eff_target = str(int(site.cable_eff_target * 100 )) + ' %'

def put_CableLen():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_cable_len = str(int(round(site.cable_len,0))) + ' m'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_cable_len = str(int(round(site.cable_len * site.convert[ 'ft-m' ],0) ))  + ' ft'

def put_ActLdV():
    siteGUI.GUI_Aload_V = str(int(site.cable_voltage + 0.5)) + ' V'

def put_CableSize():
    siteGUI.GUI_cable_size = str(round(site.cable_size,3 )) + ' mm^2'

def put_CableAWG():    
    siteGUI.GUI_cable_AWG = str( site.cable_gauge ) + ' AWG'

    
def put_CableDetails():    
    siteGUI.GUI_cable_dia_mm_sld = str(round(pow(site.cable_size/pi,0.5)*2 ,2 )) + ' mm'
    siteGUI.GUI_cable_dia_mm_str = str(round(pow(site.cable_size/0.58/pi, 0.5)*2 ,2) ) + ' mm'
    siteGUI.GUI_cable_dia_in_sld = str(round(pow(site.cable_size/pi,0.5)*2/25.4 ,3)) + ' in'
    siteGUI.GUI_cable_dia_in_str = str(round(pow(site.cable_size/0.58/pi, 0.5)*2/25.4 ,3)) + ' in'


    if site.LH_pwr_tot == 0:
        siteGUI.GUI_cable_A = '0 A'
        siteGUI.GUI_actual_cable_eff = '0 %'
        siteGUI.GUI_cable_Vgen = '0 V'
        siteGUI.GUI_Load_pwr = '0 W' 
    else:        
        siteGUI.GUI_cable_A = str(round(site.cable_A,1 )) + ' A'
        siteGUI.GUI_actual_cable_eff = str(int(site.Load_pwr / site.LH_pwr_tot * 100 + 0.5 )) + ' %'
        siteGUI.GUI_cable_Vgen = str(int(site.LH_V_Opr + 0.5 )) + ' V'
        siteGUI.GUI_Load_pwr = str(int(site.Load_pwr + 0.5 )) + ' W' 







def fetchall(): # Fetch all user inputs
    fetchlps()
    fetchpipehead()
    fetch_LHhead()
    fetchpenlen()
    fetchpentype()
    fetchpendia()
    fetchpenheight()
    fetchNum_LH()
    fetchcablelen()
    fetchLoadVmax()
    fetchLoadVmin()
    fetchcableefftarg()
    site.cable_material = siteGUI.GUI_cable_material
    site.cableLock = int(siteGUI.GUI_LockCable)
    if siteGUI.GUI_cable_mm_AWG == 'mm':
        fetchcablesize()
    if siteGUI.GUI_cable_mm_AWG == 'AWG':
        fetchAWG()


def fetchlps():         # Get users lps entered.  Only called from fetchall() and BasicData()
    temp = site.avail_lps

    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.avail_lps = textread( siteGUI.GUI_avail_lps, 'lps', 'lps' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.avail_lps = textread( siteGUI.GUI_avail_lps, 'gpm', 'lps' )

    if( (temp <= 500) and (temp >= 10) and (site.avail_lps == 0)  ):
        site.avail_lps = temp
    else:
        if( (temp != 0) or (site.avail_lps != 0)  ):
            if( site.avail_lps > 500 ):
                site.avail_lps = 500
            if( site.avail_lps < 10 ):
                site.avail_lps = 10

    site.lps = site.avail_lps


def fetchpipehead():         # Get site head entered.  Only called from fetchall() and newBasicData()
    temp = site.pipe_head

    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.pipe_head = textread( siteGUI.GUI_pipe_head, 'mm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.pipe_head = textread( siteGUI.GUI_pipe_head, 'in', 'm' )

    if( (temp <= 200) and (temp >= 0.01) and (site.pipe_head == 0)  ):
        site.pipe_head = temp
    else:
        if( site.pipe_head > 200 ):
            site.pipe_head = 200
        if( site.pipe_head < 0.01 ):
            site.pipe_head = 0.01



def fetch_LHhead():         # Get site head entered.  Only called from fetchall() and newBasicData()
    temp = site.LH_head

    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.LH_head = textread( siteGUI.GUI_LH_head, 'm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.LH_head = textread( siteGUI.GUI_LH_head, 'ft', 'm' )

    if( (temp <= 5) and (temp >= 1) and (site.LH_head == 0) ):
        site.LH_head = temp
    else:
        if( site.LH_head > 5 ):
            site.LH_head = 5
        if( site.LH_head < 1 ):
            site.LH_head = 1

        
def fetchpenlen():         # Get this site data entered.  Only called from fetchall()
    temp = site.pipe_len

    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.pipe_len = textread( siteGUI.GUI_pipe_len, 'm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.pipe_len = textread( siteGUI.GUI_pipe_len, 'ft', 'm' )

    if( (temp <= 5000) and (temp >= 0.1) and (site.pipe_len == 0 )  ):
        site.pipe_len = temp
    else:
        if( site.pipe_len > 5000 ):
            site.pipe_len = 5000
        if( site.pipe_len < 0.1 ):     # Was site.pipe_head before instead of 3m as min length
            site.pipe_len = 0.1        # Was site.pipe_head before instead of 3m as min length


def fetchpentype():         # Read type of penstock. Flume or pipe
    if siteGUI.GUI_PipeFlume == 'Pipe':
        siteGUI.GUI_PipeFlumeT1 = 'Pipe diameter'     # R Title for pipe diameter
        siteGUI.GUI_PipeFlumeT2 = ''                  # R Title for flume height so is blank for pipe
        
    if siteGUI.GUI_PipeFlume == 'PS_pipe':
        siteGUI.GUI_PipeFlumeT1 = 'Pipe diameter'     # R Title for pipe diameter
        siteGUI.GUI_PipeFlumeT2 = ''                  # R Title for flume height so is blank for pipe

    if siteGUI.GUI_PipeFlume == 'Flume':
        siteGUI.GUI_PipeFlumeT1 = 'Flume width'     # R Title for pipe diameter / flume width
        siteGUI.GUI_PipeFlumeT2 = 'Flume depth'     # R Title for flume height or is blank



def fetchpendia():         # Get this site data entered.  Only called from fetchall()
    temp = site.pipe_dia
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.pipe_dia = textread( siteGUI.GUI_pipe_dia, 'mm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.pipe_dia = textread( siteGUI.GUI_pipe_dia, 'in', 'm' )

    if( (temp <= 4) and (temp >= 0.01) and (site.pipe_dia == 0) ):
        site.pipe_dia = temp
    else:
        if( site.pipe_dia > 4 ):
            site.pipe_dia = 4
        if( site.pipe_dia < 0.01 ):
            site.pipe_dia = 0.01

        
def fetchpenheight():         # Get this site data entered.  Only called from fetchall()
    temp = site.pipe_height
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.pipe_height = textread( siteGUI.GUI_pipe_height, 'mm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.pipe_height = textread( siteGUI.GUI_pipe_height, 'in', 'm' )

    if( (temp <= 4) and (temp >= 0.01) and (site.pipe_height == 0) ):
        site.pipe_height = temp
    else:
        if( site.pipe_height > 4 ):
            site.pipe_height = 4
        if( site.pipe_height < 0.01 ):
            site.pipe_height = 0.01

        
def fetchNum_LH():         # Get this site data entered.  Only called from newNoLH() and LockLH()
    temp = site.Num_LH

    site.Num_LH = int( siteGUI.GUI_Num_LH )

    if( (temp <= 10) and (temp >= 1 ) and (site.Num_LH == 0)  ):
        site.Num_LH = temp
    else:
        if( (temp != 0) or (site.Num_LH != 0)  ):
            if( site.Num_LH > site.MaxLH ):
               site.Num_LH = site.MaxLH
            if( site.Num_LH < 1):
               site.Num_LH = 1


def fetchLoadVmax():       # Get the max voltage the inverter/charge controller can operate at
    temp = site.Load_Vmax
    siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.Load_Vmax) + siteGUI.GUI_diag_cr 
    site.Load_Vmax = textread( siteGUI.GUI_Load_Vmax, 'V', 'V' )

    if( (temp <= 600) and (temp >= 75) and (site.Load_Vmax == 0) ):
        site.Load_Vmax = temp
    else:
        if( (temp != 0) or (site.Load_Vmax != 0)  ):
            if( site.Load_Vmax > 600 ):
               site.Load_Vmax = 600
            if( site.Load_Vmax < 75):
               site.Load_Vmax = 75
    # print( "fetched Vmax ", site.Load_Vmax)

def fetchLoadVmin():       # Get the max voltage the inverter/charge controller can operate at
    temp = site.Load_Vmin
    siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.Load_Vmin) + siteGUI.GUI_diag_cr 
    site.Load_Vmin = textread( siteGUI.GUI_Load_Vmin, 'V', 'V' )

    if( (temp <= 200) and (temp >= 50) and (site.Load_Vmin == 0) ):
        site.Load_Vmin = temp
    else:
        if( (temp != 0) or (site.Load_Vmax != 0)  ):
            if( site.Load_Vmin > 200 ):
               site.Load_Vmin = 200
            if( site.Load_Vmin < 50):
               site.Load_Vmin = 50
    # print( "fetched Vmax ", site.Load_Vmax)


def fetchcablelen():         # Get this site data entered.  Only called from fetchall()
    temp = site.cable_len

    if( siteGUI.GUI_meas_sys == 'Metric' ):
        site.cable_len = textread( siteGUI.GUI_cable_len, 'm', 'm' )
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        site.cable_len = textread( siteGUI.GUI_cable_len, 'ft', 'm' )

    if( (temp <= 4000) and (temp >= 2) and (site.cable_len == 0)  ):
        site.cable_len = temp
    else:
        if( (temp != 0) or (site.pipe_head != 0)  ):
            if( site.cable_len > 4000 ):
                site.cable_len = 4000
            if( site.cable_len < 2 ):
                site.cable_len = 2

       


def fetchcableefftarg():         # Get this site data entered.  Only called from fetchall()
    temp = site.cable_eff_target

    site.cable_eff_target = float(textread( siteGUI.GUI_cable_eff_target, '%', '%' )) / float(100)      # %% in key removed

    if( (temp <= 1) and (temp >= 0.5 ) and (site.cable_eff_target == 0)  ):
        site.cable_eff_target = temp
    else:
        if( (temp != 0) or (site.pipe_eff_target != 0)  ):
            if( site.cable_eff_target > 0.995):
                site.cable_eff_target = 0.99
            if( site.cable_eff_target < 0.5 ):
                site.cable_eff_target = 0.5



def fetchcablesize():         # Get this site data entered.  Only called from fetchall()
    temp = site.cable_size

    site.cable_size = float(textread( siteGUI.GUI_cable_size, 'mm^2', 'mm^2' ))

    if( (temp <= 170) and (temp >= 0.5 ) and (site.cable_size == 0)  ):
        site.cable_size = temp
    else:
        if( (temp != 0) or (site.cable_size != 0) ):
            if( site.cable_size > 170):
                site.cable_size = 170
            if( site.cable_size < 0.5):
                site.cable_size = 0.5

    
    # Check are if mm mode and round as needed
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Checking mm mode' + siteGUI.GUI_diag_cr
    if( siteGUI.GUI_cable_mm_AWG == 'mm' ):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'found mm mode' + siteGUI.GUI_diag_cr
        site.cable_size = round(site.cable_size,1)
        createAWG()
    


def fetchAWG():         # Get this site data entered.  Only called from fetchall()
    pointer = 0
    value = str('')
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Inputted cable AWG' + siteGUI.GUI_cable_size + siteGUI.GUI_diag_cr
    while( len( siteGUI.GUI_cable_AWG ) > 0 ):
        try:
            digi = str(siteGUI.GUI_cable_AWG[ pointer ])
        except:
            break
        
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'digit in input ' + digi + siteGUI.GUI_diag_cr
        if( (digi == ' ') or (digi == '.')  or (digi == 'A') ):
            pointer = pointer + 1
            break
        value = value + digi
        pointer = pointer + 1
    create_mm_4_AWG( value )



def textread( texttoread, inp_unit, calc_unit ):   # Reads in a string with input sensability checks and does unit conversion as appropiate
    restofline = ''
    pointer = 0
    value = float(0)
    prepostdot = 'pre'
    decimals = float(0.1)
    while( len(texttoread) > 0 ):
        digi = texttoread[ pointer ]
        if( digi == ' '):
            pointer = pointer + 1
            try:
                dig = texttoread[ pointer+1 ]
            except:
                break
            continue
            
        if( digi == '.' ):
            prepostdot = 'post'
            pointer = pointer + 1
            continue
        
        try:
            digit = int(digi)
        except:
            break
        
        if( prepostdot == 'pre' ):
            value = value * 10 + digit
        else:
            value = value + float(decimals * digit)
            decimals = decimals / float(10)
        
        try:
            dig = texttoread[ pointer+1 ]
        except:
            pointer = pointer + 1
            break

        pointer = pointer + 1
    
    if( pointer > 0):
        try:
            restofline = texttoread[pointer:]
        except:
            restofline = ''

    restofline = restofline.rstrip()
    # convert dictionary items gives multiplier for wanted-source unit order
        
    whichC = (calc_unit + '-' + restofline).lower()
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Conversion being used " + whichC + siteGUI.GUI_diag_cr

    
    try:
        converter = site.convert[ whichC ]
    except:
        whichC = calc_unit + '-' + inp_unit
        try:
            converter = site.convert[ whichC ]
        except:
            converter = 1

    value = value * converter
    return(value)




def reportGUI():    # Fill up diagnostics "siteGUI.GUI_diag" with info
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_initial_data " + str(siteGUI.GUI_initial_data) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_process_option " + str(siteGUI.GUI_process_option) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_meas_sys " + str(siteGUI.GUI_meas_sys) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      GUI_LHtype " + str(siteGUI.GUI_LHtype) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_avail_lps " + str(siteGUI.GUI_avail_lps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_actual_lps " + str(siteGUI.GUI_actual_lps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_pipe_head " + str(siteGUI.GUI_pipe_head) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_pipe_len " + str(siteGUI.GUI_pipe_len) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               GUI_pipe_capacity " + str(siteGUI.GUI_pipe_capacity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_pipe_dia " + str(siteGUI.GUI_pipe_dia) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      GUI_Num_LH " + str(siteGUI.GUI_Num_LH) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_LockNumLH " + str(siteGUI.GUI_LockNumLH) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               GUI_pipe_capacity " + str(siteGUI.GUI_pipe_capacity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_rpm_Opr " + str(siteGUI.GUI_LH_rpm_Opr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_LH_watts_Opr " + str(siteGUI.GUI_LH_watts_Opr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_LH_pwr_tot " + str(siteGUI.GUI_LH_pwr_tot) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_eff_target " + str(siteGUI.GUI_cable_eff_target) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_cable_len " + str(siteGUI.GUI_cable_len) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_Load_Vmax " + str(siteGUI.GUI_Load_Vmax) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_Aload_V " + str(siteGUI.GUI_Aload_V) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      GUI_load_W " + str(siteGUI.GUI_Load_pwr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_LockCable " + str(siteGUI.GUI_LockCable) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_cable_material " + str(siteGUI.GUI_cable_material) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_cable_size " + str(siteGUI.GUI_cable_size) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_cable_AWG " + str(siteGUI.GUI_cable_AWG) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_cable_mm_AWG " + str(siteGUI.GUI_cable_mm_AWG) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_cable_mm_title " + str(siteGUI.GUI_cable_mm_title) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             GUI_cable_AWG_title " + str(siteGUI.GUI_cable_AWG_title) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_mm_sld " + str(siteGUI.GUI_cable_dia_mm_sld) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_mm_str " + str(siteGUI.GUI_cable_dia_mm_str) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_in_sld " + str(siteGUI.GUI_cable_dia_in_sld) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_in_str " + str(siteGUI.GUI_cable_dia_in_str) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_cable_A " + str(siteGUI.GUI_cable_A) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_actual_cable_eff " + str(siteGUI.GUI_actual_cable_eff) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_LH_V_Opr " + str(siteGUI.GUI_LH_V_Opr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_Load_pwr " + str(siteGUI.GUI_Load_pwr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "          GUI_design_notes_hydro " + str(siteGUI.GUI_design_notes_hydro) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "           GUI_design_notes_elec " + str(siteGUI.GUI_design_notes_elec) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "         GUI_design_notes_safety " + str(siteGUI.GUI_design_notes_safety) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_revision " + str(siteGUI.GUI_revision) + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr




# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
def process_here(*args):
    site.debug = 'PROCESS HERE'
    
    siteGUI.GUI_diag = 'Before' + siteGUI.GUI_diag_cr       # The initiation of      #  siteGUI.GUI_diag = ''
    reportGUI()
    fetchall()
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'After fetch all' + siteGUI.GUI_diag_cr       # The initiation of      #  siteGUI.GUI_diag = ''
    reportGUI()

    site.alarms = []     # Clear the alarm list
    site.pipe_iterations = 0
    site.LHtype = siteGUI.GUI_LHtype
    #print ( siteGUI.GUI_process_option, siteGUI.GUI_initial_data )
    if( siteGUI.GUI_process_option == 'basicdata' ):
        siteGUI.GUI_diag = siteGUI.GUI_diag + 'Doing basic data' + siteGUI.GUI_diag_cr
        if(siteGUI.GUI_initial_data == 1):
            siteGUI.GUI_LockNumLH = 0
            siteGUI.GUI_LockCable = 0
            
            if( siteGUI.GUI_meas_sys == 'Metric'):
                siteGUI.GUI_cable_mm_AWG = 'mm'
                siteGUI.GUI_cable_mm_title = 'Cable cross section'
                siteGUI.GUI_cable_AWG_title = 'Next size up cable'
            else:
                siteGUI.GUI_cable_mm_AWG = 'AWG'
                siteGUI.GUI_cable_mm_title = 'Metric cross section'
                siteGUI.GUI_cable_AWG_title = 'Cable size'

            # print("Do basic fetch")
            fetch_LHhead()
            fetchlps()
            fetchLoadVmax()
            computeALL()
            reportAll()
            # print("Basic fetching done")

                        
            if( (siteGUI.GUI_initial_data == 1) and (site.lps != 0) and (site.LH_head != 0)and (site.Load_Vmax >= 50 )):   # Test if have enough preliminary data
                # print( " Doing initial data ")
                siteGUI.GUI_diag = siteGUI.GUI_diag + ' Have a data set!' + siteGUI.GUI_diag_cr
                site.cable_eff_target = 0.9
                siteGUI.GUI_pipeLkd = 1
                siteGUI.GUI_pipe_dia = '0.4 m'
                siteGUI.GUI_pipe_len = '20 m'

                fetchpipehead()
                fetchpenlen()
                fetchpendia()
                computeALL()
                reportAll()             # Display all results to gui and print to terminal window for diagnostics

                siteGUI.GUI_initial_data = 0
                return

            
        else:       # Else means have working data and just need to update for new head, lps or LH type
            fetchall()
            computeALL()
            reportAll()
            return
    
    
    # What to do for new pipe length
    if( siteGUI.GUI_process_option == 'pipelen'):
        fetchall()
        computeALL()
        reportAll()


    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "#########################################################################" + siteGUI.GUI_diag_cr
    # What to do when user enters a specific pipe diameter
    if(siteGUI.GUI_process_option == 'pipe_dia'):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Doing a new pipe diameter " + str(siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr
        siteGUI.GUI_PenSLkd = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "See new pipe locked " + str(siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr

    # What to do when user presses the pipe size lock or has been a new pipe size given
    if( (siteGUI.GUI_process_option == 'pipediaLk') or (siteGUI.GUI_process_option == 'pipe_dia') ):
        fetchall()
        computeALL()
        reportAll()

    # What to do when user enters a new number of LH hydros
    if( siteGUI.GUI_process_option == 'SetNumLH' ):
        siteGUI.GUI_LockNumLH = 1
        fetchall()
        computeALL()
        reportAll()

    # What to do when user clicks the lock number LH hydros
    if( siteGUI.GUI_process_option == 'SetLockNumLH' ):
        fetchall()
        # siteGUI.GUI_Num_LH is used in PowerSpout_calc() to effect result
        computeALL()
        reportAll()

    # What to do when user enters a new efficiency target for the cable
    if( siteGUI.GUI_process_option == 'SetCableEff' ):
        siteGUI.GUI_LockCable = 0
        site.cableLock = 0
        fetchall()
        computeALL()
        reportAll()

    # What to do when user enters a new cable length
    if( siteGUI.GUI_process_option == 'NewCable' ):
        fetchall()
        computeALL()
        reportAll()

    # What to do when user enters a new target load voltage
    if( siteGUI.GUI_process_option == 'NewCableV' ):
        fetchall()
        computeALL()
        reportAll()

    # What to do when user chooses a new material for the cable.
    if( siteGUI.GUI_process_option == 'NewCableMaterial' ):

        previous = site.cable_material
        fetchall()
        site.cable_size = site.cable_size * site.material[ site.cable_material ] / site.material[ previous ]

        computeALL()
        reportAll()

    # What to do when user chooses a new cable size based on sqr mm
    if( siteGUI.GUI_process_option == 'NewCablesize' ):
        siteGUI.GUI_LockCable = 1
        site.cableLock = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'New mm based cable size selected' + siteGUI.GUI_diag_cr
        siteGUI.GUI_cable_mm_title = 'Cable cross section'
        siteGUI.GUI_cable_AWG_title = 'Next size up cable'
        siteGUI.GUI_cable_mm_AWG = 'mm'
        fetchall()
        computeALL()
        reportAll()

    # What to do when user chooses a new cable size based on AWG
    if( siteGUI.GUI_process_option == 'NewCableAWG' ):
        siteGUI.GUI_LockCable = 1
        site.cableLock = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'New AWG based cable size selected' + siteGUI.GUI_diag_cr
        siteGUI.GUI_cable_mm_AWG = 'AWG'
        siteGUI.GUI_cable_mm_title = 'Metric cross section'
        siteGUI.GUI_cable_AWG_title = 'Cable size'
        fetchall()
        computeALL()
        reportAll()


    # What to do when user chooses to lock the cable size
    if( ( siteGUI.GUI_process_option == 'NewCableAWG' ) or (siteGUI.GUI_process_option == 'NewCablesize' ) or ( siteGUI.GUI_process_option == 'CableLock' )  ):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Cable size now locked/unlocked' + siteGUI.GUI_diag_cr
        fetchall()
        if( int(siteGUI.GUI_LockCable) == 0 ):
            site.cableLock = 0
            siteGUI.GUI_cable_mm_AWG = 'mm'
            computeALL()
            reportAll()
            
        if( int(siteGUI.GUI_LockCable) == 1 ):
            site.cableLock = 1
            computeALL()
            reportAll()

    siteGUI.GUI_diag = siteGUI.GUI_diag + 'After processing all' + siteGUI.GUI_diag_cr       # The initiation of      #  siteGUI.GUI_diag = ''
    reportGUI()

