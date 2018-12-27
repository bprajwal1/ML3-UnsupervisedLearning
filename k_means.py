from sklearn.cluster import KMeans
import numpy as np
import data_service
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA, FastICA
from sklearn.random_projection import GaussianRandomProjection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def run_k_means(x_train, x_test, y_train, y_test):

    kmeans = KMeans(n_clusters=2, random_state=None).fit(x_train)

    train_accuracy_score_1 = accuracy_score(y_train, kmeans.labels_)
    train_accuracy_score_2 = accuracy_score(y_train, np.logical_not(kmeans.labels_))

    print("Train accuracy 1: {0}".format(train_accuracy_score_1))
    print("Train accuracy 2: {0}".format(train_accuracy_score_2))

    test_prediction = kmeans.predict(x_test)
    if train_accuracy_score_2 > train_accuracy_score_1:
        test_prediction = np.logical_not(test_prediction)

    test_accuracy = accuracy_score(y_test, test_prediction)
    print("Test Accuracy: {0}".format(test_accuracy))


scale_data = True
transform_data = False
random_slice = None
random_seed = None
dataset = 'breast_cancer'
test_size = 0.2

x_train, x_test, y_train, y_test = data_service.\
    load_and_split_data(scale_data=scale_data, transform_data=transform_data, random_slice=random_slice,
                        random_seed=random_seed, dataset=dataset, test_size=test_size)


run_k_means(x_train, x_test, y_train, y_test)

print("Applying PCA...")

pca = PCA(n_components=10)
x_train_PCA = pca.fit_transform(x_train.copy())
x_test_PCA = pca.transform(x_test.copy())

run_k_means(x_train_PCA, x_test_PCA, y_train, y_test)

print("Applying ICA...")

fastICA = FastICA(n_components=3, random_state=0)
x_train_ICA = fastICA.fit_transform(x_train.copy())
x_test_ICA = fastICA.transform(x_test.copy())

run_k_means(x_train_ICA, x_test_ICA, y_train, y_test)

print("Applying RCA...")

rca = GaussianRandomProjection(n_components=26)
x_train_RCA = rca.fit_transform(x_train.copy())
x_test_RCA = rca.transform(x_test.copy())

run_k_means(x_train_RCA, x_test_RCA, y_train, y_test)

print("Applying LDA...")

rca = LinearDiscriminantAnalysis(n_components=1)
x_train_LDA = rca.fit_transform(x_train.copy(), y_train)
x_test_LDA = rca.transform(x_test.copy())

run_k_means(x_train_LDA, x_test_LDA, y_train, y_test)
