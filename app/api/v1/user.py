import json
from flask import Blueprint, jsonify, request
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from flask import g
from app.validators.forms import UserEmailForm, ClientForm

#blueprint
#redprint
#user=Blueprint('user',__name__)


api=Redprint('user')

@api.route('',methods=['GET'])
@auth.login_required
def get_user():
    #url不应该包含动词
    uid=g.user.uid
    user=User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

@api.route('',methods=['PUT'])
@auth.login_required
def update_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        data=request.get_data()
        json_re=json.loads(data)
        json_re['email']=json_re.pop('account')
        #UserEmailForm().validate_for_api()
        user.set_attrs(json_re)
    return jsonify(user)

@api.route('',methods=['DELETE'])
@auth.login_required
def delete_user():
    uid=g.user.uid
    with db.auto_commit():
        user=User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()

#管理员
@api.route('/<int:uid>',methods=['GET'])
@auth.login_required
def super_get_user(uid):
    #url不应该包含动词
    user=User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)

@api.route('/<int:uid>',methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()