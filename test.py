import schedule
import time
import pandas as pd

def test():
    print("Program Masih Jalan")

def statusBot():
    statusbot = "1nzzMebmvMyODar_9LivVMh7U8UuGwAwUL6kQzSZaAtI"

    status = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{statusbot}/export?format=csv")

    if(status.iloc[0][0] == "Aktif"):
        print("Status Berjalan")
    else :
        print("Mati")
        exit()


schedule.every(0.5).minutes.do(test)
schedule.every(1).minutes.do(statusBot)
 

while True:
    schedule.run_pending()
    time.sleep(1)