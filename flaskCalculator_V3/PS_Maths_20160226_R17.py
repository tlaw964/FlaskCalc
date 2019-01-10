#!/usr/bin/python
from math import pi, log10, log, sqrt
# import os
import sys  # Needed to find out what platform are using.  sys.platform = win32 or win64? or linux2 or????


# Designed and developed by Smithies Technology Ltd
# Email andrew.smithies@paradise.net.nz



# Revision History


# R17   Removed cutdowns from automatic SD selector in favour of packing the rotor out to reduce magnetisim.
#           New suffix in SD code (0) for packers
#           Changed columns in list of suggested SD codes to now be Vo, Voc, and stators V/rpm for table in EcoInnovation workshop
#       Major replacement of SD lookup table. Removed unused parameters
#       Revised weighting factors for which SD codes to show first
#           Removed "Magic7"
#           Added in a weighting factor for packers. n = number of packers. use 1+(n*0.02)^2
#           Added in a weighting factor for optimal fitness. There is a max efficiency point which gives a 1
#               As power per finger approaches max weighting increases by 2 using square law
#               As power per finger reduces max weighting factor increases to 2 at 50% W/finger, then to 5 at 0% W/finger
#
#       A new alarm for high current per LHpowerspout. Was just a over 32A warning
#           Over 32A requires "high current upgrade needed",
#           If turbine amp >50 then print "current too high, lift your load voltage and reduce input flow to keep under 50 amp load current"


# R16   Requested change to increase max jet diameter for TRG from 20 to 25mm

# R15   Bug found in SD code generator added in version R09. Cutdowns codes where given when the loading operating point was for
#       more than the cutdown number of fingersets. Would result in designs where the cutdown was unable to load the
#       pelton wheel properly

# R14   Added a performance drop off to TRG results for less than 8 lps flow rates. See use of new dictionary site.lpseff
#       Prevents showing HP stator options when user has not selected an HP product
#       Added support for new rewound versions of smart drives
#       Added a preference dictionary so particular SD versions are put to the top of the list
#       Added a limiter to only show the top 10 SD options
#       Cutdown stators are not suggested for TRG turbines
#       Only 42 finger, 14 finger set stators (ie 100, 80 and 60 series) are considered for cutdowns
#       Cable loss defaults to 5% loss for basicdata
#       PLT and TRG and HP versions default to 80V at startup with basicdata
#       SD codes now have a dash in them. ie 2S-7P
#       When you select a PS type the number jets is updated. If a TRG then selects 4 jets, else 2 jets. Requires caller to now use "PSchange" function request


# R13   Added in table info in electrical user notes so users understand what to enter
#       into their inverter/charge controller

# R12   Added in a 1V drop for rectifier losses by ratio-ing down cable amps. See lines 814-817 and at 1015 See allowance setting at line 194
#       Wording change to alarm number 53 for PLT and TRG option.
#       And updated alarm 53 to not use the < symbol as trips up the web page html display
#       Fixed lack of HP turbine results. water watts used vaule now set correctly in 2057-2061 and 2086-2091 like in 2117-2120

# R11   Changes to simplify PLT versions and add in TRG
#       New PLT, PLT HP, TRG and TRG HP default to 56V load voltage and max turbine voltage of 400
#       Jet diameter calculation now increases jet area by 1/0.83 to account for discharge coefficient
#       Change runaway rpm limit to 3000 rpm for warning and updated text message
#       Changed no load voltage warning to better reflect ELV rules
#       Changed number of nozzles to suit when a TRG is selected

# R10   Minor tweaks

# R09   Min cable length reduced from 10 down to 2m
#       Static head now allowed to be up to 160m from 130m
#       Operating head now ok at 130m before warning is given to user. Up from 100m
#       Updated/New design voltage targets for new turbines. ('BE':-none-, 'ME100':90, 'ME120':105, 'ME140':125, 'ME250':230, 'GE400':350)
#         and max operating voltages to { 'BE': 400, 'ME100': 96, 'ME120': 115, 'ME140': 135, 'ME250': 240, 'GE400': 380 }
#       Introduced ' HP' as a suffix to above types to designate a HP rotor. Premium price unit and 0.9W/rpm on the test bench and 0.77W/rpm for Std. non DC
#         Std product have been computed at 1.42 UWW/rpm  (Used Water Watt)
#         Max effeciency is 54% by this calculator. At 0.77W/rpm output is 1.4259 UWW/rpm.  At 0.9W/rpm output is 1.6666UWW/rpm.
#         So use 1.42 and 1.65 for Std and HP versions. This causes number of PS required to update correctly.
#       Changed safety warnings codes 81 82 to refer to ME series powerspout
#       Changed safety warnings code 51 to not refer to the HE powerspout
#       Add cfs.  28.316846592 lps for 1 cfs
#       Added code to determine SD stator code
#       Reduced min penstock length to be just 3m
#       Added recognition of system environment. If on Linux then adds html codes to string results to tabultae SD codes in monospace font and also to
#         add a single non printing space character to the end of the warning fields to mask a web host issue with not accepting a blank string and displaying
#         a previous value instead
#       Added SD code generator


# R08   Removed case sensitivity for units

# R07   Added units psi and kpa for entering water head.

# R06   Correction to unit conversion. US gpm and not Imperial English gpm

# R05   Change to number of PowerSpouts recomended to be limited to a maximum of 10

# R04   Minor update to the unit conversion dictionary. Inclution of th.
#       Updates and corrections to error messages
#       Fixup so can include AWG in the AWG cable size entry box.

# R03   More fixings for web site implementation. Changing to a ME, GE is required to cause a resetting of the design load voltage. Removed
#       the persitency requirement that was needed beforehand to make this work.
#       site.PStype = siteGUI.GUI_PStype assertion in process_here() fixed wrongful calculation of min cable size when changing PS type or water

# R02   Fixings for web site implementation. Removal of all terminal output and redirected to a new varible siteGUI.diag for reporting back to caller
#       Assertion of float for where plain integers are divided etc.   1/3  become float91/3) etc!!! for  PY2.4 compatability

# R01   First release for the web site. Has new lookup table for PS efficiency curve

# Pa05  Updated bulk resistance for copper, aluminium and steel
#       Corrected jet sizing limits for determining how many PS to use at low heads
#       Reduced min acceptable head down to 3m

# Pa05  Jet size calc fix attempt and pipe calcs use available lps not fixed 100 as upper limit to prevent over lps reporting for used lps!
#       Change cable warning to show if within 50% of cable rating, not 20% as before

# Pa04  Introduced alarm report of how variable steel is for resistance
#       Fixed use of int to include round function for display of results. Caused calculation itterations to reduce input values!
#               Cable length, penstock diameter, penstock length
#       Reduced W/rpm for SD from 0.65 to 0.6
#       Introduced use of dictionary to hold material resistances
#       Introduced alarm codes in a list so each alarm report is shown only once.
#       Changing PS type now updates load voltages if select ME, GE or HE type.
#       Changing cable type maintains same wire loss by selecting new cable size

# Pa3   Voltage limits now stored in a dictionary
#       Seperated out itterator counters so can see which iterator gets lost
#       Correction to penstock size slope cal for newton R approximation
#       Major rewrite of electrical wire loss to reduce water flow when cable limits power transfer. Applies to ME, GE and HE.

# Pa2   Introduced units into inputs using strings and conversion values
#       Alarm reporting for GUI as simple concatenated string. (Ended up with multiple reporting sometimes.)

# Pa1   First maths library version that uses a seperate GUI caller


# These varibles are to keep track of instalation parameters. All are in SI

class siteGUI:  # User input or Report or both?        Description
    GUI_initial_data = int(1)  # Once turns a 0 then unlock rest of inputs
    GUI_process_option = str(
        'basicdata')  # U   Contents is one of.... 'basicdata' 'penstock' 'penstockeff' 'pendiaLk' 'pendia' 'SetLkNumPSandJ' 'SetNumPSandJ' 'SetCableEff'  'NewCable' 'NewCableV' 'NewCableMaterial' 'NewCablesize' 'NewCableAWG'  'NewCablesize' 'CableLock'
    GUI_meas_sys = str('Metric')  # U   Units system to use  'Metric' or Imperial'
    GUI_PStype = str('BE')  # U   'BE' 'ME100' 'ME120' 'ME140' 'ME250' 'GE400'
    GUI_avail_Wflow = str('')  # U   either lps or gpm float.  eg '12 lps'  or '23 gpm'
    GUI_Wflow = str('')  # R   either lps or gpm float.  eg '12 lps'  or '23 gpm'
    GUI_penstock_head = str('')  # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_eff_head = str('')  # R   This is the actual head at the turbine with water flow   eg '34 m' or '100 ft'
    GUI_penstock_len = str('')  # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_penstock_eff_target = str('')  # U   a string of int %.  eg '89 %'
    GUI_penstock_dia = str('')  # UR  either mm or inch float  eg '34 mm' or '1.2 in'
    GUI_PenSLkd = int(0)  # UR  A 0 or a 1. if 1 then penstock size is locked
    GUI_Num_PS = int(1)  # UR  Number of turbines. Ranges from 1 to 10
    GUI_turbine_nozzles = int(1)  # UR  Number of nozzles on each turbine. Either 1 or 2
    GUI_Num_PS_Lkd = int(0)  # UR  A 0 or a 1. if 1 then number of PowerSpouts and Jets is locked
    GUI_jet_dia = str('')  # R   either mm or inch float  eg '34 mm' or '1.2 in'
    GUI_actual_pipe_eff = str('')  # R   % float  eg '88 %'
    GUI_Opr_rpm = str('')  # R   eg '589 rpm'
    GUI_PS_pwr_ea = str('')  # R   eg '156 W'
    GUI_Actual_turbine_electric_pwr = str('')  # R   eg '2562 W'

    GUI_cable_eff_target = str('')  # U   a string of int %.  eg '89 %'
    GUI_cable_len = str('')  # UR  either metres or feet float  eg '34 m' or '100 ft'
    GUI_Dload_V = str('')  # UR  a united int string eg '56 V'
    GUI_Aload_V = str('')  # R   a united int string eg '56 V'

    GUI_LockCable = int(0)  # UR  A 0 or a 1. if 1 then cable size is locked
    GUI_cable_material = str('')  # U   'Copper', 'Aluminium' or 'Steel'
    GUI_cable_size = str('')  # UR  A 3 decimal place number or sqr mm  eg '2.256'
    GUI_cable_AWG = str('')  # UR  AWG.  eg '0000' '0'  '13'
    GUI_cable_mm_AWG = str('mm')  # Just needs to be set for maths routine to know if are in mm or AWG mode

    GUI_cable_mm_title = str('')  # R   Title for cables sqr mm size
    GUI_cable_AWG_title = str('')  # R   Title for cables AWG size
    GUI_cable_dia_mm_sld = str('')  # R   eg '2.23 mm'
    GUI_cable_dia_mm_str = str('')  # R   eg '2.23 mm'
    GUI_cable_dia_in_sld = str('')  # R   eg '0.213 in'
    GUI_cable_dia_in_str = str('')  # R   eg '0.213 in'

    GUI_cable_amps = str('')  # R   eg '34.3 A'
    GUI_actual_cable_eff = str('')  # R   eg '87 %'
    GUI_cable_Vgen = str('')  # R   eg '115 V'
    GUI_Load_pwr = str('')  # R   eg '895 W'

    GUI_design_notes_hydro = str('')  # An empty string for design comments for the end user to read and understand
    GUI_design_notes_elec = str('')  # An empty string for design comments for the end user to read and understand
    GUI_design_notes_safety = str('')  # An empty string for design comments for the end user to read and understand

    GUI_revision = str('R17')  # Version number for this maths routine for GUI to display
    GUI_diag = str('')  # All diagn ostics go to here
    GUIcr = '<br>'  # Carriage return with a line feed character
    GUI_diag_cr = str('\r\n')  # or '<br>'   # Carriage return with a line feed character


