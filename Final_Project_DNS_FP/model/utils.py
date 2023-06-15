dns_packets = [
    {
        'source_ip': '192.168.1.10',
        'destination_ip': '8.8.8.8',
        'query': 'example.com',
        'response': '192.0.2.1',
        'response_code': 'NOERROR',
        'target': 'malicious'
    },
    {
        'source_ip': '192.168.1.20',
        'destination_ip': '8.8.8.8',
        'query': 'google.com',
        'response': '172.217.12.14',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.30',
        'destination_ip': '8.8.8.8',
        'query': 'example.com',
        'response': '192.0.2.1',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.40',
        'destination_ip': '8.8.8.8',
        'query': 'example.net',
        'response': '198.51.100.2',
        'response_code': 'NXDOMAIN',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.50',
        'destination_ip': '8.8.8.8',
        'query': 'example.org',
        'response': '203.0.113.1',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.60',
        'destination_ip': '8.8.8.8',
        'query': 'malicious.com',
        'response': '192.0.2.10',
        'response_code': 'NOERROR',
        'target': 'malicious'
    },
    {
        'source_ip': '192.168.1.70',
        'destination_ip': '8.8.8.8',
        'query': 'malicious.net',
        'response': '203.0.113.5',
        'response_code': 'NOERROR',
        'target': 'malicious'
    },
    {
        'source_ip': '192.168.1.80',
        'destination_ip': '8.8.8.8',
        'query': 'malicious.org',
        'response': '192.0.2.20',
        'response_code': 'NOERROR',
        'target': 'malicious'
    },
{
        'source_ip': '192.168.1.10',
        'destination_ip': '8.8.8.8',
        'query': 'www.openai.com',
        'response': '50.16.205.214',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.20',
        'destination_ip': '8.8.8.8',
        'query': 'www.google.com',
        'response': '172.217.12.14',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.30',
        'destination_ip': '8.8.8.8',
        'query': 'www.facebook.com',
        'response': '31.13.65.1',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.40',
        'destination_ip': '8.8.8.8',
        'query': 'www.amazon.com',
        'response': '176.32.98.166',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.50',
        'destination_ip': '8.8.8.8',
        'query': 'www.netflix.com',
        'response': '54.152.220.239',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.60',
        'destination_ip': '8.8.8.8',
        'query': 'www.yahoo.com',
        'response': '72.30.35.10',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.70',
        'destination_ip': '8.8.8.8',
        'query': 'www.microsoft.com',
        'response': '13.77.161.179',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.80',
        'destination_ip': '8.8.8.8',
        'query': 'www.apple.com',
        'response': '17.253.144.10',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.90',
        'destination_ip': '8.8.8.8',
        'query': 'www.github.com',
        'response': '140.82.112.4',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.100',
        'destination_ip': '8.8.8.8',
        'query': 'www.wikipedia.org',
        'response': '91.198.174.192',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.10',
        'destination_ip': '8.8.8.8',
        'query': 'www.openai.com',
        'response': '50.16.205.214',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.20',
        'destination_ip': '8.8.8.8',
        'query': 'www.google.com',
        'response': '172.217.12.14',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.30',
        'destination_ip': '8.8.8.8',
        'query': 'www.facebook.com',
        'response': '31.13.65.1',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.40',
        'destination_ip': '8.8.8.8',
        'query': 'www.amazon.com',
        'response': '176.32.98.166',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.50',
        'destination_ip': '8.8.8.8',
        'query': 'www.netflix.com',
        'response': '54.152.220.239',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.60',
        'destination_ip': '8.8.8.8',
        'query': 'www.yahoo.com',
        'response': '72.30.35.10',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.70',
        'destination_ip': '8.8.8.8',
        'query': 'www.microsoft.com',
        'response': '13.77.161.179',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.80',
        'destination_ip': '8.8.8.8',
        'query': 'www.apple.com',
        'response': '17.253.144.10',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.90',
        'destination_ip': '8.8.8.8',
        'query': 'www.github.com',
        'response': '140.82.112.4',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.100',
        'destination_ip': '8.8.8.8',
        'query': 'www.wikipedia.org',
        'response': '91.198.174.192',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.110',
        'destination_ip': '8.8.8.8',
        'query': 'www.reddit.com',
        'response': '151.101.129.140',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.120',
        'destination_ip': '8.8.8.8',
        'query': 'www.youtube.com',
        'response': '172.217.12.206',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.130',
        'destination_ip': '8.8.8.8',
        'query': 'www.twitter.com',
        'response': '104.244.42.193',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.140',
        'destination_ip': '8.8.8.8',
        'query': 'www.instagram.com',
        'response': '3.214.46.135',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.150',
        'destination_ip': '8.8.8.8',
        'query': 'www.linkedin.com',
        'response': '108.174.10.10',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.160',
        'destination_ip': '8.8.8.8',
        'query': 'www.spotify.com',
        'response': '35.186.224.25',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.170',
        'destination_ip': '8.8.8.8',
        'query': 'www.pinterest.com',
        'response': '151.101.0.84',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.180',
        'destination_ip': '8.8.8.8',
        'query': 'www.netflix.com',
        'response': '54.152.220.239',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.190',
        'destination_ip': '8.8.8.8',
        'query': 'www.amazon.com',
        'response': '176.32.98.166',
        'response_code': 'NOERROR',
        'target': 'benign'
    },
    {
        'source_ip': '192.168.1.200',
        'destination_ip': '8.8.8.8',
        'query': 'www.stackoverflow.com',
        'response': '151.101.65.69',
        'response_code': 'NOERROR',
        'target': 'benign'
    }
]