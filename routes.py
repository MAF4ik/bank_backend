from flask import Blueprint, jsonify, request
from models import User, Account
import repository

app = Blueprint('routes', __name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "server is up and running..."}), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], surname=data['surname'], age=data['age'])
    repository.create_user(user)
    return {"status": "user created"}, 201


@app.route('/user/<int:id>/details', methods=['GET'])
def get_user_by_id(id):
    user = repository.get_user_by_id(id)
    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]
    return {"user": user_dict}, 200


@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User(name=data["name"], surname=data["surname"], age=data["age"])
    repository.update_user(id, user)
    return {"status": "user updated"}, 200


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    repository.delete_user(id)
    return {"status": "user deleted"}, 200


@app.route('/account/<int:user_id>', methods=['POST'])
def create_account(user_id):
    acc = Account(user_id=user_id)
    repository.create_account(acc)
    return {"status": "account created"}, 201


@app.route('/account/<int:user_id>/details', methods=['GET'])
def account_details(user_id):
    accounts = repository.get_account_by_user_id(user_id)
    serialized_accounts = []
    for account in accounts:
        account_dict = account.__dict__
        del account_dict["_sa_instance_state"]
        serialized_accounts.append(account_dict)

    return {"account": serialized_accounts}, 200


@app.route('/account/<int:user_id>/<int:account_number>', methods=['DELETE'])
def delete_account(user_id, account_number):
    repository.delete_account(user_id, account_number)
    return {"status": "account deleted"}, 200


@app.route('/account/<int:account_number>', methods=['PATCH'])
def top_up_balance(account_number):
    data = request.get_json()
    new_balance = data['new_balance']
    repository.top_up_balance(account_number, new_balance)
    return {"status": "balance updated"}, 200


@app.route('/account/<int:user_id>/<int:account_number>', methods=['PATCH'])
def withdrawing_money(user_id, account_number):
    data = request.get_json()
    new_balance = data['new_balance']
    repository.withdrawing_money(user_id, account_number, new_balance)
    return {"status": "balance updated"}, 200


@app.route('/account/<int:user_id>''/<int:transfer_account_number>'
           '/<int:receive_account_number>', methods=['PATCH'])
def transfer_account(user_id, transfer_account_number, receive_account_number):
    data = request.get_json()
    new_balance = data['new_balance']
    repository.transfer_account(user_id, transfer_account_number, receive_account_number, new_balance)
    return {"status": "balance updated"}, 200
