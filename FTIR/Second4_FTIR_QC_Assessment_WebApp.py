import plotly.express as px
list_CRMs = df_NIR_2_melt_pivot.index.get_level_values('Sample ID').unique().tolist()
list_samples = {}
fig = {}
df4 = {}

# input_files = list(df_uploader2.value.values())

for list_CRM in list_CRMs:
    list_samples[list_CRM] = df_NIR_2_melt_pivot[
        df_NIR_2_melt_pivot.index.get_level_values('Sample ID') == list_CRM].index.get_level_values(
        'Sample').unique().tolist()
    df4[list_CRM] = pd.DataFrame(columns=['wavenumber', 'intensity', 'File_name'])
    # f4 = df4.set_index('wavenumber').sort_index()

    #input_files = list(df_uploader2.value.values())
    # for file in input_files:
    #     decod = io.StringIO(file['content'].decode('utf8'))
    #     df = pd.read_csv(decod, header=None)

    for list_sample in list_samples[list_CRM]:
        # for file in (Path(fc.selected_path)).glob('**/' + str(list_sample) + '.*'):
        #     break
        # file = file.name
        for file in list(df_uploader2.value.keys()):
            #print(file.split('.')[0],list_sample)
            if (int(file.split('.')[0]) == list_sample):
                #print('ciao')
                break
                #name=file
                # print(file.split('.')[0])
        #print(file)
        decod = io.StringIO(df_uploader2.value[file]['content'].decode('utf8')) #decod = io.StringIO(df_uploader2.value[str(list_sample) + '.*'].decode('utf8'))
        temp4 = pd.read_csv(decod, header=None)

        # for file in (Path(fc.selected_path)).glob('**/' + str(list_sample) + '.*'):
        #     break
        # file = file.name
        # temp4 = pd.read_csv(Path(fc.selected_path) / file, header=None)
        temp4.columns = ['wavenumber', 'intensity']
        #         temp4 = temp4.set_index('wavenumber').sort_index()
        temp4['File_name'] = df_uploader2.value[file]['metadata']['name']
        df4[list_CRM] = pd.concat([df4[list_CRM], temp4])

    fig[list_CRM] = px.line(df4[list_CRM],
                            x=df4[list_CRM]['wavenumber'],  # x='File_name',
                            y='intensity',
                            color=df4[list_CRM]['File_name'],
                            title='<b>FTIR Spectrum of readings of ' + list_CRM + '</b>',
                            )
    fig[list_CRM].add_vrect(x0=3620, x1=3800)  # 'Clay_wt%'
    fig[list_CRM].add_vrect(x0=1430, x1=1770)  # 'Carb_wt%'
    fig[list_CRM].add_vrect(x0=1570, x1=1770)  # 'TOC_wt%'
    fig[list_CRM].show()