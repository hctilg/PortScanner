"""
PortScanner
~~~~~~~~~~~~
Scan All Open Ports Of The Target IP
""" if __name__ == '__main__' else quit()

from time import sleep
from datetime import datetime
from os import get_terminal_size
from sys import version_info, argv
from socket import ( socket, gaierror, error, setdefaulttimeout, gethostbyname, AF_INET, SOCK_STREAM as TCP, SOCK_DGRAM as UDP, SOCK_RAW as ICMP )

# if version_info <= (3, 7):
#   class VersionError(SystemExit): 'return error due to old version'
#   raise VersionError('please update your python. because this version is not suitable for running PortScanner.')

def date():
  date = str(datetime.now()).split(' ')
  date[-1] = date[-1].split('.')[0]
  return ' '.join(date)

try:
  columns_terminal, lines_terminal = get_terminal_size()
except:
  columns_terminal, lines_terminal = (80, 24)  # Unix standard terminal size

class ConnectionError(SystemExit): "return error due to no connection"

def check_port_open(__address: tuple, stype) -> bool:
  try:
    connection = socket(AF_INET, stype)
    setdefaulttimeout(0.7)
    result = connection.connect_ex(__address)
    connection.close()
    return (result == 0)
  except error:
    raise ConnectionError("Couldn't connect to the server.")

def argv_error() -> 0 :
  class ArgumentsError(SystemExit): "return error due to invalid arguments"
  raise ArgumentsError("Invalid amount of arguments!\nSyntax: python3 PortScanner --help")

try:
  
  if (len(argv) <= 1): argv_error()
  
  if (len(argv) == 2):
    
    if (argv[1] == '--developer') or (argv[1] == '-D') :
      
      print(f"\n"+"GitHub : https://github.com/hctilg".center(columns_terminal,' ')+"\n")
      quit()
      
    elif (argv[1] == '--help') or (argv[1] == '-H') :
      
      print(f"""\n{'[ Commands ]'.center(columns_terminal,'-')}\n
Usage: Python3 PortScanner [options] or [args...]
   --help or -H
   --developer or -D

Args:
   --hostname or -h # required
   --port or -p # optional
   --maximum-port or -max-port # optional
   --minimum-port or -min-port # optional
   --protocol # TCP , UDP , ... # optional
   --filter or -f # all , open , closed # optional
    \n{'-'*columns_terminal}\n""")
    quit()
  
  def argv_not_find_error(argv_name: str = "argument") -> 0:
    class ArgumentNotFindError(SystemExit): "return error due to argument not find"
    raise ArgumentNotFindError(f"Error -> {argv_name} not find.")

  if ('--hostname' in argv) or ('-h' in argv) :
    try: hostname = gethostbyname(argv[argv.index('--hostname' if ('--hostname' in argv) else '-h')+1])
    except IndexError: argv_not_find_error("HostName")
  else: argv_not_find_error("HostName")

  if ('--protocol' in argv) :
    try:
      s_protocol = str(argv[argv.index('--protocol')+1]).upper()
      if (s_protocol == 'TCP') : protocol = TCP
      elif (s_protocol == 'UDP') : protocol = UDP
      elif (s_protocol == 'ICMP') or (s_protocol == 'RAW') or (s_protocol == 'IP'): protocol = ICMP
      else: argv_not_find_error("Protocol")
    except IndexError: argv_not_find_error("Protocol")
  else: protocol = TCP

  if ('--minimum-port' in argv) or ('-min-port' in argv) :
    try: min_port = int(argv[argv.index('--minimum-port' if ('--minimum-port' in argv) else '-min-port')+1])
    except IndexError: argv_not_find_error("MinimumPort")
  else: min_port = 1


  if '--maximum-port' in argv or '-max-port' in argv :
    try:max_port = int(argv[argv.index('--maximum-port' if '--maximum-port' in argv else '-max-port')+1])
    except IndexError: argv_not_find_error("MaximumPort")
  else: max_port = 65535

  if ('--port' in argv) or ('-p' in argv) :
    try: min_port = max_port = argv[argv.index('--port' if ('--port' in argv) else '-p')+1]
    except IndexError: argv_not_find_error("Port")

  if ('--filter' in argv) or ('-f' in argv) :
    try:
      filter = str(argv[argv.index('--filter' if ('--filter' in argv) else '-f')+1]).lower()
      if not ((filter == 'all') or (filter == 'open') or (filter == 'closed')) : argv_not_find_error("Filter")
    except IndexError: argv_not_find_error("Filter")

  print(f"\n{'-'.center(columns_terminal,'-')}\n{('Scanning : '+hostname).center(columns_terminal,' ')}\n{('Time started : '+date()).center(columns_terminal,' ')}\n{'-'.center(columns_terminal,'-')}\n")
  
  for port in range(int(min_port), int(max_port)+1):
    
    port_status = check_port_open((hostname, port), protocol)
    
    if (filter == 'open') :
      if not port_status : continue
    elif (filter == 'closed') :
      if port_status : continue
    
    status = 'open ' if port_status else 'closed'
    
    if (protocol == UDP) : sleep(0.12)
    
    margin = 8
    
    print('\n'+f"{' '*margin}Port {port}"+' '.center((columns_terminal-((6+margin+len(str(port)))+(len(status)+7))),' ')+f"{status}{' '*margin}")
  
  print("\n")

except gaierror:
  raise ConnectionError("Error -> hostname couldn't be resolved.")
except KeyboardInterrupt: quit("\n")
except ValueError: argv_error()
except TypeError: argv_error()
except EOFError: ...
