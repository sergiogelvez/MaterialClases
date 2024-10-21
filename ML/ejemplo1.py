import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import numpy as np

print("TensorFlow version:", tf.__version__)

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
print(predictions)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_algo = loss_fn(y_train[:1], predictions).numpy()
print(loss_algo)

imtest2 = []

img_pil = Image.open("./ML/siete.jpg")
img_28x28 = np.array(img_pil.resize((28, 28)))
#img_array = (img_28x28.flatten())
#img_array  = img_array.reshape(-1,1).T



plt.imshow(img_28x28, cmap=plt.cm.binary)
plt.show()

img_28x28 = img_28x28 / 255.0

print(img_28x28)
print(x_train[0])
print(img_28x28.shape)
print(x_train[0].shape)

imtest2.append(img_28x28)

img_pil = Image.open("./ML/ocho.jpg")
img_28x28 = np.array(img_pil.resize((28, 28)))

plt.imshow(img_28x28, cmap=plt.cm.binary)
plt.show()

img_28x28 = img_28x28 / 255.0

imtest2.append(img_28x28)


img_pil = Image.open("./ML/nueve.jpg")
img_28x28 = np.array(img_pil.resize((28, 28), Image.LANCZOS))

plt.imshow(img_28x28, cmap=plt.cm.binary)
plt.show()

img_28x28 = img_28x28 / 255.0

imtest2.append(img_28x28)


img_pil = Image.open("./ML/uno.jpg")
img_28x28 = np.array(img_pil.resize((28, 28), Image.LANCZOS))

plt.imshow(img_28x28, cmap=plt.cm.binary)
plt.show()

img_28x28 = img_28x28 / 255.0

imtest2.append(img_28x28)


test2 = np.array(imtest2)

print(test2.shape)

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

salidas = probability_model(x_test[:5])

print(salidas)

'''for i in range(len(salidas)):
  plt.imshow(x_test[i], cmap=plt.cm.binary)
  plt.show()
  print(y_test[i])
 plt.imshow(x_test[1], cmap=plt.cm.binary)
plt.show()
plt.imshow(x_test[2], cmap=plt.cm.binary)
plt.show()
plt.imshow(x_test[3], cmap=plt.cm.binary)
plt.show()
plt.imshow(x_test[4], cmap=plt.cm.binary)
plt.show()
'''



imr = probability_model(test2)

print(imr)
