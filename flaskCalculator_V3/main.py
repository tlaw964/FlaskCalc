from flask import Flask, render_template, request
import re
#plt and trg
from PS_Maths_20160226_R17 import siteGUI as PS_siteGUI
from PS_Maths_20160226_R17 import process_here as PS_process_here
#lh
from LH_Maths_20170418_R09 import siteGUI as LH_siteGUI
from LH_Maths_20170418_R09 import process_here as LH_process_here

from PHP_Maths_py27_2015_08_20 import siteGUI as PHP_siteGUI
from PHP_Maths_py27_2015_08_20 import process_here as PHP_process_here

from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import urllib
import json



app = Flask(__name__)


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'noreply.powerspout@gmail.com',
    MAIL_PASSWORD = '4i7oki7y',
    EMAIL_SENDER = 'no-reply@localhost.com'))

mail = Mail(app)

@app.route('/ps')
def ps_index():
    return render_template('ps.html')

@app.route('/lh')
def lh_index():
    return render_template('lh.html')

@app.route('/php')
def php_index():
    return render_template('php.html')


def PS_putHTTP_data():
    response = "{"

    response += "\"initial_data\" : \"" + str(PS_siteGUI.GUI_initial_data) + "\", "
    response += "\"avail_Wflow\" : \"" + str(PS_siteGUI.GUI_avail_Wflow) + "\", "
    response += "\"Wflow\" : \"" + str(PS_siteGUI.GUI_Wflow) + "\", "
    response += "\"penstock_head\" : \"" + str(PS_siteGUI.GUI_penstock_head) + "\", "
    response += "\"eff_head\" : \"" + str(PS_siteGUI.GUI_eff_head) + "\", "
    response += "\"penstock_len\" : \"" + str(PS_siteGUI.GUI_penstock_len) + "\", "
    response += "\"penstock_eff_target\" : \"" + str(PS_siteGUI.GUI_penstock_eff_target) + "\", "
    response += "\"penstock_dia\" : \"" + str(PS_siteGUI.GUI_penstock_dia) + "\", "
    response += "\"PenSLkd\" : \"" + str(PS_siteGUI.GUI_PenSLkd) + "\", "
    response += "\"Num_PS\" : \"" + str(PS_siteGUI.GUI_Num_PS) + "\", "
    response += "\"turbine_nozzles\" : \"" + str(PS_siteGUI.GUI_turbine_nozzles) + "\", "
    response += "\"Num_PS_Lkd\" : \"" + str(PS_siteGUI.GUI_Num_PS_Lkd) + "\", "
    response += "\"jet_dia\" : \"" + str(PS_siteGUI.GUI_jet_dia) + "\", "
    response += "\"actual_pipe_eff\" : \"" + str(PS_siteGUI.GUI_actual_pipe_eff) + "\", "
    response += "\"Opr_rpm\" : \"" + str(PS_siteGUI.GUI_Opr_rpm) + "\", "
    response += "\"PS_pwr_ea\" : \"" + str(PS_siteGUI.GUI_PS_pwr_ea) + "\", "
    response += "\"Actual_turbine_electric_pwr\" : \"" + str(PS_siteGUI.GUI_Actual_turbine_electric_pwr) + "\", "
    response += "\"cable_eff_target\" : \"" + str(PS_siteGUI.GUI_cable_eff_target) + "\", "
    response += "\"cable_len\" : \"" + str(PS_siteGUI.GUI_cable_len) + "\", "
    response += "\"Dload_V\" : \"" + str(PS_siteGUI.GUI_Dload_V) + "\", "
    response += "\"Aload_V\" : \"" + str(PS_siteGUI.GUI_Aload_V) + "\", "
    response += "\"LockCable\" : \"" + str(PS_siteGUI.GUI_LockCable) + "\", "
    response += "\"cable_mm_title\" : \"" + str(PS_siteGUI.GUI_cable_mm_title) + "\", "
    response += "\"cable_size\" : \"" + str(PS_siteGUI.GUI_cable_size) + "\", "
    response += "\"cable_AWG\" : \"" + str(PS_siteGUI.GUI_cable_AWG) + "\", "
    response += "\"cable_AWG_title\" : \"" + str(PS_siteGUI.GUI_cable_AWG_title) + "\", "
    response += "\"cable_dia_mm_sld\" : \"" + str(PS_siteGUI.GUI_cable_dia_mm_sld) + "\", "
    response += "\"cable_dia_mm_str\" : \"" + str(PS_siteGUI.GUI_cable_dia_mm_str) + "\", "
    response += "\"cable_amps\" : \"" + str(PS_siteGUI.GUI_cable_amps) + "\", "
    response += "\"actual_cable_eff\" : \"" + str(PS_siteGUI.GUI_actual_cable_eff) + "\", "
    response += "\"cable_Vgen\" : \"" + str(PS_siteGUI.GUI_cable_Vgen) + "\", "
    response += "\"Load_pwr\" : \"" + str(PS_siteGUI.GUI_Load_pwr) + "\", "
    response += "\"design_notes_hydro\" : \"" + re.sub('\s{2,}|\r|\n', ' ', PS_siteGUI.GUI_design_notes_hydro) + "\", "
    response += "\"design_notes_elec\" : \"" + re.sub('\s{2,}|\r|\n', ' ', PS_siteGUI.GUI_design_notes_elec) + "\", "
    response += "\"design_notes_safety\" : \"" + re.sub('\s{2,}|\r|\n', ' ', PS_siteGUI.GUI_design_notes_safety) + "\""
    response += "}"
    return response

