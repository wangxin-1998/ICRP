# author:高璆华
import os
import time
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

def create_floder(floder_path):
    if not os.path.exists(floder_path):
        os.makedirs(floder_path)
        os.chmod(floder_path,os.O_RDWR)

#判断是否上传图像
def detection_image(file):
    if file:
        return True
    return False

# 图像格式判断
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])
def allowed_file(filename):#后缀
    return filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#修改文件名(唯一文件名）
def change_filename_with_timestamp_uuid(filename):   #uuid:通用唯一标识符
    fileinfo = os.path.splitext(filename)#将文件名划分为包含名字和后缀的元组（替换前部分）
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + \
                str(uuid.uuid4().hex) + fileinfo[-1]
                # 获取当前时间保留“年月日时分秒”#hex表转化为16进制+文件后缀
    return filename

def get_time():
    time_str = time.strftime("%Y{}%m{}%d{}")
    return time_str.format("年","月","日")

#模型

import tensorflow as tf
import  numpy as np
import PIL.Image as Image
from skimage import io, transform
from tensorflow.python.platform import gfile

def recognize(jpg_path, pb_file_path):
    with tf.Graph().as_default():
        output_graph_def = tf.GraphDef()

        with open(pb_file_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(output_graph_def, name="")#导入图

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)#初始化过程
            #输入tensor
            input_x = sess.graph.get_tensor_by_name("Placeholder:0")
           # print(input_x)
            #输出tensor
            out_softmax = sess.graph.get_tensor_by_name("ArgMax:0")
            print(out_softmax)
            out_label = sess.graph.get_tensor_by_name("ArgMax:0")
            print ("out_label:",out_label)
            #out_softmax = sess.graph.get_tensor_by_name("layer11-fc3:0")
            img = io.imread(jpg_path)
            img = transform.resize(img, (100, 100,3))
            #img_out_softmax = sess.run(out_softmax, feed_dict={input_x:np.reshape(img, [-1, 224, 224, 3])})
            img_out_softmax = sess.run(out_softmax,feed_dict={input_x:np.reshape(img,[-1,100,100,3])})
            print("img_out_softmax:",type(img_out_softmax))
            prediction_labels = np.argmax(img_out_softmax)
            print("img_out_softmax:", prediction_labels)
    return prediction_labels

if __name__=="__main__":
    print(get_time())