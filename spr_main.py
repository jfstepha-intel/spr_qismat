import sys
import pandas as pd
import pickle
import QISMAT


q = QISMAT.QISMAT()

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 160)

#####
reload_FIT_tables = False
reload_comp_libs = False
add_one_comp_lib = False

excel_file = r'spr_fit_tables(JStephan)19ww04.xlsx'
complibmap={
    'Cluster_Name': 'Cluster',
    'Block_Name': 'Block',
    'Unit_Name': 'FUB Name',
    'Design_Style': 'Design Style',
    'Port_Configuration': 'Port Configuration',
    'Circuit_Topology': 'Circuit Topology',
    'Circuit_Subtype': 'Circuit Subtype',
    'Operating_Voltage': 'Operating Voltage',
    'Temperature': 'Temperature',
    'Altitude': 'Altitude',
    'TDF': 'TDF',
    'FlopLatch_Protection': 'Flop/Latch Protection',
    'Instance_Count': 'Instances'}
##################################################################
# Create a new workbook
print("------------------------------------------------------")
q = QISMAT.QISMAT()

q.sheet_list['default'].read_csv('params.csv')
q.sheet_list['default'].QISMAT_print()

##################################################################
# FIT table Download
print("------------------------------------------------------")

if reload_FIT_tables:
    q.create_FIT_table("FIT_seq",19000)
    q.read_legacy("FIT_seq",excel_file,"I_EC0_x2r3_18ww15_SOFA_runs")
    q.create_FIT_table("FIT_ary",3800)
    q.read_legacy("FIT_ary",excel_file,"I_P1274_RF_x2r2_Rev2p5")
    with open('spr_fit_tables.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
else:
    with open('spr_fit_tables.pkl', 'rb') as f: q = pickle.load(f)

##################################################################
# create arch comp lib files
def my_read_arch_comp_lib(q,base_name):
    print("##### loading %s #### " % base_name)
    sheet_name = "F_"+base_name
    csv_file = 'stats/'+base_name+'.apr_final.vg.qismat.csv'
    q.create_ArchCompLib(sheet_name, fitsource="FIT_seq", csv_filename=csv_file,
                         mapping=complibmap, do_calc=True)
    q.sheet_list[sheet_name].QISMAT_print(maxrow=10, cols=['Cluster_Name', 'Total_SDC', 'Total_DUE'])
    print("total:")
    print("   SDC: %f" % q.sheet_list[sheet_name].main.df.Total_SDC.sum(skipna=True))
    print("   DUE: %f" % q.sheet_list[sheet_name].main.df.Total_DUE.sum(skipna=True))

##################################################################
# create arch comp lib files
def my_read_arch_comp_lib_syn(q,base_name):
    print("##### loading %s #### " % base_name)
    sheet_name = "F_"+base_name+"_syn"
    csv_file = '../../spr_stats_19ww04/syn/'+base_name+'.syn_final.vg.qismat.csv'
    q.create_ArchCompLib(sheet_name, fitsource="FIT_seq", csv_filename=csv_file,
                         mapping=complibmap, do_calc=True)
    q.sheet_list[sheet_name].QISMAT_print(maxrow=10, cols=['Cluster_Name', 'Total_SDC', 'Total_DUE'])
    print("total:")
    print("   SDC: %f" % q.sheet_list[sheet_name].main.df.Total_SDC.sum(skipna=True))
    print("   DUE: %f" % q.sheet_list[sheet_name].main.df.Total_DUE.sum(skipna=True))

if reload_FIT_tables or reload_comp_libs:
    my_read_arch_comp_lib(q, "chtopaonv" )
    my_read_arch_comp_lib(q, "chtopaonv230")
    my_read_arch_comp_lib(q, "fivrnorthex")
    my_read_arch_comp_lib(q, "hbmio_2dw_slice")
    my_read_arch_comp_lib(q, "hbmio_4aw_slice")
    my_read_arch_comp_lib(q, "pmsrvr_mspmas")
    my_read_arch_comp_lib(q, "pmsrvr_pmax_top")
    my_read_arch_comp_lib(q, "pmsrvr_sapmas")
    my_read_arch_comp_lib(q, "pmsrvr_upmas")
    my_read_arch_comp_lib(q, "soc_cnxtile_misc")
    my_read_arch_comp_lib(q, "ubox")
    my_read_arch_comp_lib(q, "cha_chassisp")
    my_read_arch_comp_lib(q, "cha_datap")
    my_read_arch_comp_lib(q, "cha_pldp")

    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
else:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)

if add_one_comp_lib:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)
    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)

if 'P_subsystems' in q.sheet_list.keys():
    del q.sheet_list['P_subsystems']
q.create_ArchProductRollup("P_subsystems",15)
q.sheet_list['P_subsystems'].read_csv("subsystems.csv")
q.sheet_list['P_subsystems'].blank_col_header_rows()
q.sheet_list['P_subsystems'].calc()
q.sheet_list['P_subsystems'].QISMAT_print(maxrow=20, cols=['Unit_Name','Subunit_Src_Sheet','Subunit_Name','Instance_Count','Total_SDC','Total_DUE'])


if 'P_Rollup' in q.sheet_list.keys():
    del q.sheet_list['P_Rollup']

q.create_ArchProductRollup("P_Rollup")
q.sheet_list['P_Rollup'].read_csv("rollup.csv")
q.sheet_list['P_Rollup'].blank_col_header_rows()
q.sheet_list['P_Rollup'].calc()
q.sheet_list['P_Rollup'].QISMAT_print(maxrow=5, cols=['Unit_Name','Subunit_Src_Sheet','Subunit_Name','Description','Instance_Count','Total_SDC','Total_DUE'])

q.create_ArchProductSummary("S_Summary",2)
q.sheet_list['S_Summary'].read_csv('summary.csv')
q.sheet_list['S_Summary'].calc()
q.sheet_list['S_Summary'].blank_col_header_rows()
q.sheet_list['S_Summary'].QISMAT_print()


q.write_csv( "output/SPR")

#### get a summary of lookup stats ####
print("summarizing lookup stats")
n = pd.DataFrame(columns=['name','match','default','not_found','error'])
for i in range(len(q.sheet_list)):
    name = list(q.sheet_list.keys())[i]
    if q.sheet_list[name].info.Sheet_Type == "Arch Component Library":
        df = q.sheet_list[name].get_lookup_stats(False)
        n.loc[i] = [name,df['MATCH']['Neutron_Status'],df['DEFAULT']['Neutron_Status'],df['NOT FOUND']['Neutron_Status'],df['ERROR']['Neutron_Status'] ]

n['total'] = n.match + n.default + n.not_found + n.error
n['match_fraction'] = n.match / n.total
print(n)

