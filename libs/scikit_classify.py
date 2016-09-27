#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from scipy.misc import imresize # for image resize
from skimage import io
from skimage.color import rgb2gray, gray2rgb

from skimage.filter import threshold_otsu
# sys.path.append('/home/can/PycharmProjects/imageprocess/libsvm/python')
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier


def prepare_data_from_img(data_file_name):
	"""
	svm_read_problem(data_file_name) -> [y, x]

	Read LIBSVM-format data from data_file_name and return labels y
	and data instances x.
	"""
	prob_x = []
	prob_y = []
	test_x = []
	test_y = []
        test_path =[]
        charlistfile = data_file_name+'char.txt'
	for line in open(charlistfile):
            img_path, label = line.split(' ')
            img_path = data_file_name+img_path
            if not os.path.exists(img_path):
                continue
            src_image = io.imread(img_path, 0)
            img_gray = rgb2gray(src_image)
            img_resize = imresize( img_gray, [10, 15], 'nearest' ) ;
            try:
                thresh = threshold_otsu(img_resize)
            except:
                continue
            binary = img_resize > thresh
            im = (binary * 1).astype('ubyte')
            im.shape = 1, -1
            x = im.tolist()
            if int(label) == 0:
                test_x += x
                test_y += [int(label)]
                test_path += [img_path]
            else:
                if int(label) < 0:
                    label = -1
                elif int(label) > 0:
                    label = 1
                prob_x += x
                prob_y += [label]
	return (prob_y, prob_x,test_y,test_x,test_path)

def output_result2html(p_labels,tpath,algo_name):
    print 'outputing'
    correct_display_html = algo_name+'correct.html'
    incorrect_display_html = algo_name+'incorrect.html'
    with open(incorrect_display_html,'w+') as inf:
        with open(correct_display_html,'w+') as cof:
            #length = [len(p_labels),2000][len(p_labels)>2000]
            length = len(p_labels)
            j = 0
            for i in range(length):
                imgtxt= "<img src='%s'>\n"%tpath[i]
                if p_labels[i] ==1 and j<1500:
                    j+=1
                    cof.write(imgtxt)
                elif p_labels[i] == -1:
                    inf.write(imgtxt)


if __name__ == '__main__':
    char = u'ming'
    root_path = '/home/can/clustering/%s/'%char
    print "reading data"
    y, X,ty,tX,tpath = prepare_data_from_img(root_path)
#    print x[0][0]
#    print len(x)
#    print len(y)
#    print len(tx)
#    print len(ty)
#    print len(tpath)
    print "traning"
# normalize the data attributes
normalized_X = preprocessing.normalize(X)
# standardize the data attributes
standardized_X = preprocessing.scale(X)

model = ExtraTreesClassifier()
model.fit(X, y)
# display the relative importance of each attribute
print "=============feature_importances_========"
print(model.feature_importances_)

print "==LogisticRegression=="
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)
print "----model------"
print(model)
# make predictions
expected = y
predicted = model.predict(X)
# summarize the fit of the model
print "-----make predictions-----"
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))
predicted = model.predict(tX)
output_result2html(predicted,tpath,'LogisticRegression')
