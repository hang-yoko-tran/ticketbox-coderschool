from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URL=os.environ.get('DATABASE_URL')
    SECRET_KET='freakingtiredkey'


