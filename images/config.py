"""General config option mostly sourced from env variables"""
import os
import pika

MQ_HOST = os.getenv('MQ_HOST', default='rabbitmq-service')
MQ_PORT = os.getenv('MQ_PORT', default=5672)
QUEUE_NAME = os.getenv('MQ_QUEUE', default='images')
REDIS_HOST = os.getenv('REDIS_HOST', default='redis-service')
BUCKET_NAME = os.getenv('BUCKET_NAME', default='assets.dailywoof.space')
S3_BASEPATH = os.getenv('S3_BASEPATH', "http://assets.dailywoof.space/")

CONNECTION_PARAMETERS = pika.ConnectionParameters(MQ_HOST,
                                                  retry_delay=5,
                                                  connection_attempts=5)
