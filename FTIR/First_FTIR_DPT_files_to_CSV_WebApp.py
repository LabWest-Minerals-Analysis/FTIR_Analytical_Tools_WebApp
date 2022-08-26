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

def sed4(df_uploader2):
    global res, files
    input_files = list(df_uploader2.value.values())
    files = []
    for f in input_files:
        if ((f.endswith('.dpt') | f.endswith('.0') | f.endswith('.1') | f.endswith('.2') | f.endswith('.3') | f.endswith('.4') | f.endswith('.5') | f.endswith('.6') | f.endswith('.7') | f.endswith('.8') | f.endswith('.9')) and (f.split('.')[0]) != 'NBG'):  # if f.endswith('.dpt'):
            files.append(f)

    res = pd.DataFrame(columns=['Sample_ID', 'Clay_abun', 'Qtz_abun',
                                'Carb_abun', 'TOC',
                                'Gibbs_abun', 'TSGversion'])
    res['Sample_ID'] = [x.split('.')[0] for x in sorted(files)]  # res['Sample_ID'] = [x[:-4] for x in sorted(files)]
    res = res.set_index('Sample_ID')

    # Warning if Sample name has a duplicate such as '90.0' and '90.1'. A warning mesasge will pop up.
    err = False
    for index in range(len(res.index.value_counts().index)):
        if res.index.value_counts().values.tolist()[index] > 1:
            print(
                f"{bcolors.BOLD}{bcolors.FAIL}Warning: There are duplicates. Please, fix this issue first and then restart this analytical tool from the beginning.{bcolors.ENDC}")
            print('Sample: {} is present {} times.'.format(res.index.value_counts().index.tolist()[index],
                                                           res.index.value_counts().values.tolist()[index]))
            err = True
    
    #This ERROR can e remove if validateing STDs (QC).
    # Warning if Sample name is not a integer
    for index in range(len(res.index.values.tolist())):  # range(len(res.index.value_counts().index)):
        try:
            bb = int(res.index.values.tolist()[index])
        except:
            print(
                f"{bcolors.BOLD}{bcolors.FAIL}Warning: There are samples that are not named correctly. A sample name should be an integer. Please, fix this issue first and then restart this analytical tool from the beginning.{bcolors.ENDC}")
            print('Sample, {}, has a wrong name.'.format(res.index.values.tolist()[index]))
            err = True

    if not err:
        print(f"{bcolors.OKGREEN}Successfully executed!{bcolors.ENDC}")
    else:
        res = pd.DataFrame()

#upload dpt files
df_uploader2 =widgets.FileUpload(
    accept='*.csv',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    multiple=True,  # True to accept multiple files upload else False
    description="Upload_dpt(s)"
)

def main3(b):
    sed4(df_uploader2=df_uploader2)


start_button = widgets.ToggleButton(
    value=False,
    description='Start',
    disabled=False,
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='check'  # (FontAwesome names without the `fa-` prefix)
)

start_button.observe(main3, "value")
display(df_uploader2)
display(start_button)