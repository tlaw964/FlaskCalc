#!/usr/bin/python
from math import pi, log10, log, sqrt, ceil
import re
import sys      # Needed to find out what platform are using.  sys.platform = win32 or win64? or linux2 or????



# 1/9/2015 Change to alm 19 text for multiple PHP systems where a shutdown PHP risks overspeed of the remaining PHPs

# Major write to provide for adjustment of any input at any time with all parameters updating
# New loss algorithim for PHP performance.
# Iteritive routines enhancement to reduce number of iterations required to solve flow computations


# V1: 10/4/15
# Contribution for PowerSpout Micro Hydro Turbine with Positive Displacement Pump by Alan Ansell (jams.ansell@gmail.com)

# Based on PLT calculator designed and developed by Smithies Technology Ltd
# Email andrew.smithies@paradise.net.nz


class siteGUI:  #   User input or Report or both?        Description
    
    GUI_process_option = 'default'  # The most recently entered item of data entered by the user
    GUI_meas_sys = 'Metric'         # UR  Units system to use  'Metric' or Imperial'
    GUI_revision = 'V1'             # R   Version number
    
    #Strings pertaining to the water supply
    GUI_available_input_flow = ''   # U   either lps or gpm float.  eg '12 lps'  or '23 gpm'
    GUI_actual_IP_flow = ''         # R  actual water flow used
    GUI_input_head = ''             # U  either metres or feet float  eg '34 m' or '100 ft'
    GUI_eff_input_head = ''         # R   head considering pipe pressure loss   eg '34 m' or '100 ft'
    GUI_input_eff = ''              # R   a string of int %.  eg '89 %'
    GUI_input_pipe_diam = ''        # U  either mm or inch float  eg '34 mm' or '1.2 in'
    GUI_input_pipe_len = ''         # U  either metres or feet float  eg '34 m' or '100 ft'
    GUI_lock_penstock_dia = 0       # UR  either 0 or 1. Disables pipe size optimization

    #Strings pertaining to the pump
    GUI_number_of_spouts = ''       # R
    GUI_number_of_jets = ''         # R
    GUI_lock_PHPs_jets = 0          # UR
    GUI_eff_input_head = ''         # R  Effective supply head to PHP considering pipe pressure loss
    GUI_jet_diam = ''               # R
    GUI_pelton_rpm = ''             # R
    GUI_cam_offset = ''             # R  recommended cam offset
    GUI_PHP_deliver_h = ''          # R  output head PHP is working into
    
    #Strings pertaining to the delivery pipe
    GUI_output_head = ''            # U  Delivery pipe output head (m)
    GUI_output_pipe_len = ''        # U  Delivery pipe length
    GUI_output_eff = ''             # R  Target output efficiency
    GUI_output_pipe_diam = ''       # U  Delivery pipe internal diameter
    GUI_lock_OP_pipe_dia = 0        # UR either 0 or 1. A 1 disables output pipe size optimization

    #Strings pertaining to water delivery and user notes
    GUI_total_OP_flow = ''          # R output flow of all PHP
    GUI_total_OP_flow_day  = ''     # R output flow of all PHP per day
    
    GUI_design_notes_hydro = ''     # An empty string for design comments for the end user to read and understand
    GUI_design_notes_safety = ''    # An empty string for design comments for the end user to read and understand
    GUI_diag = ''                   # All diagnostics go to here
    GUI_last_prob = ''              # To capture last issue
    GUIcr = '<br>'                  # Carriage return with a line feed character
    GUI_diag_cr = str('\r\n')       # or '<br>'   # Carriage return with a line feed character
    GUI_revision = str('R01')       # Version number for this PHP maths routine for GUI to display


class site:
    # Inputs and outputs pertaining to the water source for the PHP
    available_input_flow = 5.0  #lps
    actual_IP_flow = 0.0 #lps
    input_head = 4.0  #m
    input_pipe_len = 10.0  #m
    input_eff = 0.0  #dimensionless
    input_pipe_diam = 0.075  #m
    lock_penstock_dia = 0

    # Inputs and outputs pertaining to the pump operation
    number_of_spouts = 1
    number_of_jets = 2
    lock_PHPs_jets = 0
    eff_input_head = 4.0  #m
    jet_diam = 0.0 #mm
    pelton_rpm = 0.0 #rpm
    cam_offset = 0.0 #mm
    PHP_deliver_h = 0.0
    
    # Inputs and outputs pertaining to the delivery pipe
    output_head = 120.0 #m
    output_pipe_len = 1000.0 #m
    output_eff = 0.0 #dimensionless
    output_pipe_diam = 0.015 #m
    lock_OP_pipe_dia = 0

    # Outputs pertaining to water delivery
    total_OP_flow  = 0.0
    total_OP_flow_day = 0.0


    # Variables used internally by this calculator routine
    penstock_Kf = float(0)      # Head Loss = q K for piping fittings in penstock
    Kf_turbine = float(2)       # Head Loss = q K for piping fittings in turbine
    eps = 1.25e-5               # Used in pipe loss calc
    viscosity = 1.32E-03        # kg/m-sec
    density = 999.4             # kg/m^3
    gravity = 9.81              # m/sec^2
    mmm_lps = 1000.00           # lps/m^3/sec
    dis_coeff = 0.83            # functional area of jet is actually smaller than cut size by this ratio
    Vjet = 0.0                  # Jet velocity in m/s
    ideal_jet_sqr_mm = 0.0      # Total site jet cross section in sqr mm and is corrected already with site.dis_coeff
    One_jet_water_W_lim = 800.0 # Water power limit for one jet to get expected warrenteed bearing life
    max_lps4PHP2J = 20.0        # There is a limit to the lps in a PHP as it will be awash with water and not go well (2 jets)
    max_lps4PHP1J = 12.0        # There is a limit to the lps in a PHP as it will be awash with water and not go well (1 jets)
    max_head_at_pelton = 13.15  # This is the max head to the pelton wheel to avoid exceeding 600rpm for PHP pump
    One_jet_dia_lim = 0.02      # Biggest jet diameter in m that works for a turbine
    Two_jet_dia_lim = 0.025     # Biggest jet size to use in a 2 jet turbine. Only applies when very low head
    jet_diam = 0.0              # Jet diameter im mm for installer to use
    pelton_diameter = 0.23      # m
    pelton_eff = 0.7            # Typical pelton wheel efficiency
    max_pelton_rpm = 600.0
    ##  max_jet_diam = 24.0         # mm
    min_pipe_efficiency = 2.0 / 3.0 # Lowest useful input pipe efficiency
    turbine_spd_jet = 0.45      # Turbine linear speed relative to jet speed

    waterWin = 0.0		# These are the energy balance figures
    shaftW = 0.0
    shaftT = 0.0
    waterWout = 0.0

    max_PHP_out_head = 250.0    # Max output pressure permitted from PHP
    PHP_OP_head_rating = 201.0  # If PHP output pressure in m of head is over this then warn user of warrantee issues. 
                                #  Used in pump displacement calculations also for standard load data
    PHP_torque_ratio = 0.132    # Torque load of PHP pump per m of heat per 6mm cam size. Was 0.022 before head fix done
    piston_diameter = 56.0      # mm
    piston_squash = 1.8         # mm of squash in diaphram piston
    PHP_eff = 0.64              # Basic efficiency of PHP pump. Shaft W to water W
    cam = 0.0                   # mm  This is the radial offset of the cam. Stroke is twice this

    min_cam_offset = 1.0        # mm
    max_cam_offset = 6.0        # mm

    
    alarms = []     # Empty list for alarms to be .append(  )ed to as alarm numbers. Valid entries are ints.
                    # Final running of prog may give a list like   [ 2, 5, 10 ]


    # Dictionary of conversion coeffecients. Enter all units here as lower case. All indexing is done via .lower() string function
    convert = { 'lps-lps': 1, 'gpm-lps': 15.87, 'lps-gpm': 0.06301, 'gpm-gpm': 1, 'm-m': 1, 'mm-m': 1000, \
                'l/min-l/min': 1, 'lps-l/min': 60, 'l/min-lps': 60, \
                'l/day-l/day': 1, 'lps-l/day': 60*60*24, 'l/day-lps': 60*60*24, 'g/day-lps': 60*60*24*0.2645,\
                'lps-l/day': 1/(60*60*24), 'lps-g/day': 1/(60*60*24*0.2645), \
                'ft-m': 3.28083989501312, 'in-m': 39.3700787401575, 'm-cm': 0.01, 'mm-cm': 10, 'ft-cm': 0.0328083989501312, \
                'm-psi': 0.703, 'm-kpa': .102, 'm-bar': 10.197, \
                'in-cm': 0.393700787401575, 'm-mm': 0.001, 'mm-mm': 1, 'ft-mm': 0.00328083989501312, 'in-mm': 0.0393700787401575, \
                'm-mile': 1609.344, 'mm-mile': 1609344, 'ft-mile': 5280, 'in-mile': 63360, 'm-ft': 0.3048, 'mm-ft': 304.8, \
                'ft-ft': 1, 'in-ft': 12, 'm-in': 0.0254, 'mm-in': 25.4, 'ft-in': 0.0833333333333333, 'in-in': 1, 'm-th': 0.0000254, \
                'mm-th': 0.0254, 'ft-th': 8.33333333333333E-05, 'in-th': 0.001, 'm-km': 1000, 'awg-awg': 1, \
                'lps-cfs':28.316846592, 'cfs-lps':0.0, '%-%':1, '-':1, 'r-%':0.01   }

    monospace_on = ''
    monospace_off = ''
    Aspace = ' '


    
