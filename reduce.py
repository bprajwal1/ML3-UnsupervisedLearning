import numpy as np
import sys
from sklearn.decomposition import PCA, FastICA
from sklearn.random_projection import GaussianRandomProjection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import data_service
import plotting_service

np.set_printoptions(suppress=True, precision=3)
if len(sys.argv) < 4 or (sys.argv[1] not in ['PCA', 'ICA', 'RCA', 'LDA']) \
        or (sys.argv[2] not in ['breast_cancer', 'kdd']):
    print("Usage: python reduce.py <algorithm: one of 'PCA', 'ICA', 'RCA', 'LDA'> <dataset: one of 'breast_cancer', 'kdd'> <number_of_components>")
    print("e.g.:")
    print("python reduce.py PCA breast_cancer 3")
    exit()

reduce_algo_name = sys.argv[1]
dataset_name = sys.argv[2]
n_components = int(sys.argv[3])
print("Running {0} down to {1} components on the {2} dataset.".format(reduce_algo_name, n_components, dataset_name))

scale_data = True
transform_data = False
random_slice = None
random_seed = None
test_size = 0.05
num_unique_classes = 2
num_dimensions = 30

reduce_kdd_to_binary = False
if dataset_name == 'kdd':
    transform_data = True
    random_slice = None
    test_size = 0.5
    num_unique_classes = 23
    if len(sys.argv) > 4:
        reduce_kdd_to_binary = sys.argv[4] == 'binary'
        if reduce_kdd_to_binary:
            num_unique_classes = 2

x_train, x_test, y_train, y_test = data_service. \
    load_and_split_data(scale_data=scale_data, transform_data=transform_data, random_slice=random_slice,
                        random_seed=random_seed, dataset=dataset_name, test_size=test_size)


if dataset_name == 'kdd':
    # random_indices = np.random.choice(y_train.shape[0], 10000, replace=False)
    # y_train = y_train[random_indices]
    # x_train = x_train[random_indices, :]
    if reduce_kdd_to_binary:
        normal_train_indices = np.where(y_train == 9)[0]
        non_normal_train_indices = np.where(y_train != 9)[0]
        y_train[normal_train_indices] = 0
        y_train[non_normal_train_indices] = 1
        normal_test_indices = np.where(y_test == 9)[0]
        non_normal_test_indices = np.where(y_test != 9)[0]
        y_test[normal_test_indices] = 0
        y_test[non_normal_test_indices] = 1

reduce_algo = None
if reduce_algo_name == 'PCA':
    reduce_algo = PCA(n_components=n_components)
elif reduce_algo_name == 'ICA':
    reduce_algo = FastICA(n_components=n_components)
elif reduce_algo_name == 'RCA':
    reduce_algo = GaussianRandomProjection(n_components=n_components)
elif reduce_algo_name == 'LDA':
    reduce_algo = LinearDiscriminantAnalysis(n_components=n_components)

x_train_reduced = reduce_algo.fit_transform(x_train.copy())
x_test_reduced = reduce_algo.transform(x_test.copy())

plotting_service.plot1D_scatter(x_train_reduced[:,:1], y_train, reduce_algo_name, dataset_name)
plotting_service.plot2D_scatter(x_train_reduced[:,:2], y_train, reduce_algo_name, dataset_name)
plotting_service.plot3D_scatter(x_train_reduced, y_train, reduce_algo_name, dataset_name)

# random_indices = np.random.choice(y_train.shape[0], 10)
# print(x_train_reduced[random_indices,:])
# print(y_train[random_indices])