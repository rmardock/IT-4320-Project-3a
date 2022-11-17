"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length
from flask import json
# Import to use the get_symbols() function from charts.py
from .charts import get_symbols

# Variables for json file paths
nyse_path = "data/nyse-listed_json.json"
nasdaq_path = "data/nasdaq-listed-symbols_json.json"

# Variables for accessing symbols from json files
nyse_key = "ACT Symbol"
nasdaq_key = "Symbol"

# Initialize symbol choices list
symbol_choices = []

# Add nyse symbols to list
symbol_choices = get_symbols(symbol_choices, nyse_path, nyse_key)
# Add nasdaq symbols to list
symbol_choices = get_symbols(symbol_choices, nasdaq_path, nasdaq_key)
# Sort list alphabetically
symbol_choices.sort()
    
class StockForm(FlaskForm):
    """Generate Your Graph."""

    symbol = SelectField("Choose Stock Symbol",[DataRequired()],
        choices=symbol_choices,
        # Read choices from list of symbols
    )

    chart_type = SelectField("Select Chart Type",[DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line"),
        ],
    )

    time_series = SelectField("Select Time Series",[DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. Monthly"),
        ],
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")



