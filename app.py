'''
author:许诗瑶
'''

from flask import Flask,request,render_template
import numpy as np
from wordcloud import WordCloud
import pymysql
app = Flask(__name__)

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

    # 生成词云
    sql = "select 病名 from disease_infomation order by 访问次数 desc"
    cur.execute(sql)
    wl = cur.fetchall()
    # 将病名整理为字符串格式（空格分割）
    wl = " ".join(str(i) for i in wl)
    wl=wl.replace(',','')
    wl=wl.replace('(', '')
    wl=wl.replace(')', '')
    wl=wl.replace('\'', '')

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置字体
        font_path='./static/simhei.ttf',
        # 设置图像大小
        width=300,
        height=900
    )

    wc.generate(wl)  # 生成词云
    wc.to_file('static/pics/wc.png')  # 把词云保存下

    # 关闭数据库连接
    conn.close()

    # 数据库数据u传递
    return render_template('browseInfo.html',u=u)



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


