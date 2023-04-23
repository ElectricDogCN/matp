import time

import paramiko
import logging

import select

from concurrent.futures import ThreadPoolExecutor

from paramiko.channel import Channel

executor = ThreadPoolExecutor()


# 定义一个控制主机的类
class ControlHost:
    def __init__(self, ip, user, passwd, port=22, encoding="gbk"):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = port
        self.encoding = encoding
        # 创建SSHClient对象
        ssh = paramiko.SSHClient()
        # 设置自动添加主机密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh = ssh
        self.sftp = None

    # 连接主机
    def connect(self):
        self.ssh.connect(self.ip, self.port, self.user, self.passwd, look_for_keys=False, allow_agent=False)
        return self

    def close(self):
        self.ssh.close()

    # 执行命令或重新连接
    def exec_or_reconnect(self, command):
        logging.info(f"Host exec amd:\r\n{command}\r\n")
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdin, stdout, stderr
        except Exception as e:
            logging.warning(e)
            self.connect()
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdin, stdout, stderr

    channel = None

    # 处理标准错误输出
    def process_stderr(self, _, stdout, stderr):
        if not stdout:
            if stderr:
                stderr = str(stderr.read().decode(self.encoding))
                if not stderr == "":
                    logging.warning("Exec command fail! \r\n%s" % stderr)
                    return False
            logging.warning("Exec command return None.")
            return ""
        return str(stdout.read().decode(self.encoding))

    def execute_command_non_blocking(self, command):

        channel = self.ssh.get_transport().open_session()
        channel.setblocking(0)
        channel.get_pty()
        channel.exec_command(command)
        start_time = time.time()
        self.channel = channel

        def printlog():
            while True:
                if channel.recv_ready():
                    rl, wl, xl = select.select([channel], [], [], 0.0)
                    if len(rl) > 0:
                        print(channel.recv(1024).decode('utf-8'))
                if channel.exit_status_ready() or time.time() - start_time > 60:
                    break

        executor.submit(printlog)

    def start_appium(self):
        self.execute_command_non_blocking("appium")

    def stop_appium(self):
        print("exit1")
        if isinstance(self.channel, Channel) and not self.channel.closed:
            self.channel.send("\x03".encode())
            print("exit2")
        executor.shutdown()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit0")
        self.stop_appium()


if __name__ == '__main__':
    test_host = ControlHost("127.0.0.1", "asus", "tang1968").connect()
    print(test_host.process_stderr(*test_host.exec_or_reconnect("ipconfig")))
    test_host.execute_command_non_blocking("appium")