class site:
    PStype = str('')
    avail_lps = float(0)  # litres per second
    lps = float(0)  # litres per second
    penstock_head = float(0)  # metres
    penstock_len = float(5)  # metres
    penstock_dia = float(0.08)  # metres
    penstock_eff_target = 0.90  # ratio of water power to be delivered to turbine
    penstock_material = 'DrawnTube'
    penstock_flow_roughness = 0.00015  # in cm.
    penstock_Kf = float(0)  # Head Loss = q K for piping fittings in penstock
    Kf_turbine = float(2)  # Head Loss = q K for piping fittings in turbine
    penstock_iterations = 0  # Counts number of times penstock calc done to solve penstock diameter
    penstock_max_pipe_iterations = 0
    jet_iterations = 0  # Counts number of times jet iteration done to solve jet size limit
    max_jets = 2  # Number of jets current turbine type supports
    UWW_iterations = 0  # Counts number of times WaterWatts iteration done to solve rpm watts limitation
    runaway_rpm_limit = 3000  # Max safe speed for turbine
    dis_coeff = 0.83  # Area of jet is actually smaller than area of nozzle exit.

    turbine_eff = 0.7  # Efficiency ratio for pelton turbine  Gets updated by calcs once water power is known
    SD_eff = 0.7  # Efficiency ratio for Smart Drive generator
    turbine_dia = 0.23  # Diameter for the pelton wheel in metres
    eps = 1.25e-5  # Used in pipe loss calc
    turbine_spd_jet = float(0.45)  # Speed of pelton buckets relative to jet velocity
    Num_PS = 1  # Number of turbines
    turbine_nozzles = 1  # Number of nozzles on each turbine

    One_jet_water_W_lim = 800  # Water power limit for one jet to get expected warrenteed bearing life
    One_jet_dia_lim = 0.02  # Biggest jet diameter in m that works for a turbine
    Two_jet_dia_lim = 0.025  # Biggest jet size to use in a 2 jet turbine. Only applies when very low head
    pelton_Wuse_rpm = 1.42  # Watts of water jet power required for the PS
    ideal_jet_sqr_mm = 0  # Ideal total sqr mm jet size to use for this penstock, head, lps combination
    UWWatts_per_SD = 0  # Used Water Watts per PS turbine. Used to figure out correct efficiency levels

    SDs2show = int(20)  # How many SD codes to list to user

    # This table maps out the effeciency degradation at low power levels.
    # Uses water jet power for x coordinates and y coordinates are put into SD_eff and turbine_eff
    # Software uses straight line interpolation between points and level above top point
    eff = {0: 0, 25: 30, 50: 36, 100: 40, 200: 45, 300: 47, 600: 49.5, 1000: 51, 1600: 52, 2500: 54, 3500: 53, 6000: 52}
    lpseff = {0: 100, 1000000: 100}

    rectifierVdrop = float(0)  # Voltage drop for rectifier losses
    cable_len = float(20)
    cable_voltage = float(48)
    design_cable_voltage = float(48)
    cable_eff_target = 0.90  # Proportion of electricity to be delivered to the power shed
    cable_material = 'Copper'
    cableR = 1
    cableR_req = 1
    cable_Vgen = 0

    viscosity = 1.32E-03  # kg/m-sec
    density = 999.4  # kg/m^3
    gravity = 9.81  # m/sec^2
    gpm = 448.9
    mmm_lps = 1000.00  # lps/m^3/sec
    meter = 0.3048  # m/ft
    mm = 25.4  # mm/in

    design_Chk = 0  # Flag that need to check the design with EcoInnovation
    Actual_turbine_electric_pwr = float(0)
    Load_pwr = float(0)
    jet_dia = float(0.01)
    cable_size = float(1)
    cable_gauge = float(1)
    cable_AWGn = int(0)
    cable_AWG = "0"
    cableLock = int(0)
    itteratorCount = float(0)

    initial_data = int(1)
    lastcable_mm_AWG = str('mm')
    OC_Vratio = float(3.5)  # This is the no load to load voltage ratio for a PS turbine
    PLT_OC_Vratio = float(3.5)  # This is the no load to load voltage ratio for a PLT turbine
    BE_damageV = float(400)  # Output voltage to damage a PS BE
    PLT_damageV = float(400)  # Output voltage to damage a PLT
    ELV_limit = float(120)  # ELV unregistered electrical worker limit
    alarms = []  # Empty list for alarms to be .append(  )ed to as alarm numbers. Valid entries are ints.
    # Final running of prog may give a list like   [ 2, 5, 10 ]

    # Dictionary of conversion coeffecients. Enter all units here as lower case. All indexing is done via .lower() string function
    convert = {'lps-lps': 1, 'gpm-lps': 15.87, 'lps-gpm': 0.06301, 'gpm-gpm': 1, 'm-m': 1, 'mm-m': 1000, \
               'l/min-l/min': 1, 'lps-l/min': 60, 'l/min-lps': 1 / 60, \
               'l/day-l/day': 1, 'lps-l/day': 60 * 60 * 24, 'l/day-lps': 1 / (60 * 60 * 24),
               'g/day-lps': 1 / (60 * 60 * 24 * 0.2645), \
               'ft-m': 3.28083989501312, 'in-m': 39.3700787401575, 'm-cm': 0.01, 'mm-cm': 10,
               'ft-cm': 0.0328083989501312, \
               'm-psi': 0.703, 'm-kpa': .102, 'm-bar': 10.197, \
               'in-cm': 0.393700787401575, 'm-mm': 0.001, 'mm-mm': 1, 'ft-mm': 0.00328083989501312,
               'in-mm': 0.0393700787401575, \
               'm-mile': 1609.344, 'mm-mile': 1609344, 'ft-mile': 5280, 'in-mile': 63360, 'm-ft': 0.3048,
               'mm-ft': 304.8, \
               'ft-ft': 1, 'in-ft': 12, 'm-in': 0.0254, 'mm-in': 25.4, 'ft-in': 0.0833333333333333, 'in-in': 1,
               'm-th': 0.0000254, \
               'mm-th': 0.0254, 'ft-th': 8.33333333333333E-05, 'in-th': 0.001, 'm-km': 1000, 'awg-awg': 1, \
               'lps-cfs': 28.316846592, 'cfs-lps': 0.0, '%-%': 1, \
               'lps-cumecs': 1000, 'mps-mps': 1, 'fps-mps': 3.28084 \
               }

    Vlimit = {'BE': 400, 'ME100': 96, 'ME120': 115, 'ME140': 135, 'ME250': 240, 'GE400': 380, \
              'BE HP': 400, 'ME100 HP': 96, 'ME120 HP': 115, 'ME140 HP': 135, 'ME250 HP': 240, 'GE400 HP': 380, \
              'PLT': 400, 'PLT HP': 400, 'TRG': 400, 'TRG HP': 400}  # Max operating voltages for each PS type

    material = {'Copper': 1.78e-8, 'Aluminium': 3.21e-8, 'Steel': 11.78e-8}
    # Reference ohms per metre for a block of metal for cable amp carring ability calcs at 20deg C with typical wire grade material
    # Steel is from http://www.kencove.com/fence/100_Fence+Construction_resource.php  (Electric fence info)
    PSeff = float(0)
    MaxPS = 20

    SD_types = ('100--S', '100--D', '80--S', '80--D', '60--S', '60--D', '60dc--S', '60dc--D')
    SD_types += ('100-HP-S', '100-HP-D', '80-HP-S', '80-HP-D', '60-HP-S', '60-HP-D', '60dc-HP-S', '60dc-HP-D',)
    SD_types += (
    '60R85-HP-S', '60R85-HP-D', '60R90-HP-S', '60R90-HP-D', '60R100-HP-S', '60R100-HP-D', '60R110-HP-S', '60R110-HP-D',
    '60R120-HP-S', '60R120-HP-D',)

    SD_finger_sets = {'100--S': 1.400000E+01, '100--D': 1.400000E+01, '80--S': 1.400000E+01, '80--D': 1.400000E+01,
                      '60--S': 1.400000E+01, '60--D': 1.400000E+01, '60dc--S': 1.200000E+01,
                      '60dc--D': 1.200000E+01}  # How many fingers on stator for each phase
    SD_mV4rpm4set = {'100--S': 1.900000E+01, '100--D': 1.085714E+01, '80--S': 4.992857E+01, '80--D': 2.842857E+01,
                     '60--S': 7.271429E+01, '60--D': 4.142857E+01, '60dc--S': 8.347987E+01,
                     '60dc--D': 4.755371E+01}  # Open circuit volts per rpm per finger
    Stator_mV4rpm4set = {'100--S': 1.900000E+01, '100--D': 1.085714E+01, '80--S': 4.992857E+01, '80--D': 2.842857E+01,
                         '60--S': 7.271429E+01, '60--D': 4.142857E+01, '60dc--S': 9.333333E+01,
                         '60dc--D': 5.316667E+01}  # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA = {'100--S': 0.000000E+00, '100--D': 0.000000E+00, '80--S': 0.000000E+00,
                            '80--D': 0.000000E+00, '60--S': 0.000000E+00, '60--D': 0.000000E+00,
                            '60dc--S': 0.000000E+00,
                            '60dc--D': 0.000000E+00}  # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB = {'100--S': 0.000000E+00, '100--D': 0.000000E+00, '80--S': 0.000000E+00,
                            '80--D': 0.000000E+00, '60--S': 0.000000E+00, '60--D': 0.000000E+00,
                            '60dc--S': 0.000000E+00,
                            '60dc--D': 0.000000E+00}  # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC = {'100--S': 5.357143E+01, '100--D': 5.357143E+01, '80--S': 5.357143E+01,
                            '80--D': 5.357143E+01, '60--S': 5.357143E+01, '60--D': 5.357143E+01,
                            '60dc--S': 6.250000E+01,
                            '60dc--D': 6.250000E+01}  # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking = {'100--S': 1.500000E+00, '100--D': 3.000000E+00, '80--S': 1.100000E+00, '80--D': 2.200000E+00,
                   '60--S': 1.000000E+00, '60--D': 2.000000E+00, '60dc--S': 1.200000E+00,
                   '60dc--D': 2.400000E+00}  # Rating of build effort and value of generator value to EcoInnovation

    SD_finger_sets.update(
        {'100-HP-S': 1.400000E+01, '100-HP-D': 1.400000E+01, '80-HP-S': 1.400000E+01, '80-HP-D': 1.400000E+01,
         '60-HP-S': 1.400000E+01, '60-HP-D': 1.400000E+01, '60dc-HP-S': 1.200000E+01,
         '60dc-HP-D': 1.200000E+01})  # How many fingers on stator for each phase
    SD_mV4rpm4set.update(
        {'100-HP-S': 2.124265E+01, '100-HP-D': 1.213865E+01, '80-HP-S': 5.582184E+01, '80-HP-D': 3.178411E+01,
         '60-HP-S': 8.129704E+01, '60-HP-D': 4.631855E+01, '60dc-HP-S': 9.333333E+01,
         '60dc-HP-D': 5.316667E+01})  # Open circuit volts per rpm per finger
    Stator_mV4rpm4set.update(
        {'100-HP-S': 1.900000E+01, '100-HP-D': 1.085714E+01, '80-HP-S': 4.992857E+01, '80-HP-D': 2.842857E+01,
         '60-HP-S': 7.271429E+01, '60-HP-D': 4.142857E+01, '60dc-HP-S': 9.333333E+01,
         '60dc-HP-D': 5.316667E+01})  # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA.update(
        {'100-HP-S': 0.000000E+00, '100-HP-D': 0.000000E+00, '80-HP-S': 0.000000E+00, '80-HP-D': 0.000000E+00,
         '60-HP-S': 0.000000E+00, '60-HP-D': 0.000000E+00, '60dc-HP-S': 0.000000E+00,
         '60dc-HP-D': 0.000000E+00})  # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB.update(
        {'100-HP-S': 0.000000E+00, '100-HP-D': 0.000000E+00, '80-HP-S': 0.000000E+00, '80-HP-D': 0.000000E+00,
         '60-HP-S': 0.000000E+00, '60-HP-D': 0.000000E+00, '60dc-HP-S': 0.000000E+00,
         '60dc-HP-D': 0.000000E+00})  # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC.update(
        {'100-HP-S': 7.142857E+01, '100-HP-D': 7.142857E+01, '80-HP-S': 7.142857E+01, '80-HP-D': 7.142857E+01,
         '60-HP-S': 7.142857E+01, '60-HP-D': 7.142857E+01, '60dc-HP-S': 8.333333E+01,
         '60dc-HP-D': 8.333333E+01})  # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking.update(
        {'100-HP-S': 3.000000E+00, '100-HP-D': 3.500000E+00, '80-HP-S': 3.000000E+00, '80-HP-D': 3.500000E+00,
         '60-HP-S': 3.000000E+00, '60-HP-D': 3.500000E+00, '60dc-HP-S': 1.600000E+00,
         '60dc-HP-D': 3.200000E+00})  # Rating of build effort and value of generator value to EcoInnovation

    SD_finger_sets.update(
        {'60R85-HP-S': 1.200000E+01, '60R85-HP-D': 1.200000E+01, '60R90-HP-S': 1.200000E+01, '60R90-HP-D': 1.200000E+01,
         '60R100-HP-S': 1.200000E+01, '60R100-HP-D': 1.200000E+01, '60R110-HP-S': 1.200000E+01,
         '60R110-HP-D': 1.200000E+01, '60R120-HP-S': 1.200000E+01,
         '60R120-HP-D': 1.200000E+01})  # How many fingers on stator for each phase
    SD_mV4rpm4set.update(
        {'60R85-HP-S': 4.033333E+01, '60R85-HP-D': 2.300000E+01, '60R90-HP-S': 4.316667E+01, '60R90-HP-D': 2.458333E+01,
         '60R100-HP-S': 4.791667E+01, '60R100-HP-D': 2.733333E+01, '60R110-HP-S': 5.275000E+01,
         '60R110-HP-D': 3.008333E+01, '60R120-HP-S': 5.750000E+01,
         '60R120-HP-D': 3.275000E+01})  # Open circuit volts per rpm per finger
    Stator_mV4rpm4set.update(
        {'60R85-HP-S': 4.033333E+01, '60R85-HP-D': 2.300000E+01, '60R90-HP-S': 4.316667E+01, '60R90-HP-D': 2.458333E+01,
         '60R100-HP-S': 4.791667E+01, '60R100-HP-D': 2.733333E+01, '60R110-HP-S': 5.275000E+01,
         '60R110-HP-D': 3.008333E+01, '60R120-HP-S': 5.750000E+01,
         '60R120-HP-D': 3.275000E+01})  # Stator nominal volts/fset/rpm for workshop selection use
    SD_Max_e_mW4rpm4setA.update(
        {'60R85-HP-S': 0.000000E+00, '60R85-HP-D': 0.000000E+00, '60R90-HP-S': 0.000000E+00, '60R90-HP-D': 0.000000E+00,
         '60R100-HP-S': 0.000000E+00, '60R100-HP-D': 0.000000E+00, '60R110-HP-S': 0.000000E+00,
         '60R110-HP-D': 0.000000E+00, '60R120-HP-S': 0.000000E+00,
         '60R120-HP-D': 0.000000E+00})  # Maximum milli-watts per rpm per set 3 fingers. (Sqr factor)
    SD_Max_e_mW4rpm4setB.update(
        {'60R85-HP-S': 0.000000E+00, '60R85-HP-D': 0.000000E+00, '60R90-HP-S': 0.000000E+00, '60R90-HP-D': 0.000000E+00,
         '60R100-HP-S': 0.000000E+00, '60R100-HP-D': 0.000000E+00, '60R110-HP-S': 0.000000E+00,
         '60R110-HP-D': 0.000000E+00, '60R120-HP-S': 0.000000E+00,
         '60R120-HP-D': 0.000000E+00})  # Maximum milli-watts per rpm per set 3 fingers. (Linear factor)
    SD_Max_e_mW4rpm4setC.update(
        {'60R85-HP-S': 8.333333E+01, '60R85-HP-D': 8.333333E+01, '60R90-HP-S': 8.333333E+01, '60R90-HP-D': 8.333333E+01,
         '60R100-HP-S': 8.333333E+01, '60R100-HP-D': 8.333333E+01, '60R110-HP-S': 8.333333E+01,
         '60R110-HP-D': 8.333333E+01, '60R120-HP-S': 8.333333E+01,
         '60R120-HP-D': 8.333333E+01})  # Maximum milli-watts per rpm per set 3 fingers. (Constant)
    Bld_ranking.update(
        {'60R85-HP-S': 5.000000E+00, '60R85-HP-D': 5.833333E+00, '60R90-HP-S': 5.050000E+00, '60R90-HP-D': 5.891667E+00,
         '60R100-HP-S': 5.100500E+00, '60R100-HP-D': 5.950583E+00, '60R110-HP-S': 5.151505E+00,
         '60R110-HP-D': 6.010089E+00, '60R120-HP-S': 5.203020E+00,
         '60R120-HP-D': 6.070190E+00})  # Rating of build effort and value of generator value to EcoInnovation

    magic7 = {'60R85-12-S1P-S': 0.5, '60R110-12S-1P-D': 0.5, '60R100-12-S1P-D': 0.5, '60R85-12-S1P-D': 0.5,
              '60R85-6S-2P-S': 0.5, '60R110-4S-3P-S': 0.5, '60R110-6S-2P-D': 1, \
              '60R100-3S-4P-S': 0.6, '60R90-3S-4P-S': 0.6, '60R100-4S-3P-D': 0.6, '60R100-2S-6P-S': 0.6,
              '60R90-3S-4P-D': 0.6, '60R90-2S-6P-S': 0.6}

    Sscore = {'14-1': 4, '14-2': 3, '14-3': 5, '14-4': 5, '14-5': 5, '14-6': 5, '14-7': 2, \
              '14-8': 5, '14-9': 5, '14-10': 5, '14-11': 5, '14-12': 5, '14-13': 5, '14-14': 1, \
              '12-1': 5, '12-2': 3.5, '12-3': 3, '12-4': 2.5, '12-5': 5, '12-6': 2, '12-7': 5, \
              '12-8': 5, '12-9': 5, '12-10': 5, '12-11': 5, '12-12': 1}

    Pscore = {'14-1': 1, '14-2': 2, '14-3': 5, '14-4': 5, '14-5': 5, '14-6': 5, '14-7': 3, \
              '14-8': 5, '14-9': 5, '14-10': 5, '14-11': 5, '14-12': 5, '14-13': 5, '14-14': 4, \
              '12-1': 1, '12-2': 2, '12-3': 2.5, '12-4': 3, '12-5': 5, '12-6': 3.5, '12-7': 5, \
              '12-8': 5, '12-9': 5, '12-10': 5, '12-11': 5, '12-12': 5}

    SDsearch = str('')
    SDdiffConEff = 0.80  # Conversion effeciency of SD after all non load related losses are discounted

    # This is a complex curve to relate Vo/Vl ratio called Vr to normalized output per fingerset per rpm.
    # Input power to the SD follows this curve at all given rpms
    # The table above has the mW per finger set per rpm for each SD type
    # The table above has the Vr above 1 scalar also as MPP is not always at Vr of 2

    pwr4Vr = {-5: -.0001, \
              0: 0, \
              1: 0.00001, \
              1.004341: 0.013055, \
              1.233832: 0.416688, \
              1.325629: 0.567330, \
              1.371527: 0.639718, \
              1.417425: 0.705019, \
              1.463324: 0.762368, \
              1.509222: 0.812648, \
              1.555120: 0.855258, \
              1.601018: 0.891995, \
              1.646917: 0.922566, \
              1.692815: 0.946355, \
              1.738713: 0.964218, \
              1.784611: 0.977666, \
              1.830510: 0.987121, \
              1.876408: 0.993923, \
              1.922306: 0.998037, \
              2.000000: 1.000000}

    SDcloseness = 12  # Percentage range for SD choice to match requirement.
    Aspace = ' '
    monospace_on = ''
    monospace_off = ''

    tracer = ''


def VIpacked(n):  # This equates number of packers in a ratio of Volt or Current output relative to 0 packers
    return (-0.00025224 * n * n - 0.05304074 * n + 1)


def PackersPref(n):  # This provides a multiplier for the preference rating based on the number of packers
    if n == 0: return (1)
    return (1.25)


def loadingPref(portion):  # This provides a multiplier for the preference rating based on normalised loading per finger
    # portion is the per finger load as a fraction of 1. 1 == max possible power
    if portion > 0.8:
        return ((portion - 0.8) * 1) + 1
    return ((0.8 - portion) * 1) + 1


def Vpref(SD_volt, wanted_volt):
    return (1 + abs(1 - SD_volt / wanted_volt) * 40)