def LH_putHTTP_data():
    response = "{"
    response += "\"initial_data\" : \"" + str(LH_siteGUI.GUI_initial_data) + "\", "
    response += "\"meas_sys\" : \"" + str(LH_siteGUI.GUI_meas_sys) + "\", "
    response += "\"LHtype\" : \"" + str(LH_siteGUI.GUI_LHtype) + "\", "
    response += "\"avail_lps\" : \"" + str(LH_siteGUI.GUI_avail_lps) + "\", "
    response += "\"pipe_mat\" : \"" + str(LH_siteGUI.GUI_pipe_mat) + "\", "
    response += "\"pipe_head\" : \"" + str(LH_siteGUI.GUI_pipe_head) + "\", "
    response += "\"pipe_len\" : \"" + str(LH_siteGUI.GUI_pipe_len) + "\", "
    response += "\"PipeFlume\" : \"" + str(LH_siteGUI.GUI_PipeFlume) + "\", "
    response += "\"pipe_dia\" : \"" + str(LH_siteGUI.GUI_pipe_dia) + "\", "
    response += "\"pipe_height\" : \"" + str(LH_siteGUI.GUI_pipe_height) + "\", "
    response += "\"LH_head\" : \"" + str(LH_siteGUI.GUI_LH_head) + "\", "
    response += "\"Num_LH\" : \"" + str(LH_siteGUI.GUI_Num_LH) + "\", "
    response += "\"LockNumLH\" : \"" + str(LH_siteGUI.GUI_LockNumLH) + "\", "
    response += "\"cable_eff_target\" : \"" + str(LH_siteGUI.GUI_cable_eff_target) + "\", "
    response += "\"cable_len\" : \"" + str(LH_siteGUI.GUI_cable_len) + "\", "
    response += "\"Load_Vmax\" : \"" + str(LH_siteGUI.GUI_Load_Vmax) + "\", "
    response += "\"Load_Vmin\" : \"" + str(LH_siteGUI.GUI_Load_Vmin) + "\", "
    response += "\"LockCable\" : \"" + str(LH_siteGUI.GUI_LockCable) + "\", "
    response += "\"cable_material\" : \"" + str(LH_siteGUI.GUI_cable_material) + "\", "
    response += "\"cable_size\" : \"" + str(LH_siteGUI.GUI_cable_size) + "\", "
    response += "\"cable_AWG\" : \"" + str(LH_siteGUI.GUI_cable_AWG) + "\", "
    response += "\"actual_lps\" : \"" + str(LH_siteGUI.GUI_actual_lps) + "\", "
    response += "\"water_depth\" : \"" + str(LH_siteGUI.GUI_water_depth) + "\", "
    response += "\"LH_Draft_T\" : \"" + str(LH_siteGUI.GUI_LH_Draft_T) + "\", "
    response += "\"pipe_capacity\" : \"" + str(LH_siteGUI.GUI_pipe_capacity) + "\", "
    response += "\"LH_rpm_Opr\" : \"" + str(LH_siteGUI.GUI_LH_rpm_Opr) + "\", "
    response += "\"LH_rpm_NL\" : \"" + str(LH_siteGUI.GUI_LH_rpm_NL) + "\", "
    response += "\"LH_watts_Opr\" : \"" + str(LH_siteGUI.GUI_LH_watts_Opr) + "\", "
    response += "\"LH_pwr_tot\" : \"" + str(LH_siteGUI.GUI_LH_pwr_tot) + "\", "
    response += "\"LH_V_Opr\" : \"" + str(LH_siteGUI.GUI_LH_V_Opr) + "\", "
    response += "\"LH_V_NL\" : \"" + str(LH_siteGUI.GUI_LH_V_NL) + "\", "
    response += "\"Aload_V\" : \"" + str(LH_siteGUI.GUI_Aload_V) + "\", "
    response += "\"cable_mm_title\" : \"" + str(LH_siteGUI.GUI_cable_mm_title) + "\", "
    response += "\"cable_AWG_title\" : \"" + str(LH_siteGUI.GUI_cable_AWG_title) + "\", "
    response += "\"cable_dia_mm_sld\" : \"" + str(LH_siteGUI.GUI_cable_dia_mm_sld) + "\", "
    response += "\"cable_dia_mm_str\" : \"" + str(LH_siteGUI.GUI_cable_dia_mm_str) + "\", "
    response += "\"cable_dia_in_sld\" : \"" + str(LH_siteGUI.GUI_cable_dia_in_sld) + "\", "
    response += "\"cable_dia_in_str\" : \"" + str(LH_siteGUI.GUI_cable_dia_in_str) + "\", "
    response += "\"cable_A\" : \"" + str(LH_siteGUI.GUI_cable_A) + "\", "
    response += "\"actual_cable_eff\" : \"" + str(LH_siteGUI.GUI_actual_cable_eff) + "\", "
    response += "\"Load_pwr\" : \"" + str(LH_siteGUI.GUI_Load_pwr) + "\", "
    response += "\"design_notes_hydro\" : \"" + re.sub('\s{2,}|\r|\n', ' ',LH_siteGUI.GUI_design_notes_hydro) + "\", "
    response += "\"design_notes_elec\" : \"" + re.sub('\s{2,}|\r|\n', ' ',LH_siteGUI.GUI_design_notes_elec) + "\", "
    response += "\"design_notes_safety\" : \"" + re.sub('\s{2,}|\r|\n', ' ',LH_siteGUI.GUI_design_notes_safety) + "\""
    response += "}"

    return response


