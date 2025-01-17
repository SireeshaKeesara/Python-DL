from keras.layers import Input, Dense
from keras.models import Model
import matplotlib.pyplot as plt
# this is the size of our encoded representations
encoding_dim = 32  # 784 floats -> compression of factor 24.5, assuming the input is 784 floats
# this is our input placeholder
input_img = Input(shape=(784,))
#hidden layer
hidden = Dense(64,activation='relu')(input_img)
# "encoded" is the encoded representation of the input
encoded = Dense(encoding_dim, activation='relu')(hidden)
hidden1 = Dense(32,activation='relu')(encoded)
# "decoded" is the lossy reconstruction of the input
decoded = Dense(784, activation='sigmoid')(hidden1)
# this model maps an input to its reconstruction
autoencoder = Model(input_img, decoded)
# this model maps an input to its encoded representation
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy',metrics=['accuracy'])
from keras.datasets import fashion_mnist
import numpy as np
(x_train, _), (x_test, _) = fashion_mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
n = 0.4
noise_train = x_train + n * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
noise_test = x_test + n * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)

history = autoencoder.fit(noise_train, x_train,
                epochs=10,
                batch_size=256,
                shuffle=True,
                validation_data=(noise_test, noise_test))

x_trans = x_test[11][np.newaxis]
x_noise_trans = noise_train[11][np.newaxis]
prediction = autoencoder.predict(x_trans)

plt.imshow(x_test[11].reshape(28, 28), cmap='gray')
plt.title("input")
plt.show()
plt.imshow(x_noise_trans.reshape(28, 28), cmap='gray')
plt.title("noisy input")
plt.show()
plt.imshow(prediction.reshape(28, 28), cmap='gray')
plt.title("reconstructed representation")
plt.show()

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