def computeSDtype():
    # return

    # have site class varibles.
    # Num_PS and "site.Actual_turbine_electric_pwr = site.jetpower * site.turbine_eff * site.SD_eff"  Also site.rpm

    ShaftPwr4SD = site.jetpower * .7 / site.Num_PS  # Use a nominal efficiency for pelton wheel at all power levels.
    PeltonPwr = ShaftPwr4SD
    # Take off lost power for bearing friction
    ShaftPwr4SD = ShaftPwr4SD - 0.25 * pi * 2 * site.rpm / 60  # 0.25Nm torque to run bearing with seals etc
    # Take off lost power for windage
    ShaftPwr4SD = ShaftPwr4SD - site.rpm * site.rpm * 0.00000005 * pi * 2 * site.rpm / 60
    # ShaftPwr4SD is the mechanical power that gets used for the making of electricity. Some is lost to magnetics hysteresis loss
    # and also to copper loss.
    SDwindBearingW = PeltonPwr - ShaftPwr4SD

    if sys.platform[:5] == 'linux':
        site.monospace_on = '<span style=\'font-family:monospace;\'><span style=\'font-size:x-small;\'>'
        site.monospace_off = '</span></span></span>'
        site.Aspace = '&nbsp;'

    # Make a list of the SD versions including a finger set count that have acceptable w/rpm/fset
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.rpm) + 'rpm    at ' + str( ShaftPwr4SD ) + 'W convertable shaft power' + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr
    SD_size_list_ptr = 0
    SD_size_listA = {}
    SD_size_listB = {}
    SD_size_listC = {}
    SD_size_listD = {}
    SD_size_listE = {}
    SD_size_listF = {}
    SD_size_listG = {}

    site.SDsearch = 'Have ' + str(round(site.jetpower / site.Num_PS)) + 'W power in water jet' + siteGUI.GUI_diag_cr
    site.SDsearch = site.SDsearch + 'Making ' + str(round(PeltonPwr)) + 'W shaft power ' + siteGUI.GUI_diag_cr
    site.SDsearch = site.SDsearch + 'Losing ' + str(
        round(SDwindBearingW)) + 'W in bearings and windage' + siteGUI.GUI_diag_cr
    site.SDsearch = site.SDsearch + 'Leaving ' + str(round(ShaftPwr4SD)) + 'W of magnetic power' + siteGUI.GUI_diag_cr

    site.SDsearch = site.SDsearch + 'Searching through all SD options with enough fingers for this power level' + siteGUI.GUI_diag_cr
    for SDchk in site.SD_types:  # Iterates over { '100--S','100--D','80--S','80--D','60--S','60--D','60dc--S','60dc--D','60dc-HPS','60dc-HP-D'}
        if (not 'HP' in site.PStype) and ('HP' in SDchk):
            continue  # If user has not selected an HP product skip searching and HP rotors for suitability

        for packers in range(0, 10):  # Itterate through all the packer sizes
            # print ( "List size of ", SD_size_list_ptr, "  and SDchk is ", SDchk )
            MaxWmake = (VIpacked(packers)) * (VIpacked(packers)) \
                       * site.SD_Max_e_mW4rpm4setA[SDchk] * site.rpm ** 2.0 \
                       + site.SD_Max_e_mW4rpm4setB[SDchk] * site.rpm \
                       + site.SD_Max_e_mW4rpm4setC[
                           SDchk]  # MaxWmake = electrical watts out at MPP of this SD in mW per finger set

            MaxWuse = (VIpacked(packers)) * (VIpacked(
                packers)) * MaxWmake / site.SDdiffConEff  # The shaft power is greater cause you have the conversion efficiency loss to scale up for
            MaxWuse = (VIpacked(packers)) * (VIpacked(
                packers)) * MaxWuse + 0.005 * site.rpm ** 0.715  # / float(site.SD_finger_sets[ SDchk ]) * float(site.SD_magnetic_loss_scalar[SDchk]) / 1000 # Add mW for hysteresis drag for a finger set

            # BestWmake = (VIpacked(packers))* (VIpacked(packers))* site.SD_eff_e_mW4rpm4setA[SDchk] * site.rpm**2  +  site.SD_eff_e_mW4rpm4setB[SDchk] * site.rpm  + site.SD_eff_e_mW4rpm4setC[SDchk] # BestWuse = electrical watts out at best effeciency point of this SD in mW per finger set
            #  site.SDsearch = site.SDsearch + str(BestWmake) + 'mW e BestWmake    '+ siteGUI.GUI_diag_cr
            # BestWuse = BestWmake / site.SDdiffConEff          #  The shaft power is greater cause you have the conversion efficiency loss to scale up for
            # BestWuse = BestWuse + (VIpacked(packers))* (VIpacked(packers))* 0.005 * site.rpm ** 0.715 / float(site.SD_finger_sets[ SDchk ]) * float(site.SD_magnetic_loss_scalar[SDchk]) / 1000 # Add mW for hysteresis drag for a finger set


            minfsets = int(ShaftPwr4SD / site.rpm / MaxWuse * 1000) + 1
            maxfsets = site.SD_finger_sets[SDchk]

            if 1 > minfsets:
                minfsets = 1

            if minfsets > maxfsets:
                continue

            # site.SDsearch = site.SDsearch + str(SDchk) + ' SDchk    ' + str(BestWuse) + ' BestWuse    ' + str(MaxWuse) + ' MaxWuse    ' + str(minfsets) + ' minfsets      ' + str( maxfsets ) + ' maxfsets    '  + siteGUI.GUI_diag_cr
            for fsets in range(int(minfsets), int(
                            maxfsets + 1)):  # Iterate through possible number of finger sets to determine if within range
                for series in range(1,
                                    fsets + 1):  # Iterate through number of ok finger sets to factorize and make list of series/parallel possibilities
                    parallel = int(fsets / series)
                    if site.SD_finger_sets[
                        SDchk] != parallel * series: continue  # Only consider combinations that use all fsets!  Cutdown skipping

                    # print (SDchk, packers, site.PStype, series, parallel, site.SD_finger_sets[ SDchk ] )
                    # if( site.PStype[:3] == 'TRG' or site.PStype[:2] == 'LH' or site.SD_finger_sets[ SDchk ] != 14 ):  # TRG and LH are only sold in full versions. No cutdowns in dc or rewounds either
                    #    continue

                    # Have a factorized version of this number of finger sets. Now determine power per finger set and Vo
                    WnormPERfset = ShaftPwr4SD / fsets / site.rpm / MaxWuse * 1000  # 1000x is from MaxWuse is in mW
                    VoutNoLoad = VIpacked(packers) * series * site.SD_mV4rpm4set[
                        SDchk] * site.rpm / 1000  # Note that the table is in mV!
                    VoutNoLoadmax = VIpacked(packers) * series * site.SD_mV4rpm4set[
                        SDchk] * site.runaway_rpm / 1000  # Note that the table is in mV!
                    # print ( site.runaway_rpm, SDchk, VIpacked(packers), packers, series, site.SD_mV4rpm4set[SDchk], VoutNoLoadmax)  #################

                    # Use normalized sampled parameters in dictionary pwr4Vr[ Vr ] to determine Vr required for this power level (WnormPERfset).
                    # Samples are in Vr,Pwr samples in asscending order of Vr. Scan through and find above and below points
                    #  site.SDsearch = site.SDsearch + "     Looking for Vr for Pwr of " + str(WnormPERfset) + siteGUI.GUI_diag_cr
                    xl = 2
                    yl = 1
                    xh = 0
                    yh = 0
                    for key in site.pwr4Vr:
                        if ((site.pwr4Vr[key] > WnormPERfset) and (site.pwr4Vr[key] <= yl)):
                            xl = key
                            yl = site.pwr4Vr[key]

                        if ((site.pwr4Vr[key] < WnormPERfset) and (site.pwr4Vr[key] >= yh)):
                            xh = key
                            yh = site.pwr4Vr[key]

                    VrRequired = (WnormPERfset - yl) / (yh - yl) * (
                    xh - xl) + xl  # Straight line interpolate between Xn,Yn points
                    TargetLdV = VoutNoLoad / VrRequired

                    Vo_diag = ('      ' + str(round(VoutNoLoad, 1)) + 'V no load')
                    Vl_diag = ('    ' + str(round(TargetLdV, 1)) + 'V loaded')

                    site.SDsearch = site.SDsearch + (SDchk + '        ')[:11] \
                                    + (str(series) + 'S' + str(parallel) + 'P(' + str(int(packers)) + ')  ' + '      ')[
                                      :11] \
                                    + (str(round(VrRequired, 3)) + 'Vr         ')[:9] \
                                    + Vo_diag[len(Vo_diag) - 16:] \
                                    + Vl_diag[len(Vl_diag) - 16:] + ' at ' \
                                    + str(round(WnormPERfset * 100, 1)) + '% of MPP ' \
                                    + siteGUI.GUI_diag_cr
                    if abs(TargetLdV / site.cable_Vgen - 1.0) < (
                        site.SDcloseness / 100.0):  # Have found a SD type that is close enough. Create the SD code!
                        site.SDsearch = site.SDsearch + 'This SD selected ' + siteGUI.GUI_diag_cr
                        SD_codes = SDchk.split('-')
                        ThisSD = SD_codes[0] + '-' + str(series) + 'S' + str(parallel) + 'P' + '-' + SD_codes[
                            2] + '(' + str(int(packers)) + ')'
                        if (SD_codes[1] != ''):
                            ThisSD = ThisSD + '-' + SD_codes[1]

                        # Determine build effort rating for this SD
                        # 'ThisSD' is the code with 'series' and 'parallel' connections and operating at 'TargetLdV' load voltage and fractional possible power load of 'WnormPERfset'
                        # It also has site.SD_finger_sets[ SDchk ] possible finger sets
                        indexSscore = str(int(site.SD_finger_sets[SDchk])) + '-' + str(int(series))
                        indexPscore = str(int(site.SD_finger_sets[SDchk])) + '-' + str(int(parallel))
                        BuildChoice = round(
                            site.Bld_ranking[SDchk] * site.Sscore[indexSscore] * site.Pscore[indexPscore], 1)
                        BuildChoice = BuildChoice * PackersPref(packers) * loadingPref(WnormPERfset) * Vpref(TargetLdV,
                                                                                                             site.cable_Vgen)
                        # print (Vpref(TargetLdV, site.cable_Vgen ), TargetLdV, site.cable_Vgen )

                        # Check for magic 7. Although now removed in ver17
                        # if ThisSD in site.magic7:
                        #    BuildChoice = site.magic7[ThisSD]

                        # print( "Adding SD ", ThisSD)
                        SD_size_list_ptr = SD_size_list_ptr + 1
                        SD_size_listA[SD_size_list_ptr] = BuildChoice
                        SD_size_listB[SD_size_list_ptr] = ThisSD
                        SD_size_listC[SD_size_list_ptr] = str(int(round(TargetLdV, 0)))
                        SD_size_listD[SD_size_list_ptr] = str(int(round(VoutNoLoadmax, 0)))
                        SD_size_listE[
                            SD_size_list_ptr] = ''  # str(round(TargetLdV / ShaftRPM,3))    # Operating V/rpm for this install
                        SD_size_listF[SD_size_list_ptr] = str(
                            round(series * site.Stator_mV4rpm4set[SDchk] / 1000, 3))  # no load V/rpm for this stator
                        SD_size_listG[SD_size_list_ptr] = str(int(round(WnormPERfset * 100, 0)))

    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + 'The following are SD type code options (These are copyright of EcoInnovation and are only provisional)' + siteGUI.GUIcr
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + 'These are the most useful SD stator/rotors of the '
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + str(
        SD_size_list_ptr) + ' options found.' + siteGUI.GUIcr
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + 'Operating at ' + str(
        round(site.Actual_turbine_electric_pwr / site.Num_PS / site.rpm, 3)) + ' W/rpm' + siteGUI.GUIcr + siteGUI.GUIcr

    if site.Actual_turbine_electric_pwr / site.Num_PS / site.rpm > 0.7:
        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + 'Operating at greater than 0.7W per rpm requires the purchase ' \
                                        + 'of the high power option. Please check your order' + siteGUI.GUIcr + siteGUI.GUIcr

    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + site.monospace_on
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec \
                                    + (' SD code               ')[:20].replace(' ', site.Aspace) \
                                    + '        Vo'[-3:].replace(' ', site.Aspace) \
                                    + '       Voc'[-5:].replace(' ', site.Aspace) \
                                    + ' V/rpm    '[:6].replace(' ', site.Aspace) \
                                    + siteGUI.GUIcr

    siteGUI.GUI_diag = siteGUI.GUI_diag + str(
        SD_size_list_ptr) + ' SD stator/rotor diag options found.' + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag \
                       + ('Pref.' + '       ')[:5] \
                       + (' SD code               ')[:20] \
                       + '        Vo'[-3:] \
                       + '       Voc'[-5:] \
                       + ' V/rpm    '[:6] \
                       + '      %ld '[-6:] \
                       + siteGUI.GUI_diag_cr

    outputlines = 0
    SD_types_done = []  # stores already displayed cores as 60R100-2S-6P-S(3) and 60R100-2S-6P-S(

    # print 'SD_size_list_ptr', SD_size_list_ptr, '  outputlines', outputlines, '  site.SDs2show', site.SDs2show
    while (SD_size_list_ptr >= 1):

        Whichrating = 1E50
        Whichchoice = 0
        for indexer in SD_size_listA:
            if (SD_size_listA[indexer] < Whichrating):
                Whichchoice = indexer
                Whichrating = SD_size_listA[indexer]
        if Whichchoice == 0: break

        # print Whichchoice, round(SD_size_listA[Whichchoice],3), SD_size_listB[Whichchoice], SD_size_listC[Whichchoice], SD_size_listD[Whichchoice]

        foundthis = SD_size_listB[Whichchoice].split('(')
        if foundthis[1] == '0)' or foundthis[
            0] not in SD_types_done:  # If a rotor not packed then include in list. Or if never displayed any packed version then display it
            # if 1 == 1:  foundthis[1] == '0)' or

            if foundthis[1][:2] == '0)':  # If the SD code has no packers then remove the packers reference
                this = SD_size_listB[Whichchoice].split('(0)')
                SD_size_listB[Whichchoice] = this[0] + this[1]

            if outputlines < site.SDs2show:
                siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec \
                                                + (SD_size_listB[Whichchoice] + '                   ')[:20].replace(' ',
                                                                                                                    site.Aspace) \
                                                + ('     ' + SD_size_listC[Whichchoice] + ' ')[-4:].replace(' ',
                                                                                                            site.Aspace) \
                                                + ('      ' + SD_size_listD[Whichchoice] + ' ')[-5:].replace(' ',
                                                                                                             site.Aspace) \
                                                + (SD_size_listF[Whichchoice] + '     ')[:6].replace(' ', site.Aspace) \
                                                + siteGUI.GUIcr

            siteGUI.GUI_diag = siteGUI.GUI_diag \
                               + ('         ' + str(int(round(SD_size_listA[Whichchoice], 0))) + ' ')[-6:] \
                               + (SD_size_listB[Whichchoice] + '                   ')[:20] \
                               + ('     ' + SD_size_listC[Whichchoice] + ' ')[-4:] \
                               + ('      ' + SD_size_listD[Whichchoice] + ' ')[-5:] \
                               + (SD_size_listF[Whichchoice] + '     ')[:6] \
                               + ('     ' + SD_size_listG[Whichchoice])[-4:] \
                               + siteGUI.GUIcr
            outputlines += 1

        if foundthis[1] != '0)': SD_types_done.append(foundthis[0])
        SD_types_done.append(SD_size_listB[Whichchoice])

        del SD_size_listA[Whichchoice]
        del SD_size_listB[Whichchoice]
        del SD_size_listC[Whichchoice]
        del SD_size_listD[Whichchoice]
        del SD_size_listE[Whichchoice]
        del SD_size_listF[Whichchoice]
        del SD_size_listG[Whichchoice]

        if (
                            SD_size_listA == {} or SD_size_listB == {} or SD_size_listC == {} or SD_size_listD == {} or SD_size_listE == {}):
            break

    siteGUI.GUI_design_notes_elec.replace(' ', site.Aspace)
    siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + site.monospace_off + siteGUI.GUIcr


def penstock_hydro():  # Calc penstock water losses results in power available in water jet
    site.penstock_area = pi * (site.penstock_dia / 2) * (site.penstock_dia / 2)
    site.pipeV = site.lps / site.mmm_lps / site.penstock_area
    site.Qm = 0.5 * site.pipeV * site.pipeV / site.gravity
    site.Re = site.density * site.pipeV * site.penstock_dia / site.viscosity  # Re = ρ u dh / μ Reynolds Number for Flow in Pipe or Duct
    if site.Re < 2100:  # laminar flow
        site.Re_consider = 16 / site.Re
    else:
        site.Re_consider = -1

    if site.Re_consider == -1:
        site.x1 = -log10(site.eps / 3.7 - 4.52 / site.Re * log(7 / site.Re + site.eps / 7, 10))
    else:
        site.x1 = -1

    site.design_Chk = 0
    if (site.eps / 3.7 + 5.02 * site.x1 / site.Re) > 0:
        site.x2 = -log10(site.eps / 3.7 + 5.02 * site.x1 / site.Re)
    else:
        site.x2 = -1
        site.design_Chk = 1

    if (site.eps / 3.7 + 5.02 * site.x2 / site.Re) > 0:
        site.x3 = -log10(site.eps / 3.7 + 5.02 * site.x2 / site.Re)
    else:
        site.x3 = -1
        site.design_Chk = 1

    if (site.eps / 3.7 + 5.02 * site.x3 / site.Re) > 0:
        site.x4 = -log10(site.eps / 3.7 + 5.02 * site.x3 / site.Re)
    else:
        site.x4 = -1
        site.design_Chk = 1

    site.Moodyfff = 1.0 / (16.0 * site.x4 * site.x4)

    if site.x1 == -1:
        site.f = site.Re_consider
    else:
        site.f = site.Moodyfff

    site.dp_m = (4.0 * site.f * site.penstock_len / site.penstock_dia + site.penstock_Kf + site.Kf_turbine) * site.Qm
    site.eff_head = site.penstock_head - site.dp_m

    # print( site.lps, site.penstock_area, site.eps, site.pipeV, site.Qm, site.Re, site.Re_consider, site.x1, site.x2, site.x3, site.x4, site.Moodyfff, site.f, site.dp_m )


    site.waterpower = site.penstock_head * site.lps * site.gravity
    site.jetpower = site.eff_head / site.penstock_head * site.waterpower

    if (site.eff_head < 0):
        site.jetpower = 0
        site.Vjet = 0
        site.shaft_pwr = 0
        site.Poss_electric_pwr = 0
        site.rpm = 0
        site.Actual_turbine_electric_pwr = 0
        site.runaway_rpm = 0
        site.jet_dia = 0
        site.ideal_jet_sqr_mm = 0
        site.UWWatts_per_SD = 0

    else:
        # Figure out jet velocity for this effective head and jet square mm with jet dia
        site.Vjet = sqrt(2 * site.gravity * site.eff_head)
        site.ideal_jet_sqr_mm = site.lps / site.mmm_lps / site.Vjet
        site.jet_dia = 2 * sqrt(
            site.ideal_jet_sqr_mm / site.dis_coeff / float(site.turbine_nozzles) / float(site.Num_PS) / pi)
        site.rpm = site.turbine_spd_jet * 60 * site.Vjet / pi / site.turbine_dia
        site.runaway_rpm = 60 * site.Vjet / pi / site.turbine_dia * 0.9  # The 0.9 is the 10% speed loss due to friction etc when electrically no load.
        # print ( site.rpm, site.runaway_rpm, site.rpm / site.runaway_rpm, site.Vjet, site.turbine_dia )  ###############
        site.UWWatts_per_SD = site.rpm * site.pelton_Wuse_rpm
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Hydros     site.Vjet ' + str(site.Vjet) + '  site.ideal_jet_sqr_mm ' + str(site.ideal_jet_sqr_mm) + '  site.jet_dia '+ str(site.jet_dia) + '  site.rpm '+ str(site.rpm) + '  site.UWWatts_per_SD ' + str(site.UWWatts_per_SD) + siteGUI.GUI_diag_cr
    return ()


def Calc_Pwr_max_pipe():  # Use penstock size, avail lps and head and work out lps for max power and what the power is
    penstock_hydro()
    if (
            site.eff_head / site.penstock_head < 0.66):  # Check if are penstock constricted. If so, find lps that gives 1/3 head loss
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + ' Reducing lps to get most from penstock'  + siteGUI.GUI_diag_cr
        site.alarms.append(
            11)  # 'Less water is being used than is available as the penstock size limits maximum power.\n\tChoose a larger penstock for more power\n\n'

        # Find lps to get most power from this penstock diameter
        site.penstock_max_pipe_iterations = 0
        site.lps = site.avail_lps
        lps_holder = site.lps
        eff_1 = 0
        eff_2 = 0
        slope = 0
        move_dist = 0

        while 1:
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + ' In max pipe itterations ' + str(site.penstock_max_pipe_iterations) + '  lps ' + str(site.lps) + ' ' + str(lps_holder) + ' effs 1,2 '  + str(eff_1) + ' ' + str(eff_2) + '  slope ' + str(slope) + '  move_dist ' +str( move_dist ) + siteGUI.GUI_diag_cr
            lps_holder = site.lps
            site.penstock_max_pipe_iterations = site.penstock_max_pipe_iterations + 1
            penstock_hydro()
            eff_1 = site.eff_head / site.penstock_head
            if abs(float(eff_1 - 0.66666666666666666666)) < 0.000001:  # If are within 0.1% then are close enough
                break

            site.lps = lps_holder * 1.01

            penstock_hydro()
            if site.eff_head <= 0:
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'In no head result'+ siteGUI.GUI_diag_cr
                site.lps = site.lps / 1.25
            else:
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Have some head' + siteGUI.GUI_diag_cr
                eff_2 = site.eff_head / site.penstock_head
                slope = (eff_2 - eff_1) / 0.01
                move_dist = (0.666666666666666666 - eff_1) / slope * float(site.lps)
                site.lps = float(lps_holder + move_dist)

            if site.lps < 0.001:
                site.lps = 0.001
            if site.lps > site.avail_lps:
                site.lps = site.avail_lps

            if site.penstock_max_pipe_iterations > 100:
                site.alarms.append(
                    10)  # 'Penstock loss calculations failed.\n\tPlease email a copy of this screen to EcoInnovation'
                break

    penstock_hydro()
    return ()


def calc_penstock_size():  # Find penstock diameter for target hydraulic loss
    penstock_dia_holder = site.penstock_dia
    while 1:
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Iteration " + str(site.penstock_iterations) + "   diameter " + str(penstock_dia_holder) + siteGUI.GUI_diag_cr
        site.penstock_dia = penstock_dia_holder
        penstock_hydro()
        site.penstock_iterations = site.penstock_iterations + 1
        eff_act = site.eff_head / site.penstock_head
        if abs(eff_act - site.penstock_eff_target) < 0.0005:
            break
        loss_ratio_1 = 1 - eff_act
        site.penstock_dia = penstock_dia_holder * 1.01

        penstock_hydro()
        if site.eff_head <= 0:
            penstock_dia_holder = penstock_dia_holder * 1.25
        else:
            loss_ratio_2 = 1 - (site.eff_head / site.penstock_head)
            slope = -(loss_ratio_1 - loss_ratio_2) / 0.01
            distance = ((1 - site.penstock_eff_target) - loss_ratio_1) / slope
            penstock_dia_holder = penstock_dia_holder + distance * penstock_dia_holder

        if penstock_dia_holder < 0.001:
            penstock_dia_holder = 0.001

        if site.penstock_iterations > 200:
            site.alarms.append(
                10)  # 'Penstock loss calculations failed.\n\tPlease email a copy of this screen to EcoInnovation\n'
            break
    penstock_hydro()
    return ()


