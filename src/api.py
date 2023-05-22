from flask import Flask
from src.bar import Bar
import os 
# print current folder 
print(os.getcwd())

path = '/Users/alessiogandelli/dev/internship/climate-networks/models/drink.json'

bar = Bar.from_json(path)


app = Flask(__name__)

@app.route("/cocktails")
def hello_world():
    return bar.cocktails

