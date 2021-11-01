from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import os

app = Flask(__name__)

@app.route('/code', methods=['POST'])  # 用右上方搜尋連結stock code
def get_post():
   
    # import os
    global code
    code = request.form.get('code')

    filepath = "/data/{code}.csv"
    directory = os.path.dirname(os.path.abspath(__file__))
    filepath = f"{directory}/data/{code}.csv"
    # temp = pd.read_csv(f"{directory}/data/{code}.csv")

    if os.path.isfile(filepath):    
        table_data = get_table_data()
        labels = get_labels()
        area_data1, area_data2 = get_area_data(code)
        area_volume = get_volume_data(code)
        bar_data, stock_name = get_bar_data(code)
        pie_labels, pie_data = get_pie_data(code)
        return render_template('charts.html', code=code, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, pie_labels=pie_labels, pie_data=pie_data, area_volume = area_volume)
    else:
        return render_template('404.html')
  
# 本次測試放大盤資料在首頁
@app.route('/')
def route():
    # # global code
    # code = '0050'
    # table_data = get_table_data()
    # labels = get_labels()
    # tw_data = get_tw_data()
    # area_data1, area_data2 = get_area_data(code)
    # bar_data, stock_name = get_bar_data(code)
    # pie_labels, pie_data = get_pie_data(code)
    # return render_template('index.html',  table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, stock_name=stock_name)
    # return render_template('index.html', table_data=table_data, labels=labels, tw_data=tw_data, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, stock_name=stock_name)
    return ("hello")
@app.route('/base.html')
def route_base():
    global code
    code = '0050'
    table_data = get_table_data()
    labels = get_labels()
    # tw_data = get_tw_data()
    # stock_name = stock_name()
    area_data1, area_data2 = get_area_data(code)
    bar_data, stock_name = get_bar_data(code)
    pie_labels, pie_data = get_pie_data(code)
    return render_template('base.html',  table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, stock_name=stock_name)

@app.route('/index.html')
def index2():
    global code
    code = '0050'
    table_data = get_table_data()
    labels = get_labels()
    tw_data = get_tw_data()
    area_data1, area_data2 = get_area_data(code)
    bar_data, stock_name = get_bar_data(code)
    pie_labels, pie_data = get_pie_data(code)
    return render_template('index.html',table_data=table_data, labels=labels, tw_data=tw_data, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, stock_name=stock_name)

@app.route('/<code_req>') # 直接用下方的stock table連結
def index_code(code_req):
    global code
    code = code_req
    table_data = get_table_data()
    labels = get_labels()
    area_data1, area_data2 = get_area_data(code)
    area_volume = get_volume_data(code)
    bar_data, stock_name = get_bar_data(code)
    pie_labels, pie_data = get_pie_data(code)
    return render_template('charts.html', code=code, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, pie_labels=pie_labels, pie_data=pie_data, area_volume=area_volume)

@app.route('/charts.html')
def charts():
    global code
    code = '0050'
    table_data = get_table_data()
    labels = get_labels()
    area_data1, area_data2 = get_area_data(code)
    area_volume = get_volume_data(code)
    bar_data,stock_name = get_bar_data(code)
    pie_labels, pie_data = get_pie_data(code)
    return render_template('charts.html', code=code, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data, pie_labels=pie_labels, pie_data=pie_data, area_volume=area_volume)

@app.route('/tables.html')
def tables():
    code = '2317'
    table_data = get_table_data()
    labels = get_labels()
    area_data1, area_data2 = get_area_data(code)
    bar_data = get_bar_data(code)
    return render_template('tables.html', table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_data=bar_data)

@app.route('/layout-sidenav-light.html')
def layout_sidenav_light():
    return render_template('layout-sidenav-light.html')

@app.route('/layout-static.html')
def layout_static():
    return render_template('layout-static.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/password.html')
def password():
    return render_template('password.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/401.html')
def E401():
    return render_template('401.html')

@app.route('/404.html')
def E404():
    return render_template('404.html')

@app.route('/500.html')
def E500():
    return render_template('500.html')

def get_table_data():
    table_data = [[145, "0050", 100.1, 100.2],
                  [1203, "2330", 600.0, 601.0],
                  [1025, "2317", 120.2, 117.9]]
    return table_data

# 日期的部分未完成
def get_labels():
    # import  os
    # import pandas as pd


    # directory = os.path.dirname(os.path.abspath(__file__))
    # temp = pd.read_csv(f"{directory}/data/{code}.csv")
    # temp['date'] = temp['date'].dt.strftime('%m/%d/%Y')
    # temp1 = str(temp['date'].astype(str), format='%m/%d/%Y')
    
    # labels = ""
    # labels = labels+str(temp["date"].to_list())[1:-1]  
   
    # 綱綱老師測試
    # directory = os.path.dirname(os.path.abspath(__file__))
    # temp = pd.read_csv(f"{directory}/data/0050.csv")
    # labels = str(temp['date'].to_list()).replace("'","").replace("[","").replace("]","")
    # 綱綱老師測試

    labels = "2021-02-01, 2021-02-02, 2021-02-03, 2021-02-04, 2021-02-05, 2021-02-06, 2021-02-07, 2021-02-08, 2021-02-09, 2021-02-10, 2021-02-11, 2021-02-12, 2021-02-13, 2021-02-14, 2021-02-15, 2021-02-16, 2021-02-17, 2021-02-18, 2021-02-19, 2021-02-20"
    return labels


# # 測試
def get_area_data(code):  
    import os
    import pandas as pd

    directory = os.path.dirname(os.path.abspath(__file__))
    temp = pd.read_csv(f"{directory}/data/{code}.csv")
    area_data1 = ""
    # temp1 = temp['Open']
    area_data1 = area_data1+str(temp['open'].to_list())[1:-1]

    area_data2 = ""
    area_data2 = area_data2+str(temp['close'].to_list())[1:-1]
    
    return area_data1, area_data2

# 2021/10/27 新增get_volume_data，將volume成交量除以1000，單位: 張
def get_volume_data(code):  
    # import os
    # import pandas as pd

    directory = os.path.dirname(os.path.abspath(__file__))
    temp = pd.read_csv(f"{directory}/data/{code}.csv")
    # area_volume = ""
    temp1 = temp['volume']/1000  
    area_volume = str(temp1.to_list())[1:-1]
    # area_volume = "17090, 18770, 17789, 17298, 16097, 16739, 16823, 16028, 16923, 16833, 17234, 18374, 17305, 17434, 17509"
    return area_volume

# 大盤指數
def get_tw_data():
    tw_data = "17090, 18770, 17789, 17298, 16097, 16739, 16823, 16028, 16923, 16833, 17234, 18374, 17305, 17434, 17509"
    return tw_data

# 新聞討論度的股票
def get_bar_data(code):
    # bar_data = "300000, 512478, 374856, 276843, 184739, 437284, 346837, 512478, 374856, 276843, 184739, 437284, 512478, 374856, 276843"
    # stock_name = "2330, 2317, 2454, 3008, 3711, 3481, 2344, 2409, 2308, 2881, 2882"
    stock_name = "台積電, 鴻海, 聯發科, 大立光, 日月光, 群創, 華邦電, 友達, 台達電, 富邦金" 
    bar_data = "165, 144, 141, 125, 118, 113, 112, 111, 107, 101"
    return stock_name, bar_data

def get_pie_data(code):
    pie_labels = "Blue, Red, Yellow, Green"
    pie_data = "12.21, 15.58, 11.25, 8.32"
    return pie_labels, pie_data


if __name__=="__main__": 
    app.run(debug=True) 