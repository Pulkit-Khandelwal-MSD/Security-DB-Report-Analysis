from flask import Flask, request, render_template
from flask_cors import cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc


#connection to database
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DHEERAJ;'
                      'Database=security_db;'
                      'Trusted_Connection=yes;');

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/datareport", methods = ["GET", "POST"])
@cross_origin()
def data():
    option = request.form['table']

    if option == 'option1':
        orgdata = pd.read_sql("SELECT * FROM organization", conn)
        result=orgdata.to_html()
        result="<center><h1>ORGANIZATION Table</h1>"+result+"</center>"

    elif option == 'option2':
        clientdata = pd.read_sql("SELECT * FROM clients", conn)
        result=clientdata.to_html()

        sns.barplot(x='client_id',y='score',data=clientdata)
        plt.xlabel('Client ID')
        plt.ylabel('Score')
        plt.title('Client ID\'s with their score')
        plt.savefig('static/client1.png')

        clientdata.plot.kde()
        plt.xlabel('Client Score')
        plt.title('Score data separation')
        plt.plot();
        plt.savefig('static/clientsscore.png')

        result="<center><h1>CLIENTS Table Report Analysis</h1>"+result
        result=append_html(result,['client1.png','clientsscore.png'])

    elif option == 'option3':
        empdata = pd.read_sql("SELECT * FROM employees", conn)
        result=empdata.to_html()

        sns.barplot(data=empdata,x='emp_name',y='age')
        plt.xlabel('Employee Name')
        plt.ylabel('Age')
        plt.title('Employees with their age')
        plt.savefig('static/emp_age.png')

        sns.barplot(data=empdata,x='emp_name',y='salary')
        plt.xlabel('Employee Name')
        plt.ylabel('Salary')
        plt.title('Employees with their salary')
        plt.savefig('static/emp_salary.png')

        result="<center><h1>EMPLOYEES Table Report Analysis</h1>"+result
        result=append_html(result,['emp_age.png','emp_salary.png'])


    elif option == 'option4':
        securitydata = pd.read_sql("SELECT * FROM security_services", conn)
        result=securitydata.to_html()

        sns.countplot(data=securitydata,x='client_id')
        plt.xlabel('Client IDs')
        plt.ylabel('Count of Client Ids')
        plt.title('Times similar client ids were there in security services')
        plt.plot();
        plt.savefig('static/security_s.png')

        result="<center><h1>SECURITY_SERVICES Table Report Analysis</h1>"+result
        result=append_html(result,['security_s.png'])

    elif option == 'option5':
        threatdata = pd.read_sql("SELECT * FROM threats", conn)
        result=threatdata.to_html()

        sns.countplot(data=threatdata,x='client_id')
        plt.xlabel('Client IDs')
        plt.ylabel('Count of Client Ids')
        plt.title('Times similar client ids were there in threats')
        plt.plot();
        plt.savefig('static/threat_c.png')

        result="<center><h1>THREATS Table Report Analysis</h1>"+result
        result=append_html(result,['threat_c.png'])

    elif option == 'option6':
        vulndata = pd.read_sql("SELECT * FROM Vulnerabilities", conn)
        result=vulndata.to_html()

        sns.countplot(data=vulndata,x='client_id')
        plt.xlabel('Client IDs')
        plt.ylabel('Count of Client Ids')
        plt.title('Times similar client ids were there in Vulnerabilities')
        plt.savefig('static/vuln_c.png')

        result="<center><h1>VULNERABILITIES Table Report Analysis</h1>"+result
        result=append_html(result,['vuln_c.png'])

    return result



def append_html(result,image_names):
    for i in image_names:
        result=result+" <img src=\"static/"+i+"\" width=\"600\" height=\"500\">"
    return result


if __name__ == "__main__":
    app.run(debug=True)
