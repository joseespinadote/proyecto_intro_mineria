#/usr/bin/python3
import numpy as np
import matplotlib.pylab as plt
import pandas as pd


class CountryAnalysis:
    def __init__(self, name, cumulativeDistribution):
        self.__cumulativeDistribution = cumulativeDistribution
        self._name = name
        self.__relativeDistribution = None
    
    def name(self):
        return self._name
    
    def getCumulativeDistribution(self):
        self.__cumulativeDistribution['Diseased'] = self.__cumulativeDistribution['Confirmed'] - self.__cumulativeDistribution['Deaths'] - self.__cumulativeDistribution['Recovered']
        return self.__cumulativeDistribution    

    def getRelativeDistribution(self):
        return self.__relativeDistribution

    def computeRelativeDistribution(self):
        """ Este metodo calcula la distribucion relativa, que se obtiene a partir de la ecumulada. Esto es, los valores diferenciales
        entre t[n+1] - t[n]. Por ejemplo en COVID, los casos confirmados corresponden a la acumulacion total de casos, y para obtener
        cuandos casos nuevos por dia se han detectado es necesario calcular la diferencia entre las observaciones del dia de hoy,
        y las de ayer.
        Se considera que el primer caso acumulado, le antecede un valor 0 (no existian casos antes de la primera observacion), por
        ello se agrega en la distribucion relativa el primer caso acumulado, y asi tener el mismo tamaño del arreglo.
        
        Arguments:
            distribucionAcumulada {[ndarray]} -- Vector de la distribucion acumulada
        
        Returns:
            [ndarray] -- Vector de la distribucion relativa
        """
        columns = ['Confirmed', 'Deaths', 'Recovered']
        cumulative = self.__cumulativeDistribution[columns].values
        relativeData = np.vstack((cumulative[0, :], cumulative[1:, :] - cumulative[:-1, :]))
        self.__relativeDistribution = pd.DataFrame(relativeData, columns=columns)
        self.__relativeDistribution['Diseased'] = self.__relativeDistribution['Confirmed'] - self.__relativeDistribution['Deaths'] - self.__relativeDistribution['Recovered']
        return self.__relativeDistribution