import plotly.express as px
if type(file2) is str:
    file2 = [file2]
df5 = pd.DataFrame(columns=['wavenumber', 'intensity', 'File_name'])
name_title = ''
for file in file2:
    decod = io.StringIO(df_uploader2.value[file]['content'].decode(
    'utf8'))  # decod = io.StringIO(df_uploader2.value[str(list_sample) + '.*'].decode('utf8'))
    temp4 = pd.read_csv(decod, header=None)
    temp4.columns = ['wavenumber', 'intensity']
    temp4['File_name'] = file
    df5 = pd.concat([df5, temp4])
    name_title = name_title + file+ ', '
fig4 = px.line(df5,
                        x=df5['wavenumber'],
                        y='intensity',
                        color=df5['File_name'],
                        title='<b>FTIR Spectrum of sample(s) '+name_title+'</b>',
                        )
fig4.add_vrect(x0=3620, x1=3800)  # 'Clay_wt%'
fig4.add_vrect(x0=1430, x1=1770)  # 'Carb_wt%'
fig4.add_vrect(x0=1570, x1=1770)  # 'TOC_wt%'
fig4.show()
# decod = io.StringIO(df_uploader2.value[file]['content'].decode(
#     'utf8'))  # decod = io.StringIO(df_uploader2.value[str(list_sample) + '.*'].decode('utf8'))
# df_temp = pd.read_csv(decod, header=None)
# # df_temp = pd.read_csv(Path(fc.selected_path) / file, header=None)
# df_temp.columns = ['wavenumber', 'intensity']
# df_temp = df_temp.set_index('wavenumber').sort_index()
# df_temp['File_name'] = file
# fig=px.line(df_temp,
#             x=df_temp.index,
#             y="intensity",
#             color=df_temp['File_name'],
#             title='<b>FTIR Spectrum of sample '+file+'</b>',
#             )
# fig.add_vrect(x0=3620, x1=3800) #'Clay_wt%'
# fig.add_vrect(x0=1430, x1=1770) #'Carb_wt%'
# fig.add_vrect(x0=1570, x1=1770) #'TOC_wt%'
# fig.show()