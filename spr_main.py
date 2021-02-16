
import pandas as pd
import pickle
import QISMAT


q = QISMAT.QISMAT()

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 160)

#####
reload_FIT_tables = True
reload_comp_libs = True
add_one_comp_lib = False

excel_file = r'QISMAT_fit_tables_txtonly_stdlib_19ww13.xlsx'
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
    q.create_FIT_table("FIT_seq",109000)
    q.read_legacy("FIT_seq",excel_file,"I_ec0_19ww13_sofa_runs")
    q.create_FIT_table("FIT_ary",3900)
    q.read_legacy("FIT_ary",excel_file,"I_P1274_rf_x2r2_Rev2p5")
    with open('spr_fit_tables.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
else:
    with open('spr_fit_tables.pkl', 'rb') as f: q = pickle.load(f)
f.close()
##################################################################
# create arch comp lib files
def my_read_arch_comp_lib(q,base_name):
    print("##### loading %s #### " % base_name)
    sheet_name = "F_"+base_name
    csv_file = 'stats/'+base_name+'.vg.qismat.csv'
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
    my_read_arch_comp_lib(q, "parcpmaram")
    my_read_arch_comp_lib(q, "parcpmcast1")
    my_read_arch_comp_lib(q, "parcpmhi")
    my_read_arch_comp_lib(q, "parcpmssma_xa")
    my_read_arch_comp_lib(q, "parcpmssmb")
    my_read_arch_comp_lib(q, "parcpmssmc_xa")
    my_read_arch_comp_lib(q, "parcpmssmd_xa")
    my_read_arch_comp_lib(q, "parcpmssme_xa")
    my_read_arch_comp_lib(q, "parcpmssmf")
    my_read_arch_comp_lib(q, "parcpmssmg_xa")

    my_read_arch_comp_lib(q, "pardinomisc")
    my_read_arch_comp_lib(q, "pardsa")
    my_read_arch_comp_lib(q, "pariax1")
    my_read_arch_comp_lib(q, "pariax2")
    my_read_arch_comp_lib(q, "pariax3")
    my_read_arch_comp_lib(q, "parnrthpk")
    my_read_arch_comp_lib(q, "parpsf")

    my_read_arch_comp_lib(q, "par_hqm_credit_hist_pipe")
    my_read_arch_comp_lib(q, "par_hqm_dir_pipe")
    my_read_arch_comp_lib(q, "par_hqm_dqed_pipe")
    my_read_arch_comp_lib(q, "par_hqm_iosf")
    my_read_arch_comp_lib(q, "par_hqm_list_sel_pipe")
    my_read_arch_comp_lib(q, "par_hqm_nalb_pipe")
    my_read_arch_comp_lib(q, "par_hqm_qed_pipe")
    my_read_arch_comp_lib(q, "par_hqm_system")

    my_read_arch_comp_lib(q, "cms3_tall")
    my_read_arch_comp_lib(q, "scf_ubox_miscpar")
    my_read_arch_comp_lib(q, "uboxpar")

    my_read_arch_comp_lib(q, "parhcachassis")
    my_read_arch_comp_lib(q, "parhcapsf")
#    my_read_arch_comp_lib(q, "parhcaws")
#    my_read_arch_comp_lib(q, "parhcasc")

    my_read_arch_comp_lib(q, "pariblcse")
    my_read_arch_comp_lib(q, "pariblmem")
    my_read_arch_comp_lib(q, "pariblsb")
    my_read_arch_comp_lib(q, "paribluc")

    my_read_arch_comp_lib(q, "llcp")
    my_read_arch_comp_lib(q, "sfp")

    my_read_arch_comp_lib(q, "parmc2lmddr")
    my_read_arch_comp_lib(q, "parmcdpddr")
    my_read_arch_comp_lib(q, "parmcscbsddr")
    my_read_arch_comp_lib(q, "parmcscpqddr")

    my_read_arch_comp_lib(q, "mdfs_hchnlp")
    my_read_arch_comp_lib(q, "mdfs_hcp")
    my_read_arch_comp_lib(q, "mdfs_hdatap")
    my_read_arch_comp_lib(q, "mdfs_hpldp")

    my_read_arch_comp_lib(q, "mdfs_vchnlp")
    my_read_arch_comp_lib(q, "mdfs_vcp")
    my_read_arch_comp_lib(q, "mdfs_vdatap")
    my_read_arch_comp_lib(q, "mdfs_vpldp")

    my_read_arch_comp_lib(q, "hsphy_wrapper0")
    my_read_arch_comp_lib(q, "hsphy_wrapper1")
    my_read_arch_comp_lib(q, "par_ialcm_dp_top")
    my_read_arch_comp_lib(q, "parfblp")
    my_read_arch_comp_lib(q, "parpi5gen4ll")
    my_read_arch_comp_lib(q, "parpi5gen4pl")
    my_read_arch_comp_lib(q, "parpi5gen4tl")
    my_read_arch_comp_lib(q, "parpi5gen5ll")
    my_read_arch_comp_lib(q, "parpi5gen5tlrx")
    my_read_arch_comp_lib(q, "parpi5gen5tltx")
    my_read_arch_comp_lib(q, "parpi5misc")
    my_read_arch_comp_lib(q, "parpi5psf")
    my_read_arch_comp_lib(q, "parvnlpif")
    my_read_arch_comp_lib(q, "parvnpipe")
    my_read_arch_comp_lib(q, "phb_filler")
    my_read_arch_comp_lib(q, "phb_vccfc")
    my_read_arch_comp_lib(q, "phb_vinf")

    my_read_arch_comp_lib(q, "pmsrvr_arrayp")
    my_read_arch_comp_lib(q, "pmsrvr_disptop")
    my_read_arch_comp_lib(q, "pmsrvr_fsmsp")
    my_read_arch_comp_lib(q, "pmsrvr_ioregsp")
    my_read_arch_comp_lib(q, "pmsrvr_srctop")
    my_read_arch_comp_lib(q, "pmsrvr_uctldp")

    my_read_arch_comp_lib(q, "scf_dummy_miscpar")

    my_read_arch_comp_lib(q, "cms3_ncap")
    my_read_arch_comp_lib(q, "m2iosf_iitcpar")
    my_read_arch_comp_lib(q, "m2iosf_iommupar")
    my_read_arch_comp_lib(q, "m2iosf_iotcpar")
    my_read_arch_comp_lib(q, "m2iosf_irppar")
    my_read_arch_comp_lib(q, "m2iosf_m2pciepar")
    my_read_arch_comp_lib(q, "m2iosf_miscpar_iocoh")

    my_read_arch_comp_lib(q, "plaoobmsm")

    my_read_arch_comp_lib(q, "plaubox")

    my_read_arch_comp_lib(q, "hsphy_wrapper_p")
    my_read_arch_comp_lib(q, "ktigen3vnhp")
    my_read_arch_comp_lib(q, "ktiphlnp")
    my_read_arch_comp_lib(q, "m2upi_bgf_wrapper")
    my_read_arch_comp_lib(q, "m2upichp")
    my_read_arch_comp_lib(q, "m2upiddp")
    my_read_arch_comp_lib(q, "miscp")

    my_read_arch_comp_lib(q, "upinvinf")

    my_read_arch_comp_lib(q, "cha_chassisp")
    my_read_arch_comp_lib(q, "cha_datap")
    my_read_arch_comp_lib(q, "cha_pipep")
    my_read_arch_comp_lib(q, "cha_pldp")

    my_read_arch_comp_lib(q, "parmcddbotddr")
    my_read_arch_comp_lib(q, "parmcddtcachemddr")
    my_read_arch_comp_lib(q, "parmcddtcachesddr")
    my_read_arch_comp_lib(q, "parmcddtopddr")
    my_read_arch_comp_lib(q, "parmcdfxbgfddr")
    my_read_arch_comp_lib(q, "parmcdfxinfddr")
    my_read_arch_comp_lib(q, "parmcsmeeddr")
    my_read_arch_comp_lib(q, "parmcvchanddr")

    my_read_arch_comp_lib(q, "parmmchas")
    my_read_arch_comp_lib(q, "parmmegr")
    my_read_arch_comp_lib(q, "parmmingr")

    my_read_arch_comp_lib(q, "fivrddra")
    my_read_arch_comp_lib(q, "gpio_sprsp")
    #my_read_arch_comp_lib(q, "miscfill00")
    my_read_arch_comp_lib(q, "miscvinf0")
    my_read_arch_comp_lib(q, "miscvinf1")

    my_read_arch_comp_lib(q, "sprcgu")
    my_read_arch_comp_lib(q, "sprfuse")
    my_read_arch_comp_lib(q, "sprglobal_misc")

    my_read_arch_comp_lib(q, "dinochnvinf")
    my_read_arch_comp_lib(q, "hch0nfivr0")
    my_read_arch_comp_lib(q, "hch0nfivr1")
    my_read_arch_comp_lib(q, "hch0nvcfc")
    my_read_arch_comp_lib(q, "hch0nvinf")
    my_read_arch_comp_lib(q, "hch1nfivr")
    my_read_arch_comp_lib(q, "hch1nvcfc")
    my_read_arch_comp_lib(q, "hch1nvinf")
    my_read_arch_comp_lib(q, "hchvmeshrpt")

    my_read_arch_comp_lib(q, "hch23nvcfc")
    my_read_arch_comp_lib(q, "hch2nfivr")
    my_read_arch_comp_lib(q, "hch2nvcfc")
    my_read_arch_comp_lib(q, "hch2nvinf")
    my_read_arch_comp_lib(q, "hch3nfivr")
    my_read_arch_comp_lib(q, "hch3nvcfc")
    my_read_arch_comp_lib(q, "hch3nvinf")
    my_read_arch_comp_lib(q, "hch4nvcfc")
    my_read_arch_comp_lib(q, "hch4nvinf")
    my_read_arch_comp_lib(q, "mdf_c_h_0")
    my_read_arch_comp_lib(q, "mdf_s_h_0")
    my_read_arch_comp_lib(q, "mdfhfivr")
    my_read_arch_comp_lib(q, "vchinf_mdf41")

    my_read_arch_comp_lib(q, "hch01svinf")
    my_read_arch_comp_lib(q, "mdf_c_v_0")
    my_read_arch_comp_lib(q, "mdfvfivr")

    my_read_arch_comp_lib(q, "hch23svinf")

    my_read_arch_comp_lib(q, "corevinf")
    my_read_arch_comp_lib(q, "fivrcore")

    my_read_arch_comp_lib(q, "mcfivr")
    my_read_arch_comp_lib(q, "parmchchanddr")
    # my_read_arch_comp_lib(q, "sprddr") # no standard cells
    my_read_arch_comp_lib(q, "vchinf_corepair")
    my_read_arch_comp_lib(q, "vchinf_mc")
    my_read_arch_comp_lib(q, "vchinf_center")

    my_read_arch_comp_lib(q, "vchcfc_mdf42")
    my_read_arch_comp_lib(q, "vchinf_mdf42")
    my_read_arch_comp_lib(q, "vchcfc_mdf43")
    my_read_arch_comp_lib(q, "vchinf_mdf43")
    my_read_arch_comp_lib(q, "vchcfc_mdf44")

    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
else:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)

