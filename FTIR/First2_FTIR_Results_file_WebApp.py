import io
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

def sed_results(df_uploader_results):
    global res

    decod = io.StringIO(list(df_uploader_results.value.values())[0]['content'].decode('utf8'))
    res = pd.read_csv(decod)
    res.replace(to_replace=np.nan, value='NULL', inplace=True)
    res = res.set_index('Sample_ID')
    res.index = res.index.astype('int64', copy=True)
    res = res.sort_values(by=['Sample_ID'], axis=0)

    # Warning if a sample has clay < 30% or the sum of clay, qtz, carbon and TOC < 40%
    res2 = res.copy()
    res2 = res2.replace('NULL', 0)
    if len(res2[res2['Clay_abun'] < 30]) > 1:
        print(f"{bcolors.BOLD}{bcolors.FAIL}Warning: The samples listed below have 'Clay_abun' lower than 30%. The measurements of these samples needs to be repeated on a new fresh sample.{bcolors.ENDC}")
        print('List of samples: {} '.format(res2[res2['Clay_abun'] < 30].index.values.tolist()))
        display(res2[res2['Clay_abun'] < 30])
    res2['total_sum'] = res2['Clay_abun'] + res2['Qtz_abun'] + res2['Carb_abun'] + res2['TOC']
    if len(res2[res2['total_sum'] < 40]) > 1:
        print(
            f"{bcolors.BOLD}{bcolors.FAIL}Warning: The samples listed below have the sum of 'Clay_abun', 'Qtz_abun', 'Carb_abun' and 'TOC' lower than 40%. The measurements of these samples needs to be repeated on a new fresh sample.{bcolors.ENDC}")
        print('List of samples: {} '.format(res2[res2['total_sum'] < 40].index.values.tolist()))
        display(res2[res2['total_sum'] < 40])

    # rounding
    list_floats = ['Clay_abun', 'Qtz_abun', 'Carb_abun', 'TOC']
    for list_float in list_floats:
        if list_float in res.columns:
            res[list_float] = pd.to_numeric(res[list_float], errors='coerce')
            res[list_float] = res[list_float].round(decimals=1)
            res[list_float] = res[list_float].fillna('NULL')

    print(f"{bcolors.OKGREEN}Successfully executed!{bcolors.ENDC}")


#upload csv files
df_uploader_results =widgets.FileUpload(
    accept='.csv',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    multiple=False,  # True to accept multiple files upload else False
    description="Upload_csv_results"
)

def main_results(b):
    sed_results(df_uploader_results=df_uploader_results)


start_button_results = widgets.ToggleButton(
    value=False,
    description='Start',
    disabled=False,
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='check'  # (FontAwesome names without the `fa-` prefix)
)

start_button_results.observe(main_results, "value")
display(df_uploader_results)
display(start_button_results)