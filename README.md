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

## Example

Bellow an example with 10 rows, 1 switch per row, network start address 10.0.0.0 and a cisco template.

    source env/bin/activate
    python3 suberduber.py -r 10 -s 1 -m 27 -ns 10.0.0.0 -f templates/kradalby_c3750g.j2

## Template

Available attributes:

    {{ row }}
    {{ network }}
    {{ gateway }}
    {{ start }}
    {{ end }}
    {{ netmask }}