f.close()

if add_one_comp_lib:
    with open('spr_with_comp_lib.pkl', 'rb') as f: q = pickle.load(f)
    my_read_arch_comp_lib(q, "vchinf_corepair")
    with open('spr_with_comp_lib.pkl', 'wb') as f: pickle.dump(q, f, pickle.HIGHEST_PROTOCOL)
    f.close()

## create the static FIT table:
q.create_StaticFITTable( "FIT_static_table", "I_spr_summary_19ww43", "F_complib", csv_filename="static_fit_cell_list.csv")
#q.create_StaticFITTable( "FIT_static_table", "I_spr_summary_19ww43", "F_complib", csv_filename="static_fit_cell_list_short.csv")
q.sheet_list["FIT_static_table"].calc()



## create the rest of the rollup:
if 'P_hier_seq' in q.sheet_list.keys():
    del q.sheet_list['P_hier_seq']
q.create_ArchProductRollup('P_hier_seq')
q.sheet_list['P_hier_seq'].read_csv('sprxcc_hier_19ww39.csv')
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

#q.sheet_list['P_hier_seq'].QISMAT_print(minrow=278,maxrow=315,cols=['Unit_Name','Subunit_Src_Sheet','Subunit_Name','Instance_Count','Total_SDC','Total_DUE'])
