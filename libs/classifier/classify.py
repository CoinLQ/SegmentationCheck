#!/usr/bin/env python
# coding=utf-8
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time
import codecs

import caffe

default_settings = {"model_def":         "./lenet_16000/deploy16000.prototxt",
        "pretrained_model":  "./lenet_16000/lenet_iter_16000.caffemodel",
                    "images_dim":        "40,40",
                    "raw_scale":         "255.0",
        "input_scale":       "1.0",
              "label_file":        "./lenet_16000/synset.txt"}

CLASSIFIER = None
LABEL_FILE = None

def init(model_settings):
    model_def = model_settings['model_def']
    if type(model_def) is unicode:
        model_def = model_def.encode("utf-8")
    pretrained_model = model_settings['pretrained_model']
    if type(pretrained_model) is unicode:
        pretrained_model = pretrained_model.encode("utf-8")
    label_file = model_settings['label_file']
    if type(label_file) is unicode:
        label_file = label_file.encode("utf-8")
    images_dim = model_settings['images_dim']
    image_dims = [int(s) for s in images_dim.split(',')]
    raw_scale = float(model_settings['raw_scale'])
    input_scale = float(model_settings['input_scale'])
    #have no mean file
    mean, channel_swap = None, None

    # CPU mode
    caffe.set_mode_cpu()

    # Make classifier.
    classifier = caffe.Classifier(model_def, pretrained_model,
            image_dims=image_dims, mean=mean,
            input_scale=input_scale, raw_scale=raw_scale,
            channel_swap=channel_swap)
    return classifier,label_file


def run(file_list, classifier, label_file):
    inputs =[caffe.io.load_image(im_f, False) for im_f in file_list]

    #start = time.time()

    predictions = classifier.predict(inputs, False)
    mdict = {k.strip():v.strip() for k, v in (l.split(' ') for l in codecs.open(label_file, "r", "utf8"))}
    pred_list = []

    for line in predictions:
      temp_list = []
      num = 1
      j = 0
      y = sorted(enumerate(line), key=lambda x:x[1], reverse = 1)

      for i in xrange(len(y)):
        j = j + 1
        if j > 10:
          break
        if y[i][1] < 1e-60:
          break
        t = '%d'%y[i][0]
        temp_list.append(mdict[t])
        temp_dict = {'%d'%num:temp_list}
      pred_list.append(temp_list)
      num = num + 1

    return pred_list

if __name__ == '__main__':
  c,lb = init(default_settings)
  print "init finished!"
  l = ["test1.jpg"]
  p = run(l, c, lb)
  print p[0][0]
