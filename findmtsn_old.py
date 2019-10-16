import ConfigParser
import os
import time
import re

INIFILE = 'setup.ini'
L2IP = ''
MTSN = ''
MTSNBAK = ''
mtsn_list_file = ''

class tests:
    def __init__(self):
        self.INIFILE = 'setup.ini'
        self.L2IP = ''
        self.MTSN = ''
        self.MTSNBAK = ''
        self.mtsn_list_file = ''
        self.output_file = 'result.log'
        self.mtsn_root = ''


    def parse_ini_file(self):
        config = ConfigParser.ConfigParser()
        config.read(INIFILE)
        self.L2IP = config.get('Server', 'l2ip').strip('\n')
        self.MTSN = config.get('Server', 'mtsn_folder').strip('\n')
        self.MTSNBAK = config.get('Server', 'mtsn_bak').strip('\n')
        self.mtsn_list_file = config.get('Client', 'mtsn_list').strip('\n')
        self.mtsn_root = os.path.join(self.L2IP, self.MTSN).strip('\n')
        return

    def handle_process(self):
        print self.mtsn_list_file, self.mtsn_root
        mtsn_info = []
        f = open(self.mtsn_list_file, 'r')
        mtsn_list = f.readlines()
        f.close()
        for ea in mtsn_list:
            ea = ea.strip().strip('\n')
            info_list = []
            pici_info = self.get_pici(ea)
            aod_info = self.get_aod(ea)
            #item_info = self.get_flowctl(ea)
            #zipfile = self.get_fail_mtsn(ea)
            print 'zipfile is ' + zipfile

            info_list.append(ea)
            info_list.extend(pici_info)
            info_list.append(aod_info)
            info_list.extend(item_info)
            mtsn_info.append(info_list)
        print mtsn_info
        return mtsn_info

    def get_pici(self, mtsn):
        mtsn_path = os.path.join(self.mtsn_root, mtsn)
        pici_file = os.path.join(mtsn_path, 'PICI.INI')
        config = ConfigParser.ConfigParser()
        config.read(pici_file)
        test_group = config.get('JIXING', 'TEST_GROUP').strip()
        bios_ver = config.get('TEST_SET', 'BIOS_VER').strip()
        return test_group, bios_ver

    def get_flowctl(self, mtsn):
        mtsn_path = os.path.join(self.mtsn_root, mtsn)
        flowctl = os.path.join(mtsn_path, 'flowctl.dat')
        f = open(flowctl, 'r')
        lines = f.readlines()
        fail_stage = 'NA'
        fail_item = 'NA'
        fail_scripts = 'NA'
        for ea in lines:
            obj = re.match('F@@.*', ea)
            if obj:
                fail_stage = obj.group().split('@@')[2]
                fail_item = obj.group().split('@@')[12]
                fail_scripts = obj.group().split('@@')[14]
                break
            obj = re.match(' @@.*', ea)
            if obj:
                fail_stage = obj.group().split('@@')[2]
                fail_item = obj.group().split('@@')[12]
                fail_scripts = obj.group().split('@@')[14]
                break
        return fail_stage, fail_item, fail_scripts

    def get_fail_mtsn(self,mtsn):
        mtsn_path = os.path.join(self.L2IP, self.MTSN, mtsn)
        fail_mtsn_root_path = os.path.join(self.L2IP, self.MTSNBAK)
        mtsn_pass_time = self.get_create_time(mtsn_path)
        year = mtsn_pass_time[1]
        month = mtsn_pass_time[2]
        folder = year + '-' + month
        fail_mtsn_path = os.path.join(fail_mtsn_root_path, folder)

        zipfile = ''s


        return zipfile

    def get_create_time(self,file):
        create_time = time.strftime("o%Y%m%d%H%M%S", time.localtime(os.path.getctime(file)))
        year = create_time[0:2]
        month = create_time[2:4]
        day = create_time[4:6]
        hour = create_time[6:8]
        min = create_time[8:10]
        sec = create_time[10:12]
        return create_time, year, month, day, hour, min, sec

    def get_aod(self, mtsn):
        mtsn_path = os.path.join(self.mtsn_root, mtsn)
        aod_file = os.path.join(mtsn_path, 'AODSTAT.DAT')
        f = open(aod_file, 'r')
        lines = f.readlines()
        ship_os = 'NA'
        for ea in lines:
            obj = re.match('.*AODOS.*', ea)
            if obj:
                #print obj.group()
                ship_os = obj.group().split('&')[1].strip('"')
                #print ship_os  
        return ship_os
            

    def output(self, dict_w_list):
        #key_list = dict_w_list.keys()
        str = ''
        str += 'MTSN' + '\t'
        str += 'TEST_GROUP' + '\t'
        str += 'BIOS_VERSION' + '\t'
        str += 'SHIP_OS' + '\t'
        str += 'Fail Stage' + '\t'
        str += 'Fail Item' + '\t'
        str += 'Fail Script' + '\t'

        str += '\n'
        for ea in dict_w_list:
            mtsn = ea[0]
            test_group = ea[1]
            bios_ver = ea[2]
            ship_os = ea[3]
            fail_stage = ea[4]
            fail_item = ea[5]
            fail_script = ea[6]
            str += mtsn + '\t'
            str += test_group + '\t'
            str += bios_ver + '\t'
            str += ship_os + '\t'
            str += fail_stage + '\t'
            str += fail_item + '\t'
            str += fail_script + '\t'
            str += '\n'
        f = open(self.output_file, 'w')
        f.write(str)
        f.close()


if __name__ == '__main__':
    self = tests()
    self.parse_ini_file()
    mtsn_info = self.handle_process()
    self.output(mtsn_info)
