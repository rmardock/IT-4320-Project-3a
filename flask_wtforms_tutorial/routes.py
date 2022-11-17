from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import StockForm
from .charts import *


@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    key = "DLEZPCELNFARX2UF"
    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the form data to query the api
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = convert_date(request.form['start_date'])
            end_date = convert_date(request.form['end_date'])

            if end_date <= start_date:
                # Generate error message as pass to the page
                err = "ERROR: End date cannot be earlier than Start date."
                chart = None
            else:
                err = None
                 
                # Format time series for use
                json_time, url_time = format_time_series(time_series)
                
                # Call query_API function and assign data to variable
                data = query_API(url_time, symbol, key)
                
                # This chart variable is what is passed to the stock.html page to render the chart returned from the api
                chart = build_chart(symbol, chart_type, data, json_time, start_date, end_date)

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")
