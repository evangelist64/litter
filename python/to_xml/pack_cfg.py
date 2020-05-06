#coding=gbk
import sys
import os
import xlrd
import csv
import time
import codecs
from xml.dom import minidom,Node
import types
import pyamf

def list_files(dir_name,file_full_name_list,wildcard,recursion,to_xml_name_list,file_name_list):
	exts = wildcard.split("|")
	files = os.listdir(dir_name)
	for name in files:
        	fullname=os.path.join(dir_name,name)
        	if(os.path.isdir(fullname) & recursion):
            		list_files(fullname,file_full_name_list,wildcard,recursion,to_xml_name_list,file_name_list)
        	else:
                        #用后缀过滤
            		for ext in exts:
               			if(name.endswith(ext)):
                    			file_full_name_list.append(fullname)
                    			to_xml_name_list.append((to_xml_path+fullname[len(xlsx_path):len(fullname)])[:-5]+'.xml')
                    			file_name_list.append(name[:-5])
                  			break

def format_data(cell,cell_type):
        if(cell == ''):
                return cell
        cell_type = cell_type.lower()
        if(cell_type == 'int'):
                if(isinstance(cell,float) or isinstance(cell,int)):
                        cell = r'%s'%int(cell)      
        #有些数据填了string类型，实际是int，也要从float转回来
        elif(cell_type == 'string'):
                if(isinstance(cell,float) or isinstance(cell,int)):
                        cell = r'%s'%int(cell)      
        elif(cell_type == 'float'):
                cell = '%s'%('%.2f'%cell)
        else:
                print "not supported type"
                raise
        return cell

def pack_cfg():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        file_full_name_list = []
        to_xml_name_list = []
        file_name_list = []
        list_files(xlsx_path,file_full_name_list,'xlsx',1,to_xml_name_list,file_name_list)
        
        print 'xlsx read begin'
        print 'begin time:'+time.strftime(ISOTIMEFORMAT, time.localtime())

        to_amf_data = {}
        for file_idx in range(0,len(file_full_name_list)):
                try:
                        file_full_name = file_full_name_list[file_idx]
                        to_xml_name = to_xml_name_list[file_idx]
                        file_name = file_name_list[file_idx]
                        
                        #xml节点
                        doc = minidom.Document()
                        root = doc.createElement("root")
                        doc.appendChild(root)
                        types = doc.createElement("types")
                        root.appendChild(types)
                        keys = doc.createElement("keys")
                        root.appendChild(keys)
                        data = doc.createElement("data")
                        root.appendChild(data)

                        #amf object
                        types_amf = []
                        keys_amf = []
                        data_amf = {}
                        
                        xls_data = xlrd.open_workbook(file_full_name)
                        table = xls_data.sheets()[0]
                        nrows = table.nrows
                        ncols = table.ncols
                        if(nrows < 5):
                                print 'wrong format, %s'%file_full_name
                                continue
                        row_data_type = table.row_values(3)
                        row_column_name = table.row_values(4)
                        skip_column = []
                        for column_idx in range(0,len(row_data_type)):
                                data_type = row_data_type[column_idx]
                                column_name = row_column_name[column_idx]
                                #无效行，跳过
                                if(data_type == None or data_type == '' or column_name == None or column_name == ''):
                                        skip_column.append(column_idx)
                                        continue;
                                #xml节点
                                type_one = doc.createElement("type")
                                type_one.setAttribute('name',data_type)
                                types.appendChild(type_one)
                                key_one = doc.createElement("key")
                                key_one.setAttribute('name',column_name)
                                keys.appendChild(key_one)
                                
                                #amf object
                                types_amf.append(data_type)
                                keys_amf.append(column_name)

                        for rownum in range(5,nrows):
                                row = table.row_values(rownum)
                                row_one = doc.createElement("record")

                                amf_data_obj = {}
                                amf_data_obj_id = ''
                                for i in range(0,len(row)):
                                        if(i in skip_column):
                                                continue;
                                        data_type = row_data_type[i]
                                        column_name = row_column_name[i]
                                        #xlrd把所有数字存成浮点数，需要取整
                                        value_final = format_data(row[i],row_data_type[i])
                                        
                                        #xml
                                        row_one.setAttribute(column_name,value_final)
                                        
                                        #amf
                                        amf_data_obj[column_name] = value_final
                                        if(i==0):
                                               amf_data_obj_id = value_final
                                if(amf_data_obj_id!='' and amf_data_obj_id!=None):
                                        data_amf[amf_data_obj_id] = amf_data_obj
                                else:
                                        print 'wrong id format'
                                        raise
                                        return
                                data.appendChild(row_one)
                        #xml
                        to_dir = os.path.dirname(to_xml_name)
                        if(os.path.exists(to_dir)==False):
                                os.makedirs(to_dir)
                        f = file(to_xml_name, 'w')
                        writer = codecs.lookup('utf-8')[3](f)

                        '''
                        #minidom会对attributes做字典排序，这里禁掉，以保持attributes按表结构顺序输出，兼容旧代码
                        with _MinidomHooker():
                                doc.writexml(writer, encoding='utf-8',newl='\n',addindent='  ')
                                writer.close()
                        '''
                        doc.writexml(writer, encoding='utf-8',newl='\n',addindent='  ')
                        writer.close()
                        #amf
                        to_amf_data[file_name] = {'keys':keys_amf,'data':data_amf,'name':file_name,'types':types_amf}
                        
                except Exception,e:
                        print "error %s,%s" % (file_full_name,e)

        encoder = pyamf.get_encoder(pyamf.AMF3)    
        stream = encoder.stream     
        encoder.writeElement(to_amf_data)    
        amf_data = stream.getvalue()
        f = file(to_dat_path+'\\temp.dat', 'wb')
        f.write(amf_data)
        f.close()
            
        print 'pack end'
        print 'end_time:'+time.strftime(ISOTIMEFORMAT, time.localtime())
        os.system('pause')

'''
class _MinidomHooker(object):
        def __enter__(self):
                minidom.NamedNodeMap.keys_orig = minidom.NamedNodeMap.keys
                minidom.NamedNodeMap.keys = self._NamedNodeMap_keys_hook
                return self

        def __exit__(self, *args):
                minidom.NamedNodeMap.keys = minidom.NamedNodeMap.keys_orig
                del minidom.NamedNodeMap.keys_orig

        @staticmethod
        def _NamedNodeMap_keys_hook(node_map):
                class OrderPreservingList(list):
                        def sort(self):
                                pass
                return OrderPreservingList(node_map.keys_orig())
'''

if __name__ == '__main__':
        cfg_global = {}
        os.chdir(os.path.dirname(sys.argv[0]))
        with open('cfg.ini','r') as f_cfg:
                cfg_data = f_cfg.read()
                cfg_array = cfg_data.split('\n')
                for c in cfg_array:
                        c_obj = c.split('=');
                        cfg_global[str(c_obj[0]).strip()] = str(c_obj[1]).strip()
        xlsx_path = cfg_global['xlsx_path']
        to_xml_path = cfg_global['to_xml_path']
        to_dat_path = cfg_global['to_dat_path']
        pack_cfg()
