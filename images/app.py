#!/usr/bin/python
"""This is it folks"""

import re
import json
import random
from io import BytesIO

from redis import Redis
import boto3
import requests
import pika
import dlib
import cv2
from skimage import io
from faceitize import replace_faces


with open('./config/config.json') as data_file:
    CONFIG = json.load(data_file)['people']

# RabbitMQ
QUEUE_NAME = 'images'
CONNECTION_PARAMETERS = pika.ConnectionParameters('messager', retry_delay=5, connection_attempts=5)

REDIS = Redis(host='redis', port=6379)

# Face Detector Models
FACE_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

# S3 Config
S3_CLIENT = boto3.resource('s3')
BUCKET_NAME = 'assets.dailywoof.space'
S3_BASEPATH = "http://assets.dailywoof.space/"

# Utility Functions
def create_queue(channel, name):
    channel.queue_declare(queue=name)

def landmarks_to_tpl(landmarks):
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 67)]

def extract_name(url):
    """Takes the a url and exracts the images name"""
    return re.search(r"[^\/]*\.(png|jpg|jpeg)", url)

def set_story(db_client, info):
    """Adds the story to redis"""
    url = info['url']
    info = json.dumps(info)
    db_client.pipeline().set(url, info).expire(url, 3600000).execute()

    return


def main():
    while True:
        connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
        channel = connection.channel()
        create_queue(channel, QUEUE_NAME)

        channel.basic_qos(prefetch_count=2)
        channel.basic_consume(callback, queue='images', no_ack=True)
        try:
            channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            continue

def callback(ch, method, properties, body):
    # Get and load image into memory
    body = json.loads(body.decode('utf-8'))
    url = body['image']

    if url == "" or url is None:
        return

    # Get a random user and image from the supplied config
    key = random.choice(list(CONFIG.keys()))
    conf_item = CONFIG[key]

    # Load image
    static_img = io.imread('config/' + random.choice(conf_item['image']))
    static_img = cv2.cvtColor(static_img, cv2.COLOR_BGR2RGB)

    # Extract landmarks for a face from the config picture
    faces = FACE_DETECTOR(static_img, 1)
    for face in faces:
        static_landmarks = landmarks_to_tpl(LANDMARK_PREDICTOR(static_img, face))

    # Wrapping in try for now, not all images succeed
    try:
        f = requests.get(url).content
        img = io.imread(BytesIO(f))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # We don't want images without faces in them
        if len(FACE_DETECTOR(img, 1)) == 0:
            return

        img = replace_faces(
            img,
            static_img,
            static_landmarks,
            landmark_predictor=LANDMARK_PREDICTOR)
    except Exception as e:
        return

    name = extract_name(url)[0]
    image_type = name.split(".")
    image_type = image_type[len(image_type) - 1]
    buffer = cv2.imencode("." + image_type, img)[1].tostring()


    # Upload image to an s3 bucket
    S3_CLIENT.Bucket(BUCKET_NAME).put_object(Key=name, Body=buffer)

    # Put everything in redis for use
    body['image'] = S3_BASEPATH + name
    body['tag'] = key
    set_story(REDIS, body)

if __name__ == '__main__':
    # Load our static image first
    main()
