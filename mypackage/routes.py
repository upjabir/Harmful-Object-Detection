from flask import redirect, render_template, flash, Blueprint, request, url_for,Response
from flask_login import login_required, current_user, login_user
from flask import current_app as app
from flask_mail import Mail, Message
import cv2
import numpy as np
import tensorflow as tf
import os
from mypackage.model.utils import load_class_names, output_boxes, draw_outputs, resize_image,draw_text
from mypackage import model,class_names
from mypackage import mail


main=Blueprint('main',__name__,template_folder='templates',static_folder='static')

@main.route('/')
def index():
   return render_template('index.html')

@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html',name=current_user.username)
    
def gen():
    max_output_size = 100
    max_output_size_per_class= 20
    iou_threshold = 0.5
    confidence_threshold = 0.5
    model_size = (416, 416,3)
    num_classes = 80

  
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

@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame',)

   