from django.http import JsonResponse

from app.models import Firmware


def get_result(request):
    dict = {}
    id = request.GET.get("id")
    firmware = Firmware.objects.get(id=id)
    service_list = []
    services = firmware.service_set.all()
    for service in services:
        cve_list = []
        cves = service.cve_set.all()
        for cve in cves:
            dict1 = {"id":cve.id,"description":cve.des,"cvss2":cve.cvss2,"cvss3":cve.cvss3}
            cve_list.append(dict1)
        dict_1 = {"service":service.name,"version":service.version,"cve":cve_list}
        service_list.append(dict_1)
    dict['data'] = {"firmware":firmware.name,"services":service_list}
    dict['msg'] = 'success'
    dict['code'] = 200

    # dict['data']
    return JsonResponse(data=dict,safe=False)