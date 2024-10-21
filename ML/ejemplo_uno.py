import tensorflow as tf
import matplotlib.pyplot as plt


print("TensorFlow version:", tf.__version__)

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(x_train[0])
print(y_train[0])
plt.imshow(x_train[0], cmap=plt.cm.binary)
plt.show()


x_train, x_test = x_train / 255.0, x_test / 255.0

#print(x_train)
#print(x_test)

print(len(x_train))
print(x_train[0])

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
print(predictions)

print(tf.nn.softmax(predictions).numpy())

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_fn(y_train[:1], predictions).numpy()

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

print(probability_model(x_test[:5]))

plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.show()

plt.imshow(x_test[1], cmap=plt.cm.binary)
plt.show()

print(probability_model(x_train[:5]))

