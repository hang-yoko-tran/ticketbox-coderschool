from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI')
    SECRET_KET='freakingtiredkey'