def PHP_putHTTP_data():
    response = "{"
    response += "\"meas_sys\" : \"" + str(PHP_siteGUI.GUI_meas_sys) + "\", "
    response += "\"available_input_flow\" : \"" + str(PHP_siteGUI.GUI_available_input_flow) + "\", "
    response += "\"actual_IP_flow\" : \"" + str(PHP_siteGUI.GUI_actual_IP_flow) + "\", "
    response += "\"input_head\" : \"" + str(PHP_siteGUI.GUI_input_head) + "\", "
    # response += "\"input_head\" : \""+str(PHP_siteGUI.GUI_input_head)+"\", "
    response += "\"eff_input_head\" : \"" + str(PHP_siteGUI.GUI_eff_input_head) + "\", "
    response += "\"input_eff\" : \"" + str(PHP_siteGUI.GUI_input_eff) + "\", "
    response += "\"input_pipe_diam\" : \"" + str(PHP_siteGUI.GUI_input_pipe_diam) + "\", "
    response += "\"input_pipe_len\" : \"" + str(PHP_siteGUI.GUI_input_pipe_len) + "\", "
    response += "\"lock_penstock_dia\" : \"" + str(PHP_siteGUI.GUI_lock_penstock_dia) + "\", "
    response += "\"number_of_spouts\" : \"" + str(PHP_siteGUI.GUI_number_of_spouts) + "\", "
    response += "\"number_of_jets\" : \"" + str(PHP_siteGUI.GUI_number_of_jets) + "\", "
    response += "\"lock_PHPs_jets\" : \"" + str(PHP_siteGUI.GUI_lock_PHPs_jets) + "\", "
    response += "\"eff_input_head\" : \"" + str(PHP_siteGUI.GUI_eff_input_head) + "\", "
    response += "\"jet_diam\" : \"" + str(PHP_siteGUI.GUI_jet_diam) + "\", "
    response += "\"pelton_rpm\" : \"" + str(PHP_siteGUI.GUI_pelton_rpm) + "\", "
    response += "\"cam_offset\" : \"" + str(PHP_siteGUI.GUI_cam_offset) + "\", "
    response += "\"PHP_deliver_h\" : \"" + str(PHP_siteGUI.GUI_PHP_deliver_h) + "\", "
    response += "\"output_head\" : \"" + str(PHP_siteGUI.GUI_output_head) + "\", "
    response += "\"output_pipe_len\" : \"" + str(PHP_siteGUI.GUI_output_pipe_len) + "\", "
    response += "\"output_eff\" : \"" + str(PHP_siteGUI.GUI_output_eff) + "\", "
    response += "\"output_pipe_diam\" : \"" + str(PHP_siteGUI.GUI_output_pipe_diam) + "\", "
    response += "\"lock_OP_pipe_dia\" : \"" + str(PHP_siteGUI.GUI_lock_OP_pipe_dia) + "\", "
    response += "\"total_OP_flow\" : \"" + str(PHP_siteGUI.GUI_total_OP_flow) + "\", "
    response += "\"total_OP_flow_day\" : \"" + str(PHP_siteGUI.GUI_total_OP_flow_day) + "\", "
    response += "\"design_notes_hydro\" : \"" + re.sub('\s{2,}|\r|\n', ' ',PHP_siteGUI.GUI_design_notes_hydro) + "\""
    response += "}"

    return response





