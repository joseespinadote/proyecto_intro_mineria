from sklearn.base import ClusterMixin, BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE
from numpy import unique
from matplotlib import colors
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame, Series

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

class TSNEVisualizer(TransformerMixin):
    def __init__(self):
        self.__tnse = None
        self.__trained = False
        self.__figure = None

    def plot(self):
        self.__figure = plt.figure()
    
    @property
    def trained(self):
        return self.__trained
    
    def fit_transform(self, X, **kwargs):
        print('Training')
        if not isinstance(X, DataFrame): raise TypeError('Must be DataFrame not {}'.format(type(X)))
        self.__tsne = TSNE(n_components=2, **kwargs).fit_transform(X.values)
        self.__trained = True
        return self.__tsne


class ClusteringTunning(BaseEstimator, ClusterMixin):
    """
    
    Usage:
        visualizer = TSNEVisualizer()
        clustering = ClusteringTunning(visualizer).fit(data)
        prediction = clustering.predict(data)
        # clustering.plot_embedded()
        clustering.scatter()

    Args:
        BaseEstimator ([type]): [description]
        ClusterMixin ([type]): [description]
    """
    def __init__(self, visualizer=None):
        super().__init__()
        self.__visualizer = TSNE(n_components=2)
        self.__prediction = None
        self.__estimator_ = None
        self.__data = None
        self.__X_embedded = None
        self.colorlist = list(colors.ColorConverter.colors.keys())
        
    @property
    def visualizer(self):
        return self.__visualizer
    
    @property
    def estimator_(self):
        return self.__estimator_
    
    @property
    def X_embedded(self):
        return self.__X_embedded
    
    @property
    def prediction(self):
        return self.__prediction

    def fit(self, X, y=None, **kwargs):
        self.__data = X
        self.__estimator_ = GaussianMixture(**kwargs).fit(X.values)
        self.__X_embedded = DataFrame(self.__visualizer.fit_transform(X), index=self.__data.index)
        #self.__estimator_ = KMeans()
        return self

    def predict(self, X=None):
        if X is None: X = self.__data
        raw_pred = self.__estimator_.predict(X.values)
        self.__prediction = DataFrame(raw_pred, index = self.__data.index)
        return self.__prediction
    
    def plot_embedded(self):
        counter = 0
        plt.figure()
        clusters = self.__prediction
        print(unique(clusters))
        print(self.__X_embedded)
        print(self.__X_embedded.loc([0, 1]))
        for cluster in unique(clusters):
            # print('Cluster {} has {} country/region'.format(cluster, features_df[clusters == cluster][['pais', 'region']].shape[0]))
            color = self.colorlist[counter % len(self.colorlist)]
            ax = sns.scatterplot(data = self.__X_embedded[clusters == cluster].values)
            counter += 1
        
    def scatter(self):
        plt.figure()
        return sns.pairplot(data=self.__data) #sns.scatterplot(x=0, y=1, data=X_embedded)