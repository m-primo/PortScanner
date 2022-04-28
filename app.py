# ==================================================================================
import socket
from contextlib import closing
import termcolor
import pyfiglet
# ==================================================================================
TARGET_SPLITTER = ',' # The charatcter that splits the targets
CHECK_TIMEOUT = 1 # Socket timeout in seconds
IS_ANY_OPEN_PORT = {} # To check and store results of the targets
# ==================================================================================
def scan_port(target, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(CHECK_TIMEOUT)
        if sock.connect_ex((target, port)) == 0:
            print(termcolor.colored('[+] Port Opened ' + str(port), 'green'))
            IS_ANY_OPEN_PORT.update({target: True})

def scan(target, ports):
    print('\n' + termcolor.colored('Scanning: ' + str(target) + '...', 'red'))

    IS_ANY_OPEN_PORT.update({target: False})
    
    for port in range(1, ports):
        scan_port(target, port)

    if not IS_ANY_OPEN_PORT[target]:
        print(termcolor.colored('[!] There are no open ports in this range: 1-' + str(ports), 'yellow'))
# ==================================================================================
if __name__ == '__main__':
    result = pyfiglet.figlet_format('Port Scanner', font='slant')
    print(termcolor.colored(result, 'blue'))

    targets = input(f'[?] Enter Targets To Scan (split by {TARGET_SPLITTER}) (e.g.: 127.0.0.1 or 127.0.0.1{TARGET_SPLITTER}192.168.1.2): ')
    ports = int(input('[?] Enter How Many Ports You Want To Scan (e.g. 3306): '))

    try:
        if TARGET_SPLITTER in targets:
            print(termcolor.colored('[*] Scanning Multiple Targets...', 'red'))
            for target in targets.split(TARGET_SPLITTER):
                scan(target.strip(' '), ports)
        else:
            scan(targets, ports)
    except Exception as ex:
        print(termcolor.colored('[-] Error: ' + str(ex), 'red'))
