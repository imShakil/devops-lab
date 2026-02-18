---
title: Memory Management
parent: Linux
---

# To Find All the Process ID

- `top` to view memory status of vm machine

# To Find details of the running services

- Show all process: `ps -e | grep processname` 
- Show with full format: `ps -f | grep processname`
- Show all together: `ps -ef | grep processname`
- Example:
    ```
    ps -ef | grep java
    ```
# To clear Cache, Buffer, Pages, entries

```
sudo su -
sync; echo 1/2/3 > /proc/sys/vm/drop_caches
```
