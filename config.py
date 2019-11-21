from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    DEBUG=True
    SQLACHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
    SECRET_KET='freakingtiredkey'


