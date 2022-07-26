# df is a pivot table.
# We do the inverse of a pivot table using 'melt', thus, we have introduced a new column 'Element'.

# df_NIR_2 = df.copy()
# I am only considering Elements that are float64.df.columns[df.dtypes == 'float64']
df_NIR_2_melt = pd.melt(df, id_vars=['Sample ID', 'Sample'],
                        value_vars=list(df.columns[2:]),
                        # value_vars=list(df.columns[df.dtypes == 'float64']),# 3:]), # list of days of the week #value_vars=list(df.columns[2:]),# 3:]), # list of days of the week
                        var_name='Element',
                        value_name='Reading')

# We can now merge the expected values and ranges (SD) of our standards.
df_NIR_2_melt = df_NIR_2_melt.merge(df_QC, how='left', on=['Sample ID', 'Element']).copy()
df_NIR_2_melt = df_NIR_2_melt[
    (df_NIR_2_melt['ConentrationClassification'].notna()) | (df_NIR_2_melt['Conentration'].notna())].copy()

# We can now pivot back the table.
# replacing values in Concentration with value of ConentrationClassification when value concentration are NaN
df_NIR_2_melt.loc[(df_NIR_2_melt['ConentrationClassification'].notna()) & (df_NIR_2_melt['Conentration'].isnull()), [
    'Conentration']] = df_NIR_2_melt.loc[
    (df_NIR_2_melt['ConentrationClassification'].notna()) & (df_NIR_2_melt['Conentration'].isnull()), [
        'ConentrationClassification']].values  # df_NIR_2_melt.loc[(df_NIR_2_melt['ConentrationClassification'].notna())&(df_NIR_2_melt['Conentration'].isnull()),['ConentrationClassification']]

df_NIR_2_melt = df_NIR_2_melt[
    (df_NIR_2_melt['ConentrationClassification'].notna()) | (df_NIR_2_melt['Conentration'].notna())].copy()

df_NIR_2_melt_pivot = df_NIR_2_melt.pivot(index=['Sample ID', 'Sample'], columns=['Element'],
                                          values=['Reading', 'Conentration', 'SD'])

# list of float Elements
list_Element_float = []
for lEl in df.columns[df.dtypes == 'float64'].tolist():
    if lEl in df_NIR_2_melt_pivot.Reading.columns.tolist():
        list_Element_float.append(lEl)
# list of object Elements
list_Element_object = []
for lEl in df.columns[df.dtypes == 'object'].tolist():
    if lEl in df_NIR_2_melt_pivot.Reading.columns.tolist():
        list_Element_object.append(lEl)

idx0_pivot = pd.IndexSlice

list_samples_fc = {}
list_samples_fc2 = {}
for lEl_float in list_Element_float:
    list_samples_fc[lEl_float] = df_NIR_2_melt_pivot[(df_NIR_2_melt_pivot.Reading[lEl_float] < (
                df_NIR_2_melt_pivot.Conentration[lEl_float] - 2 * df_NIR_2_melt_pivot.SD[lEl_float])) | (
                                                                 df_NIR_2_melt_pivot.Reading[lEl_float] > (
                                                                     df_NIR_2_melt_pivot.Conentration[lEl_float] + 2 *
                                                                     df_NIR_2_melt_pivot.SD[lEl_float]))].index
    list_samples_fc2[lEl_float] = idx0_pivot[
        idx0_pivot[list_samples_fc[lEl_float]], idx0_pivot['Reading':'Reading', lEl_float:lEl_float]]

for lEl_object in list_Element_object:
    list_samples_fc[lEl_object] = df_NIR_2_melt_pivot[
        (df_NIR_2_melt_pivot.Reading[lEl_object] != df_NIR_2_melt_pivot.Conentration[lEl_object]) & (
            df_NIR_2_melt_pivot.Reading[lEl_object].notnull())].index
    list_samples_fc2[lEl_object] = idx0_pivot[
        idx0_pivot[list_samples_fc[lEl_object]], idx0_pivot['Reading':'Reading', lEl_object:lEl_object]]

df_NIR_2_melt_pivot_formatting = df_NIR_2_melt_pivot.style
for lEl_float in list_Element_float:
    df_NIR_2_melt_pivot_formatting = df_NIR_2_melt_pivot_formatting.set_properties(**{'background-color': '#00FFFF;'},
                                                                                   subset=list_samples_fc2[lEl_float])

for lEl_object in list_Element_object:
    df_NIR_2_melt_pivot_formatting = df_NIR_2_melt_pivot_formatting.set_properties(**{'background-color': '#00FFFF;'},
                                                                                   subset=list_samples_fc2[lEl_object])

# df_NIR_2_melt_pivot_formatting
display(df_NIR_2_melt_pivot_formatting)