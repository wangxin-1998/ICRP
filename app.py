# author:高璆华
# coding=utf-8
from flask import Flask,flash,render_template,request,redirect, url_for, make_response, jsonify
from templates.utils import change_filename_with_timestamp_uuid, detection_image,allowed_file
from datetime import timedelta, datetime
import os
import templates.utils as utils
import glob
import time
#...
# from Flask_moment import Moment
from templates import utils
app = Flask(__name__)
#moment = Moment(app)
app.secret_key="1234"

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

#访问网站主页面（hmoepage)
@app.route("/")
def homwpage():
    time = datetime.now().strftime("%y%m%d")
    mm = datetime.now().strftime("%m")
    dd = datetime.now().strftime("%d")
    return render_template('homepage.html',time=time)

@app.route("/time")
def get_time():
    return utils.get_time()

#访问网站病虫害识别与诊断页面（catchrp)
@app.route('/Catchrp.html')
def Catchrp():
    return render_template("catchrp.html")

@app.route('/up_photo',methods=['POST', 'GET'])
def up_photo():
    if request.method == 'POST':
        #创建图像文件
        f = request.files['file']
        if detection_image(f.filename):#是否输入
            if not allowed_file(f.filename): #判断图像类型
                flash("请输入'png'或'jpg'图像")
                return render_template("error.html")
                #return render_template("error.html",str="请输入'png'、'jpg'或'bmp'图像")
            basepath = os.path.dirname(__file__)
            files = change_filename_with_timestamp_uuid(f.filename)
            upload_path = os.path.join(basepath, 'static/images',files)
            #upload_path = os.path.join(basepath, 'static/images/',username+'/'+files)
            f.save(upload_path)
            # f.save(os.path.join(basepath,'static/images',secure_filename(f.filename)))
            # return render_template('RP_info.html', file = '../static/images/' + files)
            pb_file_path = os.path.join(basepath, 'static/saved_pb','tensorflow.pb')
            return render_template('RP_info.html',info = utils.recognize(upload_path,pb_file_path),file=upload_path)
            #建立模型和用户
            # result = moxing(upload_path)
            # return render_template('new.html', file='../static/images/'+username+'/'+files,result)
    return render_template('catchrp.html')

if __name__ == '__main__':
    app.run()
