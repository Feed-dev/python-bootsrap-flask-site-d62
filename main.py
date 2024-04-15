from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), validators.URL(message='Invalid URL')])
    open_time = StringField('Open Time', validators=[DataRequired()])
    close_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('0', '☕️0'), ('1', '☕️1'), ('2', '☕️2'), ('3', '☕️3'), ('4', '☕️4'), ('5', '☕️5')], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=[('0', '💪0'), ('1', '💪1'), ('2', '💪2'), ('3', '💪3'), ('4', '💪4'), ('5', '💪5')], validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating', choices=[('0', '🔌0'), ('1', '🔌1'), ('2', '🔌2'), ('3', '🔌3'), ('4', '🔌4'), ('5', '🔌5')], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


def emoji_rating(rating, type):
    if type == "coffee":
        emoji = '☕'
    elif type == "wifi":
        emoji = '💪'
    else:  # power outlets
        emoji = '🔌'

    return emoji * int(rating)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Convert ratings to emoji strings
        coffee_emojis = emoji_rating(form.coffee_rating.data, "coffee")
        wifi_emojis = emoji_rating(form.wifi_rating.data, "wifi")
        power_emojis = emoji_rating(form.power_outlet_rating.data, "power")

        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([
                form.cafe.data,
                form.location_url.data,
                form.open_time.data,
                form.close_time.data,
                coffee_emojis,
                wifi_emojis,
                power_emojis
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