def PowerSpout_calc():  # Compute SD output power. Considers SD rpm power limit and jet size limit & reduce lps for jet/PS count if cheap skate design
    if (siteGUI.GUI_PenSLkd == 1):  # Test if penstock size is locked so therefore call
        Calc_Pwr_max_pipe()

    if (siteGUI.GUI_PenSLkd == 0):  # Test if penstock size is unlocked so therefore call
        calc_penstock_size()

    if (siteGUI.GUI_Num_PS_Lkd == 0):  # Figure if number of PS is locked ( =1) and if not then decide how many required
        Cal_PS4maxW()

    if (site.eff_head > 0):  # If no head then no calcs to be done. Should not ever happen..............
        if (site.turbine_nozzles * site.Num_PS == 1):  # Determine how much jet size is available
            avail_jet_sqr_mm2use = site.dis_coeff * (site.One_jet_dia_lim / 2) * (
            site.One_jet_dia_lim / 2) * pi  # jet size limit in square mm
        else:
            avail_jet_sqr_mm2use = site.dis_coeff * site.turbine_nozzles * site.Num_PS * (site.Two_jet_dia_lim / 2) * (
            site.Two_jet_dia_lim / 2) * pi  # jet size limit in square mm

        if (site.ideal_jet_sqr_mm > avail_jet_sqr_mm2use):  # Are jet size constrained!  Reduce lps to suit.
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "site.ideal_jet_sqr_m, avail_jet_sqr_mm2use" + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.ideal_jet_sqr_mm) + '  ' + str(avail_jet_sqr_mm2use) + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Jet size limit constrained" + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr

            if (site.turbine_nozzles < site.max_jets):  # Determine how much jet size is available
                site.alarms.append(
                    12)  # 'Less water is being used than is available as the maximum jet size is in use.\n\tUse 2 Jets per PowerSpout or more PowerSpouts for more power\n\n
            else:
                site.alarms.append(
                    13)  # 'Less water is being used than is available as the maximum jet size is in use.\n\tUse more PowerSpouts for more power\n\n

            while 1:
                lps_holder = site.lps
                site.jet_iterations = site.jet_iterations + 1
                if (siteGUI.GUI_PenSLkd == 0):  # Test if penstock size is unlocked so therefore call
                    calc_penstock_size()
                penstock_hydro()

                if site.eff_head <= 0:
                    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'In no head jet sizing result. Reducing site.lps by 12.5% from site.lps ' + str(site.lps) + siteGUI.GUI_diag_cr
                    site.lps = site.lps / 1.125
                    continue

                site.lps = lps_holder * avail_jet_sqr_mm2use / site.ideal_jet_sqr_mm  # Figure new lps by simple scaling of jet cross section ideal and actual limit(target)
                if site.lps < 0.001:
                    site.lps = 0.001
                if site.lps > site.avail_lps:
                    site.lps = site.avail_lps

                if site.jet_iterations > 100:
                    break

                # siteGUI.GUI_diag = siteGUI.GUI_diag + '\nIn jet size limit while loop ' + str(site.jet_iterations) + '  lpsB4 ' + str(lps_holder) + '  site.lps now ' + str(site.lps) + "  site.ideal_jet_sqr_mm " + str(site.ideal_jet_sqr_mm) + "  avail_jet_sqr_mm2use " + str(avail_jet_sqr_mm2use) + siteGUI.GUI_diag_cr


                if (abs(
                            site.ideal_jet_sqr_mm - avail_jet_sqr_mm2use) < 0.5):  # If are within 0.5mm^2 jet size then are close enough
                    break


                    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'At end of a jet size while looping ' + str(site.jet_iterations) + '  lpsB4 ' + str(lps_holder) + '  site.lps now , ' + str(site.lps) + '  J 1,2 ' + str(J1) + ' ' + str(J2) + '  slope ' + str(slope) + '  move_dist ' + str(move_dist) + siteGUI.GUI_diag_cr
                    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Rapid find jet site.lps = lps_holder * J1 / avail_jet_sqr_mm2use  ' + str(site.lps) + ' ' + str(lps_holder) + ' ' + str(J1) + ' ' + str(avail_jet_sqr_mm2use) + siteGUI.GUI_diag_cr

        jetlimitlps = site.lps

        if (site.Num_PS * site.UWWatts_per_SD < site.jetpower):  # Are W per rmp constrained!  Reduce lps to suit.
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Power limited by W per rpm of SD gen  Described to user as water processing ability' + siteGUI.GUI_diag_cr
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
            site.alarms.append(
                15)  # 'Less water is being used than is available as the output is limited by the amount of water each PowerSpout can use at this head.\n\t Use more PowerSpouts for more power\n\n'

            while 1:
                lps_holder = site.lps
                site.UWW_iterations = site.UWW_iterations + 1
                if (siteGUI.GUI_PenSLkd == 0):  # Test if penstock size is unlocked so therefore call
                    calc_penstock_size()
                penstock_hydro()

                if site.eff_head <= 0:
                    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'In no head UWW rpm result. Reducing site.lps by 12.5% from site.lps ' + str(site.lps) + siteGUI.GUI_diag_cr
                    site.lps = site.lps / 1.125
                    continue

                UWW = site.Num_PS * site.UWWatts_per_SD  # UWW is Used Water Watts. This is the water watts usable for this number of PowerSpouts.
                site.lps = lps_holder * UWW / site.jetpower
                if site.lps < 0.001:
                    site.lps = 0.001
                if site.lps > site.avail_lps:
                    site.lps = site.avail_lps

                if site.UWW_iterations > 100:
                    break

                # siteGUI.GUI_diag = siteGUI.GUI_diag + 'In W watts / rpm size while loop ' + str(site.UWW_iterations) + '  lpsB4 ' + str(lps_holder) + '  site.lps now ' + str(site.lps) + "  UWW " + str(UWW) + "  site.UWWatts_per_SD " + str(site.UWWatts_per_SD) + "  site.jetpower " + str(site.jetpower) + siteGUI.GUI_diag_cr

                if (
                        site.jetpower - UWW < 0.5):  # If are within 0.5W then are close enough        Idea is to match UWW usable to jet water watts
                    break

        # This is a mop up routine to recalculate the jet size for reduced water flow
        if (jetlimitlps < site.lps):  # Pick lowest lps limit of jet size or rotor speed above
            site.lps = jetlimitlps
        if (siteGUI.GUI_PenSLkd == 0):  # Test if penstock size is unlocked so therefore call
            calc_penstock_size()
        penstock_hydro()

        # Now have reduced lps for the number of PS and jets.
        site.shaft_pwr = site.eff_head * site.lps / site.mmm_lps * site.density * site.turbine_eff * site.gravity
        eff2use()  # Get efficiency for PSs

        if ((site.runaway_rpm > site.runaway_rpm_limit + 1) and (siteGUI.GUI_PStype[0:2] != 'ME') and (
            siteGUI.GUI_PStype[0:2] != 'GE')):
            site.alarms.append(17)

        # print ( site.jetpower, site.Num_PS, site.turbine_nozzles, site.One_jet_water_W_lim, site.turbine_nozzles, site.max_jets )

        if ((site.jetpower / site.Num_PS / site.turbine_nozzles > site.One_jet_water_W_lim) and (
            site.turbine_nozzles != site.max_jets)):
            site.alarms.append(18)

    return ()


def eff2use():
    # What turbine effeciency to use?
    waterPwr_p_SD = site.jetpower / site.Num_PS  # Shaft power per turbine used to figure low power eff drop
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "waterPwr_p_SD = site.jetpower / site.Num_PS " + str(waterPwr_p_SD) + ' ' + str(site.jetpower) + ' ' + str(site.Num_PS) + siteGUI.GUI_diag_cr

    # Dictionary eff{} has water power: % effeciency points in asscending order. Scan through and find above and below points
    x1 = 0
    y1 = 0
    x2 = 1000000
    y2 = 52
    for key in site.eff:
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "key is " + str(key) + ' ' + str(site.eff[key]) + siteGUI.GUI_diag_cr
        if ((float(key) > float(x1)) and (float(key) <= float(waterPwr_p_SD))):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new higher x1' + siteGUI.GUI_diag_cr
            x1 = key
            y1 = float(site.eff[key]) / 100.0
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x1,y1 is now' + str(x1) + ',' + str(y1) + siteGUI.GUI_diag_cr

        if ((float(key) < float(x2)) and (float(key) >= float(waterPwr_p_SD))):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new lower x2' + siteGUI.GUI_diag_cr
            x2 = key
            y2 = float(site.eff[key]) / 100.0
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x2,y2 is now' + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr

    # siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + '  x1,y1  x2,y2    finalizes at ' + str(x1) + ',' + str(y1)  + '    '   + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "WaterPwr/PS = " + str(waterPwr_p_SD) + "  x1 " + str(x1) + "  y1 " + str(y1) + "  x2 " + str(x2) + "  y2 " + str(y2) + siteGUI.GUI_diag_cr

    # print( waterPwr_p_SD, x1, x2, y1, y2)
    site.PSeff = (waterPwr_p_SD - x1) / (x2 - x1) * (y2 - y1) + y1  # Straight line interpolate between Xn,Yn points
    # print( site.PSeff )



    # Dictionary lpseff{} has lps: % effeciency points in asscending order. Scan through and find above and below points
    x1 = 0
    y1 = 0
    x2 = 1000000
    y2 = 100
    for key in site.lpseff:
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "key is " + str(key) + ' ' + str(site.eff[key]) + siteGUI.GUI_diag_cr
        if ((float(key) > float(x1)) and (float(key) <= float(site.lps))):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new higher x1' + siteGUI.GUI_diag_cr
            x1 = key
            y1 = float(site.lpseff[key]) / 100.0
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x1,y1 is now' + str(x1) + ',' + str(y1) + siteGUI.GUI_diag_cr

        if ((float(key) < float(x2)) and (float(key) > float(site.lps))):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      Using new lower x2' + siteGUI.GUI_diag_cr
            x2 = key
            y2 = float(site.lpseff[key]) / 100.0
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + '      x2,y2 is now' + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr

    # siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + '  x1,y1  x2,y2    finalizes at ' + str(x1) + ',' + str(y1)  + '    '   + str(x2) + ',' + str(y2) + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "WaterPwr/PS = " + str(waterPwr_p_SD) + "  x1 " + str(x1) + "  y1 " + str(y1) + "  x2 " + str(x2) + "  y2 " + str(y2) + siteGUI.GUI_diag_cr

    # print( site.lps, x1, x2, y1, y2)
    site.PSeff *= (site.lps - x1) / (x2 - x1) * (y2 - y1) + y1  # Straight line interpolate between Xn,Yn points
    # print ( site.lpseff )
    # print( site.PSeff )

    site.SD_eff = site.PSeff ** 0.5
    site.turbine_eff = site.SD_eff
    siteGUI.GUI_diag = siteGUI.GUI_diag + " Rectifier loss correction Vgen check. Vgen = " + str(
        site.cable_Vgen) + siteGUI.GUI_diag_cr
    if (site.cable_Vgen == 0):
        site.cable_Vgen = site.cable_voltage / site.cable_eff_target
        siteGUI.GUI_diag = siteGUI.GUI_diag + " Rectifier loss correction found 0V Vgen. Made Vgen = " + str(
            site.cable_Vgen) + siteGUI.GUI_diag_cr
    site.Actual_turbine_electric_pwr = site.jetpower * site.turbine_eff * site.SD_eff * site.cable_Vgen / (
    site.cable_Vgen + site.rectifierVdrop)

    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "    PS efficiency = " + str(site.PSeff) + "  component " + str(site.SD_eff) + "  PS W " + str(site.Actual_turbine_electric_pwr) + siteGUI.GUI_diag_cr
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    return ()


def Cal_PS4maxW():  # This is the routine to figure out the number of PS and jets for max output power
    if (site.eff_head <= 0):
        site.eff_head = 0
        site.Actual_turbine_electric_pwr = 0
        site.cable_A = 0
        site.Load_pwr = 0
        site.cable_Vgen = 0
        site.jetpower = 0
        site.Num_PS = 1
        site.SD_eff = 0
        if (site.PStype[:3] == 'TRG'):
            site.turbine_nozzles = 4
        if (site.PStype[:3] == 'PLT'):
            site.turbine_nozzles = 2

    else:
        # Have water power at turbine shaft. Consider how many turbines required based on water volume (jet size) and power to operating rpm ratio
        if (site.PStype[:3] == 'TRG'):
            site.turbine_nozzles = 4  # Default to 4 nozzles as is best practice

            avail_jet_sqr_mm2use_per_TRG = site.dis_coeff * site.turbine_nozzles * (site.Two_jet_dia_lim / 2) * (
            site.Two_jet_dia_lim / 2) * pi  # jet size limit in square mm

            # Figure out jet velocity for this effective head and jet square mm with jet dia
            site.Vjet = sqrt(2 * site.gravity * site.eff_head)
            site.ideal_jet_sqr_mm = site.lps / site.mmm_lps / site.Vjet
            TRGs_4_vol = int(0.9999 + site.ideal_jet_sqr_mm / avail_jet_sqr_mm2use_per_TRG)

            site.rpm = site.turbine_spd_jet * 60 * site.Vjet / (pi * site.turbine_dia)
            TRGs_4_head = int(0.9999 + site.jetpower / (site.pelton_Wuse_rpm * site.rpm))

            site.Num_PS = max(TRGs_4_vol, TRGs_4_head)



        else:  # must be a PLT or older BE, ME, GE variant. Consider how many turbines required based on water watts and operating rpm
            if (siteGUI.GUI_Num_PS_Lkd == 0):
                site.Num_PS = int(
                    site.jetpower / site.rpm / site.pelton_Wuse_rpm) + 1  # Can use only ~1.42W/rpm so need many turbines for much water

            if (site.jetpower / site.Num_PS > site.One_jet_water_W_lim):
                site.turbine_nozzles = 2

            if (site.jet_dia > site.One_jet_dia_lim):
                site.turbine_nozzles = 2

            # Also check jet size as need to not exceed max jet size limit. Applies to very low head installs
            jetlimitednum = int(
                site.ideal_jet_sqr_mm / ((site.Two_jet_dia_lim / 2) * (site.Two_jet_dia_lim / 2) * pi * 2) + 1)

            if (jetlimitednum > site.Num_PS):
                site.Num_PS = jetlimitednum
                site.turbine_nozzles = 2

            if (site.Num_PS > site.MaxPS):
                site.Num_PS = site.MaxPS
            if (site.Num_PS < 1):
                site.Num_PS = 1

    return ()


def calc_penstock_material():  # Convert penstock material into a roughness factor
    if site.penstock_material == 'DrawnTube':
        site.penstock_flow_roughness = 0.00015  # in cm.
    if site.penstock_material == 'GeneralSteel':
        site.penstock_flow_roughness = 0.00457  # in cm.
    if site.penstock_material == 'AsphaltedIron':
        site.penstock_flow_roughness = 0.01219  # in cm.
    if site.penstock_material == 'GalvSteel':
        site.penstock_flow_roughness = 0.01524  # in cm.
    if site.penstock_material == 'CastSteel':
        site.penstock_flow_roughness = 0.02540  # in cm.
    if site.penstock_material == 'Wood':
        site.penstock_flow_roughness = 0.09  # in cm.
    if site.penstock_material == 'Concrete':
        site.penstock_flow_roughness = 0.9  # in cm.
    if site.penstock_material == 'RivetedSteel':
        site.penstock_flow_roughness = 0.9  # in cm.

    # DrawnTube       0.00015         Drawn tubing (PVC, HTPE (poly), brass, etc.)
    #   GeneralSteel    0.00457         Commercial steel or wrought iron
    #   AsphaltedIron   0.01219         Asphalted cast iron
    #   GalvSteel       0.01524         Galvanized iron
    #   CastSteel       0.02540	        Cast iron
    #   Wood            0.018-0.09      Wood stave
    #   Concrete        0.03-0.3        Concrete
    #   RivetedSteel    0.09-0.9        Riveted steel

    return ()


def CalcCable(
        *args):  # Calculate the cable loss. Includes min conductor size for amps check and adjustments to water flow if there are cable power limitations
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Entering CalcCable' + siteGUI.GUI_diag_cr
    if (site.eff_head <= 0):
        site.cable_voltage = 0
        site.cable_A = 0
        site.Actual_turbine_electric_pwr = 0.001
        site.Load_pwr = 0
        site.cable_Vgen = 0
    else:
        site.amplimCount = 0

        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "And the cable lock is..... " + str(site.cableLock) + '   HTTP.PY says ' + str(siteGUI.GUI_LockCable) + siteGUI.GUI_diag_cr
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "And the cable size is..... " + str(site.cable_size) + siteGUI.GUI_diag_cr

        if (int(site.cableLock) == int(
                0)):  # If no user lock on cable size then go pick a cable size for the target cable loss
            calc_cable_size()

        # siteGUI.GUI_diag = siteGUI.GUI_diag + "And the cable size is..... " + str(site.cable_size) + siteGUI.GUI_diag_cr

        calc_wire_loss()  # Find loss in the current given cable size. Increases Vgen to use the PS output W. Gives resultant load watts. Ignores over volts

        if (((siteGUI.GUI_PStype[0:2] == 'ME') or (siteGUI.GUI_PStype[0:2] == 'GE')) and (
            site.cable_Vgen > site.Vlimit[siteGUI.GUI_PStype])):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Working out operating voltages for GE and ME types..... " + siteGUI.GUI_diag_cr
            VClampVOadj()
            if (site.cable_voltage < (
                site.Vlimit[siteGUI.GUI_PStype] / 2)):  # Check if are cable limited for power transfer
                #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Doing cable power transfer limited water flow reduction for GE and ME types..... " + siteGUI.GUI_diag_cr
                cable_limitedPwr()  # As cable limited then need to reduce water flow to match transferrable power

        if ((siteGUI.GUI_PStype[0:2] == 'BE') and (site.cable_Vgen > site.Vlimit[siteGUI.GUI_PStype])):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Doing V gen max voltage limited water flow reduction for BE types..... " + siteGUI.GUI_diag_cr
            cable_limitedPwr()  # As cable limited then need to reduce water flow to match transferrable power

        site.cable_amp_spec = cable_amps_rate(site.cable_size)

        if (site.cable_amp_spec / site.cable_A < 1.5):
            site.alarms.append(
                54)  # Cable size within 50% of likely current rating. Please check with your cable supplier for suitability. Amps temp rise etc

        if (site.cable_amp_spec < site.cable_A):
            #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Need a bigger cable for this number of amps " + siteGUI.GUI_diag_cr
            MinCable4Amps()  # Need to choose bigger cable. Rating for this cable just " + str(site.cable_amp_spec) )

        if (site.cable_A / site.Num_PS > 50.0):
            site.alarms.append(60)  # Excess high current warning
        else:
            if (site.cable_A / site.Num_PS > 32.0):
                site.alarms.append(59)  # High current upgrade required


