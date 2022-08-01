#!/usr/bin/env python3
import tensorflow as tf
import nni

def load_dataset():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data() # Load MNIST dataset, The MNIST dataset is a set of handwritten digits (0-9) that have been preprocessed to make them easier to work with.
    return (x_train/255., y_train, x_test/255., y_test) # normalize data


(x_train, y_train, x_test, y_test) = load_dataset()
#print(x_tain.shape) # (60000, 28, 28)
#print(x_test.shape) # (10000, 28, 28)

# Create function that creates a model
def create_model(num_units, dropout_rate, lr, activation):
    model = tf.keras.models.Sequential([ # create sequential model
        tf.keras.layers.Flatten(), # flatten the input data from 2D to 1D 
        tf.keras.layers.Dense(num_units, activation=activation), # add a dense layer with num_units neurons and an activation function
        tf.keras.layers.Dropout(dropout_rate), # add a dropout layer with dropout_rate to prevent overfitting
        tf.keras.layers.Dense(10, activation='softmax') # add a dense layer with 10 neurons and an activation function of softmax to output a probability distribution
    ])
    model.compile( # compile the model with loss function and optimizer 
        loss='sparse_categorical_crossentropy', # sparse_categorical_crossentropy is a loss function that is used to train a model to classify data.
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr), # Adam is a gradient-based optimizer that is a good choice for stochastic gradient descent.
        metrics=['accuracy'] # metrics is a list of metrics to be evaluated by the model during training and testing.
    )
    return model

# Create a function that trains our model
# The params dictionary is a dictionary that contains the parameters of the model that we want to train.
def train(params):

    class ReportIntResult(tf.keras.callbacks.Callback): # create a callback class that reports the results of the training
        def on_epoch_end(self, epoch, logs=None): # on_epoch_end is a callback method that is called at the end of each epoch.
            acc = logs.get('val_accuracy') # get the accuracy of the model on the validation set
            if acc:
                nni.report_intermediate_result(acc) # report the accuracy of the model on the validation set to NNI

    num_units = params.get('num_units') 
    dropout_rate = params.get('dropout_rate') 
    lr = params.get('lr')
    activation = params.get('activation')
    batch_size = params.get('batch_size')

    model = create_model(num_units, dropout_rate, lr, activation) # create model based on parameters
    (x_train, y_train, x_test, y_test) = load_dataset() # reload dataset

    _ = model.fit( 
        x_train, y_train,
        validation_data=(x_test, y_test), # validation_data is a tuple of (x_test, y_test)
        epochs=10, # number of epochs to train the model, epochs is a measure of how many times the model will iterate over the entire dataset.
        batch_size=batch_size, # batch_size is the number of samples that will be passed to the model at a time.
        callbacks=[ReportIntResult()], # callbacks is a list of callbacks to be called during training.
        verbose=False # verbose is a boolean that controls the verbosity of the output.
    )

    _, acc = model.evaluate(x_test, y_test, verbose=False) # evaluate the model on the test data and return the loss and accuracy
    #print('Validation Accuracy: ', acc) # print the accuracy of the model... Change to below
    nni.report_final_result(acc) # report the accuracy of the model to NNI

if __name__ == '__main__': # if the file is run directly, run the train function
    params = {
        'num_units': 32, # number of neurons in the dense layer set to 32
        'dropout_rate': 0.1, # dropout rate set to 0.1
        'lr': 0.001, # learning rate set to 0.001 (default value)
        'activation': 'relu', # activation function set to relu (default value)
        'batch_size': 1024 # batch size set to 1024 (default value)
    }


    tuned_params = nni.get_next_parameter() # get the next parameter from NNI
    params.update(tuned_params) # update the parameters with the tuned parameters

    train(params)

