import pandas as pd
import numpy as np
Nan = np.NaN

infilename = 'stats_19ww32/blocks_info_19ww32_with_sch.csv'
outfilename = 'sprxcc_hier_19ww32.csv'
sheet_name = 'P_hier_seq'
top='sprspxcc'

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 160)

def process_sub_template( mydf, sub_template, level):
    print("l%d: processing %s" % (level, sub_template) )
    this_df = mydf[ df.physical_parent == sub_template]
    df_out = this_df
    df_out['comment']="sub_template:%s"%sub_template
    df_out['level']=level

    template_list = this_df.template
    for template in template_list:
        # print("  processing sub template %s" %template)
        if sum(mydf.physical_parent == template) > 0:
            header_row = pd.Series(['', '', template, '', '', '', '', level+1, template,'',''],
                                  index=['name', 'template', 'physical_parent', 'date', 'time', 'path', 'comment',
                                         'level','Unit_Name','Subunit_Src_Sheet','Subunit_Name'])
            df_out = df_out.append( header_row, ignore_index=True )
            sub_df = process_sub_template( mydf, template, level+1)
            df_out = df_out.append( sub_df )
        else:
            df_out.loc[ df_out.template == template, 'comment'] = 'No Subcell'
            df_out.loc[ df_out.template == template, 'Subunit_Src_Sheet'] = 'F_' + template


    return df_out

df_tmp = pd.read_csv(infilename)
df = df_tmp[ ['name','template','physical_parent','date','time','path']]
df['level'] = 0
df['Unit_Name'] = df.physical_parent
df['Subunit_Src_Sheet'] = sheet_name
df['Subunit_Name'] = df.template
df_final = process_sub_template( df, top, 1)
df_final = df_final.sort_values(['level','physical_parent'], ascending=[0,1])
df_final.to_csv(outfilename)
