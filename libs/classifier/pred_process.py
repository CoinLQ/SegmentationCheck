import classify

def init():
  model_setting =   {
    "model_def":       "/data/share/lenet_40000/deploy.prototxt",
    "pretrained_model":  "/data/share/lenet_40000/lenet_iter_40000.caffemodel",
    "images_dim":      "48,48",
    "raw_scale":       "255.0",
    "input_scale":       "0.00390625",
    "label_file":      "/data/share/lenet_40000/synset.txt"
  }
  classify.CLASSIFIER, classify.LABEL_FILE = classify.init(model_setting)

def process(file_list):
  if not classify.CLASSIFIER:
    init()
  pred_list = classify.run(file_list, classify.CLASSIFIER, classify.LABEL_FILE)
  pred_dict = {}
  pred_dict['predictions'] = pred_list
  return pred_dict