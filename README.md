# proyecto_intro_mineria
proyecto mineria de datos 1er semestre 


# Actualizar datos de kaggle

* Actualizar archivos de la carpeta 'novel-corona-virus-2019-dataset'
* Ejecutar script *correcion_nombres.py* en la carpeta atributos_extra
* Ejecutar script *preproceso.py* en el directorio principal
* En *dataset.csv* estara el resultado del preproceso, y en *atributos_extra/atributos_paises.csv* la tabla con los datos de interes para los paises del dataset
* Para obtener un dataframe que contenga la informacion de kaggle y los atributos encontrados:
- dataset = pd.read_csv('dataset.csv')
- atributos = pd.read_csv('atributos_extra/atributos_paises.csv')
- df = dataset.join(atributos.set_index('pais'), on='pais')