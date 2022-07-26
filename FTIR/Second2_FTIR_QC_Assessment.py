# df come from the previous step. Unfrotunatelly at moment the previus step does not work. It needs to be fixed.
###df = pd.read_csv('TSG_script/ALW006393_NIR.csv') #remove this
###df = df.rename(columns={'Grp1 uTSAS': 'MinGrp1'}) #remove this
###df = df.rename(columns={'Grp2 uTSAS': 'MinGrp2'}) #remove this

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# # This is valid only for NIR data
# df['Sample'] = df['Sample'].str.split('.asd').str[0]  # df['Sample'] = df['Sample'].str.split('.').str[0]
# # right = df['Identifier'].str[-5:]
# # left = df['Identifier'].str[:5]
# df['Sample'] = df['Sample'].str.split('_').str[1]
# df['Sample'] = pd.to_numeric(df['Sample'])

# For FTIR data the name of samples should be like '126.0'. However, by mistake, some times the name of samples are wronlgy like '126.1'
# Thus, we should replace 'df['Sample'] = df['Sample'].str.split('.asd').str[0]' with 'df['Sample'] = df['Sample'].str.split('.').str[0]'
#No, thi is already been done previously

# # Warning if Sample name is wrong such as 'sdrrf6596.sed'. A warning mesasge will pop up.
# err = False
# if np.count_nonzero(np.isnan(df.Sample)) > 0:
#     print(
#         f"{bcolors.BOLD}{bcolors.FAIL}Warning: There are some samples name that are in the wrong format. Please, fix this issue first and then restart this analytical tool from the beginning.{bcolors.ENDC}")
#     err = True


df = res.copy()
df = df.reset_index()
###We have already checked that the 'Sample_ID' are all unique and all numbers.
df.Sample_ID = pd.to_numeric(df.Sample_ID)
df = df.rename(columns={"Sample_ID": "Sample"}, errors="raise")

df_QC = pd.read_csv('FTIR/FTIR_QC_STDs_Validated.csv') #QC_UFF_320_REFSAM_STD_FTIR_df-style
df_QC = df_QC.rename(columns={'CRMID': 'Sample ID'})

# # Warning if Sample name has a duplicate such as '6596_00008 (2).sed' (Sample is 8) and '6596_00008.sed' (Sample is 8). A warning mesasge will pop up.
# for index in range(len(df['Sample'].value_counts().index)):
#     if df['Sample'].value_counts().values.tolist()[index] > 1:
#         print(
#             f"{bcolors.BOLD}{bcolors.FAIL}Warning: There are duplicates. Please, fix this issue first and then restart this analytical tool from the beginning.{bcolors.ENDC}")
#         print('Sample: {} is present {} times.'.format(df['Sample'].value_counts().index.tolist()[index],
#                                                        df['Sample'].value_counts().values.tolist()[index]))
#         err = True

#if not err:
# Warning if a Sample expected to be read according with 'df_FTIR_sample_list' does not have a .sed file (df['Sample'])
list_expected_samples = df_FTIR_sample_list.Sample.tolist()
list_read_samples = df.Sample.tolist()
for list_expected_sample in list_expected_samples:
    if not list_expected_sample in list_read_samples:
        print(
            f"{bcolors.BOLD}{bcolors.FAIL}Warning: There are samples not read. Please, check if these samples were ment to be read or not. If they were meant to be read, please read this samples and then restart this analytical tool from the beginning. This script was not stopped.{bcolors.ENDC}")
        print('Sample: {} is MISSING.'.format(list_expected_sample))
# the df is merged with the info from df_QC
df = df.merge(df_FTIR_sample_list, how='left', on='Sample').copy()
list_QC = df_QC['Sample ID'].unique()
df = df[df['Sample ID'].isin(list_QC)].copy()
cols = df.columns.tolist()
#Place the new header 'Sample ID' in the first column
cols = cols[-1:] + cols[:-1]
df = df[cols]
list_floats = ['Clay_abun', 'Qtz_abun', 'Carb_abun', 'TOC']
for list_float in list_floats:
    if list_float in df.columns:
        df[list_float] = pd.to_numeric(df[list_float], errors='coerce')
#display(df_QC) #df_QC