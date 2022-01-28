import psycopg2



def connect():
    mydb = psycopg2.connect(
            database="d98j2ktql4vmti", 
            user='duzosxfzunzfsm', 
            password='6c69825680f61e29276ebe2bd67d2bd957c6391ef72b1fe6b27df1cf8393d5b2', 
            host='ec2-3-216-113-109.compute-1.amazonaws.com', 
            port= '5432'
            )
    return mydb




