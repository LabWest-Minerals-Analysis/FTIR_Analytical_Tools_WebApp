import plotly.express as px
decod = io.StringIO(df_uploader2.value[file]['content'].decode(
    'utf8'))  # decod = io.StringIO(df_uploader2.value[str(list_sample) + '.*'].decode('utf8'))
df_temp = pd.read_csv(decod, header=None)
# df_temp = pd.read_csv(Path(fc.selected_path) / file, header=None)
df_temp.columns = ['wavenumber', 'intensity']
df_temp = df_temp.set_index('wavenumber').sort_index()
df_temp['File_name'] = file
fig=px.line(df_temp,
            x=df_temp.index,
            y="intensity",
            color=df_temp['File_name'],
            title='<b>FTIR Spectrum of sample '+file+'</b>',
            )
fig.add_vrect(x0=3620, x1=3800) #'Clay_wt%'
fig.add_vrect(x0=1430, x1=1770) #'Carb_wt%'
fig.add_vrect(x0=1570, x1=1770) #'TOC_wt%'
fig.show()