from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import glob

import numpy as np
import tensorflow as tf
 

def model_fn(features, labels, mode, params):
  conv1 = tf.layers.conv2d(
    inputs=features['image'],
    filters=16,
    kernel_size=[3,3],
    padding="valid",
    activation=tf.nn.relu)

  pool1 = tf.layers.average_pooling2d(
    inputs=conv1,
    pool_size=[3,3],
    strides=3)

  conv2 = tf.layers.conv2d(
    inputs=pool1,
    filters=32,
    kernel_size=[3,3],
    padding="valid",
    activation=tf.nn.relu)

  pool2 = tf.layers.average_pooling2d(
    inputs=conv2,
    pool_size=[2,2],
    strides=2)

  flat1 = x = tf.reshape(pool2, [-1, 32*4*4])
  
  for i in range(10):
    x = tf.layers.dense(inputs=x, units=144)
  
  logits = tf.layers.dense(inputs=x, units=10)
  
  predictions = {
    "classes": tf.argmax(input=logits, axis=1),
    "probabilities": tf.nn.softmax(logits, name="softmax_tensor")}

  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions) 
   
  loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
  
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(
      loss=loss,
      global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  accuracy = tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])
  eval_metric_ops = {"accuracy": accuracy}

  return tf.estimator.EstimatorSpec(
    mode=mode,
    loss=loss, 
    eval_metric_ops=eval_metric_ops)
  

if __name__=="__main__":
  features = {
    "image": tf.placeholder(tf.float32, (None, 32, 32, 3))}
  labels = tf.placeholder(tf.int32, (None, 1))

  model_fn(features, labels, tf.estimator.ModeKeys.TRAIN, {})
