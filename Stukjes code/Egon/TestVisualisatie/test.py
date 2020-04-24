from keras.models import Sequential
from keras.layers import Dense
from ann_visualizer.visualize import ann_viz

network = Sequential()

network.add(Dense(units=6,
                  activation='relu',
                  kernel_initializer='uniform',
                  input_dim=11))

network.add(Dense(units=6,
                  activation='relu',
                  kernel_initializer='uniform'))

network.add(Dense(units=1,
                  activation='sigmoid',
                  kernel_initializer='uniform'))

ann_viz(network)