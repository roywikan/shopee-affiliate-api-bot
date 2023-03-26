import mysql.connector

def db_connection(query) :
    mydb = mysql.connector.connect(
        host="biofresma.my.id",
        user="biofresm_shopee_aff",
        password="Azzukhruf26",
        database="biofresm_shopee_aff"
    )
    
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute(query)
    accountResult = mycursor.fetchall()
    return accountResult


