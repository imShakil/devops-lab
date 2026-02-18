---
title: LDAP Search
parent: Active Directory
---

## To count total users in opendj backends:

```bash
/opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' 'oxAuthGrantId=*' dn | grep 'dn:' | wc -l
```

## To Find a specific user using its `uid`:

```bash
/opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w "password" -b 'o=gluu' "(uid=admin)"
```