def calc_head_diff(pipe_diam, flow, pipe_len):  # Return difference between actual and effective head given actual head and pipe diameter and length
    if( flow <= 0.0 ): return(0)   # If flow is 0 or -ve then return 0 pressure drop

    pipe_area = pi * (pipe_diam / 2) * (pipe_diam / 2)
    pipeV = flow / site.mmm_lps / pipe_area
    Qm = 0.5 * pipeV * pipeV / site.gravity
    Re = site.density * pipeV * pipe_diam / site.viscosity
    if Re < 2100:
        Re_consider = 16.0 / Re
    else:
        Re_consider = -1


    if Re_consider == -1:
        x1 = -log10(site.eps / 3.7 - 4.52 / Re * log(7 / Re + site.eps / 7 , 10))
    else:
        x1 = -1

    site.design_Chk = 0
    if (site.eps / 3.7 + 5.02 * x1 / Re) > 0:
        x2 = -log10(site.eps / 3.7 + 5.02 * x1 / Re)
    else:
        x2 = -1
        site.design_Chk = 1

    if (site.eps / 3.7 + 5.02 * x2 / Re) > 0:    
        x3 = -log10(site.eps / 3.7 + 5.02 * x2 / Re)
    else:
        x3 = -1
        site.design_Chk = 1
    
    if (site.eps / 3.7 + 5.02 * x3 / Re) > 0:
        x4 = -log10(site.eps / 3.7 + 5.02 * x3 / Re)
    else:
        x4 = -1
        site.design_Chk = 1
        
    Moodyfff = 1.0 / (16.0 * x4 * x4)

    if x1 == -1:
        f = Re_consider
    else:
        f = Moodyfff

    dp_m = (4.0 * f * pipe_len / pipe_diam + site.penstock_Kf + site.Kf_turbine) * Qm
    #print flow, pipe_area, site.eps, pipeV, Qm, Re, Re_consider, x1, x2, x3, x4, Moodyfff, f, dp_m
    return dp_m



def compute_pipe_input_lps():
    dp_high = calc_head_diff(site.input_pipe_diam, site.actual_IP_flow, site.input_pipe_len)  # If all available water used then dp is...
    max_dp = ( 1 - site.min_pipe_efficiency ) * site.input_head  # Figure allowable max pressure drop in penstock
    converge_prob = "compute_pipe_input_lps(): dp_max, current " + str(max_dp) + " " + str(dp_high) + "\r\n"
    
    if dp_high > max_dp:  # Too much penstock head loss. Find flow rate for 66% penstock eff
        site.alarms.append( 11 )    # 'Less water is being used than is available as the penstock size limits maximum power.\n\tChoose a larger penstock for more power\n\n'
        lps_low = 0
        dp_low = 0
        lps_high = site.actual_IP_flow

        while 1:
            site.penstock_pipe_iterations += 1
            if site.penstock_pipe_iterations > 200:
                site.alarms.append( 10 )        # 'Penstock loss calculations failed.\n\tPlease email a copy of this screen to EcoInnovation'
                siteGUI.GUI_last_prob = converge_prob
                break
            
            # Using straight line interpolation... Best guess option
            lps_holder = lps_low + (lps_high - lps_low ) * (max_dp - dp_low) / ( dp_high - dp_low ) 
            dp_holder = calc_head_diff(site.input_pipe_diam, lps_holder, site.input_pipe_len)
            if dp_holder < max_dp:  # Estimate is for less flow than target
                lps_low = lps_holder
                dp_low = dp_holder
            if dp_holder >= max_dp:  # Estimate is for more flow than target
                lps_high = lps_holder
                dp_high = dp_holder
            converge_prob = converge_prob + "lps find " + str(lps_low) + " " + str(lps_high) + "\r\n"

            # Using plain scaling do another prediction. Helps dramaticlly if way up exponential loss curve
            lps_holder =  ( lps_low + lps_high ) /2
            dp_holder = calc_head_diff(site.input_pipe_diam, lps_holder, site.input_pipe_len)
            if dp_holder < max_dp:  # Estimate is for less flow than target
                lps_low = lps_holder
                dp_low = dp_holder
            if dp_holder >= max_dp:  # Estimate is for more flow than target
                lps_high = lps_holder
                dp_high = dp_holder
            converge_prob = converge_prob + "Two " + str(lps_low) + " " + str(lps_high) + "\r\n"
            


            if abs( 1- dp_holder / max_dp ) < 0.001: # Found answer. pressure drop within 0.1% of requested
                site.actual_IP_flow  = lps_holder
                converge_prob = converge_prob + "compute_pipe_input_lps result is " + str(site.actual_IP_flow) + " lps\r\n"
                break



def compute_pipe_size():
    target_dp = ( 1 - site.input_eff ) * site.input_head
    big_pipe = 2
    big_pipe_loss = calc_head_diff(big_pipe, site.actual_IP_flow, site.input_pipe_len)
    small_pipe = 0.01
    small_pipe_loss = calc_head_diff(small_pipe, site.actual_IP_flow, site.input_pipe_len)

    converge_prob = 'compute_pipe_size(): ' + str(round(target_dp,1)) + ' target dp in m\r\n' 
    
    while 1:
        site.penstock_pipe_iterations += 1
        if site.penstock_pipe_iterations > 200:
            site.alarms.append( 10 )        # 'Penstock loss calculations failed.\n\tPlease email a copy of this screen to EcoInnovation'
            siteGUI.GUI_last_prob = converge_prob
            break
        
        # Using straight line interpolation... Best guess option
        dia_holder = small_pipe + (big_pipe - small_pipe ) * (target_dp - big_pipe_loss) / ( small_pipe_loss - big_pipe_loss )
        dp_holder = calc_head_diff(dia_holder, site.actual_IP_flow, site.input_pipe_len)
        if dp_holder < target_dp:  # Estimate is for a bigger pipe than target pressure drop
            big_pipe = dia_holder
            big_pipe_loss = dp_holder
        if dp_holder >= target_dp:  # Estimate is for more flow than target
            small_pipe = dia_holder
            small_pipe_loss = dp_holder
        #print small_pipe, "\t", small_pipe_loss, "\t", big_pipe, "\t", big_pipe_loss
        converge_prob = converge_prob + "dia find one" + str(small_pipe_loss) + " " + str(big_pipe_loss) + "\r\n"

        # Using plain scaling do another prediction. Helps dramaticlly if way up exponential loss curve
        dia_holder =  ( big_pipe + small_pipe ) /2
        #print dia_holder
        dp_holder = calc_head_diff(dia_holder, site.actual_IP_flow, site.input_pipe_len)
        if dp_holder < target_dp and dp_holder > big_pipe_loss:  # Estimate is for a bigger pipe than target pressure drop
            big_pipe = dia_holder
            big_pipe_loss = dp_holder
        if dp_holder >= target_dp and dp_holder < small_pipe_loss:  # Estimate is for more flow than target
            small_pipe = dia_holder
            small_pipe_loss = dp_holder
        #print small_pipe, "\t", small_pipe_loss, "\t", big_pipe, "\t", big_pipe_loss
        converge_prob = converge_prob + "dia find two " + str(small_pipe_loss) + " " + str(big_pipe_loss) + "\r\n"
        

        # print converge_prob
        
        if abs( 1- dp_holder / target_dp ) < 0.00001: # Found answer. pressure drop within 0.1% of requested
            site.input_pipe_diam = (small_pipe + big_pipe)/2
            converge_prob = converge_prob + "compute_pipe_size dia result is " + str(site.input_pipe_diam) + " m\r\n"
            break



