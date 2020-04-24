#!/usr/bin/python
# crea nuevo dataset a partir del novel-corona-virus-2019-dataset/covid_19_data.csv
# encontrado en kaggle (por jose)
import datetime
import csv

filepath_read = 'novel-corona-virus-2019-dataset/covid_19_data.csv'
filepath_write = 'dataset.csv'
dataset_headers = ['num_dia_desde_primer_caso','region','pais',
    'num_confirmados','num_fallecidos','num_recuperados','acc_confirmados',
    'acc_fallecidos','acc_recuperados']
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
                num_dia_desde_primer_caso = 0
                num_confirmados = 0
                num_fallecidos = 0
                num_recuperados = 0
                arrFechaObservacion = line[1].split("/")
                fechaObservacion = datetime.date(int(arrFechaObservacion[2]),
                    int(arrFechaObservacion[0]),
                    int(arrFechaObservacion[1]))
                region = line[2]
                pais = line[3]
                acc_confirmados = int(float(line[5]))
                acc_fallecidos = int(float(line[6]))
                acc_recuperados = int(float(line[7]))
                CFR = [acc_confirmados,acc_fallecidos,acc_recuperados]
                llave_pais_region = region
                # waaaaaat ??
                if llave_pais_region == "Recovered" :
                    continue
                if region.strip() == "" :
                    llave_pais_region = pais
                if llave_pais_region not in primera_fecha_region_pais :
                    primera_fecha_region_pais[llave_pais_region] = fechaObservacion
                else :
                    num_dia_desde_primer_caso = (fechaObservacion - primera_fecha_region_pais[llave_pais_region]).days
                if llave_pais_region in ultimo_dato_region_pais :
                    num_confirmados = CFR[0] - ultimo_dato_region_pais[llave_pais_region][0]
                    num_fallecidos = CFR[1] - ultimo_dato_region_pais[llave_pais_region][1]
                    num_recuperados = CFR[2] - ultimo_dato_region_pais[llave_pais_region][2]
                ultimo_dato_region_pais[llave_pais_region] = CFR
                # para echar un ojo descomenten la linea a continuación. Excelente dupla para usar con "grep"
                # print([num_dia_desde_primer_caso, region, pais, num_confirmados, num_fallecidos, num_recuperados, acc_confirmados, acc_fallecidos, acc_recuperados])
                row = [num_dia_desde_primer_caso, region, pais, num_confirmados, num_fallecidos, num_recuperados, acc_confirmados, acc_fallecidos, acc_recuperados]
                csv_writer.writerow(row)
            contador += 1
# ['SNo,ObservationDate,Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered']
