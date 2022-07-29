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


def closest(num, df):
    """Return the closest wavenumber to a given number"""
    # print(num, min(df.index.values, key = lambda x : abs(x - num)))
    return min(df.index.values, key=lambda x: abs(x - num))  # return min(wavenumber, key = lambda x : abs(x - num))


def get_baseline(x1, df):
    """Return the baseline intensity of a given wavenumber index"""
    i = 0
    ind = df.index.values.tolist().index(x1)  # df.index.values.index(x1) #ind = wavenumber.index(x1)
    # print(x1,ind,ind+1)
    y = df.iloc[ind - i:ind + i + 1, 0].mean()

    return y


def area_horizontal(x1, x2, x3, df):
    """Get the peak area for x1 to x2 after removing x3 baseline area"""

    x1 = closest(x1, df)  # x1 = closest(x1)
    x2 = closest(x2, df)  # x2 = closest(x2)
    x3 = closest(x3, df)  # x3 = closest(x3)

    y = get_baseline(x3, df)
    area = trapz(df.loc[x1:x2, 'intensity'].values - y,
                 df.loc[x1:x2, 'intensity'].index)

    return area


def area_2point(x1, x2, df):
    """Get the peak area between x1 & x2 after removing x1 to x2 baseline area"""

    x1 = closest(x1, df)  # closest(x1)
    x2 = closest(x2, df)  # closest(x2)

    area = trapz(df.loc[x1:x2, 'intensity'].values,
                 df.loc[x1:x2, 'intensity'].index)
    area_2point = (df.loc[x1, 'intensity'] + df.loc[x2, 'intensity']) * (x2 - x1) / 2

    return area - area_2point


def intensity_horizontal(x1, x2, df):
    """Get the peak area between x1 & x2"""
    x1 = closest(x1, df)  # x1 = closest(x1)
    x2 = closest(x2, df)  # x2 = closest(x2)

    intensity = df.loc[x1, 'intensity']
    y = get_baseline(x2, df)

    return intensity - y


def check_value(val, low, high):
    """Check data range and assign values in final spreadsheet"""
    if val < low:
        res = 'NULL'  # '<' + str(low)
    elif val > high:
        res = high  # '>' + str(high)
    else:
        res = val
    return res


def check_gibbsite(val):
    """Check gibbsite data range and assign values in final spreadsheet"""
    if val < 0.02:
        res = 'NULL'
    elif val < 0.2:
        res = "Low"
    elif val < 0.6:
        res = "Medium"
    else:
        res = "High"

    return res


def get_value(df, label):
    """Get the values for each mineral based on raw data"""
    if label == 'Clay_abun':  # 'Clay_wt%':
        val = intensity_horizontal(3620, 3800, df)
        percentage = round((val + 0.026) / 0.0013, 2)
        final_val = check_value(percentage, 1, 90)

    elif label == 'Qtz_abun':  # 'Qtz_wt%':
        val = area_2point(1157, 1178, df)
        percentage = round((val + 0.0046) / 0.0048, 2)
        final_val = check_value(percentage, 1, 12)

    elif label == 'Carb_abun':  # 'Carb_wt%':
        val = intensity_horizontal(1430, 1770, df)
        percentage = round((val + 0.0016) / 0.0135, 2)
        final_val = check_value(percentage, 1, 40)

    elif label == 'TOC':  # 'TOC_wt%':
        val = intensity_horizontal(1570, 1770, df)
        percentage = round((val - 0.0032) / 0.0027, 2)
        final_val = check_value(percentage, 0.5, 15)

    elif label == 'Gibbs_abun':  # 'Gibbs_indx':
        val = area_2point(3500, 3550, df)
        percentage = round(val, 2)
        final_val = check_gibbsite(percentage)
    elif label == 'TSGversion':  # 'TSGVersion':
        final_val = '3.4'  # final_val = 'Python_script'
    else:
        print('Something wrong with the mineral label')

    return final_val


