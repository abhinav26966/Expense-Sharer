# 💸 Daily Expense Sharing App

Welcome to the **Daily Expense Sharing App**! This project simplifies the often tedious task of splitting expenses among friends, colleagues, or family. Whether it's a weekend getaway, dinner with friends, or shared utilities—this app has got you covered. Split expenses with precision and fairness through multiple methods, and manage all your transactions effortlessly.

## 🚀 Features

- **User Management**
  - Add users with their email, name, and mobile number.
  
- **Expense Management**
  - Record and track expenses added by users.
  - Split expenses in three convenient ways:
    1. **Equal Split**: Divide the amount equally among participants.
    2. **Exact Split**: Specify exact amounts for each participant.
    3. **Percentage Split**: Allocate expenses based on predefined percentages (must sum up to 100%).

- **Balance Sheet**
  - Get a detailed breakdown of individual and group expenses.
  - Generate and download balance sheets for easy tracking.

- **Data Validation**
  - Smart validation of user inputs to ensure consistency.
  - Auto-checks percentage-based splits to guarantee they sum up to 100%.

## 📊 Expense Calculation Examples

### Equal Split
Scenario: You go out with 3 friends, and the total bill is 3000. Each friend owes 1000.

### Exact Split
Scenario: You shop with 2 friends and pay 4299. Friend 1 owes 799, Friend 2 owes 2000, and you owe 1500.

### Percentage Split
Scenario: You attend a party with 2 friends and 1 cousin. You owe 50%, Friend 1 owes 25%, and Friend 2 owes 25%.

## 🔧 Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite

## 📋 API Endpoints

### User Endpoints:
- `POST/user` - Create a new user
- `GET/user/id` - Retrieve user details by ID

### Expense Endpoints:
- `POST/expenses` - Add a new expense
- `GET/expense/user/id` - Get individual user expenses
- `GET/expenses` - Retrieve overall expenses
- `GET/balance-sheet` - Download the balance sheet

## 💡 Getting Started

### Running Locally
-----------------------

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/daily-expense-sharing-app.git
    cd daily-expense-sharing-app
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables in a `.env` file:
    ```bash
    SECRET_KEY=YOUR_SECRET_KEY
    DATABASE_URL=YOUR_DATABASE_URL
    ```

5. Make sure you're in the project root directory and your virtual environment is activated.

6. Run the following command:
    ```
    python run.py
    ```

### You can use tools like cURL or Postman to test the API endpoints:

- Create a user: POST /users
- Get user details: GET /users/<user_id>
- Add an expense: POST /expenses
- Get user expenses: GET /users/<user_id>/expenses
- Get all expenses: GET /expenses
- Get balance sheet: GET /balance-sheet

🛠️ Future Enhancements
-----------------------

*   **User Authentication & Authorization**: Secure your app with login systems and permission-based access.
    
*   **Error Handling & Input Validation**: Robust error responses and comprehensive validation for even better user experience.
    
*   **Performance Optimization**: Optimize for large datasets and faster query times.
    
*   **Testing**: Add unit and integration tests to ensure code reliability.