# Calculate the jet power. Reduce lps if required
def calc_jet_power():
    # The jet power is the watts of water power into the PHP. But depends on some constraints...
    # If number PHP is locked then limit water flow to PHP rating
    # If the penstock dia is not locked then work out a new pipe size
    # Call compute_pipe_input_lps() to limit lps based on pipe size
    # Then do basic energy sums to compute the jet power
    # siteGUI.GUI_diag = siteGUI.GUI_diag +\
    #                   str(site.available_input_flow ) + " " +\
    #                   str(site.input_head ) + " " +\
    #                   str(site.input_pipe_len ) + " " +\
    #                   str(site.input_eff ) + " " +\
    #                   str(site.input_pipe_diam  ) + " " +\
    #                   str(site.lock_penstock_dia  ) + " " +\
    #                   "\r\n"

    site.penstock_pipe_iterations = 0   # Track iterations that can go mad and need to know about
    

    # If lock_penstock_dia == 0 then compute new penstock diameter
    if site.lock_penstock_dia == 0:
        converge_prob = "Off to compute_pipe_size()\r\n"
        if site.input_head * site.input_eff > site.max_head_at_pelton:  # Penstock efficiency will over speed PHP at this supply head
            site.input_eff = site.max_head_at_pelton / site.input_head
            #print "Reduced penstock efficiency to prevent overspeed to PHP"
            site.alarms.append( 19 )  # To prevent overspeed of PHP input flow loss has been increased. Check installation for warrentable operation
        compute_pipe_size()
    else:
        # Is penstock efficency low and choked then compute new flow rate
        converge_prob = "Off to compute_actual_input_lps()\r\n"
        compute_pipe_input_lps()
        if site.input_head * site.input_eff > site.max_head_at_pelton:  # Penstock efficiency will over speed PHP at this supply head
            site.input_eff = site.max_head_at_pelton / site.input_head
            #print "Reduced penstock size to reduce efficiency to prevent overspeed to PHP"
            site.alarms.append( 19 )  # To prevent overspeed of PHP input flow loss has been increased. Check installation for warrentable operation
            site.lock_penstock_dia = 0
            compute_pipe_size()

    # Recompute hydro situation so numbers are updated
    dp = calc_head_diff(site.input_pipe_diam, site.actual_IP_flow, site.input_pipe_len)  # If all available water used then dp is...
    site.eff_input_head = site.input_head - dp





    if site.lock_penstock_dia == 1:  # Do not recompute penstock eff if it is the source.
        site.input_eff = site.eff_input_head / site.input_head

    # Figure out jet velocity for this effective head and jet square mm with jet dia
    try:
        site.Vjet = sqrt( 2 * site.gravity * site.eff_input_head )
        site.ideal_jet_sqr_mm = site.actual_IP_flow / site.mmm_lps / site.Vjet / site.dis_coeff #
        site.jet_diam = 2.0 * sqrt( site.ideal_jet_sqr_mm / float(site.number_of_jets ) / float(site.number_of_spouts )  / pi )
        site.pelton_rpm = site.turbine_spd_jet * 60 * site.Vjet /( pi * site.pelton_diameter )
    except:
        site.Vjet = 0
        site.ideal_jet_sqr_mm = 0
        site.jet_diam = 0
        site.pelton_rpm = 0








def calc_OP_lps_dia( Watts ):  # Find lps through given output pipe size at this PHP output power
    min_output_lps = 0   # There will always be some flow. But 0 provides a min for the range.
    min_output_lps_watts = 0
    max_output_lps = site.eff_input_head * site.actual_IP_flow / site.output_head  # If PHP and output pipe 100% eff then output lps is simple
    max_output_lps_watts = ( calc_head_diff(site.output_pipe_diam, max_output_lps, site.output_pipe_len) + site.output_head ) * site.gravity * max_output_lps
    site.out_pipe_iterations = 0
    converge_prob = '/r/ncalc_OP_lps_dia(Watts) with ' + str(round(Watts)) + ' W to find dia for\r\n'
    while 1:
        site.out_pipe_iterations += 1
        if site.out_pipe_iterations > 400:
            site.alarms.append( 12 )        # 'Output pipe loss calculations failed when working out flow capacity.\n\tPlease email a copy of this screen to EcoInnovation'
            #print 'calc_OP_lps_dia too many laps'
            siteGUI.GUI_last_prob = converge_prob
            break
        
        # Using straight line interpolation... Best guess option
        lps_holder = min_output_lps + (max_output_lps - min_output_lps ) * ( Watts - min_output_lps_watts ) / (max_output_lps_watts - min_output_lps_watts ) 
        pumphead = calc_head_diff(site.output_pipe_diam, lps_holder, site.output_pipe_len) + site.output_head
        W_holder = pumphead * site.gravity * lps_holder
        if W_holder < Watts:  # Estimate is for less flow than target
            min_output_lps = lps_holder
            min_output_lps_watts = W_holder
        if W_holder > Watts:  # Estimate is for more flow than target
            max_output_lps = lps_holder
            max_output_lps_watts = W_holder
        converge_prob = converge_prob + "Out lps 1 find " + str(min_output_lps) + " " + str(max_output_lps) + "\r\n"

        # Using plain scaling do another prediction. Helps dramaticlly if way up exponential loss curve
        lps_holder =  ( min_output_lps + max_output_lps ) /2
        pumphead = calc_head_diff(site.output_pipe_diam, lps_holder, site.output_pipe_len) + site.output_head
        W_holder = pumphead * site.gravity * lps_holder
        if W_holder < Watts:  # Estimate is for less flow than target
            min_output_lps = lps_holder
            min_output_lps_watts = W_holder
        if W_holder > Watts:  # Estimate is for more flow than target
            max_output_lps = lps_holder
            max_output_lps_watts = W_holder
        converge_prob = converge_prob + str(site.out_pipe_iterations) + " Out lps 2 find " +\
                           str(round(min_output_lps,4)) + " " + str(round(max_output_lps,4)) +" "+\
                           str(round(lps_holder,4)) +" "+ str(round(pumphead,4)) +" "+\
                           str(round(Watts,2)) +" "+ str(round(W_holder,2)) + "\r\n"
        


        if abs( W_holder - Watts ) < 0.1 or\
           ( abs( W_holder - Watts ) < 1.0 and site.out_pipe_iterations > 20) or\
           ( abs( W_holder - Watts ) < 10.0 and site.out_pipe_iterations > 100): # Found answer. pressure drop within 0.1% of requested
            site.total_OP_flow  = lps_holder
            site.PHP_deliver_h = pumphead
            site.output_eff = site.output_head / pumphead
            # print siteGUI.GUI_diag
            break






        

