import json
import os
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
        # for files
        dict['code'] = 400
        dict['msg'] = 'fail'
        dict['data'] = None
        return JsonResponse(dict, safe=False)