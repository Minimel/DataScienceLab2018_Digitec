import sys
import os.path
# To import from sibling directory ../utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from tensorflow import keras
import tensorflow as tf


def create_model(number_filters, length_state, h1=1048, h2=512): 
        # loss: 1.3718 - acc: 0.6029 - val_loss: 1.5231 - val_acc: 0.6466
        # epoch 28
        # best h1256_h2128_ts1543838439
        # Define architecture of the model
        main_input = keras.layers.Input((length_state,), dtype='float32', name='main_input')
        mask_input = keras.layers.Input(shape=(number_filters,), dtype='float32', name='mask_input')
        x = keras.layers.Dense(2048, activation=tf.nn.relu, input_shape=(length_state,))(main_input)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(1024, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.3)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.3)(x)
        x = keras.layers.Dense(256, activation=tf.nn.relu)(x)
        x = keras.layers.Dropout(rate=0.3)(x)
        probas =keras.layers.Dense(number_filters, activation=tf.nn.softmax)(x)
        out = keras.layers.Lambda(lambda x: x[0]*x[1])([probas, mask_input]) #have to apply the mask AFTER softmax
        # Wrap in Keras model
        model =  keras.Model(inputs=[main_input, mask_input], outputs=out)
        # Compile the model
        model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        return model


""" MODEL TESTED
def create_model_donright2(number_filters, length_state, h1=256, h2=128): 
        # loss: 1.1307 - acc: 0.6708 - val_loss: 1.5321 - val_acc: 0.6319 - epoch 18
        # Define architecture of the model
        main_input = keras.layers.Input((length_state,), dtype='float32', name='main_input')
        mask_input = keras.layers.Input(shape=(number_filters,), dtype='float32', name='mask_input')
        x = keras.layers.Dense(5096, activation=tf.nn.relu, input_shape=(length_state,))(main_input)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(1024, activation=tf.nn.relu)(x)
        probas = keras.layers.Dense(number_filters, activation=tf.nn.softmax)(x)
        out = keras.layers.Lambda(lambda x: x[0]*x[1])([probas, mask_input]) #have to apply the mask AFTER softmax
        # Wrap in Keras model
        model =  keras.Model(inputs=[main_input, mask_input], outputs=out)
        # Compile the model
        model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        return model


def create_model_downright(number_filters, length_state, h1=1048, h2=512): 
         # very BAD loss: loss: 1.7884 - acc: 0.5075 - val_loss: 1.6992 - val_acc: 0.5840 epoch 57
        # down right
        main_input = keras.layers.Input((length_state,), dtype='float32', name='main_input')
        mask_input = keras.layers.Input(shape=(number_filters,), dtype='float32', name='mask_input')
        x = keras.layers.Dense(h1, activation=tf.nn.relu, input_shape=(length_state,))(main_input)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(h1, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(h1, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(h2, activation=tf.nn.relu)(x)
        x = keras.layers.Dropout(rate=0.5)(x)
        probas =keras.layers.Dense(number_filters, activation=tf.nn.softmax)(x)
        out = keras.layers.Lambda(lambda x: x[0]*x[1])([probas, mask_input]) #have to apply the mask AFTER softmax
        # Wrap in Keras model
        model =  keras.Model(inputs=[main_input, mask_input], outputs=out)
        # Compile the model
        model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        return model


def create_model_downleft(number_filters, length_state, h1=1048, h2=512):
        # Define architecture of the model
        # loss: 1.3546 - acc: 0.6223 - val_loss: 1.5417 - val_acc: 0.6146
        main_input = keras.layers.Input((length_state,), dtype='float32', name='main_input')
        mask_input = keras.layers.Input(shape=(number_filters,), dtype='float32', name='mask_input')
        x = keras.layers.Dense(2048, activation=tf.nn.relu, input_shape=(length_state,))(main_input)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(2048, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.5)(x)
        x = keras.layers.Dense(1024, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.2)(x)
        x = keras.layers.Dense(256, activation=tf.nn.relu)(x)
        probas = keras.layers.Dense(number_filters, activation=tf.nn.softmax)(x)
        out = keras.layers.Lambda(lambda x: x[0]*x[1])([probas, mask_input]) #have to apply the mask AFTER softmax
        # Wrap in Keras model
        model =  keras.Model(inputs=[main_input, mask_input], outputs=out)
        # Compile the model
        model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        return model

def create_model_big_bad(number_filters, length_state, h1=1048, h2=512):
        # loss: 1.7063 - acc: 0.5518 - val_loss: 1.7624 - val_acc: 0.5803
        # top left
        main_input = keras.layers.Input((length_state,), dtype='float32', name='main_input')
        mask_input = keras.layers.Input(shape=(number_filters,), dtype='float32', name='mask_input')
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(main_input)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(length_state,))(x)
        x = keras.layers.Dropout(rate=0.4)(x)
        x = keras.layers.Dense(256, activation=tf.nn.relu)(x)
        probas = keras.layers.Dense(number_filters, activation=tf.nn.softmax)(x)
        out = keras.layers.Lambda(lambda x: x[0]*x[1])([probas, mask_input]) #have to apply the mask AFTER softmax
        # Wrap in Keras model
        model =  keras.Model(inputs=[main_input, mask_input], outputs=out)
        # Compile the model
        model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
        return model
"""