import os

class Config:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flsk_tut.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False