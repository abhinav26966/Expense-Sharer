from flask import Blueprint, jsonify, request, current_app
from app.models import User, Expense, ExpenseSplit
from app.utils import validate_percentage_split, generate_balance_sheet
from app import db

bp = Blueprint('main', __name__)

@bp.route('/users/', methods=['POST'])
def create_user():
    data = request.json
    user = User(email=data['email'], name=data['name'], mobile=data['mobile'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile': user.mobile
    })

@bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route working"})

@bp.route('/expenses/', methods=['POST'])
@bp.route('/expenses', methods=['POST'])
def add_expense():
    print("Reached add_expense function")
    try:
        data = request.json
        print("Received data:", data)
        
        payer = User.query.get_or_404(data['payer_id'])
        print("Found payer:", payer.name)
        
        expense = Expense(
            amount=data['amount'],
            description=data['description'],
            split_method=data['split_method'],
            payer=payer
        )
        db.session.add(expense)
        print("Added expense to session")

        if data['split_method'] == 'equal':
            total_participants = len(data['participants'])
            split_amount = data['amount'] / total_participants
            for participant_id in data['participants']:
                participant = User.query.get_or_404(participant_id)
                split = ExpenseSplit(expense=expense, user=participant, amount=split_amount)
                db.session.add(split)

        elif data['split_method'] == 'exact':
            for split in data['splits']:
                participant = User.query.get_or_404(split['user_id'])
                split = ExpenseSplit(expense=expense, user=participant, amount=split['amount'])
                db.session.add(split)

        elif data['split_method'] == 'percentage':
            if not validate_percentage_split(data['splits']):
                return jsonify({'error': 'Percentage splits must add up to 100%'}), 400
            for split in data['splits']:
                participant = User.query.get_or_404(split['user_id'])
                amount = (split['percentage'] / 100) * data['amount']
                split = ExpenseSplit(expense=expense, user=participant, amount=amount, percentage=split['percentage'])
                db.session.add(split)

        print("Committing to database")
        db.session.commit()
        print("Commit successful")
        return jsonify({'message': 'Expense added successfully'}), 201

    except Exception as e:
        print("Error occurred:", str(e))
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/users/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile': user.mobile
    } for user in users])

@bp.route('/')
def home():
    return jsonify({'message': 'Welcome to the Daily Expenses Sharing Application'})

@bp.route('/users/<int:user_id>/expenses', methods=['GET'])
def get_user_expenses(user_id):
    user = User.query.get_or_404(user_id)
    expenses = [
        {
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date,
            'split_method': expense.split_method
        }
        for expense in user.expenses
    ]
    return jsonify(expenses)

@bp.route('/expenses', methods=['GET'])
def get_all_expenses():
    expenses = Expense.query.all()
    return jsonify([
        {
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date,
            'split_method': expense.split_method,
            'payer': expense.payer.name
        }
        for expense in expenses
    ])

@bp.route('/balance-sheet', methods=['GET'])
def download_balance_sheet():
    balance_sheet = generate_balance_sheet()
    return jsonify(balance_sheet)
