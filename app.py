'''
author:许诗瑶
'''
import os

import pymsgbox as pymsgbox
from flask import Flask, request, render_template, redirect
from wordcloud import WordCloud
import pymysql
app = Flask(__name__)

# 生成词云 author:许诗瑶
def getWL():
    # 连接数据库获取数据
    conn = pymysql.connect(host='icrpmysql.mysql.database.chinacloudapi.cn', user='icrpmysql@icrpmysql',
                           password='IC123rp456', db='ICRP', charset='utf8')
    cur = conn.cursor()
    # 生成词云
    sql = "select 病名,访问次数 from disease_infomation"
    cur.execute(sql)
    wlist = cur.fetchall()
    # 将病名及频次整理为dic格式
    name = [col[0] for col in wlist]
    value = [col[1] for col in wlist]
    wlist = dict(zip(name, value))
    # print(wlist)

    path = os.path.dirname(os.path.realpath(__file__))
    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置字体
        # ？？？ 为什么./不能代替为本工程路径 ？？？
        font_path=path+"/static/simhei.ttf",
        # font_path="./static/simhei.ttf",
        # 设置图像大小
        width=300,
        height=900
    )

    wc.generate_from_frequencies(wlist) # 根据词频生成词云
    #wc.generate(wlist)  # 生成词云
    # ？？？ 为什么./不能代替为本工程路径 ？？？
    wc.to_file(path+'/static/pics/wc.png')  # 把词云保存下
    # wc.to_file('/static/pics/wc.png')  # 把词云保存下

    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/browseInfo')
def browseInfo():
    # 连接数据库获取数据
    conn = pymysql.connect(host='icrpmysql.mysql.database.chinacloudapi.cn', user='icrpmysql@icrpmysql',
                           password='IC123rp456', db='ICRP', charset='utf8')
    cur = conn.cursor()
    # 执行sql语句获取数据
    sql = "select * from disease_infomation order by 访问次数 desc"
    cur.execute(sql)
    u = cur.fetchall()

    # 关闭数据库连接
    conn.close()

    # 获取搜索框内容，初始为空
    searchValue = str(request.args.get("searchValue"))
    if(searchValue=="None"):
        searchValue = ""

    # 数据库数据u传递  搜索值默认为空
    return render_template('browseInfo.html',u=u,sValue=searchValue)

# 删除信息条目
@app.route('/deleteItem',methods=['GET','POST'])
def deleteItem():
    # 连接数据库获取数据
    conn = pymysql.connect(host='icrpmysql.mysql.database.chinacloudapi.cn', user='icrpmysql@icrpmysql',
                           password='IC123rp456', db='ICRP', charset='utf8')
    cur = conn.cursor()
    if (request.method == 'POST'):
        # 执行sql语句获取数据
        no = request.form.get("no")
        sql = "DELETE FROM `icrp`.`disease_infomation` WHERE (`编号` = '"+ no +"')"
        # print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(request.referrer)
        # return render_template('browseInfo.html')


@app.route('/detail_info/<a>')
def detail_info(a):
    #conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='ICRP', charset='utf8')
    conn = pymysql.connect(host='icrpmysql.mysql.database.chinacloudapi.cn', user='icrpmysql@icrpmysql', password='IC123rp456', db='ICRP', charset='utf8')
    cur = conn.cursor()
    a=str(a)
    print(a)
    sql = "select * from disease_infomation where 病名='%s'" % a
    #print(sql)
    cur.execute(sql)
    u = cur.fetchall()
    print(u[0][1])
    conn.close()
    return render_template('detail_info.html',u=u)

if __name__ == '__main__':
    app.run()


