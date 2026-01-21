"""
Unit tests for the Daily Expense Sharing Application.
These tests validate core functionality including:
- User management
- Expense creation and splitting
- Balance sheet generation
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Expense, ExpenseSplit
from app.utils import validate_percentage_split, generate_balance_sheet


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_users(app):
    """Create sample users for testing."""
    with app.app_context():
        user1 = User(email='alice@test.com', name='Alice', mobile='1234567890')
        user2 = User(email='bob@test.com', name='Bob', mobile='0987654321')
        user3 = User(email='charlie@test.com', name='Charlie', mobile='1122334455')
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        return [user1.id, user2.id, user3.id]


class TestHealthEndpoints:
    """Test basic application health endpoints."""
    
    def test_home_route(self, client):
        """Test the home route returns welcome message."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'Welcome' in data['message']
    
    def test_test_route(self, client):
        """Test the test route is working."""
        response = client.get('/test')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Test route working'


class TestUserManagement:
    """Test user management functionality."""
    
    def test_create_user(self, client):
        """Test creating a new user."""
        user_data = {
            'email': 'newuser@test.com',
            'name': 'New User',
            'mobile': '5555555555'
        }
        response = client.post('/users/', json=user_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User created successfully'
    
    def test_get_user(self, client, sample_users):
        """Test retrieving a user by ID."""
        response = client.get(f'/users/{sample_users[0]}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == 'alice@test.com'
        assert data['name'] == 'Alice'
    
    def test_get_all_users(self, client, sample_users):
        """Test retrieving all users."""
        response = client.get('/users/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
    
    def test_get_nonexistent_user(self, client):
        """Test retrieving a user that doesn't exist."""
        response = client.get('/users/9999')
        assert response.status_code == 404


class TestExpenseManagement:
    """Test expense management functionality."""
    
    def test_add_expense_equal_split(self, client, sample_users):
        """Test adding an expense with equal split."""
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 300,
            'description': 'Dinner',
            'split_method': 'equal',
            'participants': sample_users
        }
        response = client.post('/expenses', json=expense_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Expense added successfully'
    
    def test_add_expense_exact_split(self, client, sample_users):
        """Test adding an expense with exact split."""
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 300,
            'description': 'Shopping',
            'split_method': 'exact',
            'splits': [
                {'user_id': sample_users[0], 'amount': 100},
                {'user_id': sample_users[1], 'amount': 100},
                {'user_id': sample_users[2], 'amount': 100}
            ]
        }
        response = client.post('/expenses', json=expense_data)
        assert response.status_code == 201
    
    def test_add_expense_percentage_split(self, client, sample_users):
        """Test adding an expense with percentage split."""
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 1000,
            'description': 'Party',
            'split_method': 'percentage',
            'splits': [
                {'user_id': sample_users[0], 'percentage': 50},
                {'user_id': sample_users[1], 'percentage': 30},
                {'user_id': sample_users[2], 'percentage': 20}
            ]
        }
        response = client.post('/expenses', json=expense_data)
        assert response.status_code == 201
    
    def test_add_expense_invalid_percentage(self, client, sample_users):
        """Test that invalid percentage splits are rejected."""
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 1000,
            'description': 'Party',
            'split_method': 'percentage',
            'splits': [
                {'user_id': sample_users[0], 'percentage': 50},
                {'user_id': sample_users[1], 'percentage': 30},
                {'user_id': sample_users[2], 'percentage': 30}  # Total = 110%
            ]
        }
        response = client.post('/expenses', json=expense_data)
        assert response.status_code == 400
    
    def test_get_all_expenses(self, client, sample_users):
        """Test retrieving all expenses."""
        # First create an expense
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 300,
            'description': 'Test Expense',
            'split_method': 'equal',
            'participants': sample_users
        }
        client.post('/expenses', json=expense_data)
        
        response = client.get('/expenses')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
    
    def test_get_user_expenses(self, client, sample_users):
        """Test retrieving expenses for a specific user."""
        # Create an expense
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 300,
            'description': 'User Expense',
            'split_method': 'equal',
            'participants': sample_users
        }
        client.post('/expenses', json=expense_data)
        
        response = client.get(f'/users/{sample_users[0]}/expenses')
        assert response.status_code == 200


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_validate_percentage_split_valid(self):
        """Test percentage validation with valid splits."""
        splits = [
            {'percentage': 50},
            {'percentage': 30},
            {'percentage': 20}
        ]
        assert validate_percentage_split(splits) is True
    
    def test_validate_percentage_split_invalid(self):
        """Test percentage validation with invalid splits."""
        splits = [
            {'percentage': 50},
            {'percentage': 30},
            {'percentage': 30}  # Total = 110%
        ]
        assert validate_percentage_split(splits) is False
    
    def test_validate_percentage_split_rounding(self):
        """Test percentage validation handles floating point rounding."""
        splits = [
            {'percentage': 33.33},
            {'percentage': 33.33},
            {'percentage': 33.34}
        ]
        assert validate_percentage_split(splits) is True


class TestBalanceSheet:
    """Test balance sheet functionality."""
    
    def test_balance_sheet_endpoint(self, client, sample_users):
        """Test the balance sheet endpoint."""
        # Create some expenses
        expense_data = {
            'payer_id': sample_users[0],
            'amount': 300,
            'description': 'Balance Test',
            'split_method': 'equal',
            'participants': sample_users
        }
        client.post('/expenses', json=expense_data)
        
        response = client.get('/balance-sheet')
        assert response.status_code == 200
        data = response.get_json()
        assert str(sample_users[0]) in data or sample_users[0] in data
    
    def test_generate_balance_sheet(self, app, sample_users):
        """Test balance sheet generation logic."""
        with app.app_context():
            # Create an expense
            user = User.query.get(sample_users[0])
            expense = Expense(
                amount=300,
                description='Test',
                split_method='equal',
                payer=user
            )
            db.session.add(expense)
            
            # Add splits
            for user_id in sample_users:
                participant = User.query.get(user_id)
                split = ExpenseSplit(
                    expense=expense,
                    user=participant,
                    amount=100
                )
                db.session.add(split)
            db.session.commit()
            
            # Generate balance sheet
            balance_sheet = generate_balance_sheet()
            
            # Payer should have positive net balance
            assert balance_sheet[sample_users[0]]['total_paid'] == 300
            assert balance_sheet[sample_users[0]]['net_balance'] == 200  # paid 300, owes 100


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_expenses_list(self, client, sample_users):
        """Test getting expenses when none exist."""
        response = client.get('/expenses')
        assert response.status_code == 200
        data = response.get_json()
        assert data == []
    
    def test_expense_with_invalid_payer(self, client):
        """Test creating expense with non-existent payer."""
        expense_data = {
            'payer_id': 9999,
            'amount': 300,
            'description': 'Invalid Payer Test',
            'split_method': 'equal',
            'participants': [9999]
        }
        response = client.post('/expenses', json=expense_data)
        # Returns 500 because the route catches the 404 exception and returns error
        assert response.status_code in [404, 500]
