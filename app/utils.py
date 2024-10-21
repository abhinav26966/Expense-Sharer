from app.models import User, Expense, ExpenseSplit

def validate_percentage_split(splits):
    total_percentage = sum(split['percentage'] for split in splits)
    return abs(total_percentage - 100) < 0.01

def generate_balance_sheet():
    users = User.query.all()
    balance_sheet = {}

    for user in users:
        balance_sheet[user.id] = {
            'name': user.name,
            'email': user.email,
            'total_paid': 0,
            'total_owed': 0,
            'net_balance': 0
        }

    expenses = Expense.query.all()
    for expense in expenses:
        payer = expense.payer
        balance_sheet[payer.id]['total_paid'] += expense.amount

        for split in expense.splits:
            balance_sheet[split.user.id]['total_owed'] += split.amount

    for user_id, data in balance_sheet.items():
        data['net_balance'] = data['total_paid'] - data['total_owed']

    return balance_sheet
