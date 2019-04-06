# Python_Tor
使用python启动tor，预留socksport 9050
下载使用
将项目克隆到本地

$ git clone https://github.com/Analyst1981/Python_Tor.git
进入工程目录

$ cd Python_Tor
运行启动脚本 scheduler.py.py 也可以分别运行抓取，验证，socks5代理，启动tor服务

$ python scheduler.py.py

运行前，在proxy.py--->api=shodan.Shodan("此处需要shodanKEY") #需要添加shodanKEY

其中使用 https://github.com/cyubuchen/ProxySpider_spys  抓取socks代理的代码，表示感谢！
