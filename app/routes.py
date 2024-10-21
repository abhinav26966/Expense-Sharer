import io
from flask import Blueprint, jsonify, request, current_app
from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User, Expense, ExpenseSplit
from app.utils import validate_percentage_split, generate_balance_sheet
from app import db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from flask_sqlalchemy import Pagination
from openpyxl import Workbook
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

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


app.config['JWT_SECRET_KEY'] = 'NxA7g7j/6zzeLDmQTHkLSZ6U5RddCH0PVStVlDse8nw=' 
jwt = JWTManager(app)

@app.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data or 'amount' not in data or 'split_method' not in data or 'participants' not in data:
        return jsonify({"error": "Invalid input"}), 400

    amount = data['amount']
    split_method = data['split_method']
    participants = data['participants']

    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    if split_method not in ['equal', 'exact', 'percentage']:
        return jsonify({"error": "Invalid split method"}), 400

    if not isinstance(participants, list) or len(participants) < 2:
        return jsonify({"error": "At least two participants required"}), 400

    if split_method == 'exact':
        if 'split_details' not in data or sum(data['split_details'].values()) != amount:
            return jsonify({"error": "Exact amounts must sum up to the total amount"}), 400

    if split_method == 'percentage':
        if 'split_details' not in data or sum(data['split_details'].values()) != 100:
            return jsonify({"error": "Percentages must add up to 100%"}), 400

    # Create and save the expense
    new_expense = Expense(
        amount=amount,
        split_method=split_method,
        added_by=current_user_id
    )
    db.session.add(new_expense)
    db.session.commit()

    # Create and save the expense splits
    for participant in participants:
        split_amount = calculate_split_amount(amount, split_method, data.get('split_details', {}), participant)
        new_split = ExpenseSplit(
            expense_id=new_expense.id,
            user_id=participant,
            amount=split_amount
        )
        db.session.add(new_split)
    
    db.session.commit()

    return jsonify({"message": "Expense added successfully", "expense_id": new_expense.id}), 201

def calculate_split_amount(total_amount, split_method, split_details, participant):
    if split_method == 'equal':
        return total_amount / len(split_details)
    elif split_method == 'exact':
        return split_details.get(participant, 0)
    elif split_method == 'percentage':
        return total_amount * (split_details.get(participant, 0) / 100)



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_all_expenses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    expenses = Expense.query.order_by(Expense.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    expenses_list = []
    for expense in expenses.items:
        expenses_list.append({
            'id': expense.id,
            'amount': expense.amount,
            'split_method': expense.split_method,
            'date': expense.date.strftime('%Y-%m-%d %H:%M:%S'),
            'added_by': expense.added_by
        })

    return jsonify({
        'expenses': expenses_list,
        'page': expenses.page,
        'per_page': expenses.per_page,
        'total_pages': expenses.pages,
        'total_items': expenses.total
    }), 200

@app.route('/user/expenses', methods=['GET'])
@jwt_required()
def get_user_expenses():
    current_user_id = get_jwt_identity()
    user_expenses = ExpenseSplit.query.filter_by(user_id=current_user_id).all()
    
    expenses_list = []
    for expense_split in user_expenses:
        expense = Expense.query.get(expense_split.expense_id)
        expenses_list.append({
            'id': expense.id,
            'amount': expense.amount,
            'split_method': expense.split_method,
            'date': expense.date.strftime('%Y-%m-%d %H:%M:%S'),
            'owed_amount': expense_split.amount
        })
    
    return jsonify(expenses=expenses_list), 200

@app.route('/balance-sheet', methods=['GET'])
@jwt_required()
def download_balance_sheet():
    current_user_id = get_jwt_identity()

    # Fetch all expenses and splits for the current user
    expenses = db.session.query(
        Expense.id,
        Expense.amount,
        Expense.split_method,
        Expense.date,
        ExpenseSplit.amount.label('split_amount'),
        User.name.label('participant_name')
    ).join(ExpenseSplit, Expense.id == ExpenseSplit.expense_id
    ).join(User, ExpenseSplit.user_id == User.id
    ).filter((Expense.added_by == current_user_id) | (ExpenseSplit.user_id == current_user_id)
    ).order_by(Expense.date.desc()).all()

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Balance Sheet"

    # Add headers
    headers = ['Expense ID', 'Total Amount', 'Split Method', 'Date', 'Participant', 'Amount Owed']
    ws.append(headers)

    # Add data to the sheet
    for expense in expenses:
        ws.append([
            expense.id,
            expense.amount,
            expense.split_method,
            expense.date.strftime('%Y-%m-%d %H:%M:%S'),
            expense.participant_name,
            expense.split_amount
        ])

    # Calculate and add total owed
    total_owed = db.session.query(func.sum(ExpenseSplit.amount)).filter_by(user_id=current_user_id).scalar()
    ws.append(['', '', '', '', 'Total Owed:', total_owed or 0])

    # Save to a BytesIO object
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        attachment_filename='balance_sheet.xlsx'
    )