#coding=gbk
import sys
import os
import xlrd
import xlwt
import csv
import time
import codecs
import types

os.chdir(os.path.dirname(sys.argv[0]))

class xlsx_obj:
        def __init__(self,idx,desc,step_name,step,result):
                self._idx = idx
                self.format_desc(desc)
                self._step_name_list = []
                self._step_name_list.append(step_name)
                self._step_list = []
                self._step_list.append(step)
                self._result_list = []
                self._result_list.append(result)
                
        def get_result(self):
                desc_str = '||Step||Description||Expected Result||\n'
                for i in range(0,len(self._step_list)):
                        desc_str += '||'
                        desc_str += str(int(self._step_name_list[i]))
                        desc_str += '||'
                        desc_str += str(self._step_list[i])
                        desc_str += '||'
                        desc_str += str(self._result_list[i])
                        desc_str += '||'
                        if(i != (len(self._step_list)-1)):
                                desc_str += '\n'
                return desc_str

        def format_desc(self,desc):
                desc_list = desc.split('\n')
                print desc_list
                self._desc = ''
                self._req = ''

                is_req_content = False
                req_start_str = 'Pre-Requisite'
                req_end_str = 'Reference'
                req_start_str = req_start_str[0:13]
                req_end_str = req_end_str[0:9]

                desc_count = 0
                is_first_req = True
                for desc_one in desc_list:
                        desc_count += 1
                        if desc_one[0:13] == req_start_str:
                                is_req_content = True
                                continue
                        if desc_one[0:9] == req_end_str:
                                is_req_content = False
                        if is_req_content:
                                if len(desc_one)>1:
                                        if not is_first_req:
                                                self._req += '\n'
                                        self._req += desc_one
                                        is_first_req = False
                                        
                        else:
                                self._desc += desc_one
                                if desc_count != len(desc_list):
                                        self._desc += '\n'

        def append_data(self,step_name,step,result):
                self._step_name_list.append(step_name)
                self._step_list.append(step)
                self._result_list.append(result)

        def print_self(self):
                print self._idx
                print self._desc
                print self._step_list
                print self._result_list
                print self.get_result()
                print ""

def format_data(file_name):
        from_file = xlrd.open_workbook(file_name)
        table = from_file.sheets()[2]
        nrows = table.nrows
        ncols = table.ncols

        obj_list = []
        last_obj = None
        for i in range(1,nrows):
                row_one = table.row_values(i)
                idx = row_one[2]
                if(idx != None and idx != ''):
                        obj = xlsx_obj(idx,row_one[3],row_one[7],row_one[8],row_one[9])
                        obj_list.append(obj)
                        last_obj = obj
                else:
                        last_obj.append_data(row_one[7],row_one[8],row_one[9])
        to_file = xlwt.Workbook()
        sheet1 = to_file.add_sheet(u'sheet1',cell_overwrite_ok=True)
        row_num = 0;
        for obj_one in obj_list:
                sheet1.write(row_num,0,str(obj_one._idx))
                sheet1.write(row_num,1,obj_one._desc)
                sheet1.write(row_num,2,obj_one._req)
                sheet1.write(row_num,3,obj_one.get_result())
                row_num += 1
        to_file.save('xx.xls')

if __name__ == '__main__':
        format_data('HAG_Name_Test_Case_V0.1.xlsx')