##############################################################
# The following defines are the actions for all widgets in gui
##############################################################
#@app.before_first_request
#def setupInital():



def PS_fetchGUI_data(*args):
    #this function Fetches the data from the form ignoring any values of type None i.e havent been entered yet

    if ((request.form.get('Type', None)) is not None): PS_siteGUI.GUI_PStype = str(request.form.get('Type', None))
    if ((request.form.get('InitialData', None)) is not None): PS_siteGUI.GUI_initial_data = int(request.form.get('InitialData', None))
    if ((request.form.get('Units', None)) is not None): PS_siteGUI.GUI_meas_sys = str(request.form.get('Units', None))
    if ((request.form.get('processOption', None)) is not None): PS_siteGUI.GUI_process_option = str(request.form.get('processOption', None))
    if ((request.form.get('Flow', None)) is not None): PS_siteGUI.GUI_avail_Wflow = str(request.form.get('Flow', None))
    if ((request.form.get('PipeHead', None)) is not None): PS_siteGUI.GUI_penstock_head = str(request.form.get('PipeHead', None))
    if ((request.form.get('PipeLenth', None)) is not None): PS_siteGUI.GUI_penstock_len = str(request.form.get('PipeLenth', None))
    if ((request.form.get('PipeEfficiency', None)) is not None): PS_siteGUI.GUI_penstock_eff_target = str(request.form.get('PipeEfficiency', None))
    if ((request.form.get('PipeDiameter', None)) is not None): PS_siteGUI.GUI_penstock_dia = str(request.form.get('PipeDiameter', None))
    if ((request.form.get('LockPipeDiameter', None)) is not None): PS_siteGUI.GUI_PenSLkd = int(request.form.get('LockPipeDiameter', None))
    if ((request.form.get('Powerspouts', None)) is not None): PS_siteGUI.GUI_Num_PS = int(request.form.get('Powerspouts', None))
    if ((request.form.get('LockPowerspouts', None)) is not None): PS_siteGUI.GUI_Num_PS_Lkd = int(request.form.get('LockPowerspouts', None))
    if ((request.form.get('Nozzles', None)) is not None): PS_siteGUI.GUI_turbine_nozzles = int(request.form.get('Nozzles', None))
    if ((request.form.get('CableEfficiency', None)) is not None): PS_siteGUI.GUI_cable_eff_target = str(request.form.get('CableEfficiency', None))
    if ((request.form.get('CableLength', None)) is not None): PS_siteGUI.GUI_cable_len = str(request.form.get('CableLength', None))
    if ((request.form.get('LoadVoltage', None)) is not None): PS_siteGUI.GUI_Dload_V = str(request.form.get('LoadVoltage', None))
    if ((request.form.get('LockCableSize', None)) is not None): PS_siteGUI.GUI_LockCable = int(request.form.get('LockCableSize', None))
    if ((request.form.get('CableMaterial', None)) is not None): PS_siteGUI.GUI_cable_material = str(request.form.get('CableMaterial', None))
    if ((request.form.get('CableSize', None)) is not None): PS_siteGUI.GUI_cable_size = str(request.form.get('CableSize', None))
    if ((request.form.get('CableAWG', None)) is not None): PS_siteGUI.GUI_cable_AWG = str(request.form.get('CableAWG', None))

