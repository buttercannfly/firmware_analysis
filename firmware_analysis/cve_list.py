import wget
import os,sys
import zipfile

def get_cve_list():
    year_from = 2010
    year_to = 2020
    year = year_from
    while year <= year_to:
        url = "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-"+str(year)+".json.zip"
        output_dir = os.path.join(os.getcwd(),"CVE-list")
        target_name = "cve"+str(year)+".zip"
        for file in os.scandir(output_dir):
            if file.name == target_name:
                continue
        print("url:"+url,"output_dir:"+output_dir,"target_name:"+target_name)
        year = year + 1
        file_name = wget.download(url,out=os.path.join(output_dir,target_name))
# get_cve_list()

def unzip(filename):
    # try:   
        file = zipfile.ZipFile(filename)
        dirname = filename.replace('.zip', '')
        if os.path.exists(dirname):
            print(f'{filename} dir has already existed')
            return
        else:
            # 创建文件夹，并解压
            os.mkdir(dirname)
            file.extractall(dirname)
            file.close()
            # 递归修复编码
            # rename(dirname)
    # except:
    #     print(f'{filename} unzip fail')


def unzip_cve():
    cve_dir = os.path.join(os.getcwd(),"CVE-list")
    for file in os.scandir(cve_dir):
        print(file.name)
        if file.name.endswith('.zip') and file.is_file():
            unzip(os.path.join(cve_dir,file.name))


unzip_cve()