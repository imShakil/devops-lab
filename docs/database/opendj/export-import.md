---
title: Export and Import
parent: Active Directory
---

## Export data

- to export data into `/opt/opendj/backup.ldiff` file, change `pwd` with **password**:

```bash
/opt/opendj/bin/export-ldif --hostname "localhost" --port 4444 --bindDN "cn=Directory manager" --bindPassword "pwd" --backendID userRoot --ldifFile ./backup.ldiff --trustAll
```

- to export data into `/opt/opendj/backup.ldiff` file, create password file as a `.pw`:

```bash
/opt/opendj/bin/export-ldif --hostname "localhost" --port 4444 --bindDN "cn=Directory manager" --bindPasswordFile /root/.pw --backendID userRoot --ldifFile ./backup.ldiff --trustAll
```

- to export while offline:

```bash
/opt/opendj/bin/stop-ds
/opt/opendj/bin/export-ldif -n userRoot --offline -l filename.ldif
/opt/opendj/bin/start-ds
```

## Import Data

- to import data into `/opt/opendj/backup.ldiff` file, change `pwd` with **password**:

```bash
/opt/opendj/bin/import-ldif --hostname "localhost" --port 4444 --bindDN "cn=Directory manager" --bindPassword "pwd" --backendID userRoot --ldifFile ./backup.ldiff --trustAll
```
