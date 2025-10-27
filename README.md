# Expense Tracker

A web-based expense tracking application built with Flask that helps you manage your income and expenses with intuitive visualizations and easy data management.

🔗 [Live Demo](https://expense-tracker-jso9.onrender.com/)

## Features

- 📊 Interactive dashboard with summary statistics
- 💰 Income tracking with source categorization
- 💸 Expense tracking with category management
- 📈 Visual data representation using charts
- 📱 Responsive design for mobile and desktop
- 📥 Export data to Excel functionality
- 🔄 Dynamic data loading with pagination
- 📊 Real-time data visualization

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript (Chart.js)
- **Database**: Excel (using pandas)
- **Deployment**: Render

## Dependencies

```plaintext
Flask              - Web framework
Jinja2             - Template engine
openpyxl          - Excel file handling
pandas            - Data manipulation
python-dotenv     - Environment variable management
SQLAlchemy        - ORM (Object Relational Mapper)
Werkzeug          - WSGI web application library
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arynjeri/expense-tracker.git
   cd expense-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Dashboard
- View total income, expenses, and current balance
- See trends through interactive charts
- Download complete financial data as Excel file

### Income Management
- Add new income entries with amount, source, and date
- View income distribution by source
- Analyze income trends over time
- Delete individual income entries

### Expense Management
- Track expenses with amount, category, and date
- View expense distribution by category
- Monitor expense trends
- Remove specific expense entries

### Data Export
- Export all financial data to Excel
- Automated file naming with timestamp
- Separate sheets for income and expenses

## Development

The application uses a simple Excel-based storage system with two sheets:
- `Income`: Stores income transactions
- `Expense`: Stores expense transactions

Demo data is automatically generated when the application starts for the first time.

## Deployment

The application is deployed on Render with the following configuration:

```yaml
services:
  - type: web
    name: expense-tracker
    env: python
    startCommand: python app.py
    buildCommand: pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available for personal and commercial use.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pandas](https://pandas.pydata.org/)
