from flask import Flask, request
from host.manager import DeviceControlHostManager as dchm

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    ip = request.args.get('ip')
    user = request.args.get('users')
    passwd = request.args.get('passwd')

    dchm.add_control_host(ip, user, passwd)
    dchm.start_appium(ip)
    return "success"


@app.route('/stop', methods=['GET'])
def stop():
    ip = request.args.get('ip')
    dchm.stop_appium(ip)
    return "success"


if __name__ == '__main__':
    app.run()