def calc_OP_dia_eff( Watts ):  # Use efficiency for output pipe and compute output pipe dia for wanted losses at this PHP output flow
    if (site.output_head / site.output_eff) > site.max_PHP_out_head:  #Check is user supplied efficiency would over load PHP
        site.alarms.append( 13 )        # To much PHP delivery pressure. Output efficiency increased to meet PHP limits
        site.output_eff = float(site.output_head) / float(site.max_PHP_out_head)

    converge_prob = 'calc_OP_dia_eff(Watts) with ' + str(round(Watts,1)) + ' W to find diameter for\r\n'
    # PHP output power into delivery pipe of given efficiency defines...
    site.PHP_deliver_h = site.output_head / site.output_eff
    site.total_OP_flow = Watts / site.PHP_deliver_h / site.gravity
    deliver_pipe_dp = site.PHP_deliver_h - site.output_head

    # Figure out pipe size for output pressure drop to be deliver_pipe_dp
    min_dia = 0.001   # There will always be some diameter. But 1 provides a min for the range.
    min_dia_dp = calc_head_diff(min_dia, site.total_OP_flow, site.output_pipe_len)
    max_dia = 1.0
    max_dia_dp = calc_head_diff(max_dia, site.total_OP_flow, site.output_pipe_len)
    
    site.out_pipe_iterations = 0
    while 1:
        site.out_pipe_iterations += 1
        if site.out_pipe_iterations > 200:
            siteGUI.GUI_last_prob = converge_prob
            site.alarms.append( 14 )        # 'Output pipe loss calculations failed when figuring output pipe diameter.\n\tPlease email a copy of this screen to EcoInnovation'
            break
        
        # Using straight line interpolation... Best guess option
        dia_holder = min_dia + (max_dia - min_dia ) * ( min_dia_dp - deliver_pipe_dp ) / (min_dia_dp - max_dia_dp ) 
        dp_holder = calc_head_diff(dia_holder, site.total_OP_flow, site.output_pipe_len)

        if dp_holder < deliver_pipe_dp:  # Estimate is for less pressure drop with a larger dia pipe than target
            max_dia = dia_holder
            max_dia_dp = dp_holder
        if dp_holder > deliver_pipe_dp:  # Estimate is for more pressure drop with a smaller dia pipe than target
            min_dia = dia_holder
            min_dia_dp = dp_holder
        converge_prob = converge_prob + "Out dia 1 find " + str(min_dia) + " " + str(max_dia) + "\r\n"

        # Using plain scaling do another prediction. Helps dramaticlly if way up exponential loss curve
        dia_holder =  ( min_dia + max_dia ) /2
        dp_holder = calc_head_diff(dia_holder, site.total_OP_flow, site.output_pipe_len)
        
        if dp_holder < deliver_pipe_dp:  # Estimate is for less pressure drop with a larger dia pipe than target
            max_dia = dia_holder
            max_dia_dp = dp_holder
        if dp_holder > deliver_pipe_dp:  # Estimate is for more pressure drop with a smaller dia pipe than target
            min_dia = dia_holder
            min_dia_dp = dp_holder
        converge_prob = converge_prob + "Out dia 2 find " + str(round(min_dia,4)) + " " + str(round(max_dia,4)) +" "+\
                           str(round(dia_holder,4)) +" "+ str(round(dp_holder,4)) + "\r\n"
        


        if abs( 1- dp_holder / deliver_pipe_dp ) < 0.001: # Found answer. pressure drop within 0.1% of requested
            site.output_pipe_diam   = dia_holder
            break





def calc_water_balance():
    calc_jet_power()    # This finds a penstock size or reduces site.actual_IP_flow to solve penstock limitations

    # Use the water jet watts to estimate PHP output watts
    site.waterWin = site.actual_IP_flow * site.gravity * site.eff_input_head
    site.shaftW = site.waterWin * site.pelton_eff
    site.waterWout = site.shaftW * site.PHP_eff 
    if site.lock_OP_pipe_dia == 1:  # If output pipe size is locked then 
        calc_OP_lps_dia( site.waterWout ) # Find OP lps for current output pipe diameter and available PHP output power
    else:
        calc_OP_dia_eff( site.waterWout ) # Use efficiency for output pipe and compute output pipe dia losses at this PHP output power






def calc_OP_water_reduce():
    # This section reduces input flow to reduce input power to reduce PHP output presure to 250m
    site.out_pipe_reduce_iterations = 0
    if site.PHP_deliver_h > site.max_PHP_out_head:  # If too much output pressure then need to reduce input lps untill site.PHP_deliver_h == max_PHP_out_head
        siteGUI.GUI_diag = siteGUI.GUI_diag + " Reducing IP lps to suit over lossy output pipe\r\n"
        site.alarms.append( 20 ) # The output pipe loss is causing the PHP output pressure to be excessive. Input water flow has been reduced to get less output pipe loss at a lower pump flow.'
        min_output_h_lps = 0.0   # There will always be some flow. 0 though so have a range.
        min_output_h = 0.0
        max_output_h_lps = site.actual_IP_flow
        keep_IP_flow = site.actual_IP_flow
        max_output_h = site.max_PHP_out_head

        converge_prob = '\r\ncalc_OP_water_reduce():  Find input lps for 250m head instead of ' + ('              ' + str(round(site.PHP_deliver_h,6)))[-11:] + '\r\n'

        while 1:
            site.out_pipe_reduce_iterations += 1
            if site.out_pipe_reduce_iterations > 200:
                site.alarms.append( 15 )        # Throughput calculations failed when figuring reduced input water to suit restricted delivery pipe. Please email a copy of this screen to EcoInnovation'
                siteGUI.GUI_last_prob = converge_prob
                break
            
            # Using straight line interpolation... Best guess option
            site.actual_IP_flow = max_output_h_lps - (max_output_h_lps - min_output_h_lps ) * \
                                  (site.PHP_deliver_h - site.max_PHP_out_head ) / ( max_output_h - min_output_h )
            if site.actual_IP_flow < min_output_h_lps or site.actual_IP_flow > max_output_h_lps:
                site.actual_IP_flow =  ( min_output_h_lps + max_output_h_lps ) /2

            converge_prob = converge_prob + str(site.out_pipe_reduce_iterations) + " Use " + \
                            ('              ' + str(round(site.actual_IP_flow,6)))[-8:] + ' lps for 1 find     ' + "\r\n"
            if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0

            # Reprocess all hydro in and out numbers
            calc_water_balance()

            if site.PHP_deliver_h < site.max_PHP_out_head and min_output_h_lps < site.actual_IP_flow:  # Estimate is for more pump pressure than pump rating
                min_output_h_lps = site.actual_IP_flow
                min_output_h = site.PHP_deliver_h
            if site.PHP_deliver_h > site.max_PHP_out_head and max_output_h_lps > site.actual_IP_flow: # Estimate is for more pump pressure than pump rating
                max_output_h_lps = site.actual_IP_flow
                max_output_h = site.PHP_deliver_h
            
            converge_prob = converge_prob + str(site.out_pipe_reduce_iterations) + " In lps for out pressure 1 find " + \
                            ('              ' + str(round(site.PHP_deliver_h,6)))[-11:] + '     ' +\
                            ('              ' + str(round(min_output_h_lps,6)))[-11:] + '     ' +\
                            ('              ' + str(round(min_output_h,6)))[-11:] + '     ' +\
                            ('              ' + str(round(max_output_h_lps,6)))[-11:] + '     ' + \
                            ('              ' + str(round(max_output_h,6)))[-11:] + "\r\n"

            # Using plain subdivision do another prediction. Helps dramaticlly if way up exponential loss curve
            site.actual_IP_flow =  ( min_output_h_lps + max_output_h_lps ) /2
            converge_prob = converge_prob + str(site.out_pipe_reduce_iterations) + " Use " + \
                            ('              ' + str(round(site.actual_IP_flow,6)))[-8:] + ' lps for 2 find     ' + "\r\n"
            if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0

            # Reprocess all hydro in and out numbers
            calc_water_balance()

            if site.PHP_deliver_h < site.max_PHP_out_head:  # Estimate is for more pump pressure than pump rating
                min_output_h_lps = site.actual_IP_flow
                min_output_h = site.PHP_deliver_h
            if site.PHP_deliver_h > site.max_PHP_out_head:  # Estimate is for more pump pressure than pump rating
                max_output_h_lps = site.actual_IP_flow
                max_output_h = site.PHP_deliver_h
            converge_prob = converge_prob + str(site.out_pipe_reduce_iterations) + " In lps for out pressure 2 find " + \
                            ('              ' + str(round(site.PHP_deliver_h,6)))[-11:] + '     ' +\
                            ('              ' + str(round(min_output_h_lps,6)))[-11:] + '     ' +\
                            ('              ' + str(round(min_output_h,6)))[-11:] + '     ' +\
                            ('              ' + str(round(max_output_h_lps,6)))[-11:] + '     ' + \
                            ('              ' + str(round(max_output_h,6)))[-11:] + "\r\n"


            if abs( 1.0 - site.PHP_deliver_h / site.max_PHP_out_head ) < 0.001: # Found answer. pressure drop within 0.1% of requested
                break # All hydro parameters are all done as used global class variables

            if max_output_h_lps - min_output_h_lps < 0.01 and site.out_pipe_reduce_iterations > 20:
                site.alarms.append( 23 )        # This prediction is based on output pipe losses which are very dependant on site installation and materials. This is a perfomance estimate.'
                break
            




