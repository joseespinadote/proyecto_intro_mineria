import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path

### Cargar datos de kaggle

parent_directory = Path().absolute().parent
covid_data = parent_directory / "novel-corona-virus-2019-dataset/covid_19_data.csv"
covid_data_frame = pd.read_csv(covid_data)

### Diccionarios de correciones

dict_error = {}
dict_pares = {}
with open('dict_error.json', 'r', encoding="utf-8") as dict_file:
    dict_error = json.load(dict_file)
with open('dict_pares_error.json', 'r', encoding="utf-8") as dict_file:
    dict_pares = json.load(dict_file)


### Correccion de Country/Region
covid_data_frame.replace(dict_error, inplace=True)

### Correcion Province/State
for key in dict_pares:
    covid_data_frame.loc[(covid_data_frame['Country/Region'] == key), ['Country/Region', 'Province/State']]=dict_pares[key]

covid_data_frame['Province/State'].fillna(value=np.nan, inplace=True)


### Pares Pais-Region
pares = []
for pair in covid_data_frame[['Country/Region', 'Province/State']].values.tolist():
    pais = pair[0]
    provincia = pair[1]
    par = str(pais) + "," + str(provincia)
    if par not in pares:
        pares.append(par)

pares.sort()
par_df = pd.DataFrame(pares)
paises_covid = covid_data_frame['Country/Region'].unique()
paises_covid.sort()

### Eliminar duplicados para (ObservationDate, Province/State, Country/Region)

covid_data_frame.sort_values(by=['ObservationDate', 'Country/Region', 'Province/State', 'Confirmed'], inplace=True)
covid_data_frame.drop_duplicates(['ObservationDate', 'Country/Region', 'Province/State'], keep='last', inplace=True)

### Cargar tablas de atributos extra

gastoEnSalud = pd.read_csv('data/chepergdp.csv')
edadMedia = pd.read_csv('data/edad_media_2018_CIA.csv')
PIB = pd.read_csv('data/gdp_2019_FMI.csv')
tazaMuerte = pd.read_csv('data/muerte_2020_CIA.csv')
indiceGINI = pd.read_csv('data/gini_coef_2020_worldpopulationreview.csv')
indiceGINI = indiceGINI[['Country/Region', 'giniIndex', 'pop2020']]

### Reemplazar typos
gastoEnSalud.replace(dict_error, inplace=True)
edadMedia.replace(dict_error, inplace=True)
PIB.replace(dict_error, inplace=True)
indiceGINI.replace(dict_error, inplace=True)
tazaMuerte.replace(dict_error, inplace=True)

#### JOIN de tablas 

paises_covid_df = pd.DataFrame(covid_data_frame['Country/Region'].unique(), columns=['Country/Region'])
paises_covid_df = paises_covid_df.join(PIB.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(gastoEnSalud.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(edadMedia.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(indiceGINI.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(tazaMuerte.set_index('Country/Region'), on='Country/Region')

#### Renombrar columnas

paises_covid_df.columns = ['pais', 'gdp_rank', 'gdp_usd', 'gdp_en_salud', 'edad_media', 'gini', 'poblacion', 'taza_muerte1000']


### Guardar datos
covid_data_frame.to_csv('covid_19_data.csv', index=False)
par_df.to_csv('pais_region.csv', index=False)
paises_covid_df.to_csv('atributos_paises.csv', index=False)


### Revisar paises entre tablas (checkear diferencias)

'''
array1 = gastoEnSalud['Country/Region'].unique()
array2 = edadMedia['Country/Region'].unique()
array3 = PIB['Country/Region'].unique()
array4 = indiceGINI['Country/Region'].unique()
array5 = tazaMuerte['Country/Region'].unique()

array1.sort()
array2.sort()
array3.sort()
array4.sort()
array5.sort()




iguales =[]
distintos = []
for pais in paises_covid:
    contador = 0
    for arreglos in [array1, array2, array3, array4, array5]:
        if pais in arreglos:
            if pais not in iguales:
                iguales.append(pais)
        else:
            contador += 1
    if contador != 0:
        distintos.append([pais, contador])
'''