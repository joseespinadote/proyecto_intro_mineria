import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path

### Cargar datos de kaggle

parent_directory = Path().absolute().parent
covid_data = parent_directory / "novel-corona-virus-2019-dataset/covid_19_data.csv"
extra_atributes = 'dataset.csv'
covid_data_frame = pd.read_csv(covid_data)

### Diccionario de correciones

dict_error = {}
with open('dict_error.json', 'r') as dict_file:
    dict_error = json.load(dict_file)

### Correccion de Country/Region

covid_data_frame.replace(dict_error, inplace=True)

paises_covid = covid_data_frame['Country/Region'].unique()

paises_covid.sort()
pd.DataFrame(paises_covid, columns=['Country/Region']).to_csv('paises_covid.csv', index=False)

### Cargar tablas de atributos extra

gastoEnSalud = pd.read_csv('data/chepergdp.csv')
edadMedia = pd.read_csv('data/edad_media_2018_CIA.csv')
PIB = pd.read_csv('data/gdp_2019_FMI.csv')
indiceGINI = pd.read_csv('data/gini_coef_2020_worldpopulationreview.csv')
tazaMuerte = pd.read_csv('data/muerte_2020_CIA.csv')

### Reemplazar typos

gastoEnSalud.replace(dict_error, inplace=True)
edadMedia.replace(dict_error, inplace=True)
PIB.replace(dict_error, inplace=True)
indiceGINI.replace(dict_error, inplace=True)
tazaMuerte.replace(dict_error, inplace=True)

indiceGINI = indiceGINI[['Country/Region', 'giniIndex', 'pop2020']]

#### JOIN de tablas

paises_covid_df = pd.DataFrame(covid_data_frame['Country/Region'].unique(), columns=['Country/Region'])
paises_covid_df = paises_covid_df.join(gastoEnSalud.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(PIB.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(edadMedia.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(indiceGINI.set_index('Country/Region'), on='Country/Region')
paises_covid_df = paises_covid_df.join(tazaMuerte.set_index('Country/Region'), on='Country/Region')

paises_covid_df.to_csv(extra_atributes, index=False)