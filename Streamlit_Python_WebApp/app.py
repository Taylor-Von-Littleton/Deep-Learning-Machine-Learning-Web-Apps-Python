import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score

# Suppress warnings about pyplot using matplotlib
st.set_option('deprecation.showPyplotGlobalUse', False) 

def main():
    st.title("Binary Classification Web App") # Title of the web app
    st.sidebar.title("Binary Classification Web App") # Title of the sidebar
    st.markdown("Are your mushrooms edible or poisonous? 🍄") # Markdown text
    st.sidebar.markdown("Are your mushrooms edible or poisonous? 🍄")

    @st.cache(persist=True) # Cache the dataframe
    def load_data(): 
        data = pd.read_csv("/home/taylor/Desktop/Projects/mushrooms.csv") # Read the dataframe
        labelencoder=LabelEncoder() # Create a label encoder object to encode the labels to numerical values (0 and 1) for the classification algorithm using the sklearn.preprocessing.LabelEncoder class
        for col in data.columns: # Loop through the columns
            data[col] = labelencoder.fit_transform(data[col]) # Apply the label encoder
        return data # Return the dataframe
    
    @st.cache(persist=True)
    def split(df): # Split the dataframe into train and test
        y = df.type # Set the target variable
        x = df.drop(columns=['type']) # Drop the target variable from the dataframe
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0) 
        # Split the dataframe into train and test using the train_test_split function from sklearn 
        return x_train, x_test, y_train, y_test # Return the train and test dataframes
    
    def plot_metrics(metrics_list): 
        if 'Confusion Matrix' in metrics_list: # If the user selected the confusion matrix
            st.subheader("Confusion Matrix") # Subheader for the confusion matrix
            plot_confusion_matrix(model, x_test, y_test, display_labels=class_names) # Plot the confusion matrix
            st.pyplot() # Display the plot and make it interactive

        if 'ROC Curve' in metrics_list:
            st.subheader("ROC Curve") # Subheader for the ROC curve
            plot_roc_curve(model, x_test, y_test) # Plot the ROC curve
            st.pyplot() # Display the plot and makes it interactive
        
        if 'Precision-Recall Curve' in metrics_list:
            st.subheader('Precision-Recall Curve') # Subheader for the precision-recall curve
            plot_precision_recall_curve(model, x_test, y_test) # Plot the precision-recall curve
            st.pyplot() # Display the plot

    df = load_data() # Load the dataframe
    class_names = ['edible', 'poisonous'] # Set the class names
    x_train, x_test, y_train, y_test = split(df) # Split the dataframe into train and test
    st.sidebar.subheader("Choose Classifier") # Subheader for the classifier selection
    classifier = st.sidebar.selectbox("Classifier", ("Support Vector Machine (SVM)", "Logistic Regression", "Random Forest")) 
    # Selectbox same as dropdown menu | Select the classifier

    if classifier == 'Support Vector Machine (SVM)':  # If the user selected the SVM
        st.sidebar.subheader("Model Hyperparameters") 
        #choose parameters *lower values of c = higher regularization strength
        C = st.sidebar.number_input("C (Regularization parameter)", 0.01, 10.0, step=0.01, key='C_SVM') # Allow user to change Number input for the C parameter with range (0.01 to 10.0)
        kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key='kernel') # Allow user to change the kernel type either rbf or linear
        gamma = st.sidebar.radio("Gamma (Kernel Coefficient)", ("scale", "auto"), key='gamma') # Allow user to change the kernel coefficient either scale or auto

        metrics = st.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix', 'ROC Curve', 'Precision-Recall Curve')) 
        # Multi-select for the metrics / Must match paremeters within the if classifier statement
    
        if st.sidebar.button("Classify", key='classify'):
            st.subheader("Support Vector Machine (SVM) Results")
            model = SVC(C=C, kernel=kernel, gamma=gamma) 
            model.fit(x_train, y_train) 
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)
    
    if classifier == 'Logistic Regression':
        st.sidebar.subheader("Model Hyperparameters")
        C = st.sidebar.number_input("C (Regularization parameter)", 0.01, 10.0, step=0.01, key='C_LR')
        max_iter = st.sidebar.slider("Maximum number of iterations", 100, 500, key='max_iter')

        metrics = st.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix', 'ROC Curve', 'Precision-Recall Curve'))

        if st.sidebar.button("Classify", key='classify'):
            st.subheader("Logistic Regression Results")
            model = LogisticRegression(C=C, penalty='l2', max_iter=max_iter) #penalty is the regularization term and l2 is the type of regularization
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)
    
    if classifier == 'Random Forest':
        st.sidebar.subheader("Model Hyperparameters")
        n_estimators = st.sidebar.number_input("The number of trees in the forest", 100, 5000, step=10, key='n_estimators') #allow user to change the number of trees in the forest
        max_depth = st.sidebar.number_input("The maximum depth of the tree", 1, 20, step=1, key='n_estimators') #allow user to change the maximum depth of the tree (1 to 20)
        bootstrap = st.sidebar.radio("Bootstrap samples when building trees", ('True', 'False'), key='bootstrap') #allow user to change the bootstrap samples when building trees
        metrics = st.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix', 'ROC Curve', 'Precision-Recall Curve')) #multiselect for the metrics / Must match paremeters within the if classifier statement

        if st.sidebar.button("Classify", key='classify'):
            st.subheader("Random Forest Results")
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs=-1) 
            #^^^n_estimators is the number of trees in the forest, max_depth is the maximum depth of the tree, bootstrap is whether to bootstrap the samples when building trees
            model.fit(x_train, y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=class_names).round(2))
            plot_metrics(metrics)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Mushroom Data Set (Classification)")
        st.write(df)
        st.markdown("This [data set](https://archive.ics.uci.edu/ml/datasets/Mushroom) includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms "
        "in the Agaricus and Lepiota Family (pp. 500-525). Each species is identified as definitely edible, definitely poisonous, "
        "or of unknown edibility and not recommended. This latter class was combined with the poisonous one.")

if __name__ == '__main__':
    main()
