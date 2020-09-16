# -*- coding:utf-8 -*-

from .. import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app, session_options={"autoflush": False, "autocommit": False, "expire_on_commit": False})