def LH_fetchGUI_data(*args):
    #this function Fetches the data from the form ignoring any values of type None i.e havent been entered yet
    LH_siteGUI.GUI_LHtype = str('LH/LH Pro')
    if ((request.form.get('InitialData', None)) is not None): LH_siteGUI.GUI_initial_data = int(request.form.get('InitialData', None))
    if ((request.form.get('processOption', None)) is not None): LH_siteGUI.GUI_process_option = str(request.form.get('processOption', None))
    if ((request.form.get('MeasSys', None)) is not None): LH_siteGUI.GUI_meas_sys = str(request.form.get('MeasSys', None))
    if ((request.form.get('AvailLPS', None)) is not None): LH_siteGUI.GUI_avail_lps = str(request.form.get('AvailLPS', None))
    if ((request.form.get('PipeHead', None)) is not None): LH_siteGUI.GUI_pipe_head = str(request.form.get('PipeHead', None))
    if ((request.form.get('PipeLen', None)) is not None): LH_siteGUI.GUI_pipe_len = str(request.form.get('PipeLen', None))
    if ((request.form.get('PipeFlume', None)) is not None): LH_siteGUI.GUI_PipeFlume = str(request.form.get('PipeFlume', None))
    if ((request.form.get('PipeMat', None)) is not None): LH_siteGUI.GUI_pipe_mat = str(request.form.get('PipeMat', None))
    if ((request.form.get('PipeDia', None)) is not None): LH_siteGUI.GUI_pipe_dia = str(request.form.get('PipeDia', None))
    if ((request.form.get('PipeHeight', None)) is not None): LH_siteGUI.GUI_pipe_height = str(request.form.get('PipeHeight', None))
    if ((request.form.get('LHHead', None)) is not None): LH_siteGUI.GUI_LH_head = str(request.form.get('LHHead', None))
    if ((request.form.get('NumLH', None)) is not None): LH_siteGUI.GUI_Num_LH = str(request.form.get('NumLH', None))
    if ((request.form.get('LockNumLH', None)) is not None): LH_siteGUI.GUI_LockNumLH = int(request.form.get('LockNumLH', None))
    if ((request.form.get('CableEffTarget', None)) is not None): LH_siteGUI.GUI_cable_eff_target = str(request.form.get('CableEffTarget', None))
    if ((request.form.get('CableLen', None)) is not None): LH_siteGUI.GUI_cable_len = str(request.form.get('CableLen', None))
    if ((request.form.get('LoadVmax', None)) is not None): LH_siteGUI.GUI_Load_Vmax = str(request.form.get('LoadVmax', None))
    # else:siteGUI.GUI_Load_Vmax =str('150 V')
    if ((request.form.get('LoadVmin', None)) is not None): LH_siteGUI.GUI_Load_Vmin = str(request.form.get('LoadVmin', None))
    if ((request.form.get('LockCable', None)) is not None): LH_siteGUI.GUI_LockCable = int(request.form.get('LockCable', None))
    if ((request.form.get('CableMaterial', None)) is not None): LH_siteGUI.GUI_cable_material = str(request.form.get('CableMaterial', None))
    if ((request.form.get('CableSize', None)) is not None): LH_siteGUI.GUI_cable_size = str(request.form.get('CableSize', None))
    if ((request.form.get('CableAWG', None)) is not None): LH_siteGUI.GUI_cable_AWG = str(request.form.get('CableAWG', None))