def calc_hydro_ballance():  # Computes hydro and then figures out PHP count and limits. Then reruns hydro again
    calc_water_balance()    # Computes all water in and out balance equations and assumes endless PHP capacity
    #print 'have done   calc_water_balance()'

    calc_OP_water_reduce()  # Only does anything if output pipe is a restriction
    #print 'have done   calc_OP_water_reduce()'


    # Either work out the PHPs needed for the above OR reduce input water to reflect reduced PHP count or PHP jets and recompute
    if site.lock_PHPs_jets == 0:  # Just compute the number of PHPs

        # Work out max and min torque PHP can apply according to cam size for this output head
        min_PHP_T = site.PHP_deliver_h * site.PHP_torque_ratio * site.min_cam_offset / site.max_cam_offset 
        max_PHP_T = site.PHP_deliver_h * site.PHP_torque_ratio * site.max_cam_offset / site.max_cam_offset
        # Work out the torque the pelton wheel can produce at max flow for this effective input head.
        # Have design rpm in site.pelton_rpm, shaft power in site.shaftW
        site.shaftT = site.shaftW / site.pelton_rpm * 60.0 / pi / 2.0  # This is the sum torque of all installed PHPs.
        if site.shaftT < min_PHP_T:
            site.alarms.append( 24 )        # Not enough torque for this configuration. You need more water supply per PHP or less output head.
            #print 'Not enough torque for this site even if all water in 1 PHP'
        torque_needed_PHPs = site.shaftT / max_PHP_T 

        #print 'Compute the number of PHPs d'
        # Consider water into the PHPs. There is a max jet size and max lps limit to uses the pelton buckets properly and not flood the wheel space
        # How many jets needed to to stay under the site.Two_jet_dia_lim  limit? site.ideal_jet_sqr_mm is the jet area required
        jets_needed = site.ideal_jet_sqr_mm / ( pi * (site.Two_jet_dia_lim / 2.0)**2 ) 
        jets_needed_PHPs = jets_needed / 2.0                         # Number of PHPs for this amount of jet size
        water_needed_PHPs = site.actual_IP_flow / site.max_lps4PHP2J # Number of PHPs for this water volume

        #print 'Compute the number of PHPs e'
        # PHP pump can only move so much water per revolution. For output flow how many needed at this site.pelton_rpm
        max_cam_displacement = (site.piston_diameter/2 )**2 * pi * 2.0 * \
                               (6.0 * 2.0-(site.piston_squash * site.PHP_deliver_h / site.PHP_OP_head_rating  )) / 1000000
        disp_needed_PHPs = site.total_OP_flow / max_cam_displacement / site.pelton_rpm * 60
        
        req_PHP = max( torque_needed_PHPs, jets_needed_PHPs, water_needed_PHPs, disp_needed_PHPs )
        site.number_of_spouts = int(round( 0.5+ req_PHP ))
        #print 'Compute the number of PHPs e'
        #print "to handle water T ", torque_needed_PHPs, "  For jet size ", jets_needed_PHPs, "   For water lps ", water_needed_PHPs, "    For OP flow PHPs ", disp_needed_PHPs
        """if req_PHP == torque_needed_PHPs:
            #print 'PHP count is to use available torque'
        if req_PHP == jets_needed_PHPs:
            #print 'PHP count is to have enough jet size'
        if req_PHP == water_needed_PHPs:
            #print 'PHP count is to use all input water flow'
        if req_PHP == disp_needed_PHPs:
            #print 'PHP count is to produce output water flow'"""
        site.number_of_jets = 2

        if site.shaftT / site.number_of_spouts < min_PHP_T:
            site.alarms.append( 24 )        # Not enough torque for this configuration. You need more water supply per PHP or less output head.
            #print 'Not enough torque for this site for these PHP(s)'






    else: # Use the current site.number_of_spouts and site.number_of_jets to ensure are in operating range for everything
        # For each of the constraints need to reduce input water flow and recompute converged result
        #print ' compute for the PHP limits'

        # A PHP has a max lps water handling.
        flag = 0
        if site.number_of_jets == 2:
            if site.actual_IP_flow > site.max_lps4PHP2J * site.number_of_spouts:
                site.actual_IP_flow = site.max_lps4PHP2J * site.number_of_spouts
                flag = 1
        if site.number_of_jets == 1:
            if site.actual_IP_flow > site.max_lps4PHP1J * site.number_of_spouts:
                site.actual_IP_flow = site.max_lps4PHP1J * site.number_of_spouts
                flag = 1

        if flag == 1:  # Recompute if new flow rates.
            calc_water_balance()    # Computes all water in and out balance equations and assumes endless PHP capacity
            calc_OP_water_reduce()  # Only does anything if output pipe is a restriction


        
        # There is input power limit via jet size
        if site.number_of_jets == 2:
            available_jet_area = ( pi * (site.Two_jet_dia_lim / 2.0)**2 ) * site. number_of_spouts * 2
        if site.number_of_jets == 1:
            available_jet_area = ( pi * (site.Two_jet_dia_lim / 2.0)**2 ) * site. number_of_spouts

        if site.ideal_jet_sqr_mm > available_jet_area:  # Need to reduce input water untill jet area is matched
            site.jet_reduce_iterations = 0
            converge_prob = " Reducing IP lps to suit lack of jet area for fixed PowerSpout count\r\n"
            site.alarms.append( 21 ) # Reducing the input water flow to suit available jet area
            
            min_in_lps = 0.0   # There will always be some flow. 0 though so have a range.
            min_in_area = 0.0
            max_in_lps = site.actual_IP_flow
            max_in_area = site.ideal_jet_sqr_mm
            
            while 1:
                site.jet_reduce_iterations += 1
                if site.jet_reduce_iterations > 100:
                    site.alarms.append( 17 )        # Input flow calculation to suit jet size calculation failed.\n\tPlease email a copy of this screen to EcoInnovation
                    siteGUI.GUI_last_prob = converge_prob
                    break
                
                # Using straight line interpolation... Best guess option
                site.actual_IP_flow = min_in_lps + (max_in_lps - min_in_lps ) * \
                                      (available_jet_area - min_in_area ) / ( max_in_area - min_in_area )
                if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0
                # Reprocess all hydro in and out numbers
                calc_water_balance()

                if site.ideal_jet_sqr_mm > available_jet_area:  # Estimate is for more input water than jets can use
                    max_in_lps = site.actual_IP_flow
                    max_in_area = site.ideal_jet_sqr_mm
                if site.ideal_jet_sqr_mm < available_jet_area:  # Estimate is for more input water than jets can use
                    min_in_lps = site.actual_IP_flow
                    min_in_area = site.ideal_jet_sqr_mm
                converge_prob = converge_prob + str(site.jet_reduce_iterations) + " jet area lps reduce " + str(min_in_lps) + " " + str(max_in_lps) + "\r\n"

                # Using plain subdivision do another prediction. Helps dramaticlly if way up exponential loss curve
                site.actual_IP_flow =  ( min_in_lps + max_in_lps ) /2
                if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0
                # Reprocess all hydro in and out numbers
                calc_water_balance()

                if site.ideal_jet_sqr_mm > available_jet_area:  # Estimate is for more input water than jets can use
                    max_in_lps = site.actual_IP_flow
                    max_in_area = site.ideal_jet_sqr_mm
                if site.ideal_jet_sqr_mm < available_jet_area:  # Estimate is for more input water than jets can use
                    min_in_lps = site.actual_IP_flow
                    min_in_area = site.ideal_jet_sqr_mm
                converge_prob = converge_prob + str(site.jet_reduce_iterations) + " jet area lps reduce " + str(min_in_lps) + " " + str(max_in_lps) + "\r\n"


                if abs( 1- site.ideal_jet_sqr_mm / available_jet_area ) < 0.001: # Found answer. pressure drop within 0.1% of requested
                    break # All hydro parameters are all done as used global class variables



        calc_OP_water_reduce()  # Only does anything if output pipe is a restriction
        # PHP pump has a max output flow rate as displacement is limited
        # PHP pump can only move so much water per revolution. For output flow how many needed at this site.pelton_rpm
        max_cam_displacement = (site.piston_diameter/2 )**2 * pi * 2.0 * \
                               (6.0 * 2.0-(site.piston_squash * site.PHP_deliver_h / site.PHP_OP_head_rating  )) / 1000000
        max_poss_flow = max_cam_displacement * site.pelton_rpm / 60 * site.number_of_spouts





        if site.total_OP_flow > max_poss_flow:
            #print "Cannot pump this much water through a PHP. Reducing input lps to suit"
            site.OP_flow_reduce_iterations = 0
            site.alarms.append( 22 ) # Too much water power for PHP to use. Reducing the input water flow to suit PHP capacity
            converge_prob = "Reducing IP lps to suit lack of PHP displacement for fixed PowerSpout count\r\n"

            min_in_lps = 0.0   # There will always be some flow. Use 0 though so have a range.
            min_in_outflow = 0.0
            max_in_lps = site.actual_IP_flow
            max_in_outflow = site.total_OP_flow
            
            while 1:
                site.OP_flow_reduce_iterations += 1
                if site.OP_flow_reduce_iterations > 100:
                    site.alarms.append( 18 )        # A PHP pump has a limited pump rate for a given rpm. Supply water has been reduced to match capacity
                    siteGUI.GUI_last_prob = converge_prob
                    break
                
                # Using straight line interpolation... Best guess option
                site.actual_IP_flow = min_in_lps + (max_in_lps - min_in_lps ) * \
                                      (site.total_OP_flow - min_in_outflow ) / ( max_in_outflow - min_in_outflow )
                if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0
                # Reprocess all hydro in and out numbers
                calc_water_balance()

                if site.total_OP_flow > max_poss_flow:          # Estimate is for more output water than PHP can pump
                    max_in_lps = site.actual_IP_flow
                    max_in_outflow = site.total_OP_flow
                if site.total_OP_flow < max_poss_flow:          # Estimate is for less output water than PHP can pump
                    min_in_lps = site.actual_IP_flow
                    min_in_outflow = site.total_OP_flow
                converge_prob = converge_prob + str(site.OP_flow_reduce_iterations) + " PHP displacement 1 lps reduce " + str(min_in_lps) + " " + str(max_in_lps) + "\r\n"

                # Using plain subdivision do another prediction. Helps dramaticlly if way up exponential loss curve
                site.actual_IP_flow =  ( min_in_lps + max_in_lps ) /2
                if site.actual_IP_flow < 0.0: site.actual_IP_flow = 0.0
                # Reprocess all hydro in and out numbers
                calc_water_balance()

                if site.total_OP_flow > max_poss_flow:          # Estimate is for more output water than PHP can pump
                    max_in_lps = site.actual_IP_flow
                    max_in_outflow = site.total_OP_flow
                if site.total_OP_flow < max_poss_flow:          # Estimate is for less output water than PHP can pump
                    min_in_lps = site.actual_IP_flow
                    min_in_outflow = site.total_OP_flow
                converge_prob = converge_prob + str(site.OP_flow_reduce_iterations) + " PHP displacement 2 lps reduce " + str(min_in_lps) + " " + str(max_in_lps) + "\r\n"


                if abs( 1- site.total_OP_flow / max_poss_flow ) < 0.001: # Found answer. Output flow within 0.1% of requested
                    break # All hydro parameters are all done as used global class variables

    

        # Work out the cam size required. Have site.pelton_rpm, site.total_OP_flow, site.number_of_spouts as well as pump dimensions
        displ_req_per_PHPrev = site.total_OP_flow / site.number_of_spouts / site.pelton_rpm * 60 # Whole site displacement per rev
        needed_stroke = displ_req_per_PHPrev/ site.number_of_spouts  / ((site.piston_diameter/2 )**2 * pi * 2.0)  *1000000  # Is mm of stroke
        raw_cam = (needed_stroke + site.piston_squash * site.PHP_deliver_h / site.PHP_OP_head_rating  ) / 2.0
        site.cam_offset = int(round(raw_cam))
        #print raw_cam, needed_stroke, site.piston_squash, site.PHP_deliver_h, site.PHP_OP_head_rating
        #print "req PHP disp. / rev =", displ_req_per_PHPrev, "   Needed stroke = ", needed_stroke, "   raw_cam is", raw_cam, "mm"
        #print "Proportion of PHP capacity used ", req_PHP / site.number_of_spouts
        siteGUI.GUI_diag = siteGUI.GUI_diag + "Raw cam size is " + str(round(raw_cam,3)) + "\r\n"
        #print "Raw cam size is ", round(raw_cam,3)
        # Redo water calc to update everythng for the user
        calc_water_balance()    # Computes all water in and out balance equations and assumes endless PHP capacity
        calc_OP_water_reduce()  # Only does anything if output pipe is a restriction

       

        # PHP pump has a max head it can pump too cause of limited input torque
        site.shaftT = site.shaftW / site.pelton_rpm * 60.0 / pi / 2.0  # This is the sum torque of all installed PHPs.
        min_PHP_T = site.PHP_deliver_h* site.PHP_torque_ratio * site.min_cam_offset / site.max_cam_offset
        if site.shaftT / site.number_of_spouts < min_PHP_T:
            site.alarms.append( 24 )        # Not enough torque for this configuration. You need more water supply per PHP or less output head.
            #print 'Not enough torque for this configuration. You need more water supply per PHP or less output head'



    # Work out the cam size required. Have site.pelton_rpm, site.total_OP_flow, site.number_of_spouts as well as pump dimensions
    displ_req_per_PHPrev = site.total_OP_flow / site.number_of_spouts / site.pelton_rpm * 60 # Whole site displacement per rev
    needed_stroke = displ_req_per_PHPrev/ site.number_of_spouts  / ((site.piston_diameter/2 )**2 * pi * 2.0)  *1000000  # Is mm of stroke
    raw_cam = (needed_stroke + site.piston_squash * site.PHP_deliver_h / site.PHP_OP_head_rating  ) / 2.0
    site.cam_offset = int(round(raw_cam))
    #print raw_cam, needed_stroke, site.piston_squash, site.PHP_deliver_h, site.PHP_OP_head_rating
    #print "req PHP disp. / rev =", displ_req_per_PHPrev, "   Needed stroke = ", needed_stroke, "   raw_cam is", raw_cam, "mm"
    #print "Proportion of PHP capacity used ", req_PHP / site.number_of_spouts
    siteGUI.GUI_diag = siteGUI.GUI_diag + "Raw cam size is " + str(round(raw_cam,3)) + "\r\n"
    # print "Raw cam size is ", round(raw_cam,3)
    # Redo water calc to update everythng for the user
    calc_water_balance()    # Computes all water in and out balance equations and assumes endless PHP capacity
    calc_OP_water_reduce()  # Only does anything if output pipe is a restriction






