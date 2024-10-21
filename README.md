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

## Screenshots

http://127.0.0.1:5000/
<img width="975" alt="Screenshot 2024-10-21 at 2 24 19 PM" src="https://github.com/user-attachments/assets/d0f0d982-0688-41d8-9579-e22cf93ab2bd">

http://127.0.0.1:5000/users/
<img width="979" alt="Screenshot 2024-10-21 at 2 24 34 PM" src="https://github.com/user-attachments/assets/fa91b28b-8855-44e0-99af-72cba5e555c6">

http://127.0.0.1:5000/users/2
<img width="584" alt="Screenshot 2024-10-21 at 2 24 44 PM" src="https://github.com/user-attachments/assets/7153d23b-149b-471f-99cd-9927710484f1">

http://127.0.0.1:5000/expenses
<img width="814" alt="Screenshot 2024-10-21 at 2 25 36 PM" src="https://github.com/user-attachments/assets/ebf459e0-724c-4aa0-8b54-5b56451d54c5">

http://127.0.0.1:5000/expenses
<img width="804" alt="Screenshot 2024-10-21 at 2 26 09 PM" src="https://github.com/user-attachments/assets/d2c14505-6617-44af-9e33-c40645c0e5fe">

http://127.0.0.1:5000/users/1/expenses
<img width="989" alt="Screenshot 2024-10-21 at 2 26 48 PM" src="https://github.com/user-attachments/assets/933bc16d-6cb4-405f-aa4b-dcd50099658e">

http://127.0.0.1:5000/expenses
<img width="979" alt="Screenshot 2024-10-21 at 2 27 11 PM" src="https://github.com/user-attachments/assets/a60ea48b-4b3e-4b32-a03e-11513c316fc8">

http://127.0.0.1:5000/balance-sheet
<img width="914" alt="Screenshot 2024-10-21 at 2 27 29 PM" src="https://github.com/user-attachments/assets/b74573f6-94c2-4a87-ad9c-9b8c1c9834f9">

🛠️ Future Enhancements
-----------------------

*   **User Authentication & Authorization**: Secure your app with login systems and permission-based access.
    
*   **Error Handling & Input Validation**: Robust error responses and comprehensive validation for even better user experience.
    
*   **Performance Optimization**: Optimize for large datasets and faster query times.
    
*   **Testing**: Add unit and integration tests to ensure code reliability.
