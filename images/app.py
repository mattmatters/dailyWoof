#!/usr/bin/python
"""This is it folks"""

import re
import json
from io import BytesIO

import boto3
import requests
import pika
import dlib
import cv2
from skimage import io
from faceitize import replace_faces

# RabbitMQ
QUEUE_NAME = 'images'

# Face Detector Models
FACE_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor(
    './shape_predictor_68_face_landmarks.dat')

# S3 Config
S3_CLIENT = boto3.resource('s3')
BUCKET_NAME = 'assets.dailywoof.space'

# Faces to replace
DMX_IMG_URL = 'https://nyppagesix.files.wordpress.com/2017/07/170714_yang_nyp___manh_fed___dmx_3.jpg'


# Utility Functions
def create_queue(channel, name):
    queue = channel.queue_declare(queue=name)
    channel.queue_bind(exchange='stories', queue=queue.method.queue)


def landmarks_to_tpl(landmarks):
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 67)]


def extract_name(url):
    """Takes the a url and exracts the images name"""
    return re.search(r"[^\/]*\.(png|jpg|jpeg)", url)


def main():
    CHANNEL.basic_qos(prefetch_count=1)
    CHANNEL.basic_consume(callback, queue='images', no_ack=True)
    CHANNEL.start_consuming()


def callback(ch, method, properties, body):
    # Get and load image into memory
    body = json.loads(body.decode('utf-8'))
    url = body['image']

    try:
        f = requests.get(url).content
        img = io.imread(BytesIO(f))
    except Exception as e:
        print(url + " is an invalid url, skipping")
        return
    print(url)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = replace_faces(
        img,
        static_img,
        static_landmarks,
        landmark_predictor=LANDMARK_PREDICTOR)
    name = extract_name(url)[0]

    image_type = name.split(".")
    image_type = image_type[len(image_type) - 1]

    buffer = cv2.imencode("." + image_type, img)[1].tostring()

    S3_CLIENT.Bucket(BUCKET_NAME).put_object(Key=name, Body=buffer)


if __name__ == '__main__':
    # Load our static image first
    static_img = requests.get(DMX_IMG_URL).content
    static_img = io.imread(BytesIO(static_img))
    static_img = cv2.cvtColor(static_img, cv2.COLOR_BGR2RGB)
    faces = FACE_DETECTOR(static_img, 1)
    for face in faces:
        static_landmarks = landmarks_to_tpl(
            LANDMARK_PREDICTOR(static_img, face))
    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(
            'messager', retry_delay=5, connection_attempts=5))
    CHANNEL = CONNECTION.channel()
    CHANNEL.exchange_declare(exchange='stories', exchange_type='fanout')
    create_queue(CHANNEL, QUEUE_NAME)
    main()