def sed3(fc):
    global res, files
    files = []
    for (root, dirs, file) in os.walk(Path(fc.selected_path)):
        # Skip the ipynb files folder"
        if root.endswith('ipynb_checkpoints'):
            continue
        for f in file:
            if ((f.endswith('.dpt') | f.endswith('.0') | f.endswith('.1')) and (f.split('.')[0])!='NBG'):  # if f.endswith('.dpt'):
                files.append(f)

    # res = pd.DataFrame(columns=['Sample_ID', 'Clay_wt%', 'Qtz_wt%',
    #                             'Carb_wt%','TOC_wt%',
    #                             'Gibbs_indx', 'TSGVersion'])
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
        # #Remove all existing output files in the output folder and create a new output folder
        # try:
        #     shutil.rmtree('./FTIR/output')
        # except:
        #     pass
        # #Path('C:/Users/e.ianni/Jupyternotebook/Fung_FTIR/FTIR/output').mkdir() #Path('C:/Users/e.ianni/Jupyternotebook/TSG_script')
        # os.mkdir('./FTIR/output')
        # os.mkdir('./FTIR/output/DPT')
        # # ('./FTIR/output').mkdir()

        for file in files:
            df = pd.read_csv(Path(fc.selected_path).as_posix() + '/' + file,
                             header=None)  # df = pd.read_csv(path + file, header=None)
            df.columns = ['wavenumber', 'intensity']
            df = df.set_index('wavenumber').sort_index()
            #         print(df)
            wavenumber = list(df.index)
            #         print(df)
            for mineral in res.columns:
                res.loc[file.split('.')[0], mineral] = get_value(df,
                                                                 mineral)  # res.loc[file[:-4], mineral] = get_value(df, mineral)
            # #copy over DPT files
            # shutil.copy(Path(fc.selected_path) / file, './FTIR/output/DPT') #shutil.copy('./FTIR/output/DPT/'+ file, Path(fc.selected_path)) #shutil.copy('./FTIR/output/DPT' / file, Path(fc.selected_path))

        #order list of samples accordinng with index 'Sample_ID'
        res.index = res.index.astype('int64', copy=True)
        res = res.sort_values(by=['Sample_ID'], axis=0)
        #res.index = res.index.astype('object', copy=True)

        # Warning if a sample has clay < 30% or the sum of clay, qtz, carbon and TOC < 40%
        res2 = res.copy()
        res2 = res2.replace('NULL', 0)
        if len(res2[res2['Clay_abun'] < 30]) > 1:
            #print(f"{bcolors.BOLD}{bcolors.FAIL}Warning: The samples listed below have 'Clay_abun' lower than 30%. The measurements of these samples needs to be repeated on a new fresh sample.{bcolors.ENDC}")
            #print('List of samples: {} '.format(res2[res2['Clay_abun'] < 30].index.values.tolist()))
            display(f"{bcolors.BOLD}{bcolors.FAIL}Warning: The samples listed below have 'Clay_abun' lower than 30%. The measurements of these samples needs to be repeated on a new fresh sample.{bcolors.ENDC}")
            display('List of samples: {} '.format(res2[res2['Clay_abun'] < 30].index.values.tolist()))
            display(res2[res2['Clay_abun'] < 30])
        res2['total_sum'] = res2['Clay_abun'] + res2['Qtz_abun'] + res2['Carb_abun'] + res2['TOC']
        if len(res2['total_sum'] < 40) > 1:
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
        # ## Remove all existing output files and create a new out folder #Enrico
        # shutil.rmtree(file_path / 'working')  # Enrico
        # (file_path / 'working').mkdir()  # Enrico
        
        # #make a csv file of dataframe res
        # res.to_csv('./FTIR/output/' + Path(fc.selected_path).name + '.csv', index=True) #res.to_csv('./FTIR/output/results.csv', index=True)  # res.to_csv('./output/results.csv', index=True)
        #save this csv also in the selected DPT folder
        res.to_csv(Path(fc.selected_path) / (Path(fc.selected_path).name + '.csv'), index=True)
        #df.to_csv(file_path / 'working' / (file.name[:-12] + '.csv'), index=False)
        print(f"{bcolors.OKGREEN}Successfully executed!{bcolors.ENDC}")
        # print(res)
        # return res
    else:
        res = pd.DataFrame()


# Create and display a FileChooser widget
fc = FileChooser() #'C:/') #SED_source)  # W:/Logista LMS/Logista LMS Shared/Final reports/NIR Results #os.path.normpath

# Switch to folder-only mode
fc.show_only_dirs = True

# Change the title (use '' to hide)
fc.title = '<b>Select DPT folder</b>'


def main3(b):
    sed3(fc=fc)


start_button = widgets.ToggleButton(
    value=False,
    description='Start',
    disabled=False,
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='check'  # (FontAwesome names without the `fa-` prefix)
)

start_button.observe(main3, "value")
display(fc)
display(start_button)