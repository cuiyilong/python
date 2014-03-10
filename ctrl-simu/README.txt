开发环境：ubuntu + Python 2.7.3

运行环境：
1）python 2.6或2.7，不能使用3.x
2）gcc

使用方法：
1. 在AC上配置AP/STA上线相关配置
	a)  wlan服务模板的ssid需要配置为gbcom_g_test（模拟用户关联时需要）
	b)  ap模板中设备类型为N200-GA200i-AGN22，Vendorid为28723
2. 使用configure文件来配置模拟工具
3. 执行python start.py开始模拟发包
    a） 第一步模拟发送AP上线报文
    b)  第二步模拟open用户关联报文
    c） 第三步模拟web认证报文（radius服务器没有模拟，需要配置正确的服务器）
    注：可以修改start.py文件来模拟发出需要的报文
