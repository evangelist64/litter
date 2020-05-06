import os,sys
import utils.user_agent

os.chdir(os.path.dirname(sys.argv[0]))

url = 'http://bbs.10jqka.com.cn/codelist.html'
save_file = 'data.txt'
utils.user_agent.grabData(url,save_file)
