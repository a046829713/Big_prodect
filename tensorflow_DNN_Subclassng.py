# 採用 Subclassing
from data_to_tensorflow import get_clean_Xy , stock_all_train_data
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

# 步驟一 先將資料整理 #3006 4919
X,y = get_clean_Xy(stock_all_train_data(str(2363)))

# 先做完預處理
scaler = StandardScaler()
X = scaler.fit_transform(X.to_numpy())

import numpy as np


# 先將基本model 建立起來
# 開始建立DNN model

from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import tensorflow as tf

tf.compat.v1.reset_default_graph()

# 讀取資料近來
class data_Loader():
    def __init__(self):
        #固定訓練參數 
        # X_train, X_test, y_train, y_test(X 題目)(y 答案) 
        X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.25, random_state=42)
        # 訓練 題                         
        self.train_data = (X_train.astype(np.float32))
        # 測試 題
        self.test_data = (X_test.astype(np.float32))
        # 訓練 答
        self.train_label = (y_train.astype(np.float32))
        # 測試 答
        self.test_label = (y_test.astype(np.float32))
        # 紀錄訓練資料有幾筆 測試資料有幾筆
        self.num_train_data, self.num_test_data = self.train_data.shape[0], self.test_data.shape[0]
        
    def get_batch(self, batch_size):

        index = np.random.randint(0, self.num_train_data, batch_size)
        return self.train_data[index, :], self.train_label[index]


class MLP(tf.keras.Model):
    # 建構器
    def __init__(self):
        super().__init__()
        self.layer_1 = tf.keras.layers.Dense(units=256, activation=tf.nn.relu)
        self.layer_2 = tf.keras.layers.Dense(units=128, activation=tf.nn.relu)
        self.layer_3 = tf.keras.layers.Dense(units=64, activation=tf.nn.relu)
        self.layer_4 = tf.keras.layers.Dense(units=3)
    def call(self, inputs):
        x = self.layer_1(inputs)
        x = self.layer_2(x)
        x = self.layer_3(x)
        x = self.layer_4(x)
        output = tf.nn.softmax(x)
        return output

num_epochs = 30 # 總共訓練10次
batch_size = 10 # 每次30張
learning_rate = 0.001 # 學習率0.001

data_loader = data_Loader()
model = MLP()

# 選擇優化器
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
#optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
# optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)

# 訓練資料/每次50張 *總共訓練幾次
num_batches = int(data_loader.num_train_data // batch_size * num_epochs)

# 迴圈 總訓練次數
for batch_index in range(num_batches):
    # 注意這邊已經更改 X y
    X, y = data_loader.get_batch(batch_size)
    with tf.GradientTape() as tape:
        y_pred = model(X)
        # 計算損失函數 # sparse 因為y沒有one hot 編碼
        loss = tf.keras.losses.sparse_categorical_crossentropy(y_true=y, y_pred=y_pred)
        loss = tf.reduce_mean(loss)
        # batch_index(第幾次)
        print("batch %d: loss %f" % (batch_index, loss.numpy()))
    # 做篇微分(參考第三章)
    grads = tape.gradient(loss, model.variables)
    # 優化器調整參數
    optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))


# 驗證準確度
sparse_categorical_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()
# 取得資料次數
num_batches = int(data_loader.num_test_data // batch_size)
# 
for batch_index in range(num_batches):
    start_index, end_index = batch_index * batch_size, (batch_index + 1) * batch_size
    # 取得預測資料
    y_pred = model.predict(data_loader.test_data[start_index: end_index])
    # 將預測資料 放入取得準確度 (每次累加)
    sparse_categorical_accuracy.update_state(y_true=data_loader.test_label[start_index: end_index], y_pred=y_pred)
print("test accuracy: %f" % sparse_categorical_accuracy.result())
# 注意這邊是整體精準度 (reset_states 並不是放在迴圈之內)
sparse_categorical_accuracy.reset_states() 
        
        
        
    

