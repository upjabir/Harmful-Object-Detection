import cv2
import tensorflow as tf
import time
from mypackage.model.utils import load_class_names, output_boxes, draw_outputs, resize_image
from mypackage import model,model_size,class_name,max_output_size,max_output_size_per_class,iou_threshold,confidence_threshold


class Videocamera(object):

    #max_output_size = 100
    #max_output_size_per_class= 20
    #iou_threshold = 0.5
    #confidence_threshold = 0.5

    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,frame=self.video.read()

        

      

        resized_frame = tf.expand_dims(frame, 0)
        resized_frame = resize_image(resized_frame, (model_size[0],model_size[1]))

        pred = model.predict(resized_frame)

        boxes, scores, classes, nums = output_boxes( \
                pred, model_size,
                max_output_size=max_output_size,
                max_output_size_per_class=max_output_size_per_class,
                iou_threshold=iou_threshold,
                confidence_threshold=confidence_threshold)

        img = draw_outputs(frame, boxes, scores, classes, nums, class_names)
        imgjpeg = cv2.imencode('.jpg', img)

        return imgjpeg.tobytes()

       

        





