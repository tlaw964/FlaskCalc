#!/usr/bin/python

import sys
import cgi
import re
import LH_Maths_20170418_R09
from LH_Maths_20170418_R09 import siteGUI
from LH_Maths_20170418_R09 import process_here

def fetchHTTP_data():
	form = cgi.FieldStorage()
	siteGUI.GUI_LHtype = str('LH/LH Pro')
	if(form.getvalue('initial_data')): siteGUI.GUI_initial_data = int(form.getvalue('initial_data'))
	if(form.getvalue('process_option')): siteGUI.GUI_process_option = str(form.getvalue('process_option'))
	if(form.getvalue('meas_sys')): siteGUI.GUI_meas_sys = str(form.getvalue('meas_sys'))
	if(form.getvalue('avail_lps')): siteGUI.GUI_avail_lps = str(form.getvalue('avail_lps'))
	if(form.getvalue('pipe_head')): siteGUI.GUI_pipe_head = str(form.getvalue('pipe_head'))
	if(form.getvalue('pipe_len')): siteGUI.GUI_pipe_len = str(form.getvalue('pipe_len'))
	if(form.getvalue('PipeFlume')): siteGUI.GUI_PipeFlume = str(form.getvalue('PipeFlume'))
	if(form.getvalue('pipe_mat')): siteGUI.GUI_pipe_mat = str(form.getvalue('pipe_mat'))
	if(form.getvalue('pipe_dia')): siteGUI.GUI_pipe_dia = str(form.getvalue('pipe_dia'))
	if(form.getvalue('pipe_height')): siteGUI.GUI_pipe_height = str(form.getvalue('pipe_height'))
	if(form.getvalue('LH_head')): siteGUI.GUI_LH_head = str(form.getvalue('LH_head'))
	if(form.getvalue('Num_LH')): siteGUI.GUI_Num_LH = str(form.getvalue('Num_LH'))
	if(form.getvalue('LockNumLH')): siteGUI.GUI_LockNumLH = int(form.getvalue('LockNumLH'))
	if(form.getvalue('cable_eff_target')): siteGUI.GUI_cable_eff_target = str(form.getvalue('cable_eff_target'))
	if(form.getvalue('cable_len')): siteGUI.GUI_cable_len = str(form.getvalue('cable_len'))
	if(form.getvalue('Load_Vmax')): siteGUI.GUI_Load_Vmax = str(form.getvalue('Load_Vmax'))
	#else:siteGUI.GUI_Load_Vmax =str('150 V')
	if(form.getvalue('Load_Vmin')): siteGUI.GUI_Load_Vmin = str(form.getvalue('Load_Vmin'))
	if(form.getvalue('LockCable')): siteGUI.GUI_LockCable = int(form.getvalue('LockCable'))
	if(form.getvalue('cable_material')): siteGUI.GUI_cable_material = str(form.getvalue('cable_material'))
	if(form.getvalue('cable_size')): siteGUI.GUI_cable_size = str(form.getvalue('cable_size'))
	if(form.getvalue('cable_AWG')): siteGUI.GUI_cable_AWG = str(form.getvalue('cable_AWG'))
        
