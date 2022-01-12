import psutil
from datetime import datetime
import platform
from requests import get
import mysql.connector as mysql
import random
from ip2geotools.databases.noncommercial import DbIpCity
import time

def get_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return ("%.2f" % bytes)
        bytes /= factor

def get_input():
    data = input()
    return data

db = mysql.connect(
    user='root',
    password='admin',
    host='localhost',
    database='srv_data'
)
cursor = db.cursor();

print("Press Ctrl-C to terminate while statement")
try:
    while True:
        ip = get('https://api.ipify.org').text
        response = DbIpCity.get(ip)
        country=format(response.country)
        county=format(response.region)
        town=format(response.city)
        coord_lat=format(response.latitude)
        coord_long=format(response.longitude)
        uname = platform.uname()
        cpu_temp=random.uniform(40, 65)
        cpu_temp=round(cpu_temp,1)
        nof=psutil.cpu_count(logical=True)
        cpufreq = psutil.cpu_freq()
        cpu_perc=psutil.cpu_percent(1)
        svmem = psutil.virtual_memory()
        ram_total=float(get_size(svmem.total))
        ram_free=float(get_size(svmem.available))
        ram_used=float(get_size(svmem.used))
        cpufreq = psutil.cpu_freq()
        partitions = psutil.disk_partitions()
        partition=partitions[0]
        partition_usage = psutil.disk_usage(partition.mountpoint)
        storage_size=float(get_size(partition_usage.total))
        storage_used=float(get_size(partition_usage.used))
        storage_free=float(get_size(partition_usage.free))
        user="INSERT EMAIL HERE"
        sql="""INSERT INTO srv_data_t
        (`ip_address`,`country`,`county`,`town`,`coord_lat`,`coord_long`,`cpu`,`cpu_temp`,`cpu_nof_cores`,`cpu_load`,`cpu_max_freq`,`ram_total`,`ram_free`,`ram_used`,`ram_load`,`storage_total`,`storage_used`,`storage_free`,`storage_load`,`user`)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val=(ip,country,county,town,coord_lat,coord_long,uname.processor,cpu_temp,nof,cpu_perc,cpufreq.max,ram_total,ram_free,ram_used,svmem.percent,storage_size,storage_used,storage_free,partition_usage.percent,user)
        cursor.execute(sql,val)
        db.commit()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Log written in database at time:", current_time)
except KeyboardInterrupt:
    pass
db.close()
input("Press enter to close")
