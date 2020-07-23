from flask import Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import cv2
import numpy as np
import tensorflow as tf
import os
from mypackage.model.yolov3 import YOLOv3Net
from mypackage.model.utils import load_class_names
from flask_login import LoginManager

db=SQLAlchemy()

login_manager=LoginManager()
mail=Mail()

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
model_size = (416, 416,3)
num_classes = 80
max_output_size = 100
max_output_size_per_class= 20
iou_threshold = 0.5
confidence_threshold = 0.5

def create_app():
    app=Flask(__name__,instance_relative_config=False)
    
    app.config.from_object('config.Config')

   
    db.init_app(app)
    login_manager.login_view='auth_bp.login'
    login_manager.init_app(app)
    mail.init_app(app)

   

    with app.app_context():

      

        from mypackage.auth import auth
        from mypackage.routes import main

        app.register_blueprint(auth)
        app.register_blueprint(main)


        db.create_all()


        return app






