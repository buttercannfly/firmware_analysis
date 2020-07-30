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
        if len(fragile_services) == 0:
            dict['code'] = 500
            dict['msg'] = 'fail'
            dict['data'] = None
            return JsonResponse(dict,safe=False)
        dict['code'] = 200
        dict['msg'] = 'success'
        dict['data'] = fragile_services
        return JsonResponse(dict, safe=False)


def find_services_versions(dir):
    dict_vuln_services = []
    fs_dir = os.path.join(os.getcwd(), "firmware_analysis", "Firmware", dir, "squashfs-root")
    services_alt = []
    for root,dirs,files in os.walk(os.path.join(fs_dir,"usr","bin")): # /usr/bin下的可运行服务
        for file in files:
            services_alt.append(file)
    opkg_path = os.path.join(fs_dir,"usr","lib","opkg","status") # TODO opkg文件夹只存在于一些路由器设备的操作系统中
    f = open(opkg_path,'r')
    line = f.readline()
    while line:
        line1 = f.readline()
        if "Package" in line:
            for service in services_alt:
                regex_serv = "Package: (.+)"
                regex_serv1 = "Package: lib(.+)"
                if re.findall(regex_serv1, line):
                    print(service,re.findall(regex_serv1,line)[0],line)
                    if service==re.findall(regex_serv1,line)[0]:
                        regex = "Version: (.+?)-"
                        regex1 = "Version: (.+?)"
                        # version = ""
                        version=re.findall(regex,line1)
                        # if version == "":
                        #     version = re.findall(regex1,line1)
                        if version:
                            if {"service":service,"version":version,"cve":[]} not in dict_vuln_services:
                                dict_vuln_services.append({"service":service,"version":version,"cve":[]})
                        else:
                            version =re.findall(regex1,line1)
                            if {"service":service,"version":version,"cve":[]} not in dict_vuln_services:
                                dict_vuln_services.append({"service":service,"version":version,"cve":[]})
                elif re.findall(regex_serv,line):
                    print(service,re.findall(regex_serv,line)[0],line)
                    if service == re.findall(regex_serv,line)[0]:
                        regex = "Version: (.+?)-"
                        regex1 = "Version: (.+?)"
                        # version = ""
                        version=re.findall(regex,line1)
                        # if version == "":
                        #     version = re.findall(regex1,line1)
                        if version:
                            if {"service":service,"version":version,"cve":[]} not in dict_vuln_services:
                                dict_vuln_services.append({"service":service,"version":version,"cve":[]})
                        else:
                            version =re.findall(regex1,line1)
                            if {"service":service,"version":version,"cve":[]} not in dict_vuln_services:
                                dict_vuln_services.append({"service":service,"version":version,"cve":[]})
        line = line1
    print("match_cve_before:")
    print(dict_vuln_services)
    list = match_cve_by_version(os.path.join(os.getcwd(), "firmware_analysis","CVE-list"),dict_vuln_services)
    return list


def match_cve_by_version(cve_dir,dict_vuln_services):
    list_res = []
    lenght = len(dict_vuln_services)
    for root,dirs,files in os.walk(cve_dir):
        for dir in dirs:
            path_dir = os.path.join(cve_dir,dir)
            for file in os.scandir(path_dir):
                if file.name.endswith('.json'):
                    path = os.path.join(cve_dir,dir,file.name)
                    print(dir,file.name)
                    with open(path,"r",encoding='utf8') as fp:
                        json_data = json.load(fp)
                        for cve in json_data["CVE_Items"]:
                            services_affected = []
                            # cve_id = cve["cve"]["CVE_data_meta"]["ID"]
                            # print("CVE_id:",cve["cve"]["CVE_data_meta"]["ID"])
                            for node in cve["configurations"]["nodes"]:
                                if "cpe_match" in node:
                                    # print("cpe_match")
                                    services_affected = node["cpe_match"]
                                    for service_affected in services_affected:
                                        for item in dict_vuln_services:
                                            if str(item["service"]) in service_affected["cpe23Uri"]:
                                                if str(item["version"][0]) in service_affected["cpe23Uri"]:
                                                    dict = {}
                                                    if "baseMetricV3" in cve["impact"]:
                                                        if "baseMetricV2" in cve["impact"]:
                                                            dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"],"cvss2":cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]}
                                                        else:
                                                             dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"],"cvss2":0}
                                                    elif "baseMetricV2" in cve["impact"]:
                                                         dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":0,"cvss2":cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]}
                                                    if dict not in item["cve"]:
                                                        item["cve"].append(dict)
                                                        continue
                                elif "children" in node:
                                    # print("children match")
                                    cpes_match = []
                                    cpes_match = node["children"]
                                    for cpe_match in cpes_match:
                                        services_affected = cpe_match["cpe_match"]
                                        for service_affected in services_affected:
                                            for item in dict_vuln_services:
                                                if str(item["service"]) in str(service_affected["cpe23Uri"]) and str(item["version"][0]) in str(service_affected["cpe23Uri"]):
                                                    dict = {}
                                                    if "baseMetricV3" in cve["impact"]:
                                                        if "baseMetricV2" in cve["impact"]:
                                                            dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"],"cvss2":cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]}
                                                        else:
                                                             dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"],"cvss2":0}
                                                    elif "baseMetricV2" in cve["impact"]:
                                                         dict={"cve_id":cve["cve"]["CVE_data_meta"]["ID"],"description":cve["cve"]["description"]["description_data"][0]["value"],
                                                            "cvss3":0,"cvss2":cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]}
                                                    if dict not in item["cve"]:
                                                        item["cve"].append(dict)
                                                        continue
                                else:
                                    print("????")
    # print(dict_vuln_services)
    for item in dict_vuln_services:
        if len(item['cve'])!=0:
            list_res.append(item)
    print("match_cve_res")
    print(list_res)
    return list_res
