from fastapi import FastAPI
import time
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
                break

    def __del__(self):
        f = open("res.txt", 'w')
        f.write("Working time: " + str(self.start_time) + " - ", + str(self.end_time))
        f.close()

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

@app.get("/")
def root():
    return {"hello": "world"}

@app.post("/api/time_counter")
def proc(command):
    if(command == "start" and not cust_process.is_alive()):
        cust_process.start()
    elif(command == "stop" and cust_process.is_alive()):
        cust_process.stop()

@app.get("/api/time_counter")
def get_res():
    if(cust_process.is_alive()):
        return {"working": None}
    else:
        return {"not working": None}
