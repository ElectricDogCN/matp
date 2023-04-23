from host.control import ControlHost


class DeviceControlHostManager:
    # ip:ControlHost
    HOST_LIST = {}

    @classmethod
    def add_control_host(cls, ip, user, passwd, port=22, encoding="gbk"):
        host = ControlHost(ip, user, passwd, port, encoding).connect()
        instance = {"ip": ip, "passwd": passwd, "port": port, "encoding": encoding, "instance": host}
        cls.HOST_LIST[ip] = instance

    @classmethod
    def remove_control_host(cls, ip):
        if ip in cls.HOST_LIST:
            host = cls.HOST_LIST[ip]["instance"]
            if isinstance(host, ControlHost):
                host.close()
            cls.HOST_LIST.pop(ip)

    @classmethod
    def start_appium(cls, ip):
        host = cls.HOST_LIST[ip]["instance"]
        if isinstance(host, ControlHost):
            host.start_appium()

    @classmethod
    def stop_appium(cls, ip):
        host = cls.HOST_LIST[ip]["instance"]
        if isinstance(host, ControlHost):
            host.stop_appium()


if __name__ == '__main__':
    DeviceControlHostManager.add_control_host("127.0.0.1", "asus", "tang1968")
    DeviceControlHostManager.start_appium("127.0.0.1")
