---
title: top
parent: Linux
---

## Top

The top command is used to show the active Linux processes. It provides a dynamic real-time view of the running system. Usually, this command shows the summary information of the system and the list of processes or threads which are currently managed by the Linux kernel.

Running this command will open an interactive command mode window where the top half portion will contain the statistics of processes and resource usage. The lower half contains a list of the currently running processes. Pressing q will simply exit the command mode.

```
top - 18:27:57 up 5 days, 32 min,  1 user,  load average: 2.64, 2.53, 2.05
Tasks: 363 total,   2 running, 313 sleeping,   0 stopped,   0 zombie
%Cpu(s):  8.5 us,  1.9 sy,  0.0 ni, 88.7 id,  0.9 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 12228648 total,  1462820 free,  9597568 used,  1168260 buff/cache
KiB Swap:     8188 total,     1284 free,     6904 used.  1672064 avail Mem   
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND     
22935 pbmac     20   0   43000   3768   3152 R  11.8  0.0   0:00.04 top         
   16 root      20   0       0      0      0 S   5.9  0.0   0:08.33 ksoftirqd/1 
 3478 pbmac     20   0 5135080 476252  77796 S   5.9  3.9 199:36.14 chrome      
16330 pbmac     20   0 4974592 149692  17480 S   5.9  1.2  54:41.58 chrome      
22890 pbmac     20   0 4792848 125380  82060 S   5.9  1.0   0:02.57 chrome      
    1 root      20   0  160616   3636    508 S   0.0  0.0   0:28.53 systemd     
    2 root      20   0       0      0      0 S   0.0  0.0   0:00.06 kthreadd    
    6 root       0 -20       0      0      0 I   0.0  0.0   0:00.00 mm_percpu_+ 
    7 root      20   0       0      0      0 S   0.0  0.0   0:08.06 ksoftirqd/0 
    8 root      20   0       0      0      0 I   0.0  0.0   3:35.28 rcu_sched   
    9 root      20   0       0      0      0 I   0.0  0.0   0:00.00 rcu_bh      
   10 root      rt   0       0      0      0 S   0.0  0.0   0:00.03 migration/0 
   11 root      rt   0       0      0      0 S   0.0  0.0   0:00.62 watchdog/0  
   12 root      20   0       0      0      0 S   0.0  0.0   0:00.00 cpuhp/0     
   13 root      20   0       0      0      0 S   0.0  0.0   0:00.00 cpuhp/1     
   14 root      rt   0       0      0      0 S   0.0  0.0   0:00.55 watchdog/1  
   15 root      rt   0       0      0      0 S   0.0  0.0   0:00.03 migration/1 
```

The columns are labeled:

PID: Shows task’s unique process ID.

USER: User name of owner of task.

PR: Stands for priority of the task.

NI: Represents a Nice Value of task. A negative nice value implies higher priority, and positive nice value means lower priority.

VIRT: Total virtual memory used by the task.

RES: Represents the amount of actual physical memory a process is consuming.

SHR: Represents the Shared Memory size (kb) used by a task.

S: The state the process is in.

%CPU: Represents the CPU usage.

%MEM: Shows the Memory usage of task.

TIME+: CPU Time, the same as ‘TIME,’ but reflecting more granularity through hundredths of a second.

COMMAND: The command that is being run.

Above the list of processes, there's a whole bunch of other useful information. Some of these details may look strange and confusing, but once you take some time to step through each one, you'll see they are very useful stats to pull up in a pinch.

The first row contains general system information:

top:  this is simply the command name...followed by:

XX:YY:XX : the time, updated every time the screen updates.

up (then X day, YY:ZZ ): the system's uptime, or how much time has passed since the system turned on.

load average (then three numbers): the system load over the last one, five, and 15 minutes, respectively.

The second row (Tasks) shows information about the running tasks, and it's fairly self-explanatory. It shows the total number of processes and the number of running, sleeping, stopped, and zombie processes. This is literally a sum of the S (state) column described above.

The third row (%Cpu(s)) shows the CPU usage separated by types. The data are the values between screen refreshes. The values are:

us : user processes
sy : system processes
ni : nice user processes
id : the CPU's idle time; a high idle time means there's not a lot going on otherwise
wa : wait time, or time spent waiting for I/O completion
hi : time spent waiting for hardware interrupts
si : time spent waiting for software interrupts
st : "time stolen from this VM by the hypervisor"
You can collapse the Tasks and %Cpu(s) rows by typing t (for "toggle").

The fourth (KiB Mem) and fifth rows (KiB Swap) provide information for memory and swap. These values are:
- total
- used
- free

But also:
- memory buffers
- swap cached Mem
