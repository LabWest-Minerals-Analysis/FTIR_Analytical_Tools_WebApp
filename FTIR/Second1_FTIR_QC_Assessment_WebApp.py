# RUN ME and select file: _EC_pH_Template.xlsm from the job folder (source folder)
# def read_files_from_uploader1(uploader):
#     df_FTIR_sample_list = pd.read_excel(open(fc2.selected, 'rb'), sheet_name='Sample CSV list', usecols =[0,1])
#     df_FTIR_sample_list = df_FTIR_sample_list[df_FTIR_sample_list['Sample ID'].notna()].copy()
#     df_FTIR_sample_list = df_FTIR_sample_list.rename(columns={'#': 'Sample'})
#     return df_FTIR_sample_list

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

def read_files_from_uploader1(uploader):
    # this if is in case we actually want to load the csv file 'SampleID_matching_list' that it is going to be generated in folder 'working'. Thus, this code can be used from CSIRO researchers who have only the backup zip file from the cloud.
    if uploader.selected[-4:] == '.csv':
        df_FTIR_sample_list = pd.read_csv(uploader.selected)
    else:
        df_FTIR_sample_list = pd.read_excel(open(uploader.selected, 'rb'), sheet_name='Sample CSV list', usecols=[0, 1])
        df_FTIR_sample_list = df_FTIR_sample_list[df_FTIR_sample_list['Sample ID'].notna()].copy()
        df_FTIR_sample_list = df_FTIR_sample_list.rename(columns={'#': 'Sample'})
    #df_FTIR_sample_list.to_csv(Path('./FTIR/output') / ('SampleID_matching_list.csv'), index=False) #df_FTIR_sample_list.to_csv(file_path / 'working' / ('SampleID_matching_list.csv'), index=False)
    print(f"{bcolors.OKGREEN}Successfully executed!{bcolors.ENDC}")
    return df_FTIR_sample_list


def main(b):
    global df_FTIR_sample_list
    df_FTIR_sample_list = read_files_from_uploader1(uploader=fc2)
    return df_FTIR_sample_list


# Create and display a FileChooser widget
# Shorthand reset
fc2 = FileChooser('C:/')#Sample_EC_pH_Template)

# Set a file filter pattern (uses https://docs.python.org/3/library/fnmatch.html)
fc2.filter_pattern = ['*.xlsm', '*.csv']  # '*.xlsm' #At Labwest we are only going to use .xlsm files

# Change the title (use '' to hide)
fc2.title = '<b>Select _EC_pH_Template.xlsm of this job</b>'

start_button2 = widgets.ToggleButton(
    value=False,
    description='Start',
    disabled=False,
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='check'  # (FontAwesome names without the `fa-` prefix)
)

start_button2.observe(main, "value")
display(fc2)
display(start_button2)