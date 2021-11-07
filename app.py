from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates/')

import yfinance as yf
from datetime import date, timedelta
today = date.today()
start = today - timedelta(days=90)
today = today.strftime('%Y-%m-%d')
start = start.strftime('%Y-%m-%d')

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
model_1 = load_model('Model/rnn_close_1_300.h5')
model_2 = load_model('Model/rnn_close_2_300.h5')
model_3 = load_model('Model/rnn_close_3_300.h5')
model_4 = load_model('Model/rnn_close_4_300.h5')
model_5 = load_model('Model/rnn_close_5_300.h5')
models = [model_1, model_2, model_3, model_4, model_5]

code = '2330'


@app.route('/yougood/home.html')
def home():
    return render_template('home.html')

@app.route('/yougood/index.html')
def index():
    labels, area_data1, area_data2, bar_labels, bar_data = get_twii_data()
    table_column, table_data = get_table_data()
    return render_template('index.html', code='TWII', table_column=table_column, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_labels=bar_labels, bar_data=bar_data)

@app.route('/yougood/index-code.html', methods=['POST'])
def index_post():
    global code
    code = request.form.get('code')
    labels, area_data1, area_data2, bar_labels, bar_data = get_data(code)
    table_column, table_data = get_table_data()
    return render_template('index-code.html', code=code, table_column=table_column, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_labels=bar_labels, bar_data=bar_data)

@app.route('/yougood/<code_req>')
def index_code(code_req):
    global code
    code = code_req
    labels, area_data1, area_data2, bar_labels, bar_data = get_data(code)
    table_column, table_data = get_table_data()
    return render_template('index-code.html', code=code, table_column=table_column, table_data=table_data, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_labels=bar_labels, bar_data=bar_data)

@app.route('/yougood/charts.html')
def charts():
    labels, area_data1, area_data2, bar_labels, bar_data = get_data(code)
    pie_labels, pie_data = get_pie_data(code)
    return render_template('charts.html', code=code, labels=labels, area_data1=area_data1, area_data2=area_data2, bar_labels=bar_labels, bar_data=bar_data, pie_labels=pie_labels, pie_data=pie_data)
    
@app.route('/yougood/tables.html')
def tables():
    table_column, table_data = get_table_data()
    return render_template('tables.html', table_column=table_column, table_data=table_data)

@app.route('/yougood/members.html')
def members():
    return render_template('members.html')

def get_twii_data():
    df = yf.Ticker('^TWII').history(start=start, end=today)
    for day in [1,2,3,4,5,6]:
        df[f'{day}days_before_close'] = df['Close'].shift(periods=day+1)
    
    df = df.iloc[10:]
    df_model = df[['Open', 'High', 'Low', 'Close', f'1days_before_close', f'2days_before_close', f'3days_before_close', f'4days_before_close', f'5days_before_close', f'6days_before_close']]
    data_all = pd.DataFrame(df_model.values.flatten())
    data_all = np.array(data_all).astype(float)
    scaler = MinMaxScaler()
    data_all = scaler.fit_transform(data_all)
    data = []
    sequence_length = len(df_model.columns) # Feature Number
    for i in range(int(len(data_all) / sequence_length)):
        data.append(data_all[i*sequence_length:(i+1)*sequence_length])
    test_x = np.array(data).astype('float64')
    test_x_last = np.array([test_x[-1]])
    predict = models[0].predict(test_x)
    predict = np.reshape(predict, (predict.size, ))
    predict = scaler.inverse_transform([[i] for i in predict])
    area_data2 = predict
    labels = df.index.astype(str).str[:10].tolist()
    area_data1 = df['Close'].values.tolist()
    for day in [1,2,3,4,5]:
        labels.append(f'{day} Days Predict')
    for day in [1,2,3,4]:
        predict = models[day].predict(test_x_last)
        predict = np.reshape(predict, (predict.size, ))
        predict = scaler.inverse_transform([[i] for i in predict])
        area_data2 = np.append(area_data2, predict)
    
    area_data2 = np.around(area_data2.flatten(), 1).tolist()
    labels.pop(0)
    area_data1.pop(0)

    df = pd.read_csv('Stock_Profile.csv', index_col=0)
    df = df[['Name', 'News_size']]
    df = df.sort_values(by=['News_size'], ascending=False)[:10]
    bar_labels = df['Name'].values.tolist()
    bar_data = df['News_size'].values.tolist()
    labels = str(labels).replace("'", "").replace("[", "").replace("]", "")
    area_data1 = str(area_data1).replace("[", "").replace("]", "")
    area_data2 = str(area_data2).replace("[", "").replace("]", "")
    bar_labels = str(bar_labels).replace("'", "").replace("[", "").replace("]", "")
    bar_data = str(bar_data).replace("[", "").replace("]", "")
    
    return labels, area_data1, area_data2, bar_labels, bar_data

