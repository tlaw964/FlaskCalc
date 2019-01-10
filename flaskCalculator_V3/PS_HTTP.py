#!/usr/bin/python

import cgi
import re
import PS_Maths_20160226_R17
from PS_Maths_20160226_R17 import siteGUI
from PS_Maths_20160226_R17 import process_here

def fetchHTTP_data():
	form = cgi.FieldStorage()
	
	if(form.getvalue('initial_data')): siteGUI.GUI_initial_data = int(form.getvalue('initial_data'))
	if(form.getvalue('process_option')): siteGUI.GUI_process_option = str(form.getvalue('process_option'))
	if(form.getvalue('meas_sys')): siteGUI.GUI_meas_sys = str(form.getvalue('meas_sys'))
	if(form.getvalue('PStype')): siteGUI.GUI_PStype = str(form.getvalue('PStype'))
	if(form.getvalue('avail_Wflow')): siteGUI.GUI_avail_Wflow = str(form.getvalue('avail_Wflow'))
	if(form.getvalue('penstock_head')): siteGUI.GUI_penstock_head = str(form.getvalue('penstock_head'))
	if(form.getvalue('penstock_len')): siteGUI.GUI_penstock_len = str(form.getvalue('penstock_len'))
	if(form.getvalue('penstock_eff_target')): siteGUI.GUI_penstock_eff_target = str(form.getvalue('penstock_eff_target'))
	if(form.getvalue('penstock_dia')): siteGUI.GUI_penstock_dia = str(form.getvalue('penstock_dia'))
	if(form.getvalue('PenSLkd')): siteGUI.GUI_PenSLkd = int(form.getvalue('PenSLkd'))
	if(form.getvalue('Num_PS')): siteGUI.GUI_Num_PS = int(form.getvalue('Num_PS'))
	if(form.getvalue('Num_PS_Lkd')): siteGUI.GUI_Num_PS_Lkd = int(form.getvalue('Num_PS_Lkd'))
	if(form.getvalue('turbine_nozzles')): siteGUI.GUI_turbine_nozzles = int(form.getvalue('turbine_nozzles'))
	if(form.getvalue('cable_eff_target')): siteGUI.GUI_cable_eff_target = str(form.getvalue('cable_eff_target'))
	if(form.getvalue('cable_len')): siteGUI.GUI_cable_len = str(form.getvalue('cable_len'))
	if(form.getvalue('Dload_V')): siteGUI.GUI_Dload_V = str(form.getvalue('Dload_V'))
	if(form.getvalue('LockCable')): siteGUI.GUI_LockCable = int(form.getvalue('LockCable'))
	if(form.getvalue('cable_material')): siteGUI.GUI_cable_material = str(form.getvalue('cable_material'))
	if(form.getvalue('cable_size')): siteGUI.GUI_cable_size = str(form.getvalue('cable_size'))
	if(form.getvalue('cable_AWG')): siteGUI.GUI_cable_AWG = str(form.getvalue('cable_AWG'))

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
	response += "\"design_notes_hydro\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_hydro)+"\", "
	response += "\"design_notes_elec\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_elec)+"\", "
	response += "\"design_notes_safety\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_safety)+"\""
	response += "}"
	
	return response

print "Content-Type: text/plain\n"
fetchHTTP_data()
process_here()
print putHTTP_data();