def report_user_notes():
    if sys.platform[:5] == 'linux':
        site.monospace_on = '<span style=\'font-family:monospace;\'><span style=\'font-size:x-small;\'>'
        site.monospace_off = '</span></span></span>'
        site.Aspace = '&nbsp;'
        siteGUI.GUIcr = '<br>'
    else:
        site.Aspace = ' '
        site.monospace_on = ''
        site.monospace_off = ''
        siteGUI.GUIcr = '\r\n'
        
    siteGUI.GUI_design_notes_hydro = ''
    siteGUI.GUI_diag = siteGUI.GUI_diag + siteGUI.GUI_last_prob

    if( site.PHP_deliver_h > site.PHP_OP_head_rating ):
        site.alarms.append( 25 )        # Warrantee warning for high output pressure




    for alm in range(10, 30+1):
        if alm in site.alarms:
            if( alm == 10 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Penstock loss calculations failed.' + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 11 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Less water is being used than is available as the input pipe size limits maximum output flow.'\
                + siteGUI.GUIcr + 'Choose a larger pipe for more output flow.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 12 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Output pipe loss calculations failed when working out flow capacity.'\
                + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr
            
            if( alm == 13 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'To much PHP delivery pressure. Output pipe efficiency has been increased to meet PHP pressure limit'\
                 + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 14 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Output pipe loss calculations failed when figuring output pipe diameter.'\
                + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr
           
            if( alm == 15 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Throughput calculations failed when figuring reduced input water to suit restricted delivery pipe.'\
                + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr


            if( alm == 17 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Input flow calculation to suit jet size calculation failed.'\
                + siteGUI.GUIcr + 'Please email a copy of this screen to EcoInnovation. Sorry. This should not have happened and we want to fix this.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 18 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'A PHP pump has a limited pump rate for a given rpm. Supply water has been reduced to match capacity. More PHPs would pump more water.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 19 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'To prevent overspeed of PHP input flow has been reduced with an unusually small input pipe. Check installation for warrentable operation as this is an approximate prediction.' + siteGUI.GUIcr + siteGUI.GUIcr
            if( alm == 19 and site.number_of_spouts >= 2 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'You have multiple PHPs. If one is not in use then the other(s) PHP will overspeed. Do not operate only one PHP.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 20 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'The output pipe loss is causing the PHP output pressure to be excessive. Input water flow is reduced to get less ouput pipe loss at a lower pump speed.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 21 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Reducing the input water flow to suit available jet area.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 22 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'Too much water power for PHP to use. Reducing the input water flow to suit PHP capacity.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 23 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'This prediction is based on output pipe losses which are very dependant on site installation and materials. This is a perfomance estimate. PHP delivery pressure and output pipe losses are not accurate.' + siteGUI.GUIcr + siteGUI.GUIcr

            if( alm == 24 ):
                siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                    'Not enough torque from pelton wheel for this configuration. You need more water supply per PHP or less output head.' + siteGUI.GUIcr + siteGUI.GUIcr
                site.total_OP_flow = 0.0

            if( alm == 25 ): siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + \
                'PHP output pressure is warranted to 200m. The pump will operate at up to 250m output pressure but without warrantee. This is at your own risk. You have been warned...' + siteGUI.GUIcr + siteGUI.GUIcr




    siteGUI.GUI_design_notes_hydro = site.monospace_on + siteGUI.GUI_design_notes_hydro + site.monospace_off + siteGUI.GUIcr
    siteGUI.GUI_design_notes_hydro.replace(' ',site.Aspace)








def report_all():  # Report all results to user gui. This is the only place where gui values get updated for the user to see
    put_available_input_flow()
    put_actual_IP_flow()
    put_input_head()
    put_input_pipe_len()
    put_input_eff_target()
    put_input_pipe_diam()
    put_lock_penstock_dia()

    put_number_of_spouts()
    put_number_of_jets()
    put_lock_number_of_spouts_and_jets()
    put_eff_input_head()
    put_jet_diam()
    put_pelton_rpm()
    put_cam_offset()
    put_PHP_deliver_h()

    put_output_head()
    put_output_pipe_len()
    put_output_eff_target()
    put_output_pipe_diam()
    put_lock_OP_pipe_dia()

    put_total_OP_flow()
    put_total_OP_flow_day()



def put_available_input_flow():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_available_input_flow = str(round(site.available_input_flow, 1)) + ' lps'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_available_input_flow = str(round(site.available_input_flow * site.convert[ 'gpm-lps' ]  , 1)) + ' gpm'

def put_actual_IP_flow():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_actual_IP_flow = str(round(site.actual_IP_flow, 1)) + ' lps'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_actual_IP_flow = str(round(site.actual_IP_flow * site.convert[ 'gpm-lps' ]  , 1)) + ' gpm'

def put_input_head():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_input_head = str(round(site.input_head, 1)) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_input_head = str(round(site.input_head * site.convert[ 'ft-m' ] , 1)) + ' ft'

def put_input_pipe_len():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_input_pipe_len = str(int(round(site.input_pipe_len, 0))) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_input_pipe_len = str(int(round(site.input_pipe_len * site.convert[ 'ft-m' ] , 0))) + ' ft'

def put_input_eff_target():
    siteGUI.GUI_input_eff = str(int(round(site.input_eff * 100, 0))) + ' %'

def put_input_pipe_diam():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_input_pipe_diam = str(int(round(site.input_pipe_diam * site.convert[ 'mm-m' ], 0))) + ' mm'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_input_pipe_diam = str(round(site.input_pipe_diam * site.convert[ 'in-m' ] , 2)) + ' in'

def put_lock_penstock_dia():  
    siteGUI.GUI_lock_penstock_dia = site.lock_penstock_dia

def put_number_of_spouts():
    siteGUI.GUI_number_of_spouts = site.number_of_spouts
    
def put_number_of_jets():
    siteGUI.GUI_number_of_jets = site.number_of_jets

def put_lock_number_of_spouts_and_jets():  
    siteGUI.GUI_lock_PHPs_jets = site.lock_PHPs_jets

def put_eff_input_head():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_eff_input_head = str(round(site.eff_input_head, 1)) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_eff_input_head = str(round(site.eff_input_head * site.convert[ 'ft-m' ] , 1)) + ' ft'
        
def put_jet_diam():
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        siteGUI.GUI_jet_diam = str(round(site.jet_diam * site.convert[ 'mm-m' ] ,1) ) + ' mm'
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        siteGUI.GUI_jet_diam = str(round(site.jet_diam * site.convert[ 'in-m' ] ,2) )  + ' in'

def put_pelton_rpm():
    siteGUI.GUI_pelton_rpm = str(round(site.pelton_rpm, 0)) + ' rpm'

def put_cam_offset():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_cam_offset = str(round(site.cam_offset, 1)) + ' mm'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_cam_offset = str(round(site.cam_offset * site.convert[ 'in-mm' ] , 2)) + ' in'

def put_PHP_deliver_h():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_PHP_deliver_h = str(round(site.PHP_deliver_h, 1)) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_PHP_deliver_h = str(round(site.PHP_deliver_h * site.convert[ 'ft-m' ] , 1)) + ' ft'

def put_output_head():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_output_head = str(round(site.output_head, 1)) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_output_head = str(round(site.output_head * site.convert[ 'ft-m' ] , 1)) + ' ft'

def put_output_pipe_len():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_output_pipe_len = str(int(round(site.output_pipe_len, 0))) + ' m'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_output_pipe_len = str(int(round(site.output_pipe_len * site.convert[ 'ft-m' ] , 0))) + ' ft'

def put_output_eff_target():
    siteGUI.GUI_output_eff = str(int(round(site.output_eff * 100, 0))) + ' %'

def put_output_pipe_diam():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_output_pipe_diam = str(int(round(site.output_pipe_diam * site.convert[ 'mm-m' ], 0))) + ' mm'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_output_pipe_diam = str(round(site.output_pipe_diam * site.convert[ 'in-m' ] , 2)) + ' in'

def put_lock_OP_pipe_dia():  
    siteGUI.GUI_lock_OP_pipe_dia = site.lock_OP_pipe_dia

def put_total_OP_flow():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_total_OP_flow = str(round(site.total_OP_flow, 3)) + ' lps     ' +\
                                    str(round(site.total_OP_flow * site.convert[ 'l/min-lps' ], 2)) + ' l/min'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_total_OP_flow = str(round(site.total_OP_flow * site.convert[ 'gpm-lps' ] , 2)) + ' gpm  '
        
def put_total_OP_flow_day():
    if(siteGUI.GUI_meas_sys == 'Metric'):
        siteGUI.GUI_total_OP_flow_day = str(int(round(site.total_OP_flow * site.convert[ 'l/day-lps' ] , 0))) + ' l/day'
    if(siteGUI.GUI_meas_sys == 'Imperial'):
        siteGUI.GUI_total_OP_flow_day = str(int(round(site.total_OP_flow * site.convert[ 'g/day-lps' ] , 0))) + ' g/day'

    







def fetch_all():  # Fetch all user inputs
    fetch_available_input_flow()  # Get users lps entered.  Only called from fetch_all() and BasicData()
    fetch_input_head()  # Get site head entered.  Only called from fetch_all() and newBasicData()
    fetch_input_pipe_len()  # Get this site data entered.  Only called from fetch_all()
    fetch_input_eff_target()  # Get this site data entered.  Only called from fetch_all()
    fetch_input_pipe_diam()  # Get this site data entered.  Only called from fetch_all()
    fetch_lock_penstock_dia()  # Get this site data entered.  Only called from fetch_all()

    fetch_number_of_spouts()  # Get this site data entered.  Only called from fetch_all()
    fetch_number_of_jets()  # Get this site data entered.  Only called from fetch_all()
    fetch_lock_number_of_spouts()  # Get this site data entered.  Only called from fetch_all()

    fetch_output_head()  # Get site head entered.  Only called from fetch_all() and newBasicData()
    fetch_output_pipe_len()  # Get this site data entered.  Only called from fetch_all()
    fetch_output_eff()  # Get this site data entered.  Only called from fetch_all()
    fetch_output_pipe_diam()  # Get this site data entered.  Only called from fetch_all()


def fetch_available_input_flow():  # Get users lps entered.  Only called from fetch_all() and BasicData()
    value = textread(siteGUI.GUI_available_input_flow, 'lps', 'lps', 'gpm', 100.0, 0.7 )
    if value[1] == 1:
        site.available_input_flow = value[0]

def fetch_input_head():  # Get site head entered.  Only called from fetch_all() and newBasicData()
    value = textread(siteGUI.GUI_input_head, 'm', 'm', 'ft', 20.0, 2.0 )
    if value[1] == 1:
        site.input_head = value[0]

def fetch_input_pipe_len():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_input_pipe_len, 'm', 'm', 'ft', 2000.0, 1.0 )
    if value[1] == 1:
        site.input_pipe_len = value[0]
    
def fetch_input_eff_target():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_input_eff, 'r', '%', '%', 0.99, 0.666666 )
    if value[1] == 1:
        site.input_eff = value[0]
    
def fetch_input_pipe_diam():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_input_pipe_diam, 'm', 'mm', 'in', 1.0, 0.03 )
    if value[1] == 1:
        site.input_pipe_diam = value[0]

def fetch_lock_penstock_dia():  # Get this site data entered.  Only called from fetch_all()
    site.lock_penstock_dia = siteGUI.GUI_lock_penstock_dia

def fetch_number_of_spouts():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_number_of_spouts, '', '', '', 20.0, 1.0 )
    if value[1] == 1:
        site.number_of_spouts = int(value[0])

def fetch_number_of_jets():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_number_of_jets, '', '', '', 2.0, 1.0 )
    if value[1] == 1:
        site.number_of_jets = int(value[0])

