from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, FloatField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    sepallength = FloatField('Sepal length', validators=[DataRequired()])
    sepalwidth = FloatField('Sepal width', validators=[DataRequired()])
    petallength = FloatField('Petal length', validators=[DataRequired()])
    petalwidth = FloatField('Petal width', validators=[DataRequired()])

    submit = SubmitField('Predict')