def putHTTP_data():
	response = "{"
	response += "\"initial_data\" : \"" +str(siteGUI.GUI_initial_data)+"\", "
	response += "\"meas_sys\" : \"" +str(siteGUI.GUI_meas_sys)+"\", "
	response += "\"LHtype\" : \"" +str(siteGUI.GUI_LHtype)+"\", "
	response += "\"avail_lps\" : \"" +str(siteGUI.GUI_avail_lps)+"\", "
	response += "\"pipe_mat\" : \"" +str(siteGUI.GUI_pipe_mat)+"\", "
	response += "\"pipe_head\" : \"" +str(siteGUI.GUI_pipe_head)+"\", "
	response += "\"pipe_len\" : \"" +str(siteGUI.GUI_pipe_len)+"\", "
	response += "\"PipeFlume\" : \"" +str(siteGUI.GUI_PipeFlume)+"\", "
	response += "\"pipe_dia\" : \"" +str(siteGUI.GUI_pipe_dia)+"\", "
	response += "\"pipe_height\" : \"" +str(siteGUI.GUI_pipe_height)+"\", "
	response += "\"LH_head\" : \"" +str(siteGUI.GUI_LH_head)+"\", "
	response += "\"Num_LH\" : \"" +str(siteGUI.GUI_Num_LH)+"\", "
	response += "\"LockNumLH\" : \"" +str(siteGUI.GUI_LockNumLH)+"\", "
	response += "\"cable_eff_target\" : \"" +str(siteGUI.GUI_cable_eff_target)+"\", "
	response += "\"cable_len\" : \"" +str(siteGUI.GUI_cable_len)+"\", "
	response += "\"Load_Vmax\" : \"" +str(siteGUI.GUI_Load_Vmax)+"\", "
	response += "\"Load_Vmin\" : \"" +str(siteGUI.GUI_Load_Vmin)+"\", "
	response += "\"LockCable\" : \"" +str(siteGUI.GUI_LockCable)+"\", "
	response += "\"cable_material\" : \"" +str(siteGUI.GUI_cable_material)+"\", "
	response += "\"cable_size\" : \"" +str(siteGUI.GUI_cable_size)+"\", "
	response += "\"cable_AWG\" : \"" +str(siteGUI.GUI_cable_AWG)+"\", "
	response += "\"actual_lps\" : \"" +str(siteGUI.GUI_actual_lps)+"\", "
	response += "\"water_depth\" : \"" +str(siteGUI.GUI_water_depth)+"\", "
	response += "\"LH_Draft_T\" : \"" +str(siteGUI.GUI_LH_Draft_T)+"\", "
	response += "\"pipe_capacity\" : \"" +str(siteGUI.GUI_pipe_capacity)+"\", "
	response += "\"LH_rpm_Opr\" : \"" +str(siteGUI.GUI_LH_rpm_Opr)+"\", "
	response += "\"LH_rpm_NL\" : \"" +str(siteGUI.GUI_LH_rpm_NL)+"\", "
	response += "\"LH_watts_Opr\" : \"" +str(siteGUI.GUI_LH_watts_Opr)+"\", "
	response += "\"LH_pwr_tot\" : \"" +str(siteGUI.GUI_LH_pwr_tot)+"\", "
	response += "\"LH_V_Opr\" : \"" +str(siteGUI.GUI_LH_V_Opr)+"\", "
	response += "\"LH_V_NL\" : \"" +str(siteGUI.GUI_LH_V_NL)+"\", "
	response += "\"Aload_V\" : \"" +str(siteGUI.GUI_Aload_V)+"\", "
	response += "\"cable_mm_title\" : \"" +str(siteGUI.GUI_cable_mm_title)+"\", "
	response += "\"cable_AWG_title\" : \"" +str(siteGUI.GUI_cable_AWG_title)+"\", "
	response += "\"cable_dia_mm_sld\" : \"" +str(siteGUI.GUI_cable_dia_mm_sld)+"\", "
	response += "\"cable_dia_mm_str\" : \"" +str(siteGUI.GUI_cable_dia_mm_str)+"\", "
	response += "\"cable_dia_in_sld\" : \"" +str(siteGUI.GUI_cable_dia_in_sld)+"\", "
	response += "\"cable_dia_in_str\" : \"" +str(siteGUI.GUI_cable_dia_in_str )+"\", "
	response += "\"cable_A\" : \"" +str(siteGUI.GUI_cable_A)+"\", "
	response += "\"actual_cable_eff\" : \"" +str(siteGUI.GUI_actual_cable_eff)+"\", "
	response += "\"Load_pwr\" : \"" +str(siteGUI.GUI_Load_pwr)+"\", "
	response += "\"design_notes_hydro\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_hydro)+"\", "
	response += "\"design_notes_elec\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_elec)+"\", "
	response += "\"design_notes_safety\" : \""+re.sub('\s{2,}|\r|\n', ' ', siteGUI.GUI_design_notes_safety)+"\""
	response += "}"
	
	return response

print ("Content-Type: text/plain\n")
fetchHTTP_data()
process_here()
print (putHTTP_data());