def fetch_lock_number_of_spouts():  # Get this site data entered.  Only called from fetch_all()
    site.lock_PHPs_jets = siteGUI.GUI_lock_PHPs_jets

def fetch_output_head():  # Get site head entered.  Only called from fetch_all() and newBasicData()
    value = textread(siteGUI.GUI_output_head, 'm', 'm', 'ft', 249.0, 3.0 )
    if value[1] == 1:
        site.output_head = int(value[0])

def fetch_output_pipe_len():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_output_pipe_len, 'm', 'm', 'ft', 5000.0, 25.0 )
    if value[1] == 1:
        site.output_pipe_len = int(value[0])

def fetch_output_eff():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_output_eff, 'r', '%', '%', 0.99, 0.2 )
    if value[1] == 1:
        site.output_eff = value[0]
            
def fetch_output_pipe_diam():  # Get this site data entered.  Only called from fetch_all()
    value = textread(siteGUI.GUI_output_pipe_diam, 'm', 'mm', 'in', 0.2, 0.012 )
    if value[1] == 1:
        site.output_pipe_diam = value[0]

def fetch_lock_OP_pipe_dia():  # Get this site data entered.  Only called from fetch_all()
    site.lock_OP_pipe_dia = siteGUI.GUI_lock_OP_pipe_dia




