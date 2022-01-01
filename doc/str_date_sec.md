```plantuml
"datetime" --> "string" : time.strtime
"datetime" <-- "string" : time.strptime
"datetime" --> "second" : time.mktime
"datetime" <-- "second" : time.localtime\ntime.gmtime

```
