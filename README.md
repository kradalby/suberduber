# suberduber
Tool for creating repetitive configuration files based on subnets


## Help

    usage: suberduber.py [-h] -r ROWS -s SWITCH_PER_ROW -m MASK -ns NETWORK_START
                         -f FILE
    
    suberduber.py, creating them config files
    
    optional arguments:
      -h, --help            show this help message and exit
      -r ROWS, --rows ROWS
      -s SWITCH_PER_ROW, --switch SWITCH_PER_ROW
      -m MASK, --mask MASK
      -ns NETWORK_START, --network-start NETWORK_START
      -f FILE, --file FILE

## Template

Available attributes:

    {{ row }}
    {{ network }}
    {{ gateway }}
    {{ start }}
    {{ end }}
    {{ netmask }}

