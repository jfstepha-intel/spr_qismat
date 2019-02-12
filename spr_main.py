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
    csv_file = 'stats/syn/'+base_name+'.syn_final.vg.qismat.csv'
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
    my_read_arch_comp_lib_syn(q, "mcfivr")
    my_read_arch_comp_lib_syn(q, "vchinf_mdf45")
    my_read_arch_comp_lib_syn(q, "vchcfc_mdf45")
    my_read_arch_comp_lib_syn(q, "mdfhfivr")
    my_read_arch_comp_lib_syn(q, "vchinf_mdf44")
    my_read_arch_comp_lib_syn(q, "vchcfc_mdf44")
    my_read_arch_comp_lib_syn(q, "vchinf_mdf43")
    my_read_arch_comp_lib_syn(q, "vchcfc_mdf43")
    my_read_arch_comp_lib_syn(q, "vchcfc_mdf42")
    my_read_arch_comp_lib_syn(q, "vchinf_mdf42")
    my_read_arch_comp_lib_syn(q, "vchinf_center")
    my_read_arch_comp_lib_syn(q, "vchinf_corepair")
    my_read_arch_comp_lib_syn(q, "fivrcore")
    my_read_arch_comp_lib_syn(q, "corevinf")
    my_read_arch_comp_lib_syn(q, "mdfvfivr")
    my_read_arch_comp_lib_syn(q, "hch23svinf")
    my_read_arch_comp_lib_syn(q, "hch01svinf")
    my_read_arch_comp_lib_syn(q, "vchinf_mdf41")
    my_read_arch_comp_lib_syn(q, "mdf_c_h_0")
    my_read_arch_comp_lib_syn(q, "hchvmeshrpt")
    my_read_arch_comp_lib_syn(q, "hch4nvinf")
    my_read_arch_comp_lib_syn(q, "hch3nvinf")
    my_read_arch_comp_lib_syn(q, "hch3nvcfc")
    my_read_arch_comp_lib_syn(q, "hch3nfivr")
    my_read_arch_comp_lib_syn(q, "hch2nvinf")
    my_read_arch_comp_lib_syn(q, "hch2nvcfc")
    my_read_arch_comp_lib_syn(q, "hch2nfivr")
    my_read_arch_comp_lib_syn(q, "hch23nvcfc")
    my_read_arch_comp_lib_syn(q, "upinvinf")
    my_read_arch_comp_lib_syn(q, "hch1nvinf")
    my_read_arch_comp_lib_syn(q, "hch1nvcfc")
    my_read_arch_comp_lib_syn(q, "hch1nfivr")
    my_read_arch_comp_lib_syn(q, "hch0nvinf")
    my_read_arch_comp_lib_syn(q, "hch0nvcfc")
    my_read_arch_comp_lib_syn(q, "hch0nfivr1")
    my_read_arch_comp_lib_syn(q, "hch0nfivr0")
    my_read_arch_comp_lib_syn(q, "dinochnvinf")
    my_read_arch_comp_lib_syn(q, "sprglobal_misc")
    my_read_arch_comp_lib_syn(q, "sprfuse")
    my_read_arch_comp_lib_syn(q, "sprcgu")
    my_read_arch_comp_lib_syn(q, "miscvinf1")
    my_read_arch_comp_lib_syn(q, "miscvinf0")
    my_read_arch_comp_lib_syn(q, "gpio_sprsp")
    my_read_arch_comp_lib_syn(q, "fivrddra")
    my_read_arch_comp_lib(q, "parmmingr")
    my_read_arch_comp_lib(q, "parmmegr")
    my_read_arch_comp_lib(q, "parmmchas")
    my_read_arch_comp_lib_syn(q, "cms3_tall")
    my_read_arch_comp_lib_syn(q, "mdfs_hpldp")
    my_read_arch_comp_lib_syn(q, "mdfs_hdatap")
    my_read_arch_comp_lib_syn(q, "parmcsmeeddr")
    my_read_arch_comp_lib_syn(q, "parmchchanddr")
    my_read_arch_comp_lib_syn(q, "parmcdfxinfddr")
    my_read_arch_comp_lib_syn(q, "parmcddtopddr")
    my_read_arch_comp_lib_syn(q, "parmcdfxbgfddr")
    my_read_arch_comp_lib_syn(q, "parmcddtcachesddr")
    my_read_arch_comp_lib_syn(q, "parmcddbotddr")
    my_read_arch_comp_lib_syn(q, "sfp")
    my_read_arch_comp_lib_syn(q, "llcp")
    my_read_arch_comp_lib_syn(q, "cha_pipep")
    my_read_arch_comp_lib(q, "miscp")
    my_read_arch_comp_lib(q, "m2upiddp")
    my_read_arch_comp_lib(q, "m2upichp")
    my_read_arch_comp_lib_syn(q, "m2upi_bgf_wrapper")
    my_read_arch_comp_lib(q, "ktiphlnp")
    my_read_arch_comp_lib(q, "ktigen3vnhp")
    my_read_arch_comp_lib_syn(q, "hsphy_wrapper_p")
    my_read_arch_comp_lib_syn(q, "cms3_ncap")
    my_read_arch_comp_lib(q, "m2iosf_miscpar_iocoh")
    my_read_arch_comp_lib(q, "m2iosf_m2pciepar")
    my_read_arch_comp_lib(q, "m2iosf_irppar")
    my_read_arch_comp_lib(q, "m2iosf_iotcpar")
    my_read_arch_comp_lib(q, "m2iosf_iommupar")
    my_read_arch_comp_lib(q, "m2iosf_iitcpar")
    my_read_arch_comp_lib_syn(q, "scf_dummy_miscpar")
    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
else:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)

if add_one_comp_lib:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)
    my_read_arch_comp_lib(q, "pmsrvr_uctldp")
    my_read_arch_comp_lib_syn(q, "pmsrvr_srctop")
    my_read_arch_comp_lib(q, "pmsrvr_ioregsp")
    my_read_arch_comp_lib(q, "pmsrvr_fsmsp")
    my_read_arch_comp_lib(q, "pmsrvr_disptop")
    my_read_arch_comp_lib(q, "pmsrvr_arrayp")
    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)

if 'P_hier_seq' in q.sheet_list.keys():
    del q.sheet_list['P_hier_seq']
q.create_ArchProductRollup('P_hier_seq')
q.sheet_list['P_hier_seq'].read_csv('sprxcc_hier.csv')
q.sheet_list['P_hier_seq'].blank_col_header_rows()
q.sheet_list['P_hier_seq'].calc()
q.sheet_list['P_hier_seq'].QISMAT_print(maxrow=400,cols=['Unit_Name','Subunit_Src_Sheet','Subunit_Name','Instance_Count','Total_SDC','Total_DUE'])


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

q.sheet_list['P_hier_seq'].QISMAT_print(minrow=100,maxrow=140,cols=['Unit_Name','Subunit_Src_Sheet','Subunit_Name','Instance_Count','Total_SDC','Total_DUE'])
