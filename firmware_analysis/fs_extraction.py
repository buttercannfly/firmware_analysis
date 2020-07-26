import json
import os

import binwalk
from django.http import JsonResponse


def extractfs(name):
            # json_data = json.loads(request.body.decode('utf-8'))
            # name = json_data['name']
        print(name)
        dir = './Firmware/'+name
        scan = binwalk.scan(os.path.join(os.getcwd(),"firmware_analysis","Firmware",name), signature=True, quiet=True, extract=True)
            # for module in scan:
            #     for result in module.results:
            #         if result.file.path in module.extractor.output:
            #             # These are files that binwalk carved out of the original firmware image, a la dd
            #             if result.offset in module.extractor.output[result.file.path].carved:
            #                 print ("Carved data from offset 0x%X to %s" % (result.offset, module.extractor.output[result.file.path].carved[result.offset]))
            #             # These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
            #             if result.offset in module.extractor.output[result.file.path].extracted:
            #                 print ("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(module.extractor.output[result.file.path].extracted[result.offset].files),
            #                                                                                 result.offset,
            #                                                                                 module.extractor.output[result.file.path].extracted[result.offset].files[0],
            #                                                                                 module.extractor.output[result.file.path].extracted[result.offset].command))

def get_dir(name):
    for root,dirs,files in os.walk('.'):
        for dir in dirs:
            if name in dir:
                return dir
    return ""