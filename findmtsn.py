import ConfigParser
import os
import time
import re

class tests:
    def __init__(self):
        self.INIFILE = 'setup.ini'
        self.L2IP = ''
        self.MTSN = ''
        self.MTSNBAK = ''
        self.mtsn_list_file = ''
        self.output_file = 'result_mtsn.log'

    def parse_ini_file(self):
        config = ConfigParser.ConfigParser()
        config.read(self.INIFILE)
        self.L2IP = config.get('Server', 'l2ip').strip('\n')
        self.MTSN = config.get('Server', 'mtsn_folder').strip('\n')
        self.MTSNBAK = config.get('Server', 'mtsn_bak').strip('\n')
        self.mtsn_list_file = config.get('Client', 'mtsn_list').strip('\n')
        return

    def handle_process(self):
        print self.L2IP, self.MTSN, self.MTSNBAK, self.mtsn_list_file
        mtsn_info = []
        f = open(self.mtsn_list_file, 'r')
        mtsn_list = f.readlines()
        f.close()
        for ea in mtsn_list:
            ea = ea.strip().strip('\n')
            info_list = []
            pici_info = self.get_pici(ea)
            aod_info = self.get_aod(ea)
            info_list.append(ea)
            info_list.extend(pici_info)
            info_list.append(aod_info)
            mtsn_info.append(info_list)
        print mtsn_info
        return mtsn_info

    def get_pici(self,mtsn):
        mtsn_path = os.path.join(self.L2IP, self.MTSN, mtsn)
        pici_file = os.path.join(mtsn_path, 'PICI.INI')
        config = ConfigParser.ConfigParser()
        config.read(pici_file)
        test_group = config.get('JIXING', 'TEST_GROUP').strip()
        bios_ver = config.get('TEST_SET', 'BIOS_VER').strip()
        return test_group, bios_ver

    def get_flowtcl(self):
        return

    def get_aod(self,mtsn):
        mtsn_path = os.path.join(self.L2IP, self.MTSN, mtsn)
        aod_file = os.path.join(mtsn_path, 'AODSTAT.DAT')
        f = open(aod_file, 'r')
        ship_os = 'NA'
        for ea in f:
            obj = re.match('.*AODOS.*', ea)
            if obj:
                ship_os = obj.group().split('&')[1].strip('"')
        return ship_os
            

    def output(self, dict_w_list):
        str = ''
        str += 'MTSN' + '\t'
        str += 'TEST_GROUP' + '\t'
        str += 'BIOS_VERSION' + '\t'
        str += 'SHIP_OS' + '\t'
        str += '\n'
        for ea in dict_w_list:
            mtsn = ea[0]
            test_group = ea[1]
            bios_ver = ea[2]
            ship_os = ea[3]
            str += mtsn + '\t'
            str += test_group + '\t'
            str += bios_ver + '\t'
            str += ship_os + '\t'
            str += '\n'
        f = open(self.output_file, 'w')
        f.write(str)
        f.close()


if __name__ == '__main__':
    self = tests()
    self.parse_ini_file()
    mtsn_info = self.handle_process()
    self.output(mtsn_info)