def PHP_fetchGUI_data(*args):
    # this function Fetches the data from the form ignoring any values of type None i.e havent been entered yet
    if((request.form.get('processOption', None)) is not None): PHP_siteGUI.GUI_process_option = str(request.form.get('processOption'))
    if((request.form.get('meas_sys', None)) is not None): PHP_siteGUI.GUI_meas_sys = str(request.form.get('meas_sys'))
    if((request.form.get('available_input_flow', None)) is not None): PHP_siteGUI.GUI_available_input_flow = str(request.form.get('available_input_flow'))
    # if(request.form.get('actual_IP_flow', None)) is not None): PHP_siteGUI.GUI_actual_IP_flow = str(request.form.get('actual_IP_flow'))
    if((request.form.get('input_head', None)) is not None): PHP_siteGUI.GUI_input_head = str(request.form.get('input_head'))
    # if(request.form.get('eff_input_head', None)) is not None): PHP_siteGUI.GUI_eff_input_head = str(request.form.get('eff_input_head'))
    if((request.form.get('input_eff', None)) is not None): PHP_siteGUI.GUI_input_eff = str(request.form.get('input_eff'))
    if((request.form.get('input_pipe_diam', None)) is not None): PHP_siteGUI.GUI_input_pipe_diam = str(request.form.get('input_pipe_diam'))
    if((request.form.get('input_pipe_len', None)) is not None): PHP_siteGUI.GUI_input_pipe_len = str(request.form.get('input_pipe_len'))
    if((request.form.get('lock_penstock_dia', None)) is not None): PHP_siteGUI.GUI_lock_penstock_dia = int(request.form.get('lock_penstock_dia'))
    if((request.form.get('number_of_spouts', None)) is not None): PHP_siteGUI.GUI_number_of_spouts = str(request.form.get('number_of_spouts'))
    if((request.form.get('number_of_jets', None)) is not None): PHP_siteGUI.GUI_number_of_jets = str(request.form.get('number_of_jets'))
    if((request.form.get('lock_PHPs_jets', None)) is not None): PHP_siteGUI.GUI_lock_PHPs_jets = int(request.form.get('lock_PHPs_jets'))
    # if(request.form.get('eff_input_head', None)) is not None): PHP_siteGUI.GUI_eff_input_head = str(request.form.get('eff_input_head'))
    # if(request.form.get('jet_diam', None)) is not None): PHP_siteGUI.GUI_jet_diam = str(request.form.get('jet_diam'))
    # if(request.form.get('pelton_rpm', None)) is not None): PHP_siteGUI.GUI_pelton_rpm = str(request.form.get('pelton_rpm'))
    # if(request.form.get('cam_offset', None)) is not None): PHP_siteGUI.GUI_cam_offset = str(request.form.get('cam_offset'))
    # if(request.form.get('PHP_deliver_h', None)) is not None): PHP_siteGUI.GUI_PHP_deliver_h = str(request.form.get('PHP_deliver_h'))
    if((request.form.get('output_head', None)) is not None): PHP_siteGUI.GUI_output_head = str(request.form.get('output_head'))
    if((request.form.get('output_pipe_len', None)) is not None): PHP_siteGUI.GUI_output_pipe_len = str(request.form.get('output_pipe_len'))
    if((request.form.get('output_eff', None)) is not None): PHP_siteGUI.GUI_output_eff = str(request.form.get('output_eff'))
    if((request.form.get('output_pipe_diam', None)) is not None): PHP_siteGUI.GUI_output_pipe_diam = str(request.form.get('output_pipe_diam'))
    if((request.form.get('lock_OP_pipe_dia', None)) is not None): PHP_siteGUI.GUI_lock_OP_pipe_dia = str(request.form.get('lock_OP_pipe_dia'))
    if((request.form.get('total_OP_flow', None)) is not None): PHP_siteGUI.GUI_total_OP_flow = str(request.form.get('total_OP_flow'))
    if((request.form.get('total_OP_flow_day', None)) is not None): PHP_siteGUI.GUI_total_OP_flow_day = str(request.form.get('total_OP_flow_day'))

