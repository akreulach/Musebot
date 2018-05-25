import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Make some data
# [a, b] -> [c, d], where c = a + b, and d = a * b
X = numpy.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2],
[1, 2], [2, 2]])
Y = numpy.array([[0, 0], [1, 0], [2, 0], [1, 0], [2, 1], [3, 2], [2, 0],
[3, 2], [4, 4]])


# make a neural net
def make_neural_net():
    model = Sequential()
    model.add(Dense(2, input_dim=2, kernel_initializer='normal',
activation='relu'))
    model.add(Dense(10, kernel_initializer='normal', activation='relu'))
    model.add(Dense(2, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


# fix random seed for reproducibility
seed = 0
numpy.random.seed(seed)

# Train the neural net
estimator = KerasRegressor(build_fn=make_neural_net, epochs=5000,
batch_size=5, verbose=0)
estimator.fit(X, Y);

# Make some test predictions
print("");
print("Target: [0, 0]")
prediction = estimator.predict(numpy.array([[0, 0]]));
print("Predicted: " + numpy.array_str(prediction))

print("");
print("Target: [3, 2]")
prediction = estimator.predict(numpy.array([[1, 2]]));
print("Predicted: " + numpy.array_str(prediction))

print("");
print("Target: [2, 0.75]")
prediction = estimator.predict(numpy.array([[1.5, 0.5]]));
print("Predicted: " + numpy.array_str(prediction))
