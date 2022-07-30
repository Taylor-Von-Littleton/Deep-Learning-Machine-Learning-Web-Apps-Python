from flask import Flask, send_file
from plotdata import regression_plot
app = Flask(__name__)

@app.route('/', methods=['GET']) # route to display the home page
def regr_plot(): # function to plot the regression plot
    image = regression_plot() # call the function to plot the regression plot
    return send_file(image, attachment_filename='regplot.png', mimetype='image/png') # return the plot as an image

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=False) 