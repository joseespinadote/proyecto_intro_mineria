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
primera_fecha_pais = dict()
primera_fecha_region = dict()
ultimo_dato_region = dict()
ultimo_dato_pais = dict()
with open(filepath_write, 'w') as fpw:
    csv_writer = csv.writer(fpw)
    csv_writer.writerow(dataset_headers)
    with open(filepath_read, encoding="utf-8") as fp:
        archivo_csv = csv.reader(fp)
        contador = 0
        for line in archivo_csv:
            if contador > 0 :
                num_dia_desde_primer_caso = 0
                num_confirmados = int(float(line[5]))
                num_fallecidos = int(float(line[6]))
                num_recuperados = int(float(line[7]))
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
                llave = region
                # waaaaaat ??
                if llave == "Recovered" :
                    continue
                if region.strip() == "" :
                    llave = pais
                    if llave not in primera_fecha_pais :
                        primera_fecha_pais[llave] = fechaObservacion
                    else :
                        num_dia_desde_primer_caso = (fechaObservacion - primera_fecha_pais[llave]).days
                        num_confirmados = CFR[0] - ultimo_dato_pais[llave][0]
                        num_fallecidos = CFR[1] - ultimo_dato_pais[llave][1]
                        num_recuperados = CFR[2] - ultimo_dato_pais[llave][2]
                    ultimo_dato_pais[llave] = CFR
                else :
                    if llave not in primera_fecha_region :
                        primera_fecha_region[llave] = fechaObservacion
                    else :
                        num_dia_desde_primer_caso = (fechaObservacion - primera_fecha_region[llave]).days
                        num_confirmados = CFR[0] - ultimo_dato_region[llave][0]
                        num_fallecidos = CFR[1] - ultimo_dato_region[llave][1]
                        num_recuperados = CFR[2] - ultimo_dato_region[llave][2]
                    ultimo_dato_region[llave] = CFR
                # para echar un ojo descomenten la linea a continuación. Excelente dupla para usar con "grep"
                # Hebei, Gansu, Grand Princess, Tennessee, Washington, Virgin Islands, Omaha, NE (From Diamond Princess), Reunion
                # occupied Palestinian territory
                #if region=="French Polynesia" :
                #if region=="Diamond Princess cruise ship" :
                #if pais=="occupied Palestinian territory" :
                #    print([num_dia_desde_primer_caso, region, pais, num_confirmados, num_fallecidos, num_recuperados, acc_confirmados, acc_fallecidos, acc_recuperados])
                row = [num_dia_desde_primer_caso, region, pais, num_confirmados, num_fallecidos, num_recuperados, acc_confirmados, acc_fallecidos, acc_recuperados]
                csv_writer.writerow(row)
            contador += 1

