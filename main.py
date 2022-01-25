import uvicorn
from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
import json

import psutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request":request})


@app.get("/process")
def get_process(request: Request):
    processes = psutil.process_iter()
    proc_list = []
    for proc in processes:
        try:
            mem_percent = proc.memory_percent()
        except:
            mem_percent = "Can't Access"
        proc_dict = {
            "pid": proc.pid,
            "name": proc.name(),
            "status": proc.status(),
            "mem_percent": mem_percent
        }
        proc_list.append(proc_dict.copy())
        with open('process.json', 'w') as f:
            json.dump(proc_list, f, ensure_ascii=False)
    return templates.TemplateResponse("process.html", {"request":request, "proces" : proc_list})


@app.post("/process")
def post_process(request: Request, nm: str = Form(...)):
    processes = psutil.process_iter()
    proc_list = []
    for proc in processes:
        try:
            mem_percent = proc.memory_percent()
        except:
            mem_percent = "Can't Access"
        if proc.name().lower() == nm.lower():
            proc_dict = {
                "pid": proc.pid,
                "name": proc.name(),
                "status": proc.status(),
                "mem_percent": mem_percent
            }
            proc_list.append(proc_dict.copy())
    if len(proc_list) >= 1:
        with open(nm+'.json', 'w') as f:
            json.dump(proc_list, f, ensure_ascii=False)
    return templates.TemplateResponse("process_by_pid.html", {"request": request, "proces": proc_list})


if __name__ == "__main__":
    uvicorn.run(app)