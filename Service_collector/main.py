from flask import Flask,jsonify, request, redirect , render_template
import os
import psutil
import json
import subprocess
import time
import platform


app=Flask(__name__)
@app.route('/')
def root():
    return render_template("./index.html")
@app.route('/metrics/memory')
def get_memory_info():
    memory_info = {"Virtual Memory" :psutil.virtual_memory().total / (1024.0 ** 3), "Available memory": psutil.virtual_memory().available / (1024.0 ** 3), "Used memory": psutil.virtual_memory().used / (1024.0 ** 3), "Memory percentage": psutil.virtual_memory().percent }
    return jsonify(memory_info)
@app.route('/metrics/disk')
def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.mountpoint] = {"Total space": partition_usage.total / (1024.0 ** 3),"Used space": partition_usage.used / (1024.0 ** 3),"Free space": partition_usage.free / (1024.0 ** 3),"Usage percentage": partition_usage.percent}
    return jsonify(disk_info)
@app.route('/metrics/kernel')
def get_kernel_info():
    try:
        kernel_info = {"Kernel Version": os.uname().release,"System name": os.uname().sysname, "Node name": os.uname().nodename,"Machine": os.uname().machine}    
        return jsonify(kernel_info)
    except:
        message_error = "Maybe not a Linux system? Try /metrics/platform instead"
        return jsonify(message_error)
@app.route('/metrics/platform')
def platform_info():
    platform_info = {"OS version" :platform.platform(), "System name": platform.system(),"Node name": platform.node(), "Machine":  platform.machine()}       
    return jsonify(platform_info)
@app.route('/metrics/cpu')
def get_cpu_info():
    cpu_info = {"Physical cores": psutil.cpu_count(logical=False),"Total cores": psutil.cpu_count(logical=True),"Processor speed": psutil.cpu_freq().current,"Cpu usage per core": dict(enumerate(psutil.cpu_percent(percpu=True, interval=1))),
        "total_cpu_usage": psutil.cpu_percent(interval=1)}
    return jsonify(cpu_info)
@app.route('/metrics/system_uptime')
def get_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_str = {"Uptime": f"{int(uptime_days)} days, {int(uptime_hours % 24)} hours, {int(uptime_minutes % 60)} minutes, {int(uptime_seconds % 60)} seconds"}
    return jsonify(uptime_str)
if __name__ == "__main__":
    app.run(debug=True,port=8001)