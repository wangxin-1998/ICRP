from flask import Flask,request,render_template
import pymysql
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail_info/<a>')
def detail_info(a):
    #conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='ICRP', charset='utf8')
    conn = pymysql.connect(host='icrpmysql.mysql.database.chinacloudapi.cn', user='icrpmysql@icrpmysql', password='IC123rp456', db='ICRP', charset='utf8')
    cur = conn.cursor()
    a=str(a)
    #print(a)
    sql = "select * from disease_infomation where 病名='%s'" % a
    #print(sql)
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('detail_info.html',u=u)
if __name__ == '__main__':
    app.run()


