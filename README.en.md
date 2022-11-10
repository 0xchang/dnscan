# dnscan

#### Description
A dnscan tool

#### Software Architecture
```
+--- dic.txt
+--- dnscan.py
+--- lib
|   +--- connects.py
|   +--- mythread.py
|   +--- opt.py
|   +--- settings.py
```

#### Installation

pip install -r requirements.txt

#### Instructions

python dnscan.py -h

#### update 2022-11-10
Fix the security vulnerability of eval function when using the p parameter.

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request