def last_entered_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list))


@app.route('/submitForm', methods=['GET', 'POST'])
def submitForm():
    message = ''
    error = 0
    #create dictionary of values from form
    formDict = request.form

    type = str((formDict.get('turbine_type', None)))
    #figure out what calculation tool was used

    if type == 'ps' :
        turbine = 'PS'
        worksheetName = 'PLT_TRG'
        mailTemplate = 'PSmail.html'
    # request by '/ps'

    elif type == 'lh':
        turbine = 'LH'
        worksheetName = 'LH'
        mailTemplate = 'LHmail.html'

    elif type == 'php':
        turbine = 'PHP'
        worksheetName = 'PHP'
        mailTemplate = 'PHPmail.html'
    # request by '/top'
    else:
            #errors requested from unkhownen place
        message = 'Error'
        error = 1
        responce = {
            "errors":error,
            "message":message
        }
        return json.dumps(responce)


    #generate a url which will autofill the form by turning dictionary into string
    url = request.url_root  + turbine.lower() + "?" + urllib.parse.urlencode(formDict)
    admin = 'admin@ecoinnovation.co.nz '

    #get the entered user and dealers email address
    user = str((request.form.get('Email', None)))
    dealer = (request.form.get('Dealer', None))

    #convert the dictionary to a list containing only the values of the form
    formValues = list(formDict.values())


    # Authorising Google Drive API

    try: # Try to submit data to spreadsheet if somthing goes wrong let them know
        scope = ['https://spreadsheets.google.com/feeds' + ' ' + 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
        client = gspread.authorize(creds)


        # open pltCalcData sheet
        sheet = client.open("pltCalcData").worksheet(worksheetName)

        # Calculate the last entered row
        last_row = int(last_entered_row(sheet))

        # Grab the numeric value of the last Calccode used and increiment it by one for the next calccode
        calccode = int(sheet.cell(last_row, 1).numeric_value + 1)

        # append the Calccode to the front of our list of values
        formValues = [calccode] + formValues

        # input that list as a row into the spreadsheet
        sheet.append_row(formValues, value_input_option='RAW')

        Calculationcode = '{0}{1}'.format(turbine, str(calccode))



    except:
        error = 1
        message = 'Error code 1: Something went wrong with submitting your data please contact admin@ecoinnovation.co.nz for support'


  #send the email

    msg = Message(subject = 'Your PowerSpout '+turbine+ ' Advanced Calculator Results (' + Calculationcode +')',
                  sender ="noreply.powerspout@gmail.com",
                  recipients = [user],
                  bcc = [admin,dealer])
    msg.html = render_template(mailTemplate, formDict=formDict, url=url, Calculationcode=Calculationcode)
    mail.send(msg)

    #error = 1
    #message = 'Error code 2: Something went wrong with submitting your data please contact admin@ecoinnovation.co.nz for support'

    if (error == 0): #then we should have success
        message = 'Success! You should have received an email of your results to the entered email address'

    responce = {
        "errors":error,
        "message":message
    }

    return json.dumps(responce)



@app.route('/PSupdateValues', methods=['GET', 'POST'])
def PSupdateValues():
    PS_fetchGUI_data()

    if (PS_siteGUI.GUI_process_option == 'firstStart'):
        # if running for the first time we need to set some additional information currenty hidden

        PS_siteGUI.GUI_cable_mm_AWG = "mm"
        # PS_siteGUI.GUI_initial_data = 0
        PS_siteGUI.GUI_process_option = 'basicdata'

        PS_siteGUI.GUIcr = '<br>'  # Carriage return with a line feed character

        PS_siteGUI.GUI_diag_cr = '<br>'

        # dialouge.cable_mm_title.set('Cable cross section mm^2')
        PS_siteGUI.GUI_cable_mm_title = 'Cable cross section mm^2'

        # dialouge.cable_AWG_title.set('Next size up cable AWG')
        PS_siteGUI.GUI_cable_AWG_title = 'Next size up cable'

        PS_siteGUI.GUI_cable_material = 'Copper'

        PS_process_here()

        #PS_siteGUI.GUI_initial_data = 1
    else:
        PS_process_here()

    #print(putHTTP_data())
    return PS_putHTTP_data()


@app.route('/LHupdateValues', methods=['GET', 'POST'])
def LHupdateValues():
    LH_fetchGUI_data()

    if (LH_siteGUI.GUI_process_option == 'firstStart'):
        # if running for the first time we need to set some additional information currenty hidden

        LH_siteGUI.GUI_cable_mm_AWG = "mm"
        # LH_siteGUI.GUI_initial_data = 0
        LH_siteGUI.GUI_process_option = 'basicdata'

        LH_siteGUI.GUIcr = '<br>'  # Carriage return with a line feed character

        LH_siteGUI.GUI_diag_cr = '<br>'

        LH_siteGUI.GUI_pipe_mat = 'Wood'
        LH_siteGUI.GUI_LHtype = 'LH/LH Pro'
        LH_siteGUI.GUI_PipeFlumeT1 = 'T1'
        LH_siteGUI.GUI_PipeFlumeT2 =  'T2'
        LH_siteGUI.GUI_PipeFlume = 'Flume'
        LH_siteGUI.GUI_Num_LH = 0

        # dialouge.cable_mm_title.set('Cable cross section mm^2')
        LH_siteGUI.GUI_cable_mm_title = 'Cable cross section mm^2'

        # dialouge.cable_AWG_title.set('Next size up cable AWG')
        LH_siteGUI.GUI_cable_AWG_title = 'Next size up cable AWG'

        LH_siteGUI.GUI_cable_material = 'Copper'

        LH_process_here()

        #LH_siteGUI.GUI_initial_data = 1
    else:
        LH_process_here()

    #print(putHTTP_data())
    return LH_putHTTP_data()


@app.route('/PHPupdateValues', methods=['GET', 'POST'])
def PHPupdateValues():
    PHP_fetchGUI_data()

    if (PHP_siteGUI.GUI_process_option == 'default'):
        # if running for the first time we need to set some additional information currenty hidden


        PHP_process_here()

        #PHP_siteGUI.GUI_initial_data = 1
    else:
        PHP_process_here()

    #print(putHTTP_data())
    return PHP_putHTTP_data()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)