import json
import os
import re
from firmware_analysis.fs_extraction import get_dir, extractfs

from django.http import JsonResponse

print(os.getcwd())


def firm_analysis(request):
    if request.method == 'POST':
        firmware = request.FILES.get("firmware",None)
        dict = {}
        if not firmware:
            dict['code'] = 400
            dict['msg'] = 'fail'
            dict['data'] = None
            return JsonResponse(dict, safe=False)
        destination = open(os.path.join(os.getcwd(),"firmware_analysis","Firmware",firmware.name),"wb+")
        for chunk in firmware.chunks():
            destination.write(chunk)
        destination.close()  # 写入文件
        name = firmware.name
        if get_dir(name)=="":
            extractfs(name)
        dir = get_dir(name)
        print(dir)  # dir是提取固件之后的文件夹
        fragile_services = {}
        fragile_services = find_services_versions(dir)
        dict['code'] = 400
        dict['msg'] = 'fail'
        dict['data'] = None
        return JsonResponse(dict, safe=False)


def find_services_versions(dir):
    dict_vuln_services = []
    fs_dir = os.path.join(os.getcwd(), "firmware_analysis", "Firmware", dir, "squashfs-root")
    services_alt = []
    for root,dirs,files in os.walk(os.path.join(fs_dir,"usr","bin")): # /usr/bin下的可运行服务
        for file in files:
            services_alt.append(file)
    opkg_path = os.path.join(fs_dir,"usr","lib","opkg","status")
    f = open(opkg_path,'r')
    line = f.readline()
    while line:
        line1 = f.readline()
        for service in services_alt:
            if service in line and "Version" in line1:
                regex = "Version: (.+?)-"
                regex1 = "Version: (.+?)"
                version = ""
                version=re.findall(regex,line1)
                # if version == "":
                #     version = re.findall(regex1,line1)
                if version:
                    if {"service":service,"version":version} not in dict_vuln_services:
                        dict_vuln_services.append({"service":service,"version":version})
                else:
                    version =re.findall(regex1,line1)
                    if {"service":service,"version":version} not in dict_vuln_services:
                        dict_vuln_services.append({"service":service,"version":version})
                break
        line = line1
    print(dict_vuln_services)