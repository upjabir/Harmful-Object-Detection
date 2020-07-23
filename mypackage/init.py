import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Blueprint,render_template,redirect,url_for,Response
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
import time
import cv2
import numpy as np
import tensorflow as tf
from mypackage.form import LoginForm,RegisterForm
from mypackage.model.utils import load_class_names, output_boxes, draw_outputs, resize_image,draw_text
from mypackage.model.yolov3 import YOLOv3Net


app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update({

	#EMAIL SETTINGS
	'MAIL_SERVER':'smtp.gmail.com',
	'MAIL_PORT':465,
	'MAIL_USE_SSL':'True',
	'MAIL_USERNAME' : os.environ.get('UNAME'),
	'MAIL_PASSWORD' : os.environ.get('PASSWORD')
})

bootstrap = Bootstrap(app)
db=SQLAlchemy(app)
Migrate(app,db)

mail = Mail(app)

physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
tf.config.experimental.set_memory_growth(physical_devices[0], True)

model_size = (416, 416,3)
num_classes = 80

basedir=os.path.abspath(os.path.dirname(__file__))
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


@app.route('/')
def index():
    form=LoginForm()
    return render_template('index.html',form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    return render_template('signup.html', form=form)









@app.route('/dashboard')
def dashboard():
    """Video streaming home page."""
    return render_template('dashboard.html')

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
            text_pred=draw_text(boxes, scores, classes, nums, class_names)
            print(text_pred)
            if text_pred =='knife':
                try:
                    msg=Message("Warning!",sender=app.config.get('MAIL_SENDER'),recipients="")
                    msg.body="A harmful object is detected"
                    mail.send(msg)
                except Exception :
                    print ('Error formatting and sending email!')


            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           


        else:
            break


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame',)









