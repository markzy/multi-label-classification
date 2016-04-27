import numpy as np
from scipy.sparse import csr_matrix
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.preprocessing import MultiLabelBinarizer
from MLDecisionTree import MLDecisionTree
import pickle
from Metrics.UniversalMetrics import UniversalMetrics

files = ['../data/scene_train', '../data/scene_test']

data = datasets.load_svmlight_files(files, multilabel=True)
train_data = data[0]
train_target = np.array(MultiLabelBinarizer().fit_transform(data[1]))
test_data = data[2]
test_target = np.array(MultiLabelBinarizer().fit_transform(data[3]))

feature_size = train_data.shape[1]
pca = PCA(n_components=(feature_size * 10) // 100)
train_data_trans = csr_matrix(pca.fit_transform(train_data.todense())).toarray()
test_data_trans = csr_matrix(pca.transform(test_data.todense())).toarray()

a = MLDecisionTree().fit(train_data_trans,train_target).predict(test_data_trans)

file_name = '../results/MLDecisionTree.pkl'
with open(file_name, 'wb') as output_:
    pickle.dump(a, output_, pickle.HIGHEST_PROTOCOL)

m = UniversalMetrics(6,test_target,a)
print(m.accuracy())