def get_data(code):
    # get realtime data
    df = yf.Ticker(str(code)+'.TW').history(start=start, end=today)
    if len(df) == 0:
        df = yf.Ticker(str(code)+'.TWO').history(start=start, end=today)
        if len(df) == 0:
            pass
    
    # feature
    for day in [1,2,3,4,5,6]:
        df[f'{day}days_before_close'] = df['Close'].shift(periods=day+1)
    
    df = df.iloc[10:]
    df_model = df[['Open', 'High', 'Low', 'Close', f'1days_before_close', f'2days_before_close', f'3days_before_close', f'4days_before_close', f'5days_before_close', f'6days_before_close']]
    data_all = pd.DataFrame(df_model.values.flatten())
    data_all = np.array(data_all).astype(float)
    scaler = MinMaxScaler()
    data_all = scaler.fit_transform(data_all)
    data = []
    sequence_length = len(df_model.columns) # Feature Number
    for i in range(int(len(data_all) / sequence_length)):
        data.append(data_all[i*sequence_length:(i+1)*sequence_length])
    test_x = np.array(data).astype('float64')
    test_x_last = np.array([test_x[-1]])
    predict = models[0].predict(test_x)
    predict = np.reshape(predict, (predict.size, ))
    predict = scaler.inverse_transform([[i] for i in predict])
    area_data2 = predict
    labels = df.index.astype(str).str[:10].tolist()
    bar_labels = labels[:-5]
    area_data1 = df['Close'].values.tolist()
    for day in [1,2,3,4,5]:
        labels.append(f'{day} Days Predict')
    for day in [1,2,3,4]:
        predict = models[day].predict(test_x_last)
        predict = np.reshape(predict, (predict.size, ))
        predict = scaler.inverse_transform([[i] for i in predict])
        area_data2 = np.append(area_data2, predict)
    
    area_data2 = np.around(area_data2.flatten(), 1).tolist()
    labels.pop(0)
    area_data1.pop(0)

    bar_data = df['Volume'].values.tolist()
    labels = str(labels).replace("'", "").replace("[", "").replace("]", "")
    area_data1 = str(area_data1).replace("[", "").replace("]", "")
    area_data2 = str(area_data2).replace("[", "").replace("]", "")
    bar_labels = str(bar_labels).replace("'", "").replace("[", "").replace("]", "")
    bar_data = str(bar_data).replace("[", "").replace("]", "")
    
    return labels, area_data1, area_data2, bar_labels, bar_data

def get_table_data():
    df = pd.read_csv('Stock_Profile.csv')
    df = df.iloc[:50, :5]
    table_column = df.columns.values.tolist()
    table_data = df.values.tolist()
    return table_column, table_data

def get_pie_data(code):
    df = pd.read_csv('Stock_Profile_Sentcount.csv', index_col=0)
    df = df.iloc[df.index == code, 7:]
    pie_labels = df.columns.values.tolist()
    pie_data = df.values.flatten().tolist()
    pie_labels = str(pie_labels).replace("'", "").replace("[", "").replace("]", "")
    pie_data = str(pie_data).replace("[", "").replace("]", "")
    return pie_labels, pie_data

if __name__=="__main__":
    app.run(debug=True)