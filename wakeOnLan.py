import platform
import subprocess
import sys
import time
from wakeonlan import send_magic_packet


devices = {
    'pc_01': {'mac': 'AA-BB-CC-DD-EE-11',
              'ip_address': '192.168.1.2',
              'broadcast_address': '192.168.1.255'},
    'pc_02': {'mac': 'AA-BB-CC-DD-EE-12',
              'ip_address': '192.168.1.3',
              'broadcast_address': '192.168.1.255'},
}


def ping(ip_address: str, times: int) -> bool:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(times), ip_address]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf8')
    print(output)
    if "Request timed out." in output or "100% packet loss" in output or "Destination host unreachable." in output:
        print("No response.")
        return False
    print("Ping response received.")
    return True


def wake_device(device_name: str) -> bool:
    if device_name in devices:
        mac, ip, broadcast_ip = devices[device_name].values()
        send_magic_packet(mac, ip_address=ip, port=9)
        send_magic_packet(mac, ip_address=broadcast_ip, port=7)
        print(f'Magic Packet Sent to {device_name} at {ip}')
        return True
    else:
        print('Device Not Found in dictionary settings.')
    return False


def invoke_wakeonlan(pc_name, is_check) -> bool:
    print("Calling device : ", pc_name)
    print("Checking PC current status.")
    ip_address = devices[pc_name]["ip_address"]
    ip_ping_test_ok = ping(ip_address, 3)
    
    if is_check:
        print("Check Mode : ", ip_ping_test_ok)
        return ip_ping_test_ok

    if ip_ping_test_ok:
        print('Device is already on')
        return True
    else:
        wake_device(pc_name)
        print("Waiting for 60 seconds to check if the device has started.")
        time.sleep(60)
        ip_ping_test_ok = ping(ip_address, 3)

        if ip_ping_test_ok:
            print('Device is up')
            return True
        else:
            print('Device DID NOT response')

    return False


if __name__ == '__main__':
    pc_name = sys.argv[1]
    is_check = False
    if len(sys.argv) > 2 :
        is_check = sys.argv[2] == '-c'
    invoke_wakeonlan(pc_name, is_check)
