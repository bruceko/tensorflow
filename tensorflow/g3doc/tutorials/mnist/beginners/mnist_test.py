# -*- coding: utf-8 -*-

import input_data
import tensorflow as tf

# MNIST データセットのダウンロードと読み込み
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# 重みと閾値を表す変数を用意する (初期値はゼロとする)
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

# 訓練時に特徴ベクトルを入れるための変数
x = tf.placeholder("float", [None, 784])

# Softmax 関数を定義
y = tf.nn.softmax(tf.matmul(x, W) + b)

# 訓練時に真のラベルの値を入れるための変数
y_ = tf.placeholder("float", [None,10])

# 損失関数を cross entropy で定義
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

# 学習手法を定義 (ステップサイズ 0.01 の勾配法で cross entropy 最小化を目標とする)
train_step = tf.train.GradientDescentOptimizer(0.005).minimize(cross_entropy)

# セッションを準備
sess = tf.Session()

# 変数の初期化処理
init = tf.initialize_all_variables()
sess.run(init)

for i in range(1000):
    # mini batch で使用する分のデータ
    batch_xs, batch_ys = mnist.train.next_batch(100)
    # 勾配を用いた更新を行う
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# 正答率を返す関数を定義
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# 結果を眺める
print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
