from fastapi import FastAPI
import time
import datetime
from tzlocal import get_localzone
import os
from threading import Thread, Event

class Proc(Thread):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.end_time = self.start_time
        self.stop_ev = Event()

    def stop(self):
        self.stop_ev.set()

    def run(self):
        while(True):
            self.end_time = time.time()
            if(self.end_time - self.start_time >= 200000 or self.stop_ev.is_set()):
                f = open("res.txt", 'w')
                date_st = datetime.datetime.fromtimestamp(self.start_time).astimezone(get_localzone())
                date_end = datetime.datetime.fromtimestamp(self.end_time).astimezone(get_localzone())
                f.write("Working time: {:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d} - {:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(\
                    date_st.day, date_st.month, date_st.year, date_st.hour, date_st.minute, date_st.second,\
                    date_end.day, date_end.month, date_end.year, date_end.hour, date_end.minute, date_end.second))
                f.close()
                break

class ProcRun:
    def __init__(self):
        self.proc = Proc()

    def start(self):
        self.proc.start()

    def stop(self):
        self.proc.stop()
        self.proc.join()
        self.proc = Proc()

    def is_alive(self):
        return self.proc.is_alive()


app = FastAPI(docs_url="/api/docs")
cust_process = ProcRun()

@app.post("/api/time_counter")
def proc_manager(command):
    if(command == "start" and not cust_process.is_alive()):
        cust_process.start()
    elif(command == "stop" and cust_process.is_alive()):
        cust_process.stop()

@app.get("/api/time_counter")
def get_status():
    if(cust_process.is_alive()):
        return {"status": "working"}
    else:
        return {"status": "not working"}
    
@app.get("/api/time_counter/result")
def get_result():
    if(not os.path.exists("res.txt")):
        return {"result": "404 Not Found"}
    else:
        f = open("res.txt", "r")
        output = f.read()
        return {"result": output}