def textread( texttoread, calc_unit, inp_unitM, inp_unitI, max_ok, min_ok  ):   # Reads in a string with input sensability checks and does unit conversion as appropiate
    if( siteGUI.GUI_meas_sys == 'Metric' ):
        inp_unit = inp_unitM
    if( siteGUI.GUI_meas_sys == 'Imperial' ):
        inp_unit = inp_unitI

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
            value = value * 10.0 + digit
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
    if value >= min_ok and value <= max_ok:
        valid = 1
    else:
        valid = 0
        if value > 0.0 and value <= max_ok:
            value = min_ok
            valid = 1
        else:
            if value < 10.0 * max_ok and value >= min_ok:
                value = max_ok
                valid = 1
                    
    return(value, valid)










# ALL PROCESSING of user data comes here
def process_here(*args):
    # These are the possible process options
    #   default
    #   units
    
    #   available_input_flow
    #   input_head
    #   input_pipe_len
    #   input_pipe_eff
    #   input_pipe_diam
    #   input_pipe_lock
    #
    #   number_of_spouts
    #   number_of_jets
    #   PHPs_lock
    #
    #   output_head
    #   output_pipe_len
    #   output_pipe_eff
    #   output_pipe_diam
    #   OP_pipe_lock
    if sys.platform[:5] == 'linux':
        site.monospace_on = '<span style=\'font-family:monospace;\'><span style=\'font-size:x-small;\'>'
        site.monospace_off = '</span></span></span>'
        site.Aspace = '&nbsp;'
    siteGUI.GUI_design_notes_hydro = siteGUI.GUI_design_notes_hydro + site.monospace_on + siteGUI.GUIcr
    site.alarms = []

    
    siteGUI.GUI_diag = "Process option is '" + siteGUI.GUI_process_option + "'\r\n"

    if siteGUI.GUI_process_option == 'default' :
        #print "applying defaults"
        siteGUI.meas_sys = 'Metric'
        site.available_input_flow = 8.0  #lps
        site.input_head = 6.0  #m
        site.input_pipe_len = 40.0  #m
        site.input_eff = 0.95  
        site.input_pipe_diam = 0.200  #m
        site.lock_penstock_dia = 0

        site.number_of_spouts = 1
        site.number_of_jets = 2
        site.lock_PHPs_jets = 0
            
        site.output_head = 100.0 #m
        site.output_pipe_len = 800.0 #m
        site.output_eff = 0.95 #dimensionless
        site.output_pipe_diam = 0.012 #m
        site.lock_OP_pipe_dia = 0

    else:
        fetch_all()
        #siteGUI.GUI_diag = siteGUI.GUI_diag + "Fetched all " + str(site.available_input_flow) + "\r\n"



    if siteGUI.GUI_process_option == 'input_pipe_eff':
        site.lock_penstock_dia = 0
    if siteGUI.GUI_process_option == 'input_pipe_diam':
        site.lock_penstock_dia = 1


    if siteGUI.GUI_process_option == 'number_of_spouts':
        site.lock_PHPs_jets = 1
    if siteGUI.GUI_process_option == 'number_of_jets':
        site.lock_PHPs_jets = 1


    #if siteGUI.GUI_process_option == 'PHPs_lock':
    #    #if siteGUI.GUI_lock_spouts_and_jets == 1:
    #    #    siteGUI.GUI_lock_spouts_and_jets = 0
    #    #else: siteGUI.GUI_lock_spouts_and_jets = 1
    #    site.lock_PHPs_jets = siteGUI.GUI_lock_PHPs_jets
    #    siteGUI.GUI_process_option = 'available_input_flow'
    #    print "HHHEEELLLOOO", site.lock_PHPs_jets

    if siteGUI.GUI_process_option == 'output_pipe_eff':
        site.lock_OP_pipe_dia = 0
        
    if siteGUI.GUI_process_option == 'output_pipe_diam':
        site.lock_OP_pipe_dia = 1
        
    if siteGUI.GUI_process_option == 'OP_pipe_lock':
        site.lock_OP_pipe_dia = siteGUI.GUI_lock_OP_pipe_dia



    site.actual_IP_flow = site.available_input_flow
    calc_hydro_ballance() # This assumes endless PHP capacity and fixed efficiency and works out ALL in and out hydro
    # A PHP can only use a given lps according to site.PHP_deliver_h and site.eff_input_head (load torque and jetV caused torque/rpm supply



    siteGUI.GUI_diag = siteGUI.GUI_diag + 'PHP input water watts  =' + str( round(site.waterWin, 3 )) + '\r\n'
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'PHP shaft watts =' + str( round(site.shaftW, 3 )) + '\r\n'
    siteGUI.GUI_diag = siteGUI.GUI_diag + 'PHP output water watts =' + str( round(site.waterWout, 3 )) + '\r\n'


    report_user_notes()

    # Send values to GUI
    report_all()
    #print ''






