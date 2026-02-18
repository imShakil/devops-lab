---
title: Setup dsconfig
parent: Active Directory
---

## get-global-configuration-prop

To get global opendj configuration:

```bash
/opt/opendj/bin/dsconfig get-global-configuration-prop -p 4444 -X -n -h localhost -D "cn=directory manager" -w "password"
```

To update global configuration:

```bash
/opt/opendj/bin/dsconfig set-global-configuration-prop -p 4444 -X -n -h localhost  -D "cn=directory manager" -w "password" --set lookthrough-limit:1000000
```

It changes default search limit to a maximum number.

## opendj log-level setting

You can do some `dsconfig` operations on `log-publishers` as described below:

1. let get log publishers status to see which are enabled:

```bash
/opt/opendj/bin/dsconfig -h localhost -p 4444 -D "cn=directory manager" -w "password" -X -n list-log-publishers
```

You will get a list of log-publishers:

```txt
Log Publisher                 : Type                   : enabled
------------------------------:------------------------:--------
File-Based Access Logger      : file-based-access      : true
File-Based Audit Logger       : file-based-audit       : true
File-Based Debug Logger       : file-based-debug       : false
File-Based Error Logger       : file-based-error       : true
File-Based HTTP Access Logger : file-based-http-access : false
Replication Repair Logger     : file-based-error       : true
```

To get info of log publisher:

```bash
/opt/opendj/bin/dsconfig -h localhost -p 4444 -D "cn=directory manager" -w "password" -X -n get-log-publisher-prop --publisher-name "File-Based Error Logger"
```

You will get some info about the selected log-publisher:

```txt
Property             : Value(s)
---------------------:---------------------------------------------------------
append               : true
default-severity     : error, notice, warning, info
enabled              : true
log-file             : logs/errors
log-file-permissions : 640
override-severity    : -
retention-policy     : File Count Retention Policy
rotation-policy      : 7 Days Time Limit Rotation Policy, Size Limit Rotation
                     : Policy
```

You may want to update default-severity, then:

```bash
/opt/opendj/bin/dsconfig -h localhost -p 4444 -D "cn=directory manager" -w "password" -X -n --advanced set-log-publisher-prop --publisher-name "File-Based Error Logger" --set default-severity:error --set default-severity:warning
```

updated File-Based Error Logger:

```txt
Property             : Value(s)
---------------------:---------------------------------------------------------
append               : true
default-severity     : error, warning
enabled              : true
log-file             : logs/errors
log-file-permissions : 640
override-severity    : -
retention-policy     : File Count Retention Policy
rotation-policy      : 7 Days Time Limit Rotation Policy, Size Limit Rotation
                     : Policy
```

To disable `access` log:

```bash
/opt/opendj/bin/dsconfig -h localhost -p 4444 -D "cn=directory manager" -w "password" -X -n set-log-publisher-prop --publisher-name "File-Based Access Logger" --set enabled:false
```

To disable `audit` log:

```bash
/opt/opendj/bin/dsconfig -h localhost -p 4444 -D "cn=directory manager" -w "password" -X -n set-log-publisher-prop --publisher-name "File-Based Audit Logger" --set enabled:false
```

Finally, restart opendj for a fresh start.
