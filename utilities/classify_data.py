#!/usr/bin/env python2

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.decomposition import PCA
from sklearn import cross_validation
from sklearn import svm
from sklearn.externals import joblib
import pandas
from scipy import signal
import numpy as np
from pprint import pprint
from pylab import *

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


d = pandas.read_csv("motor_data_derrick.csv")
d = d.dropna()
d = d.reset_index(drop=True)

M = 25
r = 250
f1, f2 = 7, 14

wavelet1 = signal.morlet(M, w=(f1*M)/(2.0*r))
wavelet2 = signal.morlet(M, w=(f2*M)/(2.0*r))

box_width = 250

features_arr = np.zeros( (len(d.index), # rows
                          # cols, FFT len * n_signals * n_wavelets * 1 (abs, no angle)
                          box_width * 3 * 3 * 2)  ) 

for i in range(box_width, len(d)-1):
    if i % 1000 == 0:
        print(i)
    
    data = np.array(d[i - box_width+1:i+1])
    sigs = np.zeros((data.shape[0], 3))
    sigs[..., 0] = (data[..., 0] + data[..., 1])/2.0
    sigs[..., 1] = (data[..., 2] + data[..., 3])/2.0
    sigs[..., 2] = (data[..., 4] + data[..., 5])/2.0

    # fft_len = np.fft.rfft(data[..., 0]).shape[0]
    features = np.array([])

    
    for j in range(3):
        sig = sigs[..., j]
        conv1 = signal.convolve(sig, wavelet1, 'same')
        conv2 = signal.convolve(sig, wavelet2, 'same')
        fourier = np.fft.fft(sig)
        fourier1 = np.fft.fft(conv1) 
        fourier2 = np.fft.fft(conv2)
        features = np.hstack([features, np.abs(fourier), np.abs(fourier1), np.abs(fourier2)])
        # not sure if this is a good idea -->
        features = np.hstack([features, np.angle(fourier), np.angle(fourier1), np.angle(fourier2)])
    
    features_arr[i, ...] = features
        

feature_names = []
for i in range(3):
    feature_names.extend(['c' + str(i) + '_abs_A_' + str(x)
                          for x in range(box_width)])
    feature_names.extend(['c' + str(i) + '_abs_B_' + str(x)
                          for x in range(box_width)])
    feature_names.extend(['c' + str(i) + '_abs_C_' + str(x)
                          for x in range(box_width)])
    feature_names.extend(['c' + str(i) + '_angle_A_' + str(x)
                          for x in range(box_width)])
    feature_names.extend(['c' + str(i) + '_angle_B_' + str(x)
                          for x in range(box_width)])
    feature_names.extend(['c' + str(i) + '_angle_C_' + str(x)
                          for x in range(box_width)])

# clf.fit(features_arr, d.tag)

def fisher_criterion(X, y, a, b):
    X_1 = X[y == a, ]
    X_2 = X[y == b, ]
    top = np.abs(X_1.mean(0) - X_2.mean(0))
    bottom = np.sqrt((X_1.std(0)**2.0 + X_2.std(0)**2) / 2.0)
    return top / bottom


X = features_arr[box_width:]
y = np.array(d.tag[box_width:])

N_train = 20000

# ETC = ExtraTreesClassifier()
# ETC.fit(X, y)
# n_features = 10
# cutoff = np.sort(ETC.feature_importances_)[-n_features:][0]
# good_features = ETC.feature_importances_ >= cutoff


n_features = n_fish_features = 5
fish = fisher_criterion(X[:N_train,], y[:N_train], -1, 1)
cutoff = np.sort(fish)[-n_fish_features:][0]
good_features = fish >= cutoff
X_new = X[..., good_features]

# good_features = ETC.feature_importances_ >= 0.003
ff = np.array(feature_names)[good_features]
print(ff)
print(np.sum(good_features))
# pprint(zip(ff, ETC.feature_importances_[good_features]))
pprint(zip(ff, fish[good_features]))

# clf = svm.SVC()
# clf.fit(X_new, y)

neigh = KNeighborsClassifier(n_neighbors=10, weights='distance')
scores = cross_validation.cross_val_score(neigh, X_new, y, cv=5)
print(scores)
# neigh.fit(X_new, y)

# good_features = ETC.feature_importances_ >= 0.0005
# print(np.sum(good_features))
# X_new2 = X[..., good_features]

# pca = PCA(n_components = 15)
# pca.fit(X_new2)
# print(pca.explained_variance_)

# X_new3 = pca.transform(X_new2)

# neigh = KNeighborsClassifier(n_neighbors=20, weights='distance')
# scores = cross_validation.cross_val_score(neigh, X_new3, y, cv=5)
# print(scores)


# clf = svm.SVC(probability=True, C=0.8, cache_size=1000,class_weight='auto')
# # scores = cross_validation.cross_val_score(clf, X_new, y, cv=2)
# # print(scores)
# clf.fit(X_new[:8000], y[:8000])


# model, good_features = joblib.load('neighbors_model.pkl')
# neigh = model


neigh = KNeighborsClassifier(n_neighbors=10, weights='distance')
neigh.fit(X_new[:N_train], y[:N_train])

pred = neigh.predict(X_new)

#probs = neigh.predict_proba(X_new)
# probs = clf.predict_proba(X_new)

# pred_l = probs[...,0]
# pred_r = probs[...,2]
# pred_b = probs[...,1]


smoother_len = 500
# smoother = np.repeat(1.0/smoother_len, smoother_len)
smoother = np.exp(-0.005 * np.arange(0,smoother_len))

smoother = smoother / sum(smoother)

#subplot(2,1,1)
# plot(signal.convolve(pred_l, np.repeat(1/500., 500), 'same'))
# plot(signal.convolve(pred_r, np.tile(smoother, 1), 'same'))
# plot(signal.convolve(pred_b, np.tile(smoother, 1), 'same'))

plot(signal.convolve(pred, smoother, 'same'))

#subplot(2,1,2)
plot(y)

#neigh.fit(X_new, y)

show()


# joblib.dump([neigh, good_features], 'neighbors_model.pkl', compress=4)

# neigh, good_features = joblib.load('neighbors_model.pkl')