def VClampVOadj():  # Reduces site.cable_voltage to bring Vgen down to site.Vlimit[ siteGUI.GUI_PStype ] as needed for ME and GE units
    while (abs(site.cable_Vgen / site.Vlimit[
        siteGUI.GUI_PStype] - 1) > 0.0001):  # This walks the load voltage down for ME and GE generators
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "VCvocAdj  site.cable_voltage = " + str(site.cable_voltage) + "   " + str(site.cable_Vgen) + "   limit is=>" + str(site.Vlimit[ siteGUI.GUI_PStype ]) + "   " + str(site.cable_Vgen - site.Vlimit[ siteGUI.GUI_PStype ]) + siteGUI.GUI_diag_cr
        site.cable_voltage = site.cable_voltage - (site.cable_Vgen - site.Vlimit[siteGUI.GUI_PStype]) / 2
        calc_wire_loss()
        if (site.cable_voltage < (
            site.Vlimit[siteGUI.GUI_PStype] / 2)):  # Check if are cable limited for power transfer
            break
        site.amplimCount = site.amplimCount + 1
        if (site.amplimCount > 100):
            break


def cable_limitedPwr():  # Reduce water flow to stay under cable's power transfer limit, load voltage and max PowerSpout output voltage
    # Figure out how much power can be transferred.
    # Then figure the total PS power and reduce water flow to suit.
    # Then rerun PowerSpout() to check
    # Cable return loop resistance is in site.cableR
    # Supply voltage is in site.Vlimit[ siteGUI.GUI_PStype ]
    # Load voltage is either site.Vlimit[ siteGUI.GUI_PStype ] / 2 for GE and ME   or site.design_cable_voltage for BE

    if ((siteGUI.GUI_PStype[0:2] == 'ME') or (siteGUI.GUI_PStype[0:2] == 'GE')):
        loadvoltage = site.Vlimit[siteGUI.GUI_PStype] / 2
        site.alarms.append(
            55)  # Tell user that the water flow is reduced to prevent continious operation of over voltage protection circuitry
    else:  # Have a BE
        loadvoltage = site.design_cable_voltage
        site.alarms.append(
            56)  # Tell user that the water flow is reduced to prevent over voltage damage of the PowerSpout
    site.cable_voltage = loadvoltage
    powertarget = ((site.Vlimit[siteGUI.GUI_PStype] - loadvoltage) / site.cableR) * site.Vlimit[
        siteGUI.GUI_PStype]  # This many watts at the PowerSpout is all that can be taken.

    while (abs(site.Actual_turbine_electric_pwr - powertarget) > 1):
        site.lps = site.lps * powertarget / site.Actual_turbine_electric_pwr
        PowerSpout_calc()

    calc_wire_loss()


def calc_wire_loss():  # Find loss in given cable size. Increases Vgen to use the PS output W. Gives resultant load watts. Ignores over volts
    # Use site.cable_size, site.material[ site.cable_material ] defined from site.cable_material, and site.cable_len
    # to calculate the return trip ohms in the DC cable. Put in site.cableR
    site.cableR = float(site.material[site.cable_material] * float(1e6) / site.cable_size * site.cable_len * float(2))
    site.cable_Vgen = float((site.cable_voltage + sqrt(
        site.cable_voltage * site.cable_voltage + float(4) * site.Actual_turbine_electric_pwr * site.cableR)) / float(
        2))

    # Update turbine power to account for rectifier losses at this Vgen and then recalc Vgen for this reduced power
    site.Actual_turbine_electric_pwr = site.jetpower * site.turbine_eff * site.SD_eff * site.cable_Vgen / (
    site.cable_Vgen + site.rectifierVdrop)
    site.cable_Vgen = float((site.cable_voltage + sqrt(
        site.cable_voltage * site.cable_voltage + float(4) * site.Actual_turbine_electric_pwr * site.cableR)) / float(
        2))

    site.cable_Vdrop = site.cable_Vgen - site.cable_voltage
    site.cable_A = site.cable_Vdrop / site.cableR
    site.Load_pwr = float(site.cable_A * site.cable_voltage)


def calc_cable_size():  # Find cable size for given cable effeciency
    # Using electric power data. Use these to compute cable size for this site for target power loss.
    # Have source power level in                site.Actual_turbine_electric_pwr
    # Have target operating load voltage in     site.design_cable_voltage
    # Have operating load voltage in            site.cable_voltage
    # Have cable length in                      site.cable_len
    # Have target cable effeciency in           site.cable_eff_target
    # Have cable material in                    site.cable_material.   Either Copper, Aluminium or Steel
    # Cable material ohm/m/m                    site.material[ site.cable_material ]
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Arrived at calc_cable_size ' + str(site.cable_size)
    site.Load_pwr = site.cable_eff_target * site.Actual_turbine_electric_pwr  # Power to load
    site.cable_A = site.Load_pwr / (
    site.rectifierVdrop + site.cable_voltage) * site.cable_eff_target  # amps in cable.  Note the 1V rectifier loss allowance in last term
    site.cable_Vdrop = site.cable_voltage / (
    1 / (1 - site.cable_eff_target))  # total volts lost accross cable in both directions
    site.cableR_req = site.cable_Vdrop / site.cable_A / site.cable_len / 2  # Cable resistance in ohm/m for each direction
    site.cable_size = site.material[site.cable_material] * 1e6 / site.cableR_req  # Sqr mm needed
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + '    ....Leaving calc_cable_size ' + str(site.cable_size) + siteGUI.GUI_diag_cr
    createAWG()


def cable_amps_rate(smm):  # Convert cable square mm into a nominal amps rating
    site.itteratorCount = site.itteratorCount + 1
    amp_limit1 = smm * 10
    amp_limit2 = smm * 10 * pow(smm, 0.74)
    if (amp_limit1 > amp_limit2):
        return (amp_limit2)
    else:
        return (amp_limit1)


def MinCable4Amps():  # Choose cable based on amps carrying ability. Rating for this cable just " + str(site.cable_amp_spec) )
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Choosing min cable size for this number of amps.  Was " + str(site.cable_size) + ' and now is '
    while (1):
        temp_holder = site.cable_size
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.cable_size) + siteGUI.GUI_diag_cr
        site.cable_size = cable_smm4amps(site.cable_A)
        if (abs(temp_holder / site.cable_size - 1) < 0.001):
            break

    # siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.cable_size) + siteGUI.GUI_diag_cr
    createAWG()


def cable_smm4amps(amps):  # Determine sqr mm cable needed for given current
    smm = 2
    amps_rating = cable_amps_rate(smm)
    while (1):
        site.itteratorCount = site.itteratorCount + 1
        smm_slope = cable_amps_rate(smm + 0.01) - amps_rating
        smm = smm + (amps - amps_rating) / smm_slope / float(100)
        amps_rating = cable_amps_rate(smm)
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "amps " + str(amps) + "  Sqr mm" + str(smm) + " & rating" + str(amps_rating) + "    at slope of " +str(smm_slope) + siteGUI.GUI_diag_cr
        if (abs(amps_rating / amps - 1) < 0.001):
            break
    return (smm)


def createAWG():  # Convert sqr mm into next size up AWG
    cable_gauge_tmp = -39 * log(2 * sqrt(site.cable_size * 0.99 / pi) / 0.127, 92) + 36
    if cable_gauge_tmp < 0:
        cable_gauge_tmp = -int(cable_gauge_tmp - 1)
        string = ""
        site.cable_gauge = string.zfill(cable_gauge_tmp + 1)
    else:
        site.cable_gauge = str(int(cable_gauge_tmp))


def create_mm_4_AWG(AWG):  # Convert AWG into sqr mm
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Arrived at create_mm_4_AWG ' + str(site.cable_size) + siteGUI.GUI_diag_cr
    temp = AWG
    temp2 = site.cable_size
    try:
        if (eval(AWG) == 0):
            site.cable_AWGn = -AWG.count("0") + 1
        else:
            site.cable_AWGn = eval(AWG)

        if (site.cable_AWGn > 20):
            site.cable_AWGn = 20
        if (site.cable_AWGn < -6):
            site.cable_AWGn = -6

        # siteGUI.GUI_diag = siteGUI.GUI_diag + str(pi * pow(0.127/2 * pow(92, (36-site.cable_AWGn) / 39 ) ,2)) + siteGUI.GUI_diag_cr
        site.cable_size = pi * pow(float(0.127 / 2) * pow(92, float(36 - site.cable_AWGn) / 39), 2)
    except:
        AWG = temp
        site.cable_size = temp2

    # siteGUI.GUI_diag = siteGUI.GUI_diag + '   Leaving create_mm_4_AWG ' + str(site.cable_size) + siteGUI.GUI_diag_cr
    return ()  # Result is an updated site.cable_size


