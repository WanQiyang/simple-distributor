# simple-distributor
A simple server for session distribution.

## Install

```bash
conda create -n simple-distributor python=3.12
conda activate simple-distributor
pip install -r requirements.txt
```

## Run

```bash
conda activate simple-distributor
python api.py
```

## Test

```bash
# 098f6bcd4621d373cade4e832627b4f6 is MD5('test')
curl -H 'Content-Type: application/json' -H 'Authorization: Bearer test:098f6bcd4621d373cade4e832627b4f6' http://127.0.0.1:8080/session
```
