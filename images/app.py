"""This is it folks"""

import re
import json
import random
import time
import multiprocessing
from io import BytesIO

from redis import Redis
import boto3
import requests
import pika
import dlib
import cv2
from skimage import io
from faceitize import replace_faces
import config

with open('./config/config.json') as data_file:
    CONFIG = json.load(data_file)['people']

# This should probably be somewhere else
REDIS = Redis(host=config.REDIS_HOST, port=6379)

# Face Detector Models
FACE_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

# S3 Config
S3_CLIENT = boto3.resource('s3')
BUCKET_NAME = 'assets.dailywoof.space'
S3_BASEPATH = "http://assets.dailywoof.space/"

def landmarks_to_tpl(landmarks):
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 67)]

def extract_name(url):
    """Takes the a url and exracts the images name"""
    return re.search(r"[^\/]*\.(png|jpg|jpeg)", url)

def set_story(db_client, info):
    """Adds the story to redis"""
    url = info['url']
    info = json.dumps(info)
    db_client.pipeline().set(info['url'], json.dumps(info)).expire(url, 3600000).execute()

    return


def run():
    # Connect
    connection = pika.BlockingConnection(config.CONNECTION_PARAMETERS)
    channel = connection.channel()

    # Set up everything to start consuming
    channel.queue_declare(queue=config.QUEUE_NAME)
    channel.basic_qos(prefetch_count=2)
    channel.basic_consume(callback, queue=config.QUEUE_NAME, no_ack=True)

    # We wrap this in a try, this is because pika is prone to missing heartbeats
    try:
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        print("Connection closed prematurely")


# Callback function for consumer
def callback(ch, method, properties, body):
    # Get and load image into memory
    body = json.loads(body.decode('utf-8'))
    url = body['image']
    if url == "" or url is None:
        return

    # Get a random user and image from the supplied config
    body['tag'] = random.choice(list(CONFIG.keys()))
    conf_item = CONFIG[body['tag']]

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
        print(e)
        return

    url_matches = extract_name(url)
    if url_matches is None:
        return

    name = url_matches[0]
    image_type = name.split(".")
    image_type = image_type[len(image_type) - 1]
    buffer = cv2.imencode("." + image_type, img)[1].tostring()


    # Upload image to an s3 bucket
    print("trying bucket")
    try:
            S3_CLIENT.Bucket(config.BUCKET_NAME).put_object(Key=name, Body=buffer)
    except Exception as e:
        print("faILED upload")
        print(e)

    # Put everything in redis for use
    body['image'] = config.S3_BASEPATH + name
    REDIS.pipeline().set(body['url'], json.dumps(body)).expire(url, 3600000).execute()

if __name__ == '__main__':
    proc = multiprocessing.Process(target=run, name="images", )
    proc.start()

    time.sleep(3600)
    if proc.is_alive():
        proc.terminate()
        proc.join()
