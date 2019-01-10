#!/usr/bin/python

import cgi
import re

from PHP_Maths_py27_2015_08_20 import siteGUI
from PHP_Maths_py27_2015_08_20 import process_here

def fetchHTTP_data():
	form = cgi.FieldStorage()
	if(form.getvalue('process_option')): siteGUI.GUI_process_option = str(form.getvalue('process_option'))
	if(form.getvalue('meas_sys')): siteGUI.GUI_meas_sys = str(form.getvalue('meas_sys'))
	if(form.getvalue('available_input_flow')): siteGUI.GUI_available_input_flow = str(form.getvalue('available_input_flow'))
	#if(form.getvalue('actual_IP_flow')): siteGUI.GUI_actual_IP_flow = str(form.getvalue('actual_IP_flow'))
	if(form.getvalue('input_head')): siteGUI.GUI_input_head = str(form.getvalue('input_head'))
	#if(form.getvalue('eff_input_head')): siteGUI.GUI_eff_input_head = str(form.getvalue('eff_input_head'))
	if(form.getvalue('input_eff')): siteGUI.GUI_input_eff = str(form.getvalue('input_eff'))
	if(form.getvalue('input_pipe_diam')): siteGUI.GUI_input_pipe_diam = str(form.getvalue('input_pipe_diam'))
	if(form.getvalue('input_pipe_len')): siteGUI.GUI_input_pipe_len = str(form.getvalue('input_pipe_len'))
	if(form.getvalue('lock_penstock_dia')): siteGUI.GUI_lock_penstock_dia = int(form.getvalue('lock_penstock_dia'))
	if(form.getvalue('number_of_spouts')): siteGUI.GUI_number_of_spouts = str(form.getvalue('number_of_spouts'))
	if(form.getvalue('number_of_jets')): siteGUI.GUI_number_of_jets = str(form.getvalue('number_of_jets'))
	if(form.getvalue('lock_PHPs_jets')): siteGUI.GUI_lock_PHPs_jets = int(form.getvalue('lock_PHPs_jets'))
	#if(form.getvalue('eff_input_head')): siteGUI.GUI_eff_input_head = str(form.getvalue('eff_input_head'))
	#if(form.getvalue('jet_diam')): siteGUI.GUI_jet_diam = str(form.getvalue('jet_diam'))
	#if(form.getvalue('pelton_rpm')): siteGUI.GUI_pelton_rpm = str(form.getvalue('pelton_rpm'))
	#if(form.getvalue('cam_offset')): siteGUI.GUI_cam_offset = str(form.getvalue('cam_offset'))
	#if(form.getvalue('PHP_deliver_h')): siteGUI.GUI_PHP_deliver_h = str(form.getvalue('PHP_deliver_h'))
	if(form.getvalue('output_head')): siteGUI.GUI_output_head = str(form.getvalue('output_head'))
	if(form.getvalue('output_pipe_len')): siteGUI.GUI_output_pipe_len = str(form.getvalue('output_pipe_len'))
	if(form.getvalue('output_eff')): siteGUI.GUI_output_eff = str(form.getvalue('output_eff'))
	if(form.getvalue('output_pipe_diam')): siteGUI.GUI_output_pipe_diam = str(form.getvalue('output_pipe_diam'))
	if(form.getvalue('lock_OP_pipe_dia')): siteGUI.GUI_lock_OP_pipe_dia = str(form.getvalue('lock_OP_pipe_dia'))
	if(form.getvalue('total_OP_flow')): siteGUI.GUI_total_OP_flow = str(form.getvalue('total_OP_flow'))
	if(form.getvalue('total_OP_flow_day')): siteGUI.GUI_total_OP_flow_day = str(form.getvalue('total_OP_flow_day'))
	
	
def putHTTP_data():
	response = "{"
	response += "\"meas_sys\" : \""+str(siteGUI.GUI_meas_sys)+"\", "
	response += "\"available_input_flow\" : \""+str(siteGUI.GUI_available_input_flow)+"\", "
	response += "\"actual_IP_flow\" : \""+str(siteGUI.GUI_actual_IP_flow)+"\", "
	response += "\"input_head\" : \""+str(siteGUI.GUI_input_head)+"\", "
	#response += "\"input_head\" : \""+str(siteGUI.GUI_input_head)+"\", "
	response += "\"eff_input_head\" : \""+str(siteGUI.GUI_eff_input_head)+"\", "
	response += "\"input_eff\" : \""+str(siteGUI.GUI_input_eff)+"\", "
	response += "\"input_pipe_diam\" : \""+str(siteGUI.GUI_input_pipe_diam)+"\", "
	response += "\"input_pipe_len\" : \""+str(siteGUI.GUI_input_pipe_len)+"\", "
	response += "\"lock_penstock_dia\" : \""+str(siteGUI.GUI_lock_penstock_dia)+"\", "
	response += "\"number_of_spouts\" : \""+str(siteGUI.GUI_number_of_spouts)+"\", "
	response += "\"number_of_jets\" : \""+str(siteGUI.GUI_number_of_jets)+"\", "
	response += "\"lock_PHPs_jets\" : \""+str(siteGUI.GUI_lock_PHPs_jets)+"\", "
	response += "\"eff_input_head\" : \""+str(siteGUI.GUI_eff_input_head)+"\", "
	response += "\"jet_diam\" : \""+str(siteGUI.GUI_jet_diam)+"\", "
	response += "\"pelton_rpm\" : \""+str(siteGUI.GUI_pelton_rpm)+"\", "
	response += "\"cam_offset\" : \""+str(siteGUI.GUI_cam_offset)+"\", "
	response += "\"PHP_deliver_h\" : \""+str(siteGUI.GUI_PHP_deliver_h)+"\", "
	response += "\"output_head\" : \""+str(siteGUI.GUI_output_head)+"\", "
	response += "\"output_pipe_len\" : \""+str(siteGUI.GUI_output_pipe_len)+"\", "
	response += "\"output_eff\" : \""+str(siteGUI.GUI_output_eff)+"\", "
	response += "\"output_pipe_diam\" : \""+str(siteGUI.GUI_output_pipe_diam)+"\", "
	response += "\"lock_OP_pipe_dia\" : \""+str(siteGUI.GUI_lock_OP_pipe_dia)+"\", "
	response += "\"total_OP_flow\" : \""+str(siteGUI.GUI_total_OP_flow)+"\", "
	response += "\"total_OP_flow_day\" : \""+str(siteGUI.GUI_total_OP_flow_day)+"\", "
	response += "\"design_notes_hydro\" : \""+re.sub('\s{2,}|\r|\n', ' ',siteGUI.GUI_design_notes_hydro)+"\""   
	response += "}"
	
	return response

print ("Content-Type: text/plain\n")
fetchHTTP_data()
process_here()
print (putHTTP_data());
