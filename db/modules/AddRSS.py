#다른 경로에 있는 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from db.main import db

