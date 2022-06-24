'''Softmax-Classifier for CIFAR-10'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import time
import RavenPiDataHandler

beginTime = time.time()

# Parameter definitions
batch_size = 100
learning_rate = 0.005
max_steps = 1000

# Uncommenting this line removes randomness
# You'll get exactly the same result on each run
# np.random.seed(1)

# Prepare data
data_sets = RavenPiDataHandler.load_data()

# -----------------------------------------------------------------------------
# Prepare the TensorFlow graph
# (We're only defining the graph here, no actual calculations taking place)
# -----------------------------------------------------------------------------

# Define input placeholders
images_placeholder = tf.keras.Input(shape=[None, 3072], dtype=tf.dtypes.float32)
labels_placeholder = tf.keras.Input(shape=[None], dtype=tf.dtypes.int64)

# Define variables (these are the values we want to optimize)
weights = tf.Variable(tf.zeros([3072, 10]))
biases = tf.Variable(tf.zeros([10]))

# Define the classifier's result
logits = tf.matmul(images_placeholder, weights) + biases

# Define the loss function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels_placeholder))

# Define the training operation
train_step = tf.optimizers.SGD(learning_rate=learning_rate, name='SGD')

# Operation comparing prediction with true label
correct_prediction = tf.equal(tf.argmax(logits, 1), labels_placeholder)

# Operation calculating the accuracy of our predictions
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# -----------------------------------------------------------------------------
# Run the TensorFlow graph
# -----------------------------------------------------------------------------

#with tf.Session() as sess:
  # Initialize variables
  #sess.run(tf.global_variables_initializer())

  # Repeat max_steps times
for i in range(max_steps):

    # Generate input data batch
    indices = np.random.choice(data_sets['images_train'].shape[0], batch_size)
    images_batch = data_sets['images_train'][indices]
    labels_batch = data_sets['labels_train'][indices]

    # Periodically print out the model's current accuracy
    if i % 100 == 0:
      train_accuracy = (accuracy, images_batch, labels_batch)
      print('Step {:5}: training accuracy {:}'.format(str(i), str(train_accuracy)))

    # Perform a single training step
    (train_step, images_batch, labels_batch)

# After finishing the training, evaluate on the test set
test_accuracy = (accuracy, data_sets['images_test'], data_sets['labels_test'])
print('Test accuracy {:}'.format(str(test_accuracy)))

endTime = time.time()
print('Total time: {:5.2f}s'.format(endTime - beginTime))