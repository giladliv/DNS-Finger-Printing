# DNS Finger Printing
this is the final project of the "Protection of communication protocols" course at Ariel University

## Running the dns cache program
for running the code that needed is: dns_probe_tool.py
windows:
```
python dns_probe_tool.py
```

linux:
```
python3 dns_probe_tool.py
```

help:
```
python dns_probe_tool.py -h
python dns_probe_tool.py --help
```

### good checks

94.153.241.134 - intresting

```
python dns_probe_tool.py -ip 94.153.241.134
```


88.80.64.8 - good dns for check
```
python dns_probe_tool.py -ip 88.80.64.8
```

### help data

there are flags:
```
usage: dns_probe_tool.py [-h] [-a] -ip IP_DNS [-nf DOMAIN_NAMES_FILE] [-jf JSON_FILE_NAME] [-sn SESSION_NAME] [-r REPEATS] [-w WAIT_SEC] [-fnc]

optional arguments:
  -h, --help            show this help message and exit

  -a, --analyze         if this flag is up than the analyzer program will be activated, else the regular progam

  -ip IP_DNS, --ip_dns IP_DNS
                        the DNS server ip address

  -nf DOMAIN_NAMES_FILE, --domain_names_file DOMAIN_NAMES_FILE
                        the file name of the domain names

  -jf JSON_FILE_NAME, --json_file_name JSON_FILE_NAME
                        the name of the json file that established as the dns

  -sn SESSION_NAME, --session_name SESSION_NAME
                        the name of current session of running

  -r REPEATS, --repeats REPEATS
                        the number of intervals in session: how many repeats on query in one session

  -w WAIT_SEC, --wait_sec WAIT_SEC
                        seconds of waiting between intervals in session

  -fnc, --first_not_recursive
                        if you wish that the first run won't be recurssive activate this flag
```
