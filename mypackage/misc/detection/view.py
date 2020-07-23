from flask import Blueprint,render_template,redirect,url_for,Response
import os
import cv2
import tensorflow as tf
from model.utils import load_class_names, output_boxes, draw_outputs, resize_image
from model.yolov3 import YOLOv3Net


detection_blueprint=Blueprint('detection',__name__,template_folder='templates/detection')

physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
tf.config.experimental.set_memory_growth(physical_devices[0], True)

model_size = (416, 416,3)
num_classes = 80

path=os.path.abspath(os.path.dirname(__file__))
basedir=os.path.abspath(os.path.join(path, os.pardir)) 
class_name = os.path.join(basedir,'model/data/coco.names')
weightfile = os.path.join(basedir,'model/weights/yolov3_weights.tf')
cfgfile = os.path.join(basedir,'model/cfg/yolov3.cfg')

max_output_size = 100
max_output_size_per_class= 20
iou_threshold = 0.5
confidence_threshold = 0.5

model = YOLOv3Net(cfgfile,model_size,num_classes)
model.load_weights(weightfile)
class_names = load_class_names(class_name)
print('weights and classes loaded')

#video_stream = Videocamera()

@detection_blueprint.route('/video',methods=['GET','POST'])
def video():
    render_template('index.html')

def gen():

    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, frame=cap.read()
        if ret == True:
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
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            print('888888888888888888888888888888888888888888888')

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            yield(bytearray(pred))

        else:
            break


@detection_blueprint.route('/video_feed')
def video_feed():
    return Response(gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

