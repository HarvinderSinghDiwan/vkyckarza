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
@app.get("/healthcheck")
def healthcheck():
  return "Healthy"
@app.get("/getsigned")
async def getPresigned(bn,key,ex):
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
    url = s3.generate_presigned_url(
          ClientMethod='get_object',
          Params={
              'Bucket': bn,
              'Key': key
          },ExpiresIn=ex
    )
    return url
  except Exception as e:
    logging.error(e,"VIDEO_ID::{},VIDEO_NAME::{}".format(key.split("/")[1],key.split("/")[2]),exc_info=True)
    return {"status":"FailedToGenerateUrl"}