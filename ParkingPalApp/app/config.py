import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    # for AutoML Tables integration
    PROJECT_ID = 'pittparkingpal'
    COMPUTE_REGION = 'us-central1'
    MODEL_DISPLAY_NAME = 'oakland_meter_non_20201014023202'