def reportAll():  # Report all results to user gui. This is the only place where gui values get updated for the user to see
    # Check are if AWG mode and round up as needed
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "And the cable is AWG or mm ..... " + siteGUI.GUI_cable_mm_AWG + siteGUI.GUI_diag_cr
    if (siteGUI.GUI_cable_mm_AWG == 'AWG'):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "A....Yep. Detected AWG mode..... " + siteGUI.GUI_diag_cr
        createAWG()
        create_mm_4_AWG(site.cable_gauge)
        CalcCable()  # And redo loss calculation with mm^2 based on AWG

        site.lastcable_mm_AWG = 'AWG'

    # Check are if mm mode and round as needed
    if (siteGUI.GUI_cable_mm_AWG == 'mm'):
        if (site.lastcable_mm_AWG == 'AWG' and site.cable_size * 10 > int(
                    site.cable_size * 10)):  # Round up if above a whole number
            site.cable_size = round(site.cable_size, 1)
        if (site.lastcable_mm_AWG == 'mm'):  # Round up if above a whole number
            site.cable_size = round(site.cable_size, 1)

        CalcCable()  # And redo loss calculation with rounded mm^2
        createAWG()

        site.lastcable_mm_AWG = 'mm'

    if ((siteGUI.GUI_PStype[0:2] == 'BE') and (site.cable_Vgen * site.OC_Vratio > site.BE_damageV) and (
            site.Load_pwr / site.Actual_turbine_electric_pwr < 0.5)):  # Open circuit damage risk on BE at low cable efficiency
        site.alarms.append(51)
    else:
        if ((siteGUI.GUI_PStype[0:2] == 'BE') and (
                site.cable_Vgen * site.OC_Vratio > site.BE_damageV)):  # Open circuit damage risk on BE
            site.alarms.append(52)

    if ((siteGUI.GUI_PStype[0:3] == 'PLT') and (site.cable_Vgen * site.PLT_OC_Vratio > site.PLT_damageV)):
        site.alarms.append(53)

    if ((siteGUI.GUI_PStype[0:2] == 'BE') and (site.cable_Vgen > site.ELV_limit)):
        site.alarms.append(81)

    if ((siteGUI.GUI_PStype[0:2] == 'BE') and (site.cable_Vgen * site.OC_Vratio > site.ELV_limit)):
        site.alarms.append(82)

    if (site.cable_material == 'Steel'):
        site.alarms.append(58)

    if (site.PStype[:3] == 'TRG'):
        if (site.eff_head > 30):
            site.alarms.append(19)
    else:
        if (site.eff_head > 130):
            site.alarms.append(19)

    put_lps()
    put_lpsused()
    put_head()
    put_OprHead()
    put_PenLen()
    put_PenEffTarget()
    put_PenDia()
    put_Num_PS()
    put_JetDia()
    put_ActPenEff()
    put_OprRPM()
    put_eaPS_W()
    put_allPS_W()
    put_cableEff_targ()
    put_CableLen()
    put_DesLdV()
    put_ActLdV()
    put_CableSize()
    put_CableAWG()
    put_CableDetails()

    if (site.PStype[:3] == 'TRG') and (site.lps < 8):
        site.alarms.append(14)

    # Create alarm string for hydro issues
    # example of list is.....     alarms = [ 10, 12, 20]
    if (site.PStype[:3] == 'TRG' or site.PStype[
                                    :3] == 'PLT'):  # These are the current alarms as defined for the current TRG and PLT PowerSpouts
        siteGUI.GUI_design_notes_hydro = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(10, 19 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 10): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Penstock loss calculations failed.' + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 11): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the pipe size limits maximum power.' \
                                                                     + siteGUI.GUIcr + 'Choose a larger pipe for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (site.PStype[:3] == 'TRG'):
                        if (alm == 12): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Less water is being used than is available as the maximum jet size is in use.' \
                                                                         + siteGUI.GUIcr + 'Use more \'jets per PowerSpout\' or more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr
                    else:
                        if (alm == 12): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Less water is being used than is available as the maximum jet size is in use.' \
                                                                         + siteGUI.GUIcr + 'Use 2 \'jets per PowerSpout\' or more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 13): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the maximum jet size is in use.' \
                                                                     + siteGUI.GUIcr + 'Use more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 14): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'PLT turbine should be used for lower flow sites' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 15): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the output is limited by the amount of water each PowerSpout can use at this operating head.' \
                                                                     + siteGUI.GUIcr + 'Use more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 17): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'No load speed is ' + str(int(
                        site.runaway_rpm)) + 'rpm!!!  Contact your supplier (and read the manual) on regulation methods that can be ' \
                                                                     + 'employed to prevent turbine runaway.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (site.PStype[:3] == 'TRG'):
                        if (alm == 18): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Too much power for reliable, warrantable operation without more jets in use. Note: All TRGs are sold with 4 jets fitted!' \
                                                                         + siteGUI.GUIcr + 'Please select more jets per PowerSpout, or more PowerSpouts, or reduce water flow and/or head, or buy additional replacement bearings.' + siteGUI.GUIcr + siteGUI.GUIcr
                    else:
                        if (alm == 18): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Too much power for reliable, warrantable single jet operation.    Note: All PLTs are sold with 2 jets fitted!' \
                                                                         + siteGUI.GUIcr + 'Please select 2 jets per PowerSpout, or more PowerSpouts, or reduce water flow and/or head, or buy additional replacement bearings.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (site.PStype[:3] == 'TRG'):
                        if (alm == 19): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Too much water pressure for reliable, warrantable operation. 30m (98ft) is the maximum operating head.' \
                                                                         + siteGUI.GUIcr + 'Use a smaller penstock size to reduce the operating head. Smaller pipe is also cheaper.' + siteGUI.GUIcr + siteGUI.GUIcr
                    else:
                        if (alm == 19): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                         'Too much water pressure for reliable, warrantable operation. 130m (427ft) is the maximum operating head.' \
                                                                         + siteGUI.GUIcr + 'Use a smaller penstock size to reduce the operating head. Smaller pipe is also cheaper.' + siteGUI.GUIcr + siteGUI.GUIcr

                    break
        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr

        siteGUI.GUI_design_notes_elec = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(51, 60 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 51): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Operation of PowerSpout on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio)) + \
                                                                    'V at the terminals and risks internal unwarrantable damage.' \
                                                                    + siteGUI.GUIcr + 'Reducing cable loss may avoid this risk, or select either a ME, GE PowerSpout, or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 52): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Operation of PowerSpout on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio)) + \
                                                                    'V at the terminals and risks internal unwarrantable damage.' \
                                                                    + siteGUI.GUIcr + 'Please ensure your site never operates without load. Or has a protection device fitted.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 53): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Operation of PowerSpout PLT on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio)) + \
                                                                    'V at the terminals and exceeds the Extra Low Voltage (ELV) limits for non electrical workers to maintain. ' \
                                                                    + siteGUI.GUIcr + 'In Australasia the ELV limit is 120 VDC, in most other parts of the world the ELV limit is 75 VDC. Hire a registered ' + \
                                                                    'electrical worker if your system is not ELV and ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 54): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Cable size is within 50% of likely current rating. Cable loss calculations are based on 20 deg C (68 deg F) conductor temperature.' \
                                                                    + siteGUI.GUIcr + 'Please check with your cable supplier for suitability for current handling, temperature rise and loss at this current.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 55): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Water flow reduced to prevent continuous operation of over voltage protection circuitry.' \
                                                                    + siteGUI.GUIcr + 'Either use a larger cable, or a shorter cable or accept less power' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 56): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Water flow reduced to prevent over voltage damage to PowerSpout.' \
                                                                    + siteGUI.GUIcr + 'Either use a larger cable, a shorter cable or accept less power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 57): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Minimum cable size for amps is in use.   Rating for this cable just ' + str(
                        round(site.cable_amp_spec, 1)) + ' A' + siteGUI.GUIcr + siteGUI.GUIcr  # Not used. See line 563

                    if (alm == 58): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Steel wire is not all created equal and can have a wide range of loss. Calculations are based on common high tensile steel.' \
                                                                    + siteGUI.GUIcr + 'Please check wih your supplier for the actual resistance of your wire' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 59): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Turbine amps are ' + str(
                        round(site.cable_A / site.Num_PS, 1)) + \
                                                                    'A, this exceeds the standard current rating of 32 amps. An upgrade to 50 amps rating is available for an extra charge. ' \
                                                                    + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 60): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Turbine amps are ' + str(
                        round(site.cable_A / site.Num_PS, 1)) + \
                                                                    'A, Turbines >50 amp are not permitted. Lift your load voltage and reduce input flow to keep under 50 amp load current.' \
                                                                    + siteGUI.GUIcr + siteGUI.GUIcr
                    break
        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr

        siteGUI.GUI_design_notes_safety = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(81, 82 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 81): siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + \
                                                                      'Operation of PowerSpout on this site under load will result in ' + str(
                        int(site.cable_Vgen + 0.5)) + \
                                                                      'V at the terminals and exceeds the Extra Low Voltage limits for non electrical workers to maintain.' \
                                                                      + siteGUI.GUIcr + 'Please either select a ME series PowerSpout, or increase cable size, or reduce cable length to reduce terminal voltage, or hire a registered electrical worker.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 82): siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + \
                                                                      'Operation of PowerSpout BE on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio + 0.5)) + \
                                                                      'V at the terminals and exceeds the Extra Low Voltage limits for non electrical workers to maintain.' \
                                                                      + siteGUI.GUIcr + 'Please either hire a registered electrical worker, or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr
                    break

        rounds = {}
        values = {}

        values['-2a'] = site.cable_voltage * 0.8
        rounds['-2a'] = -len(str(int(values['-2a']))) + 3
        values['-2b'] = site.Load_pwr * 0.25
        rounds['-2b'] = -len(str(int(values['-2b']))) + 3

        values['-1a'] = site.cable_voltage * 0.9
        rounds['-1a'] = -len(str(int(values['-1a']))) + 3
        values['-1b'] = site.Load_pwr * 0.5
        rounds['-1b'] = -len(str(int(values['-1b']))) + 3

        values['0a'] = site.cable_voltage
        rounds['0a'] = -len(str(int(values['0a']))) + 3
        values['0b'] = site.Load_pwr
        rounds['0b'] = -len(str(int(values['0b']))) + 3

        values['+1a'] = site.cable_voltage * 1.1
        rounds['+1a'] = -len(str(int(values['+1a']))) + 3
        values['+1b'] = site.Load_pwr * 1.5
        rounds['+1b'] = -len(str(int(values['+1b']))) + 3

        values['+2a'] = site.cable_voltage * 1.2
        rounds['+2a'] = -len(str(int(values['+2a']))) + 3
        values['+2b'] = site.Load_pwr * 2
        rounds['+2b'] = -len(str(int(values['+2b']))) + 3

        for items in rounds:
            if rounds[items] > 0: rounds[items] = 0

        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                        'Table mode ( in some inverters) can be used to resolve MPPT tracking stability issues. ' + \
                                        'Below is a suggested table that will help in getting you started. ' + \
                                        'On site adjustment (by trial and error) will be needed to get the best result when using table mode. ' + \
                                        'Only Power-One, EnaSolar and Ginlong inverters have a table mode setting. ' + \
                                        'Some off grid MPPT regulators also have table modes. ' + \
                                        siteGUI.GUIcr + 'Suggested table' + siteGUI.GUIcr + \
                                        'min voltage setting, min power setting' + siteGUI.GUIcr + \
                                        str(int(round(values['-2a'], rounds['-2a']))) + ', ' + str(
            int(round(values['-2b'], rounds['-2b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['-1a'], rounds['-1a']))) + ', ' + str(
            int(round(values['-1b'], rounds['-1b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['0a'], rounds['0a']))) + ', ' + str(
            int(round(values['0b'], rounds['0b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['+1a'], rounds['+1a']))) + ', ' + str(
            int(round(values['+1b'], rounds['+1b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['+2a'], rounds['+2a']))) + ', ' + str(
            int(round(values['+2b'], rounds['+2b']))) + siteGUI.GUIcr + \
                                        'max voltage setting, max power setting' + siteGUI.GUIcr + siteGUI.GUIcr

        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr















    else:
        siteGUI.GUI_design_notes_hydro = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(10, 19 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 10): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Penstock loss calculations failed.' + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 11): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the pipe size limits maximum power.' \
                                                                     + siteGUI.GUIcr + 'Choose a larger pipe for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 12): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the maximum jet size is in use.' \
                                                                     + siteGUI.GUIcr + 'Use 2 \'jets per PowerSpout\' or more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 13): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the maximum jet size is in use.' \
                                                                     + siteGUI.GUIcr + 'Use more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 15): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Less water is being used than is available as the output is limited by the amount of water each PowerSpout can use at this operating head.' \
                                                                     + siteGUI.GUIcr + 'Use more PowerSpouts for more power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 17): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'No load speed is ' + str(
                        int(site.runaway_rpm)) + 'rpm!!!  Damage from no load over speed is not covered by warranty.' \
                                                                     + siteGUI.GUIcr + 'Please either: Select a ME or GE PowerSpout to limit no load speed to less than the required 2000rpm, ' \
                                                                                       'or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 18): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Too much power for reliable, warrantable single jet operation.    Note: All PowerSpouts are sold with 2 jets fitted!' \
                                                                     + siteGUI.GUIcr + 'Please select 2 jets per PowerSpout, or more PowerSpouts, or reduce water flow and/or head, or buy additional replacement bearings.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 19): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                                                                     'Too much water pressure for reliable, warrantable operation. 130m (427ft) is the maximum operating head.' \
                                                                     + siteGUI.GUIcr + 'Use a smaller penstock size to reduce the operating head. Smaller pipe is also cheaper.' + siteGUI.GUIcr + siteGUI.GUIcr

                    break
        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr

        siteGUI.GUI_design_notes_elec = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(51, 59 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 51): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Operation of PowerSpout BE on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio)) + \
                                                                    'V at the terminals and risks internal unwarrantable damage.' \
                                                                    + siteGUI.GUIcr + 'Reducing cable loss may avoid this risk, or select either a ME, GE PowerSpout, or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 52): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Operation of PowerSpout BE on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio)) + \
                                                                    'V at the terminals and risks internal unwarrantable damage.' \
                                                                    + siteGUI.GUIcr + 'Please select either a ME or GE PowerSpout, or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 54): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Cable size is within 50% of likely current rating. Cable loss calculations are based on 20 deg C (68 deg F) conductor temperature.' \
                                                                    + siteGUI.GUIcr + 'Please check with your cable supplier for suitability for current handling, temperature rise and loss at this current.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 55): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Water flow reduced to prevent continuous operation of over voltage protection circuitry.' \
                                                                    + siteGUI.GUIcr + 'Either use a larger cable, or a shorter cable or accept less power' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 56): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Water flow reduced to prevent over voltage damage to PowerSpout.' \
                                                                    + siteGUI.GUIcr + 'Either use a larger cable, a shorter cable or accept less power.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 57): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Minimum cable size for amps is in use.   Rating for this cable just ' + str(
                        round(site.cable_amp_spec, 1)) + ' A' + siteGUI.GUIcr + siteGUI.GUIcr  # Not used. See line 563

                    if (alm == 58): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Steel wire is not all created equal and can have a wide range of loss. Calculations are based on common high tensile steel.' \
                                                                    + siteGUI.GUIcr + 'Please check wih your supplier for the actual resistance of your wire' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 59): siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                                                    'Turbine amps are ' + str(
                        round(site.cable_A / site.Num_PS, 1)) + \
                                                                    'A, this exceeds the standard current rating of 32 amps, an upgrade to 50 amps is available for an extra charge. ' + \
                                                                    'Turbines >50 amp are not permitted.' \
                                                                    + siteGUI.GUIcr + siteGUI.GUIcr

                    break
        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr

        siteGUI.GUI_design_notes_safety = ''  # An empty string for design comments for the end user to read and understand
        for alm in range(81, 82 + 1):
            for search in site.alarms:
                if (search == alm):
                    if (alm == 81): siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + \
                                                                      'Operation of PowerSpout BE on this site under load will result in ' + str(
                        int(site.cable_Vgen + 0.5)) + \
                                                                      'V at the terminals and exceeds the Extra Low Voltage limits for non electrical workers to maintain.' \
                                                                      + siteGUI.GUIcr + 'Please either select a ME series PowerSpout, or increase cable size, or reduce cable length to reduce terminal voltage, or hire a registered electrical worker.' + siteGUI.GUIcr + siteGUI.GUIcr

                    if (alm == 82): siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + \
                                                                      'Operation of PowerSpout BE on this site with no load will result in ' + str(
                        int(site.cable_Vgen * site.OC_Vratio + 0.5)) + \
                                                                      'V at the terminals and exceeds the Extra Low Voltage limits for non electrical workers to maintain.' \
                                                                      + siteGUI.GUIcr + 'Please select either a ME series PowerSpout, or hire a registered electrical worker, or ensure your site never operates without load.' + siteGUI.GUIcr + siteGUI.GUIcr
                    break

        rounds = {}
        values = {}

        values['-2a'] = site.cable_voltage * 0.8
        rounds['-2a'] = -len(str(int(values['-2a']))) + 3
        values['-2b'] = site.Load_pwr * 0.25
        rounds['-2b'] = -len(str(int(values['-2b']))) + 3

        values['-1a'] = site.cable_voltage * 0.9
        rounds['-1a'] = -len(str(int(values['-1a']))) + 3
        values['-1b'] = site.Load_pwr * 0.5
        rounds['-1b'] = -len(str(int(values['-1b']))) + 3

        values['0a'] = site.cable_voltage
        rounds['0a'] = -len(str(int(values['0a']))) + 3
        values['0b'] = site.Load_pwr
        rounds['0b'] = -len(str(int(values['0b']))) + 3

        values['+1a'] = site.cable_voltage * 1.1
        rounds['+1a'] = -len(str(int(values['+1a']))) + 3
        values['+1b'] = site.Load_pwr * 1.5
        rounds['+1b'] = -len(str(int(values['+1b']))) + 3

        values['+2a'] = site.cable_voltage * 1.2
        rounds['+2a'] = -len(str(int(values['+2a']))) + 3
        values['+2b'] = site.Load_pwr * 2
        rounds['+2b'] = -len(str(int(values['+2b']))) + 3

        for items in rounds:
            if rounds[items] > 0: rounds[items] = 0

        siteGUI.GUI_design_notes_elec = siteGUI.GUI_design_notes_elec + \
                                        'Table mode ( in some inverters) can be used to resolve MPPT tracking stability issues. ' + \
                                        'Below is a suggested table that will help in getting you started. ' + \
                                        'On site adjustment (by trial and error) will be needed to get the best result when using table mode. ' + \
                                        'Only Power-One, EnaSolar and Ginlong inverters have a table mode setting. ' + \
                                        'Some off grid MPPT regulators also have table modes. ' + \
                                        siteGUI.GUIcr + 'Suggested table' + siteGUI.GUIcr + \
                                        'min voltage setting, min power setting' + siteGUI.GUIcr + \
                                        str(int(round(values['-2a'], rounds['-2a']))) + ', ' + str(
            int(round(values['-2b'], rounds['-2b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['-1a'], rounds['-1a']))) + ', ' + str(
            int(round(values['-1b'], rounds['-1b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['0a'], rounds['0a']))) + ', ' + str(
            int(round(values['0b'], rounds['0b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['+1a'], rounds['+1a']))) + ', ' + str(
            int(round(values['+1b'], rounds['+1b']))) + siteGUI.GUIcr + \
                                        str(int(round(values['+2a'], rounds['+2a']))) + ', ' + str(
            int(round(values['+2b'], rounds['+2b']))) + siteGUI.GUIcr + \
                                        'max voltage setting, max power setting' + siteGUI.GUIcr + siteGUI.GUIcr

        if sys.platform[:5] == 'linux':
            siteGUI.GUI_design_notes_safety = siteGUI.GUI_design_notes_safety + siteGUI.GUIcr + site.Aspace + siteGUI.GUIcr

    computeSDtype()

    siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "  Calculation process" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     It took " + str(
        site.penstock_iterations) + " iterations to solve penstock flow rate" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     It took " + str(
        site.penstock_max_pipe_iterations) + " iterations to solve max penstock flow rate" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     It took " + str(
        site.jet_iterations) + " iterations to solve jet size limit" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     It took " + str(
        site.UWW_iterations) + " iterations to solve rpm W limit" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               penstock_area " + str(
        site.penstock_area) + "m^2" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             pelton_Wuse_rpm " + str(
        site.pelton_Wuse_rpm) + "W/rpm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  Kf_turbine " + str(site.Kf_turbine) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "    Kf for penstock fittings " + str(site.penstock_Kf) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                 turbine_eff " + str(
        site.turbine_eff * 100) + "%" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      SD_eff " + str(
        site.SD_eff * 100) + "%" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            turbine_dia  PCD " + str(
        site.turbine_dia) + "m" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             turbine_spd_jet " + str(
        site.turbine_spd_jet * 100) + "% runner to water speed" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                         eps " + str(site.eps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               Pipe velocity " + str(
        site.pipeV) + "m/s" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          Qm " + str(site.Qm) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          Re " + str(site.Re) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                 Re_consider " + str(site.Re_consider) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          x1 " + str(site.x1) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          x2 " + str(site.x2) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          x3 " + str(site.x3) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          x4 " + str(site.x4) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    Moodyfff " + str(site.Moodyfff) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                           f " + str(site.f) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                        dp_m " + str(site.dp_m) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              Effective head " + str(
        site.eff_head) + "m" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "          Water jet velocity " + str(site.Vjet) + "m/s" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   Shaft pwr " + str(
        site.shaft_pwr) + "W" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "Turbine speed for max. power " + str(site.rpm) + "rpm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                 runaway_rpm " + str(
        site.runaway_rpm) + "rpm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             Water jet power " + str(
        site.jetpower) + "W" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + " Some constants" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     density " + str(site.density) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                         gpm " + str(site.gpm) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     gravity " + str(site.gravity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                       meter " + str(site.meter) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                          mm " + str(site.mm) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     mmm_lps " + str(site.mmm_lps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   viscosity " + str(site.viscosity) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "     penstock_flow_roughness " + str(
        site.penstock_flow_roughness) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              cable_material " + str(
        site.cable_material) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "         Water power at site " + str(site.waterpower) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "A 1 = Need to check design..." + str(site.design_Chk) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  cableR_req " + str(
        site.cableR_req) + "ohm/m" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "      Cable ohms (ret. trip) " + str(
        site.cableR) + "ohm" + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "           Cable voltage drop" + str(
        site.cable_Vdrop) + " V" + siteGUI.GUI_diag_cr

    siteGUI.GUI_diag = siteGUI.GUI_diag + "           Itterator counter " + str(
        site.itteratorCount) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + " I limited itterator counter " + str(site.amplimCount) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "      siteGUI.GUI_Num_PS_Lkd " + str(
        siteGUI.GUI_Num_PS_Lkd) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     PenSLkd " + str(
        siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "    siteGUI.GUI_initial_data " + str(
        siteGUI.GUI_initial_data) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_diag_cr

    siteGUI.GUI_diag = site.SDsearch + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr + siteGUI.GUI_diag + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr + 'After' + siteGUI.GUI_diag_cr
    reportGUI()
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'Electrical notes here ' + siteGUI.GUI_design_notes_elec + siteGUI.GUI_diag_cr

    siteGUI.GUI_diag = siteGUI.GUI_diag + str(site.alarms) + siteGUI.GUI_design_notes_elec + siteGUI.GUI_diag_cr



    # siteGUI.GUI_cable_AWG = siteGUI.GUI_diag



    # siteGUI.GUI_penstock_dia = siteGUI.GUI_diag
    # tofile = open('diag.txt', 'w')
    # tofile.write(siteGUI.GUI_diag)


def put_lps():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_avail_Wflow = str(round(site.avail_lps, 1)) + ' lps'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_avail_Wflow = str(round(site.avail_lps * site.convert['gpm-lps'], 1)) + ' gpm'


def put_lpsused():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_Wflow = str(round(site.lps, 1)) + ' lps'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_Wflow = str(round(site.lps * site.convert['gpm-lps'], 1)) + ' gpm'


def put_head():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_penstock_head = str(round(site.penstock_head, 1)) + ' m'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_penstock_head = str(round(site.penstock_head * site.convert['ft-m'], 1)) + ' ft'


def put_OprHead():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_eff_head = "Operating head is " + str(round(site.eff_head, 1)) + ' m'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_eff_head = "Operating head is " + str(round(site.eff_head * site.convert['ft-m'], 1)) + ' ft'


def put_PenLen():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_penstock_len = str(int(round(site.penstock_len, 0))) + ' m'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_penstock_len = str(int(round(site.penstock_len * site.convert['ft-m'], 0))) + ' ft'


def put_PenEffTarget():
    siteGUI.GUI_penstock_eff_target = str(int(site.penstock_eff_target * 100)) + ' %'


def put_PenDia():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_penstock_dia = str(int(round(site.penstock_dia * site.convert['mm-m'], 0))) + ' mm'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_penstock_dia = str(round(site.penstock_dia * site.convert['in-m'], 2)) + ' in'


def put_Num_PS():
    siteGUI.GUI_Num_PS = int(site.Num_PS)
    siteGUI.GUI_turbine_nozzles = int(site.turbine_nozzles)


def put_JetDia():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_jet_dia = str(round(site.jet_dia * site.convert['mm-m'], 1)) + ' mm'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_jet_dia = str(round(site.jet_dia * site.convert['in-m'], 2)) + ' in'


def put_ActPenEff():
    siteGUI.GUI_actual_pipe_eff = str(int(site.jetpower / site.waterpower * 100)) + ' %'


def put_OprRPM():
    siteGUI.GUI_Opr_rpm = str(int(site.rpm)) + ' rpm'


def put_eaPS_W():
    siteGUI.GUI_PS_pwr_ea = str(int(site.Actual_turbine_electric_pwr / site.Num_PS)) + ' W'


def put_allPS_W():
    siteGUI.GUI_Actual_turbine_electric_pwr = str(int(site.Actual_turbine_electric_pwr)) + ' W'


def put_cableEff_targ():
    siteGUI.GUI_cable_eff_target = str(int(site.cable_eff_target * 100)) + ' %'


def put_CableLen():
    if (siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_cable_len = str(int(round(site.cable_len, 0))) + ' m'
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_cable_len = str(int(round(site.cable_len * site.convert['ft-m'], 0))) + ' ft'


def put_DesLdV():
    siteGUI.GUI_Dload_V = str(int(site.design_cable_voltage + 0.5)) + ' V'


def put_ActLdV():
    siteGUI.GUI_Aload_V = str(int(site.cable_voltage + 0.5)) + ' V'


def put_CableSize():
    siteGUI.GUI_cable_size = str(round(site.cable_size, 3)) + ' mm^2'


def put_CableAWG():
    siteGUI.GUI_cable_AWG = str(site.cable_gauge) + ' AWG'


def put_CableDetails():
    siteGUI.GUI_cable_dia_mm_sld = str(round(pow(site.cable_size / pi, 0.5) * 2, 2)) + ' mm'
    siteGUI.GUI_cable_dia_mm_str = str(round(pow(site.cable_size / 0.58 / pi, 0.5) * 2, 2)) + ' mm'
    siteGUI.GUI_cable_dia_in_sld = str(round(pow(site.cable_size / pi, 0.5) * 2 / 25.4, 3)) + ' in'
    siteGUI.GUI_cable_dia_in_str = str(round(pow(site.cable_size / 0.58 / pi, 0.5) * 2 / 25.4, 3)) + ' in'

    siteGUI.GUI_cable_amps = str(round(site.cable_A, 1)) + ' A'
    siteGUI.GUI_actual_cable_eff = str(int(site.Load_pwr / site.Actual_turbine_electric_pwr * 100 + 0.5)) + ' %'
    siteGUI.GUI_cable_Vgen = str(int(site.cable_Vgen + 0.5)) + ' V'
    siteGUI.GUI_Load_pwr = str(int(site.Load_pwr + 0.5)) + ' W'


def fetchall():  # Fetch all user inputs
    fetchlps()
    fetchhead()
    fetchpenlen()
    fetchpenefftarg()
    fetchpendia()
    fetchcablelen()
    fetchcableefftarg()
    fetchloadV()
    site.cable_material = siteGUI.GUI_cable_material
    site.cableLock = int(siteGUI.GUI_LockCable)
    fetchcablesize()
    fetchNum_PS()
    fetchNumNoz()


def fetchlps():  # Get users lps entered.  Only called from fetchall() and BasicData()
    temp = site.avail_lps

    if (siteGUI.GUI_meas_sys == 'Metric'):
        site.avail_lps = textread(siteGUI.GUI_avail_Wflow, 'lps', 'lps')
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        site.avail_lps = textread(siteGUI.GUI_avail_Wflow, 'gpm', 'lps')

    maxlps = 50
    minlps = 0.1
    if (site.PStype[:3] == 'TRG'):
        maxlps = 200
        minlps = 6

    if ((temp <= maxlps) and (temp >= minlps) and (site.avail_lps == 0)):
        site.avail_lps = temp
    else:
        if ((temp != 0) or (site.avail_lps != 0)):
            if (site.avail_lps > maxlps):
                site.avail_lps = maxlps
            if (site.avail_lps < minlps):
                site.avail_lps = minlps

    site.lps = site.avail_lps


def fetchhead():  # Get site head entered.  Only called from fetchall() and newBasicData() # converts users values into the max or min values
    temp = site.penstock_head

    if (siteGUI.GUI_meas_sys == 'Metric'):
        site.penstock_head = textread(siteGUI.GUI_penstock_head, 'm', 'm')
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        site.penstock_head = textread(siteGUI.GUI_penstock_head, 'ft', 'm')

    max_m = 160
    min_m = 3
    if (site.PStype[:3] == 'TRG'):
        max_m = 40
        min_m = 2

    if ((temp <= max_m) and (temp >= min_m) and (site.penstock_head == 0)):
        site.penstock_head = temp
    else:
        if ((temp != 0) or (site.penstock_head != 0)):
            if (site.penstock_head > max_m):
                site.penstock_head = max_m
            if (site.penstock_head < min_m):
                site.penstock_head = min_m


def fetchpenlen():  # Get this site data entered.  Only called from fetchall()
    temp = site.penstock_len

    if (siteGUI.GUI_meas_sys == 'Metric'):
        site.penstock_len = textread(siteGUI.GUI_penstock_len, 'm', 'm')
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        site.penstock_len = textread(siteGUI.GUI_penstock_len, 'ft', 'm')

    if ((temp <= 5000) and (temp >= site.penstock_len) and (site.penstock_len == 0)):
        site.penstock_len = temp
    else:
        if ((temp != 0) or (site.penstock_len != 0)):
            if (site.penstock_len > 5000):
                site.penstock_len = 5000
            if (site.penstock_len < 3):  # Was site.penstock_head before instead of 3m as min length
                site.penstock_len = 3  # Was site.penstock_head before instead of 3m as min length


def fetchpenefftarg():  # Get this site data entered.  Only called from fetchall()
    temp = site.penstock_eff_target

    site.penstock_eff_target = float(textread(siteGUI.GUI_penstock_eff_target, '%', '%')) / float(
        100)  # %% in key removed

    if ((temp <= 1) and (temp >= 0.66) and (site.penstock_eff_target == 0)):
        site.penstock_eff_target = temp
    else:
        if ((temp != 0) or (site.penstock_eff_target != 0)):
            if (site.penstock_eff_target > 0.995):
                site.penstock_eff_target = 0.99
            if (site.penstock_eff_target < 0.66666666):
                site.penstock_eff_target = 0.66666666


def fetchpendia():  # Get this site data entered.  Only called from fetchall()
    temp = site.penstock_dia

    if (siteGUI.GUI_meas_sys == 'Metric'):
        site.penstock_dia = textread(siteGUI.GUI_penstock_dia, 'mm', 'm')
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        site.penstock_dia = textread(siteGUI.GUI_penstock_dia, 'in', 'm')

    if ((temp <= 2) and (temp >= 0.01) and (site.penstock_dia == 0)):
        site.penstock_dia = temp
    else:
        if ((temp != 0) or (site.penstock_head != 0)):
            if (site.penstock_dia > 2):
                site.penstock_dia = 2
            if (site.penstock_dia < 0.01):
                site.penstock_dia = 0.01


def fetchNum_PS():  # Get this site data entered.  Only called from newNoPS() and LockPS()
    temp = site.Num_PS

    site.Num_PS = int(siteGUI.GUI_Num_PS)

    if ((temp <= 10) and (temp >= 1) and (site.Num_PS == 0)):
        site.Num_PS = temp
    else:
        if ((temp != 0) or (site.Num_PS != 0)):
            if (site.Num_PS > site.MaxPS):
                site.Num_PS = site.MaxPS
            if (site.Num_PS < 1):
                site.Num_PS = 1


def fetchNumNoz():  # Get this site data entered.  Only called from newNoPS() and LockPS()
    temp = site.turbine_nozzles
    site.turbine_nozzles = int(siteGUI.GUI_turbine_nozzles)
    max_nozzles = 2
    if (site.PStype[:3] == 'TRG'):
        max_nozzles = 4

    if ((temp <= 2) and (temp >= 1) and (site.turbine_nozzles == 0)):
        site.turbine_nozzles = temp
    else:
        if ((temp != 0) or (site.turbine_nozzles != 0)):
            if (site.turbine_nozzles > max_nozzles):
                site.turbine_nozzles = max_nozzles
            if (site.turbine_nozzles < 1):
                site.turbine_nozzles = 1


def fetchcablelen():  # Get this site data entered.  Only called from fetchall()
    temp = site.cable_len

    if (siteGUI.GUI_meas_sys == 'Metric'):
        site.cable_len = textread(siteGUI.GUI_cable_len, 'm', 'm')
    if (siteGUI.GUI_meas_sys == 'Imperial'):
        site.cable_len = textread(siteGUI.GUI_cable_len, 'ft', 'm')

    if ((temp <= 4000) and (temp >= 2) and (site.cable_len == 0)):
        site.cable_len = temp
    else:
        if ((temp != 0) or (site.penstock_head != 0)):
            if (site.cable_len > 4000):
                site.cable_len = 4000
            if (site.cable_len < 2):
                site.cable_len = 2


def fetchloadV():  # Get this site data entered.  Only called from fetchall()
    temp = site.design_cable_voltage

    site.design_cable_voltage = textread(siteGUI.GUI_Dload_V, 'V', 'V')

    if ((temp <= site.Vlimit[siteGUI.GUI_PStype]) and (temp >= 10) and (site.design_cable_voltage == 0)):
        site.design_cable_voltage = temp
    else:
        if ((temp != 0) or (site.design_cable_voltage != 0)):
            if (site.design_cable_voltage > site.Vlimit[siteGUI.GUI_PStype]):
                site.design_cable_voltage = site.Vlimit[siteGUI.GUI_PStype]
            if (site.design_cable_voltage < 10):
                site.design_cable_voltage = 10

    site.cable_voltage = site.design_cable_voltage


def fetchcableefftarg():  # Get this site data entered.  Only called from fetchall()
    temp = site.cable_eff_target

    site.cable_eff_target = float(textread(siteGUI.GUI_cable_eff_target, '%', '%')) / float(100)  # %% in key removed

    if ((temp <= 1) and (temp >= 0.5) and (site.cable_eff_target == 0)):
        site.cable_eff_target = temp
    else:
        if ((temp != 0) or (site.penstock_eff_target != 0)):
            if (site.cable_eff_target > 0.995):
                site.cable_eff_target = 0.99
            if (site.cable_eff_target < 0.5):
                site.cable_eff_target = 0.5


def fetchcablesize():  # Get this site data entered.  Only called from fetchall()
    temp = site.cable_size

    site.cable_size = float(textread(siteGUI.GUI_cable_size, 'mm^2', 'mm^2'))

    if ((temp <= 170) and (temp >= 0.5) and (site.cable_size == 0)):
        site.cable_size = temp
    else:
        if ((temp != 0) or (site.cable_size != 0)):
            if (site.cable_size > 170):
                site.cable_size = 170
            if (site.cable_size < 0.5):
                site.cable_size = 0.5

    # Check are if mm mode and round as needed
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Checking mm mode' + siteGUI.GUI_diag_cr
    if (siteGUI.GUI_cable_mm_AWG == 'mm'):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'found mm mode' + siteGUI.GUI_diag_cr
        site.cable_size = round(site.cable_size, 1)
        createAWG()


def fetchAWG():  # Get this site data entered.  Only called from fetchall()
    pointer = 0
    value = str('')
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Inputted cable AWG' + siteGUI.GUI_cable_size + siteGUI.GUI_diag_cr
    while (len(siteGUI.GUI_cable_AWG) > 0):
        try:
            digi = str(siteGUI.GUI_cable_AWG[pointer])
        except:
            break

        # siteGUI.GUI_diag = siteGUI.GUI_diag + 'digit in input ' + digi + siteGUI.GUI_diag_cr
        if ((digi == ' ') or (digi == '.') or (digi == 'A')):
            pointer = pointer + 1
            break
        value = value + digi
        pointer = pointer + 1

    create_mm_4_AWG(value)


def textread(texttoread, inp_unit,
             calc_unit):  # Reads in a string with input sensability checks and does unit conversion as appropiate
    restofline = ''
    pointer = 0
    value = float(0)
    prepostdot = 'pre'
    decimals = float(0.1)
    while (len(texttoread) > 0):
        digi = texttoread[pointer]
        if (digi == ' '):
            pointer = pointer + 1
            try:
                dig = texttoread[pointer + 1]
            except:
                break
            continue

        if (digi == '.'):
            prepostdot = 'post'
            pointer = pointer + 1
            continue

        try:
            digit = int(digi)
        except:
            break

        if (prepostdot == 'pre'):
            value = value * 10 + digit
        else:
            value = value + float(decimals * digit)
            decimals = decimals / float(10)

        try:
            dig = texttoread[pointer + 1]
        except:
            pointer = pointer + 1
            break

        pointer = pointer + 1

    if (pointer > 0):
        try:
            restofline = texttoread[pointer:]
        except:
            restofline = ''

    restofline = restofline.rstrip()
    # convert dictionary items gives multiplier for wanted-source unit order

    whichC = (calc_unit + '-' + restofline).lower()
    #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Conversion being used " + whichC + siteGUI.GUI_diag_cr


    try:
        converter = site.convert[whichC]
    except:
        whichC = calc_unit + '-' + inp_unit
        try:
            converter = site.convert[whichC]
        except:
            converter = 1

    value = value * converter
    return (value)


def reportGUI():
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_initial_data " + str(
        siteGUI.GUI_initial_data) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_process_option " + str(
        siteGUI.GUI_process_option) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_meas_sys " + str(
        siteGUI.GUI_meas_sys) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      GUI_PStype " + str(
        siteGUI.GUI_PStype) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                 GUI_avail_Wflow " + str(
        siteGUI.GUI_avail_Wflow) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                       GUI_Wflow " + str(
        siteGUI.GUI_Wflow) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "               GUI_penstock_head " + str(
        siteGUI.GUI_penstock_head) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_eff_head " + str(
        siteGUI.GUI_eff_head) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_penstock_len " + str(
        siteGUI.GUI_penstock_len) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "         GUI_penstock_eff_target " + str(
        siteGUI.GUI_penstock_eff_target) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_penstock_dia " + str(
        siteGUI.GUI_penstock_dia) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_PenSLkd " + str(
        siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      GUI_Num_PS " + str(
        siteGUI.GUI_Num_PS) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             GUI_turbine_nozzles " + str(
        siteGUI.GUI_turbine_nozzles) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_Num_PS_Lkd " + str(
        siteGUI.GUI_Num_PS_Lkd) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_jet_dia " + str(
        siteGUI.GUI_jet_dia) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             GUI_actual_pipe_eff " + str(
        siteGUI.GUI_actual_pipe_eff) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_Opr_rpm " + str(
        siteGUI.GUI_Opr_rpm) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_PS_pwr_ea " + str(
        siteGUI.GUI_PS_pwr_ea) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + " GUI_Actual_turbine_electric_pwr " + str(
        siteGUI.GUI_Actual_turbine_electric_pwr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_eff_target " + str(
        siteGUI.GUI_cable_eff_target) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_cable_len " + str(
        siteGUI.GUI_cable_len) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_Dload_V " + str(
        siteGUI.GUI_Dload_V) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     GUI_Aload_V " + str(
        siteGUI.GUI_Aload_V) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_LockCable " + str(
        siteGUI.GUI_LockCable) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_cable_material " + str(
        siteGUI.GUI_cable_material) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_cable_size " + str(
        siteGUI.GUI_cable_size) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                   GUI_cable_AWG " + str(
        siteGUI.GUI_cable_AWG) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                GUI_cable_mm_AWG " + str(
        siteGUI.GUI_cable_mm_AWG) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "              GUI_cable_mm_title " + str(
        siteGUI.GUI_cable_mm_title) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "             GUI_cable_AWG_title " + str(
        siteGUI.GUI_cable_AWG_title) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_mm_sld " + str(
        siteGUI.GUI_cable_dia_mm_sld) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_mm_str " + str(
        siteGUI.GUI_cable_dia_mm_str) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_in_sld " + str(
        siteGUI.GUI_cable_dia_in_sld) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_cable_dia_in_str " + str(
        siteGUI.GUI_cable_dia_in_str) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_cable_amps " + str(
        siteGUI.GUI_cable_amps) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "            GUI_actual_cable_eff " + str(
        siteGUI.GUI_actual_cable_eff) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                  GUI_cable_Vgen " + str(
        siteGUI.GUI_cable_Vgen) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_Load_pwr " + str(
        siteGUI.GUI_Load_pwr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "          GUI_design_notes_hydro " + str(
        siteGUI.GUI_design_notes_hydro) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "           GUI_design_notes_elec " + str(
        siteGUI.GUI_design_notes_elec) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "         GUI_design_notes_safety " + str(
        siteGUI.GUI_design_notes_safety) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                    GUI_revision " + str(
        siteGUI.GUI_revision) + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr + siteGUI.GUI_diag_cr

    siteGUI.GUI_diag = siteGUI.GUI_diag + "site.Actual_turbine_electric_pwr " + str(
        site.Actual_turbine_electric_pwr) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                     site.Num_PS " + str(site.Num_PS) + siteGUI.GUI_diag_cr
    siteGUI.GUI_diag = siteGUI.GUI_diag + "                      site.PSeff " + str(site.PSeff) + siteGUI.GUI_diag_cr


# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
# ALL PROCESSING of user data comes here
def process_here(*args):
    site.tracer = siteGUI.GUI_PStype

    siteGUI.GUI_diag = 'Before' + siteGUI.GUI_diag_cr  # The initiation of      #  siteGUI.GUI_diag = ''
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'HP det |' + site.PStype[-2:] + '|' + siteGUI.GUI_diag_cr

    reportGUI()

    site.alarms = []  # Clear the alarm list
    site.UWW_iterations = 0
    site.jet_iterations = 0
    site.penstock_iterations = 0
    site.PStype = siteGUI.GUI_PStype

    siteGUI.GUI_diag = siteGUI.GUI_diag + 'HP det |' + site.PStype[-2:] + '|' + siteGUI.GUI_diag_cr

    if (site.PStype[-2:] == 'HP'):
        site.pelton_Wuse_rpm = 1.65
        siteGUI.GUI_diag = siteGUI.GUI_diag + 'HP detected' + siteGUI.GUI_diag_cr  # The initiation of      #  siteGUI.GUI_diag = ''
    else:
        site.pelton_Wuse_rpm = 1.42

    if (site.PStype[:3] == 'PLT' or site.PStype[:3] == 'TRG'):
        site.dis_coeff = 0.83
    else:
        site.dis_coeff = 1

    if (site.PStype[:3] != 'PLT' and site.PStype[:3] != 'TRG'):
        site.runaway_rpm_limit = 2000  # Max safe speed for turbine
        site.dis_coeff = 1  # Area of jet is actually smaller than area of nozzle exit.
        site.turbine_eff = 0.7  # Efficiency ratio for pelton turbine  Gets updated by calcs once water power is known
        site.SD_eff = 0.7  # Efficiency ratio for Smart Drive generator  Gets updated by calcs once water power is known
        site.turbine_dia = 0.23  # Diameter for the pelton wheel in metres
        site.eps = 1.25e-5  # Used in pipe loss calc
        site.turbine_spd_jet = float(0.45)  # Speed of pelton buckets relative to jet velocity
        site.Num_PS = 1  # Number of turbines
        site.turbine_nozzles = 2  # Number of nozzles on each turbine
        site.One_jet_water_W_lim = 800  # Water power limit for one jet to get expected warrenteed bearing life
        site.One_jet_dia_lim = 0.02  # Biggest jet diameter in m that works for a turbine
        site.Two_jet_dia_lim = 0.025  # Biggest jet size to use in a 2 jet turbine. Only applies when very low head
        site.pelton_Wuse_rpm = 1.42  # Watts of water jet power required for the PS
        site.ideal_jet_sqr_mm = 0  # Ideal total sqr mm jet size to use for this penstock, head, lps combination
        site.UWWatts_per_SD = 0  # Used Water Watts per PS turbine. Used to figure out correct efficiency levels

        if (site.PStype[-2:] == 'HP'):
            site.pelton_Wuse_rpm = 1.65
            siteGUI.GUI_diag = siteGUI.GUI_diag + 'HP detected' + siteGUI.GUI_diag_cr  # The initiation of      #  siteGUI.GUI_diag = ''
        else:
            site.pelton_Wuse_rpm = 1.42

        # This table maps out the effeciency degradation at low power levels.
        # Uses water jet power for x coordinates and y coordinates are put into SD_eff and turbine_eff
        # Software uses straight line interpolation between points and level above top point
        site.eff = {0: 0, 25: 30, 50: 36, 100: 40, 200: 45, 300: 47, 600: 49.5, 1000: 51, 1600: 52, 2500: 54, 3500: 53,
                    6000: 52}  # (Water power W, % eff)
        site.lpseff = {0: 100, 0.1: 100, 1000000: 100}  # ( lps, % eff)

    if (site.PStype[:3] == 'PLT'):
        site.runaway_rpm_limit = 3000  # Max safe speed for turbine
        site.dis_coeff = 0.83  # Area of jet is actually smaller than area of nozzle exit.
        site.turbine_eff = 0.7  # Efficiency ratio for pelton turbine  Gets updated by calcs once water power is known
        site.SD_eff = 0.7  # Efficiency ratio for Smart Drive generator  Gets updated by calcs once water power is known
        site.turbine_dia = 0.23  # Diameter for the pelton wheel in metres
        site.eps = 1.25e-5  # Used in pipe loss calc
        site.turbine_spd_jet = float(0.45)  # Speed of pelton buckets relative to jet velocity
        site.Num_PS = 1  # Number of turbines
        site.turbine_nozzles = 2  # Number of nozzles on each turbine
        site.One_jet_water_W_lim = 800  # Water power limit for one jet to get expected warrenteed bearing life
        site.One_jet_dia_lim = 0.02  # Biggest jet diameter in m that works for a turbine
        site.Two_jet_dia_lim = 0.025  # Biggest jet size to use in a 2 jet turbine. Only applies when very low head
        site.pelton_Wuse_rpm = 1.42  # Watts of water jet power required for the PS
        site.ideal_jet_sqr_mm = 0  # Ideal total sqr mm jet size to use for this penstock, head, lps combination
        site.UWWatts_per_SD = 0  # Used Water Watts per PS turbine. Used to figure out correct efficiency levels

        if (site.PStype[-2:] == 'HP'):
            site.pelton_Wuse_rpm = 1.65
            siteGUI.GUI_diag = siteGUI.GUI_diag + 'HP detected' + siteGUI.GUI_diag_cr  # The initiation of      #  siteGUI.GUI_diag = ''
        else:
            site.pelton_Wuse_rpm = 1.42

        # This table maps out the effeciency degradation at low power levels.
        # Uses water jet power for x coordinates and y coordinates are put into SD_eff and turbine_eff
        # Software uses straight line interpolation between points and level above top point
        site.eff = {0: 0, 25: 30, 50: 36, 100: 40, 200: 45, 300: 47, 600: 49.5, 1000: 51, 1600: 52, 2500: 54, 3500: 53,
                    6000: 52}
        site.lpseff = {0: 100, 0.1: 100, 1000000: 100}

    site.max_jets = 2
    if (site.PStype[:3] == 'TRG'):
        site.runaway_rpm_limit = 3000  # Max safe speed for turbine
        site.dis_coeff = 0.83  # Area of jet is actually smaller than area of nozzle exit.
        site.turbine_eff = 0.785  # Efficiency ratio for pelton turbine  Gets updated by calcs once water power is known
        site.SD_eff = 0.7  # Efficiency ratio for Smart Drive generator  Gets updated by calcs once water power is known
        site.turbine_dia = 0.14513  # Diameter for the pelton wheel in metres
        site.eps = 1.25e-5  # Used in pipe loss calc
        site.turbine_spd_jet = float(0.6135)  # Speed of pelton buckets relative to jet velocity
        site.Num_PS = 1  # Number of turbines
        site.turbine_nozzles = 4  # Number of nozzles on each turbine
        site.One_jet_water_W_lim = 727  # Water power limit for one jet to get expected warrenteed bearing life 400W output target @ 55% eff
        site.One_jet_dia_lim = 0.025  # Biggest jet diameter in m that works for a turbine
        site.Two_jet_dia_lim = 0.025  # Biggest jet size to use in a 2 jet turbine. Only applies when very low head
        site.pelton_Wuse_rpm = 1.65  # Watts of water jet power required for the PS
        site.ideal_jet_sqr_mm = 0  # Ideal total sqr mm jet size to use for this penstock, head, lps combination
        site.max_jets = 4  # Need to know how many jets there could be

        if (site.PStype[-2:] == 'HP'):
            site.pelton_Wuse_rpm = 1.63
        else:
            site.pelton_Wuse_rpm = 1.282

        site.UWWatts_per_SD = 0  # Used Water Watts per PS turbine. Used to figure out correct efficiency levels

        # This table maps out the effeciency degradation at low power levels.
        # Uses water jet power for x coordinates and y coordinates in % are put into SD_eff and turbine_eff
        # SD_eff * turbine_eff = site.eff[%]
        # Software uses straight line interpolation between points and level above top point
        site.eff = {0: 0, 182: 55, 6000: 55}
        site.lpseff = {0: 0, 0.1: 50, 8: 85, 9: 100, 1000000: 100}

    if (siteGUI.GUI_process_option == 'basicdata'):
        if (siteGUI.GUI_initial_data == 1):
            siteGUI.GUI_Num_PS_Lkd = 0
            siteGUI.GUI_PenSLkd = 0

            if (siteGUI.GUI_PStype[0:5] == 'ME100'):
                siteGUI.GUI_Dload_V = str(90)
            if (siteGUI.GUI_PStype[0:5] == 'ME120'):
                siteGUI.GUI_Dload_V = str(105)
            if (siteGUI.GUI_PStype[0:5] == 'ME140'):
                siteGUI.GUI_Dload_V = str(125)
            if (siteGUI.GUI_PStype[0:5] == 'ME250'):
                siteGUI.GUI_Dload_V = str(230)
            if (siteGUI.GUI_PStype[0:5] == 'GE400'):
                siteGUI.GUI_Dload_V = str(350)
            if (siteGUI.GUI_PStype[0:3] == 'PLT'):
                siteGUI.GUI_Dload_V = str(80)
            if (siteGUI.GUI_PStype[0:6] == 'PLT HP'):
                siteGUI.GUI_Dload_V = str(80)
            if (siteGUI.GUI_PStype[0:3] == 'TRG'):
                siteGUI.GUI_Dload_V = str(80)
            if (siteGUI.GUI_PStype[0:3] == 'TRG HP'):
                siteGUI.GUI_Dload_V = str(80)

            if (siteGUI.GUI_meas_sys == 'Metric'):
                siteGUI.GUI_cable_mm_AWG = 'mm'
                siteGUI.GUI_cable_mm_title = 'Cable cross section'
                siteGUI.GUI_cable_AWG_title = 'Next size up cable'
            else:
                siteGUI.GUI_cable_mm_AWG = 'AWG'
                siteGUI.GUI_cable_mm_title = 'Metric cross section'
                siteGUI.GUI_cable_AWG_title = 'Cable size'

            if (siteGUI.GUI_PStype[0:2] == 'BE'):
                site.design_cable_voltage = 55
            if (siteGUI.GUI_PStype[0:5] == 'ME100'):
                site.design_cable_voltage = 90
            if (siteGUI.GUI_PStype[0:5] == 'ME120'):
                site.design_cable_voltage = 105
            if (siteGUI.GUI_PStype[0:5] == 'ME140'):
                site.design_cable_voltage = 125
            if (siteGUI.GUI_PStype[0:5] == 'ME250'):
                site.design_cable_voltage = 230
            if (siteGUI.GUI_PStype[0:5] == 'GE400'):
                site.design_cable_voltage = 350
            if (siteGUI.GUI_PStype[0:3] == 'PLT'):
                site.design_cable_voltage = 80
            if (siteGUI.GUI_PStype[0:6] == 'PLT HP'):
                site.design_cable_voltage = 80
            if (siteGUI.GUI_PStype[0:3] == 'TRG'):
                site.design_cable_voltage = 80
            if (siteGUI.GUI_PStype[0:3] == 'TRG HP'):
                site.design_cable_voltage = 80

            fetchhead()  # important

            fetchlps()  # important

            put_lps()
            put_head()

            #  siteGUI.GUI_diag = siteGUI.GUI_diag + str(siteGUI.GUI_initial_data) + ' ' + str(site.Vlimit[ siteGUI.GUI_PStype ]) + ' ' + str(site.lps) + ' ' + str(site.penstock_head)+ siteGUI.GUI_diag_cr


            if ((siteGUI.GUI_initial_data == 1) or (site.Vlimit[siteGUI.GUI_PStype] == 0) or (site.lps == 0) or (
                site.penstock_head == 0)):  # Test if have enough preliminary data
                if ((site.Vlimit[siteGUI.GUI_PStype] != 350) and (site.lps != 0) and (
                    site.penstock_head != 0)):  # Test if have enough preliminary data
                    site.penstock_len = 5 * site.penstock_head
                    site.penstock_eff_target = 0.9
                    site.cable_eff_target = 0.95

                    site.cable_voltage = site.design_cable_voltage
                    # siteGUI.GUI_Dload_V = site.cable_voltage
                    siteGUI.GUI_initial_data = 0

                    PowerSpout_calc()  # Figure out hydro and PS output power for this number of turbines and jets
                    CalcCable()  # Calculate the cable size required for design loss and confirm results numbers. Includes min conductor size for amps check
                    reportAll()  # Display all results to gui and print to terminal window for diagnostics


        else:  # Else means have working data and just need to update for new head, lps or PS type
            fetchall()
            PowerSpout_calc()
            CalcCable()
            reportAll()

    # What to do for new PS type
    if (siteGUI.GUI_process_option == 'PSchange'):
        # siteGUI.GUI_Num_PS_Lkd = 0  Leave lock as it was. Perhaps user knows number of PowerSpouts for budget reasons
        if (siteGUI.GUI_PStype[0:3] == 'TRG'):
            siteGUI.GUI_turbine_nozzles = 4
        else:
            siteGUI.GUI_turbine_nozzles = 2

        fetchall()
        if (siteGUI.GUI_initial_data == 0):  # Check if have any data before calling calculations to avoid / by 0 error
            PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
            CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
            reportAll()

    # What to do for new penstock length
    if (siteGUI.GUI_process_option == 'penstock'):
        fetchall()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do for new penstock effeciency target
    if (siteGUI.GUI_process_option == 'penstockeff'):
        fetchall()
        siteGUI.GUI_PenSLkd = 0
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # siteGUI.GUI_diag = siteGUI.GUI_diag + "#########################################################################" + siteGUI.GUI_diag_cr
    # What to do when user enters a specific penstock diameter
    if (siteGUI.GUI_process_option == 'pendia'):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "Doing a new penstock diameter " + str(siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr
        siteGUI.GUI_PenSLkd = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + "See new penstock locked " + str(siteGUI.GUI_PenSLkd) + siteGUI.GUI_diag_cr

    # What to do when user presses the penstock size lock or has been a new penstock size given
    if ((siteGUI.GUI_process_option == 'pendiaLk') or (siteGUI.GUI_process_option == 'pendia')):
        fetchall()  # User entered new data
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user enters a new number of PowerSpouts or PowerSpout jets
    if (siteGUI.GUI_process_option == 'SetNumPSandJ'):
        siteGUI.GUI_Num_PS_Lkd = 1

    # What to do when user presses the PowerSpout numer/jets lock or enters a new number of PS/jets
    if ((siteGUI.GUI_process_option == 'SetLkNumPSandJ') or (siteGUI.GUI_process_option == 'SetNumPSandJ')):
        fetchall()
        # siteGUI.GUI_Num_PS is used in PowerSpout_calc() to effect result
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user enters a new effeciency target for the cable
    if (siteGUI.GUI_process_option == 'SetCableEff'):
        siteGUI.GUI_LockCable = 0
        site.cableLock = 0
        fetchall()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable size required for design loss and confirm results numbers. Includes min conductor size for amps check
        reportAll()

    # What to do when user enters a new cable length
    if (siteGUI.GUI_process_option == 'NewCable'):
        fetchall()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user enters a new target load voltage
    if (siteGUI.GUI_process_option == 'NewCableV'):
        fetchall()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user chooses a new material for the cable.
    if (siteGUI.GUI_process_option == 'NewCableMaterial'):
        previous = site.cable_material
        fetchall()
        site.cable_size = site.cable_size * site.material[site.cable_material] / site.material[previous]

        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable size required for design loss and confirm results numbers. Includes min conductor size for amps check
        reportAll()

    # What to do when user chooses a new cable size based on sqr mm
    if (siteGUI.GUI_process_option == 'NewCablesize'):
        siteGUI.GUI_LockCable = 1
        site.cableLock = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'New mm based cable size selected' + siteGUI.GUI_diag_cr
        siteGUI.GUI_cable_mm_title = 'Cable cross section'
        siteGUI.GUI_cable_AWG_title = 'Next size up cable'
        siteGUI.GUI_cable_mm_AWG = 'mm'
        fetchall()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user chooses a new cable size based on AWG
    if (siteGUI.GUI_process_option == 'NewCableAWG'):
        siteGUI.GUI_LockCable = 1
        site.cableLock = 1
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'New AWG based cable size selected' + siteGUI.GUI_diag_cr
        siteGUI.GUI_cable_mm_AWG = 'AWG'
        siteGUI.GUI_cable_mm_title = 'Metric cross section'
        siteGUI.GUI_cable_AWG_title = 'Cable size'
        fetchall()
        fetchAWG()
        PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
        CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
        reportAll()

    # What to do when user chooses to lock the cable size
    if ((siteGUI.GUI_process_option == 'NewCableAWG') or (siteGUI.GUI_process_option == 'NewCablesize') or (
        siteGUI.GUI_process_option == 'CableLock')):
        #  siteGUI.GUI_diag = siteGUI.GUI_diag + 'Cable size now locked/unlocked' + siteGUI.GUI_diag_cr
        fetchall()
        if (int(siteGUI.GUI_LockCable) == 0):
            site.cableLock = 0
            siteGUI.GUI_cable_mm_AWG = 'mm'
            PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
            CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
            reportAll()

        if (int(siteGUI.GUI_LockCable) == 1):
            site.cableLock = 1
            PowerSpout_calc()  # Calculate number of PowerSpouts required and jet(s) sizes for this water jet power
            CalcCable()  # Calculate the cable loss. Includes min conductor size for amps check
            reportAll()


"""def fetchHTTP_data():
	siteGUI.GUI_initial_data = 1
	siteGUI.GUI_process_option = 'basicdata'
	siteGUI.GUI_meas_sys = 'Metric'
	siteGUI.GUI_PStype = 'PLT'
	siteGUI.GUI_avail_Wflow = '1'
	siteGUI.GUI_penstock_head = '100'
	siteGUI.GUI_penstock_len = '22'
	siteGUI.GUI_penstock_eff_target = '77'
	siteGUI.GUI_penstock_dia = '88mm'
	siteGUI.GUI_PenSLkd = 1
	siteGUI.GUI_Num_PS = 1
	siteGUI.GUI_Num_PS_Lkd = 1
	siteGUI.GUI_turbine_nozzles = 2
	siteGUI.GUI_cable_eff_target = '98'
	siteGUI.GUI_cable_len = '123ft'
	siteGUI.GUI_Dload_V = '66'
	siteGUI.GUI_LockCable = 0
	siteGUI.GUI_cable_material = 'Copper'
	siteGUI.GUI_cable_size = ''
	siteGUI.GUI_cable_AWG = ''

def putHTTP_data():
	response = "{"

	response += "\"initial_data\" : \""+str(siteGUI.GUI_initial_data)+"\", "
	response += "\"avail_Wflow\" : \""+str(siteGUI.GUI_avail_Wflow)+"\", "
	response += "\"Wflow\" : \""+str(siteGUI.GUI_Wflow)+"\", "
	response += "\"penstock_head\" : \""+str(siteGUI.GUI_penstock_head)+"\", "
	response += "\"eff_head\" : \""+str(siteGUI.GUI_eff_head)+"\", "
	response += "\"penstock_len\" : \""+str(siteGUI.GUI_penstock_len)+"\", "
	response += "\"penstock_eff_target\" : \""+str(siteGUI.GUI_penstock_eff_target)+"\", "
	response += "\"penstock_dia\" : \""+str(siteGUI.GUI_penstock_dia)+"\", "
	response += "\"PenSLkd\" : \""+str(siteGUI.GUI_PenSLkd)+"\", "
	response += "\"Num_PS\" : \""+str(siteGUI.GUI_Num_PS)+"\", "
	response += "\"turbine_nozzles\" : \""+str(siteGUI.GUI_turbine_nozzles)+"\", "
	response += "\"Num_PS_Lkd\" : \""+str(siteGUI.GUI_Num_PS_Lkd)+"\", "
	response += "\"jet_dia\" : \""+str(siteGUI.GUI_jet_dia)+"\", "
	response += "\"actual_pipe_eff\" : \""+str(siteGUI.GUI_actual_pipe_eff)+"\", "
	response += "\"Opr_rpm\" : \""+str(siteGUI.GUI_Opr_rpm)+"\", "
	response += "\"PS_pwr_ea\" : \""+str(siteGUI.GUI_PS_pwr_ea)+"\", "
	response += "\"Actual_turbine_electric_pwr\" : \""+str(siteGUI.GUI_Actual_turbine_electric_pwr)+"\", "
	response += "\"cable_eff_target\" : \""+str(siteGUI.GUI_cable_eff_target)+"\", "
	response += "\"cable_len\" : \""+str(siteGUI.GUI_cable_len)+"\", "
	response += "\"Dload_V\" : \""+str(siteGUI.GUI_Dload_V)+"\", "
	response += "\"Aload_V\" : \""+str(siteGUI.GUI_Aload_V)+"\", "
	response += "\"LockCable\" : \""+str(siteGUI.GUI_LockCable)+"\", "
	response += "\"cable_mm_title\" : \""+str(siteGUI.GUI_cable_mm_title)+"\", "
	response += "\"cable_size\" : \""+str(siteGUI.GUI_cable_size)+"\", "
	response += "\"cable_AWG\" : \""+str(siteGUI.GUI_cable_AWG)+"\", "
	response += "\"cable_AWG_title\" : \""+str(siteGUI.GUI_cable_AWG_title)+"\", "
	response += "\"cable_dia_mm_sld\" : \""+str(siteGUI.GUI_cable_dia_mm_sld)+"\", "
	response += "\"cable_dia_mm_str\" : \""+str(siteGUI.GUI_cable_dia_mm_str)+"\", "
	response += "\"cable_amps\" : \""+str(siteGUI.GUI_cable_amps)+"\", "
	response += "\"actual_cable_eff\" : \""+str(siteGUI.GUI_actual_cable_eff)+"\", "
	response += "\"cable_Vgen\" : \""+str(siteGUI.GUI_cable_Vgen)+"\", "
	response += "\"Load_pwr\" : \""+str(siteGUI.GUI_Load_pwr)+"\", "
	response += "\"design_notes_hydro\" : \"\n"+ siteGUI.GUI_design_notes_hydro+"\", "
	response += "\"design_notes_elec\" : \"\n"+siteGUI.GUI_design_notes_elec+"\", "
	response += "\"design_notes_safety\" : \"\n"+siteGUI.GUI_design_notes_safety+"\""
	response += "}"

	return response

print "Content-Type: text/plain\n"
fetchHTTP_data()
process_here()
print putHTTP_data()"""






