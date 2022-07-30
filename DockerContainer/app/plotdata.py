import pandas as pd
import seaborn as sns
import matplotlib
import io

if __name__ == '__main__':
    from PIL import Image 

matplotlib.use('agg') #To avoid threading issues when running with flask server. 
def regression_plot():
    df = pd.read_csv('tempYearly.csv') # read the dataframe

    sns_plot = sns.regplot(x='Rainfall', y='Temperature', data=df) # plot the regression line

    image = io.BytesIO() # io.BytesIO is a in-memory stream for image data. 

    sns_plot.figure.savefig(image, format = 'png') # save the plot as an image

    image.seek(0) # rewind the stream to the beginning so that it can be read
    return image # return the image data

if __name__ == '__main__':
    image = regression_plot() # call the function to plot the regression plot
    im = Image.open(image) # open the image
    im.save('regress.png', 'PNG') # save the <image_name> as a PNG file