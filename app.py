from flask import Flask ,render_template, url_for, request , jsonify
import joblib
scaler = joblib.load('scaler.lb')
kmeans =  joblib.load('kmeans_model.lb')

import mysql.connector # type: ignore

# Connect to the database
conn = mysql.connector.connect(
    host="13.61.15.17",
    user="Admin",
    password="Pass@12345",
    database="farmer"

)
if conn.is_connected():
    print("hm connect ho chuke ")
else:
    print("not conn")    

mysql_cursor = conn.cursor()
query = "INSERT INTO users (nitrogen, phosphorus, potassium, temperature, humidity, ph,rainfall) VALUES (%s, %s, %s, %s, %s, %s,%s)"
df = joblib.load('df.lb')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# POST
@app.route('/predict',methods = ['GET','POST'])
def predict():
    if request.method =='POST':
        n = int(request.form['nitrogen'])
        p = int(request.form['phosphorus'])
        k = int(request.form['potassium'])
        t = float(request.form['temperature'])
        h = float(request.form['humidity'])
        ph = float(request.form['ph'])
        r = float(request.form['rainfall'])




        user_data = [[n , p , k , t, h, ph , r ]]
        user_data1 = (n , p , k , t, h, ph , r )

        try:
    # Execute the query with user data
            mysql_cursor.execute(query, user_data1)
            print("row is instered :", mysql_cursor.rowcount)
    
    # Commit the transaction
            conn.commit()

        except mysql.connector.Error as error:
            print("Error:", error)

        finally:
    # Close the cursor and connection
            mysql_cursor.close()
            conn.close()
        trans_data = scaler.transform(user_data)
        prediction = kmeans.predict(trans_data)[0]
        print(prediction)
        dt = dict(df[df['cluster_12'] == prediction]['label'].value_counts())
        ls = []
        for k,v in dt.items():
            if v>=70:
                ls.append(k)
        return jsonify(ls)



if __name__ =="__main__":
    app.run(debug = True)