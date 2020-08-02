# 2.1.1 DATA IMPUTATION
from pandas import DataFrame, Series
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger(logging.DEBUG)

# 2.1.2 OUTLIERS REPLACEMENT FOR TARGET

class OutliersReplacement(TransformerMixin):
    """Reemplaza los outliers de una serie, quitando aquellos elementos
    en el cuantil mas elevado y reemplazandolos por una interpolacion (u otra
    tendencia central)

    Usage:
        time_serie = X[some_column]
        OutliersReplacement(method='threshold').fit_transform(X=time_serie)

    Args:
        TransformerMixin ([type]): [description]
    """

    def __init__(self, method):
        self.__method = method
        self.__meta = {}
    
    @property
    def method(self):
        return self.__method
    
    @property
    def meta(self):
        return self.__meta

    def __implements(self, *args, **kwargs):
        # Check pandas dataframe
        logger.debug(self.__method)
        logger.debug(kwargs)
        if self.__method == 'IsolationForest':
            return self.__isolationForest(*args, **kwargs)
        elif self.__method == 'thresholding':
            return self.__thresholding(*args, **kwargs)
        else: raise NotImplemented('Method {} not implemented for outliers replacement'.format(self.__method))

    def fit(self, *args, **kwargs):
        return self.__implements(*args, **kwargs)

    def transform(self, *args, **kwargs):
        kwargs['transform'] = True
        return self.__implements(*args, **kwargs)
    
    @staticmethod
    def __checkDataFrame(data):
        if not isinstance(data, DataFrame):
            raise TypeError('X must be {} not {}'.format(type(DataFrame), type(data)))
            
    @staticmethod
    def __checkSeries(data):
        if not isinstance(data, Series):
            raise TypeError('X must be {} not {}'.format(type(Series), type(data)))

    def __thresholding(self, X, y = None, transform=False, upper_q=0.999, lower_q=0.001):
        logger.debug(self.__meta)
        self.__checkSeries(X)
        if transform:
            upper_bound = self.__meta['uppper_quantile']
            lower_bound = self.__meta['lower_quantile']
            ans = (X > lower_bound ) & (X < upper_bound)
            logger.info('Detected {} outliers'.format((~ans).sum()))
            X[~ans] = np.nan
            # self.__params['imputer'] = SimpleImputer(missing_values=np.nan, strategy='median').fit(X)
            X.interpolate(method='linear', axis=0, inplace=True)
            return X

        logger.debug('Traning tresholding')
        self.__meta['mean'] = X.mean()
        self.__meta['uppper_quantile'] = X.quantile(q=upper_q)
        self.__meta['lower_quantile'] = X.quantile(q=lower_q)
        return self

    def __isolationForest(self, X, y = None):
        outliers = IsolationForest(random_state=1993).fit(experiment.values)
        # Resolve Series
        result = Series(outliers.predict(experiment.values), experiment.index)
        logger.info('Total of outliers {}'.format((result == -1).sum()))
        return result