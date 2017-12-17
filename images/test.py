from io import BytesIO
import boto3
import requests
import pika
from face_replace import replace_faces

# S3 Config
S3_CLIENT = boto3.resource('s3')
BUCKET_NAME = 'assets.dailywoof.space'

# Faces to replace
FACE_FRONT = "./dmx-head.png"

FILE_PATH = './image.jpg'
URL = 'https://static01.nyt.com/images/2017/12/12/us/12Alabama1/12Alabama1-facebookJumbo.jpg'

def main():
    image = get_img(URL)
    aws_s3 = boto3.resource('s3')

    if image:
        image = process_img(image)
        save_img(aws_s3, FILE_PATH, image)


# Basic Wrappers

def get_img(url):
    res = requests.get(url)

    if res:
        return res.content

    return False

def process_img(img):
    img = replace_faces(img, FACE_FRONT)

    # Convert to bytes
    io_out = BytesIO()
    img.save(io_out, 'PNG')
    byte_img = io_out.getvalue()
    io_out.close()

    return byte_img

def save_img(s3, name, img):
    s3.Bucket(BUCKET_NAME).put_object(Key=name, Body=img)
    return

main()
