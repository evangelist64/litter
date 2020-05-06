import os,os.path 
import zipfile
import sys
import shutil

version = '15-12-07'

def zip_dir(dirname,zipfilename): 
    filelist = [] 
    if os.path.isfile(dirname): 
        filelist.append(dirname) 
    else : 
        for root, dirs, files in os.walk(dirname): 
            for name in files: 
                filelist.append(os.path.join(root, name)) 
          
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED) 
    for tar in filelist: 
        arcname = tar[len(dirname):] 
        zf.write(tar,arcname) 
    zf.close()
  
def unzip_file(zipfilename, unziptodir): 
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777) 
    zfobj = zipfile.ZipFile(zipfilename) 
    for name in zfobj.namelist(): 
        name = name.replace('\\','/') 
         
        if name.endswith('/'): 
            os.mkdir(os.path.join(unziptodir, name)) 
        else:             
            ext_filename = os.path.join(unziptodir, name) 
            ext_dir= os.path.dirname(ext_filename) 
            if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0777) 
            outfile = open(ext_filename, 'wb') 
            outfile.write(zfobj.read(name)) 
            outfile.close()

def cp_tree_ext(exts,src,dest):
    fp={}
    extss=exts.lower().split()
    for dn,dns,fns  in os.walk(src):
        for fl in fns:
            if os.path.splitext(fl.lower())[1][1:] in extss:
                if dn not in fp.keys():
                    fp[dn]=[]
                fp[dn].append(fl)
    for k,v in fp.items():
        relativepath=k[len(src):]
        newpath=os.path.join(dest,relativepath)
        for f in v:
            oldfile=os.path.join(k,f)
            #print("Copying ["+oldfile+"] To ["+newpath+"]")
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            shutil.copy(oldfile,newpath)

os.chdir('E:/SGSBAYE_ZYH/')

DEPLOY_SERVER_PATH = 'E:/SGSBAYE_ZYH/Deploy_Server/'
DEPLOY_CLIENT_PATH = 'E:/SGSBAYE_ZYH/Deploy_Client/'
print 'rm old file...'
if(os.path.exists(DEPLOY_SERVER_PATH)):
    shutil.rmtree(DEPLOY_SERVER_PATH)
if(os.path.exists(DEPLOY_CLIENT_PATH)):
    shutil.rmtree(DEPLOY_CLIENT_PATH)
print 'copy server...'
cp_tree_ext('pdb exe dll sql','E:/SGSBAYE_ZYH/Server/DailyDist/',DEPLOY_SERVER_PATH)
print 'copy client...'
os.mkdir(DEPLOY_CLIENT_PATH)
shutil.copy('E:/SGSBAYE_ZYH/Client/trunk/SGSQWeb/bin-release/Entry.swf',DEPLOY_CLIENT_PATH)
shutil.copy('E:/SGSBAYE_ZYH/Client/trunk/SGSQWeb/bin-release/SGSQWeb.swf',DEPLOY_CLIENT_PATH)
shutil.copytree('E:/SGSBAYE_ZYH/Client/trunk/SGSQWeb/bin-debug/assist/',DEPLOY_CLIENT_PATH+'assist/')
print 'copy config...'
DEPLOY_SERVER_CFG_DEBUG_PATH = DEPLOY_SERVER_PATH+'SGSQ_Server_Debug/Server/xmlconfig'
DEPLOY_SERVER_CFG_RELEASE_PATH = DEPLOY_SERVER_PATH+'SGSQ_Server_Release/Server/xmlconfig'
if(os.path.exists(DEPLOY_SERVER_CFG_DEBUG_PATH)):
    shutil.rmtree(DEPLOY_SERVER_CFG_DEBUG_PATH)
    shutil.copytree('E:/SGSBAYE_ZYH/Config/sgsby/deploy/xmlconfig/',DEPLOY_SERVER_CFG_DEBUG_PATH)
if(os.path.exists(DEPLOY_SERVER_CFG_RELEASE_PATH)):
    shutil.rmtree(DEPLOY_SERVER_CFG_RELEASE_PATH)
    shutil.copytree('E:/SGSBAYE_ZYH/Config/sgsby/deploy/xmlconfig/',DEPLOY_SERVER_CFG_RELEASE_PATH)
os.mkdir(DEPLOY_CLIENT_PATH+'data/')
shutil.copy('E:/SGSBAYE_ZYH/Config/sgsby/deploy/temp.dat',DEPLOY_CLIENT_PATH+'data/')
print 'zip server...'
zip_dir(DEPLOY_SERVER_PATH,'server_%s.zip'%version)
print 'zip client...'
zip_dir(DEPLOY_CLIENT_PATH,'client_%s.zip'%version)
print 'end'
