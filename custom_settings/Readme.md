
下面是一个基于CS的远程监控Windows进程是否存在的一个monitor的实现：

- 服务端(monitor_server.py),监听20000端口，客户端建立连接之后，按照客户端发送的进程字符串，使用tasklist命令确认进程是否存在
    - 存在返回\x01
    - 不存在返回\x00
- 自定义monitor，客户端(win_process_monitor.py)
    - 和Server建立连接之后，发送需要监控的进程名
    - 根据服务端返回的结果，判断是否发生Crash
