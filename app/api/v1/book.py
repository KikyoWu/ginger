from flask import Blueprint
from app.libs.redprint import Redprint

#blueprint
#book=Blueprint('book',__name__)
#redprint
api=Redprint('book')

@api.route('',methods=['GET'])
def get_book():
    return 'get book'