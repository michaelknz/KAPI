from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


def get_response(response, title):
    output = "<html>\
                 <head>\
                     <title>" + title + "</title>\
                 </head>\
                 <body>" + response + "</body>\
             </html>"
    return HTMLResponse(output)

app_description = "Run process and see it's working time"

tags_metadata = [
    {
        "name": "Proc info",
        "description": "Get proc info",
    },
    {
        "name": "Result",
        "description": "Get result of proc",
    },
    {
        "name": "Proc manager",
        "description": "Manage proc (type **start** - to start proc; type **stop** - to stop proc)",
    }
]

app = FastAPI(docs_url="/api/docs", title = "Time Counter API", description=app_description, openapi_tags=tags_metadata)
cust_process = ProcRun()

@app.post("/api/time_counter", tags=["Proc manager"])
def proc_manager(command):
    if(command == "start" and not cust_process.is_alive()):
        cust_process.start()
    elif(command == "stop" and cust_process.is_alive()):
        cust_process.stop()

@app.get("/api/time_counter", response_class=HTMLResponse, tags=["Proc info"])
def get_status():
    output = ""
    if(cust_process.is_alive()):
        output = "status: working"
    else:
        output = "status: not working"
    return get_response(output, "Proc info")
    
@app.get("/api/time_counter/result", tags=["Result"])
def get_result():
    if(not os.path.exists("res.txt")):
        return get_response("Result: 404 Not Found", "Result")
    else:
        f = open("res.txt", "r")
        output = f.read()
        f.close()
        return get_response("Result: " + output, "Result")