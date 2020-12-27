## src-scan

Simple artifact parser and extractor. Testcases are removed for privacy reasons.

## Usage

Install required dependency

```
pip3 install -r requirements.txt
```

Extract information from target and output in JSON format

```
%> python3 ./main.py /tmp/example
{"htpasswd": [{"type": "credentials", "data": {"username": "admin", "password": "$apr1$2NS2rIqW$unBL1mdWm6W4eKChOPN4H1"}, "filename": "/tmp/example/htpasswd"}]}
```
