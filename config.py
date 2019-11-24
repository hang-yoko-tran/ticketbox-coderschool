from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
    SECRET_KEY='freakingtiredkey'
    EMAIL_API=os.environ.get("EMAIL_API")


