#!/usr/bin/python
# crea nuevo dataset a partir del novel-corona-virus-2019-dataset/covid_19_data.csv
# encontrado en kaggle
# fuentes de nuevos atributos:
#  - (gdp, 2019)    https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)
#  - (gini, 2020)   https://worldpopulationreview.com/countries/gini-coefficient-by-country/
#  - (edad, 2018)   https://www.cia.gov/library/publications/resources/the-world-factbook/fields/343rank.html
#  - (muerte, 2018) https://www.cia.gov/library/publications/resources/the-world-factbook/fields/346rank.html
# (x el terrible jose)

import datetime
import csv

top_ten_gdp = ['US', 'Mainland China', 'Japan', 'Germany',
    'India', 'UK', 'France', 'Italy', 'Brazil', 'Canada']

filepath_read = 'novel-corona-virus-2019-dataset/covid_19_data.csv'
filepath_write = 'dataset_atributos_extra.csv'
dataset_headers = ['region','pais','es_top_ten_gdp']
primera_fecha_region_pais = dict()
ultimo_dato_region_pais = dict()
with open(filepath_write, 'w') as fpw:
    csv_writer = csv.writer(fpw)
    csv_writer.writerow(dataset_headers)
    with open(filepath_read, encoding="utf-8") as fp:
        archivo_csv = csv.reader(fp)
        contador = 0
        for line in archivo_csv:
            if contador > 0 :
                region = line[2]
                pais = line[3]
                es_top_ten_gdp = pais in top_ten_gdp
                llave_pais_region = region
                if region.strip() == "" :
                    llave_pais_region = pais
                row = [region, pais, "1" if es_top_ten_gdp else "0"]
                csv_writer.writerow(row)
            contador += 1
