import boto3
from botocore.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.logger import logger
from fastapi_log.log_request import LoggingRoute
from os import environ as env

ACCESS_KEY=env.get('ACCESS_KEY')#"AKIAQ5JGGPI34PP7FI57"
SECRET_KEY=env.get('SECRET_KEY')#"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"
REGION=env.get('REGION')
BUCKET_NAME=env.get('BUCKET_NAME')
EXPIRY=env.get('EXPIRY')
formats="""logname::%(name)s logtime::%(asctime)s timestamp::%(created)f level::%(levelname)s MODULE::%(lineno)d FILENAME::%(filename)s PROCESS_NAME::%(processName)s PROCESS_ID::%(process)d THREAD_NAME::%(threadName)s THREAD_ID::%(thread)d LINE_NO::%(lineno)d message::%(message)s"""
logging.basicConfig(datefmt='%d-%b-%y %H:%M:%S',format=formats,level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastAPI(debug=True)
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.router.route_class = LoggingRoute
@app.get("/vkyc/{video_id}/{video_name}")
async def getPresigned(video_id,video_name):
  my_session = boto3.session.Session()
  my_config = Config(
      region_name = REGION,
      signature_version = 'v4',
      retries = {
          'max_attempts': 10
      }
  )
  s3 = my_session.client(
                        's3',
                        aws_access_key_id= ACCESS_KEY,
                        aws_secret_access_key= SECRET_KEY,
                        config=my_config,
                        endpoint_url='https://s3.ap-south-1.amazonaws.com'
                        )
  try:
    print("vkyc"+video_id+"/"+video_name)
    url = s3.generate_presigned_url(
          ClientMethod='get_object',
          Params={
              'Bucket': BUCKET_NAME,
              'Key': "vkyc/"+video_id+"/"+video_name
          },ExpiresIn=EXPIRY
    )
    return url
  except Exception as e:
    print("\n\n")
    print(e)
    print("\n\n")
    logging.error("VIDEO_ID::{},VIDEO_NAME::{}".format(video_id,video_name),exc_info=False)
    return "FailedToGenerateUrl"