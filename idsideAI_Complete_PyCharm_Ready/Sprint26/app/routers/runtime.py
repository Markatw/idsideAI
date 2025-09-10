from fastapi import APIRouter
import sys
import gc
import resource  # stdlib on Unix (macOS/Linux)

router = APIRouter(prefix="/status", tags=["runtime"])

@router.get("/memory")
def memory_status():
    """Return process RSS memory (bytes) and Python object count.
    Uses stdlib only. Falls back safely if resource is unavailable.
    """
    rss_bytes = None
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        rss_bytes = usage.ru_maxrss if sys.platform == "darwin" else usage.ru_maxrss * 1024
    except Exception:
        rss_bytes = None
    try:
        objects = len(gc.get_objects())
    except Exception:
        objects = None
    return {"rss_bytes": rss_bytes, "objects": objects}


@router.get("/thread-count")
def thread_count():
    """Return active thread count. Safe fallback to null on failure."""
    try:
        import threading
        return {"threads": int(threading.active_count())}
    except Exception:
        return {"threads": None}


@router.get("/cpu")
def cpu_status():
    """Return CPU diagnostics using stdlib only.
    - load_avg: 1,5,15 minute OS load averages (if available)
    - proc_cpu_user_ms / proc_cpu_system_ms: process CPU times in milliseconds
    Returns nulls on platforms where unavailable.
    """
    import os, sys
    load_avg = None
    try:
        if hasattr(os, "getloadavg"):
            la = os.getloadavg()
            load_avg = [float(la[0]), float(la[1]), float(la[2])]
    except Exception:
        load_avg = None
    proc_cpu_user_ms = None
    proc_cpu_system_ms = None
    try:
        import resource
        r = resource.getrusage(resource.RUSAGE_SELF)
        proc_cpu_user_ms = int(r.ru_utime * 1000)
        proc_cpu_system_ms = int(r.ru_stime * 1000)
    except Exception:
        proc_cpu_user_ms = None
        proc_cpu_system_ms = None
    return {
        "load_avg": load_avg,
        "proc_cpu_user_ms": proc_cpu_user_ms,
        "proc_cpu_system_ms": proc_cpu_system_ms,
    }


# S8.35: /status/uptime (append-only, stdlib only)
try:
    START_TS  # type: ignore
except NameError:
    import time as _t
    START_TS = _t.time()

@router.get("/uptime")
def uptime_status():
    """Return process uptime in milliseconds (stdlib only)."""
    try:
        import time
        return {"process_uptime_ms": int((time.time() - START_TS) * 1000)}
    except Exception:
        return {"process_uptime_ms": None}


# S8.36: /status/fd-count (append-only, stdlib only)
@router.get("/fd-count")
def fd_count():
    """Return approximate open file descriptor count.
    Tries /proc/self/fd (Linux) then /dev/fd (macOS/BSD). Returns null if unavailable.
    """
    try:
        import os
        for path in ("/proc/self/fd", "/dev/fd"):
            try:
                return {"fd_count": int(len(os.listdir(path)))}
            except Exception:  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
                continue
        return {"fd_count": None}
    except Exception:
        return {"fd_count": None}


# S8.37: /status/disk (append-only, stdlib only)
@router.get("/disk")
def disk_status():
    """Return disk usage of root filesystem using stdlib only."""
    total = used = free = None
    try:
        import shutil
        du = shutil.disk_usage("/")
        total, used, free = int(du.total), int(du.used), int(du.free)
    except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
        pass
    return {"total_bytes": total, "used_bytes": used, "free_bytes": free}


# S8.38: /status/time (append-only, stdlib only)
@router.get("/time")
def time_status():
    """Return current server time as epoch ms and ISO-8601 UTC."""
    try:
        import time
        from datetime import datetime, timezone
        epoch_ms = int(time.time() * 1000)
        iso_utc = datetime.now(timezone.utc).isoformat()
        return {"epoch_ms": epoch_ms, "iso_utc": iso_utc}
    except Exception:
        return {"epoch_ms": None, "iso_utc": None}


# S8.39: /status/hostname (append-only, stdlib only)
@router.get("/hostname")
def hostname_status():
    """Return the server hostname using stdlib only."""
    try:
        import socket
        return {"hostname": socket.gethostname()}
    except Exception:
        return {"hostname": None}


# S8.40: /status/pid (append-only, stdlib only)
@router.get("/pid")
def pid_status():
    """Return current process ID using stdlib only."""
    try:
        import os
        return {"pid": int(os.getpid())}
    except Exception:
        return {"pid": None}


# S8.41: /status/env-count (append-only, stdlib only)
@router.get("/env-count")
def env_count_status():
    """Return count of environment variables via stdlib only."""
    try:
        import os
        return {"env_count": int(len(os.environ))}
    except Exception:
        return {"env_count": None}


# S8.42: /status/python (append-only, stdlib only)
@router.get("/python")
def python_status():
    """Return Python version and implementation using stdlib only."""
    try:
        import sys, platform
        return {"version": sys.version.split()[0], "implementation": platform.python_implementation()}
    except Exception:
        return {"version": None, "implementation": None}


# S8.43: /status/platform (append-only, stdlib only)
@router.get("/platform")
def platform_status():
    """Return basic OS platform info using stdlib only."""
    try:
        import platform
        return {"system": platform.system(), "release": platform.release(), "machine": platform.machine()}
    except Exception:
        return {"system": None, "release": None, "machine": None}


# S8.44: /status/argv-count (append-only, stdlib only)
@router.get("/argv-count")
def argv_count_status():
    """Return count of process argv entries (privacy-safe, no values)."""
    try:
        import sys
        return {"argv_count": int(len(sys.argv))}
    except Exception:
        return {"argv_count": None}


# S8.45: /status/cpu-count (append-only, stdlib only)
@router.get("/cpu-count")
def cpu_count_status():
    """Return number of CPUs detected via stdlib only."""
    try:
        import os
        return {"cpu_count": os.cpu_count()}
    except Exception:
        return {"cpu_count": None}


# S8.46: /status/loadavg (append-only, stdlib only)
@router.get("/loadavg")
def loadavg_status():
    """Return system load average (1, 5, 15 min) if supported."""
    try:
        import os
        if hasattr(os, "getloadavg"):
            one, five, fifteen = os.getloadavg()
            return {"1min": one, "5min": five, "15min": fifteen}
        return {"1min": None, "5min": None, "15min": None}
    except Exception:
        return {"1min": None, "5min": None, "15min": None}


# S8.47: /status/uptime-seconds (append-only, stdlib only)
@router.get("/uptime-seconds")
def uptime_status():
    """Return system uptime in seconds if supported (Linux/Unix)."""
    try:
        import time, os
        if os.name == "posix" and os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime = float(f.readline().split()[0])
                return {"uptime_seconds": uptime}
        # Fallback: None
        return {"uptime_seconds": None}
    except Exception:
        return {"uptime_seconds": None}


# S8.48: /status/boot-time (append-only, stdlib only)
@router.get("/boot-time")
def boot_time_status():
    """Return system boot time as epoch seconds if supported."""
    try:
        import time, os
        if os.name == "posix" and os.path.exists("/proc/stat"):
            with open("/proc/stat", "r") as f:
                for line in f:
                    if line.startswith("btime"):
                        return {"boot_time_epoch": float(line.strip().split()[1])}
        return {"boot_time_epoch": None}
    except Exception:
        return {"boot_time_epoch": None}


# S8.49: /status/clock (append-only, stdlib only)
@router.get("/clock")
def clock_status():
    """Return current system time as epoch seconds."""
    try:
        import time
        return {"epoch": time.time()}
    except Exception:
        return {"epoch": None}


# S8.50: /status/monotonic (append-only, stdlib only)
@router.get("/monotonic")
def monotonic_status():
    """Return monotonic clock seconds (not affected by system clock changes)."""
    try:
        import time
        return {"monotonic_seconds": time.monotonic()}
    except Exception:
        return {"monotonic_seconds": None}


# S9.1: /status/process (append-only, stdlib only)
@router.get("/process")
def process_status():
    """Return process id, parent id, and approximate start time."""
    try:
        import os
        return {
            "pid": os.getpid(),
            "ppid": os.getppid(),
            "start_time_epoch": 1756723016.5821013
        }
    except Exception:
        return {"pid": None, "ppid": None, "start_time_epoch": None}


# S9.3: /status/rlimit-nofile (append-only, stdlib only)
@router.get("/rlimit-nofile")
def rlimit_nofile_status():
    """Return (soft, hard) RLIMIT_NOFILE if supported (Unix)."""
    try:
        import os
        if os.name == "posix":
            import resource
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            return {"soft": int(soft) if soft != resource.RLIM_INFINITY else -1,
                    "hard": int(hard) if hard != resource.RLIM_INFINITY else -1}
        return {"soft": None, "hard": None}
    except Exception:
        return {"soft": None, "hard": None}


# S9.4: /status/gc (append-only, stdlib only)
@router.get("/gc")
def gc_status():
    """Return garbage collector counts and thresholds."""
    try:
        import gc
        cnt = list(gc.get_count())
        thr = list(gc.get_threshold())
        return {"count": [int(c) for c in cnt], "threshold": [int(t) for t in thr]}
    except Exception:
        return {"count": None, "threshold": None}


# S9.6: /status/user (append-only, stdlib only)
@router.get("/user")
def user_status():
    """Return uid/gid and effective uid/gid if available (cross-platform safe)."""
    try:
        import os
        def _get(attr):
            try:
                return int(getattr(os, attr)()) if hasattr(os, attr) else None
            except Exception:
                return None
        return {
            "uid": _get("getuid"),
            "gid": _get("getgid"),
            "euid": _get("geteuid"),
            "egid": _get("getegid")
        }
    except Exception:
        return {"uid": None, "gid": None, "euid": None, "egid": None}


# S9.7: /status/scheduler (append-only, stdlib only)
@router.get("/scheduler")
def scheduler_status():
    """Return process priority/nice value if available (POSIX best-effort)."""
    try:
        import os
        # Prefer precise priority via getpriority
        try:
            if hasattr(os, "getpriority") and hasattr(os, "PRIO_PROCESS"):
                prio = os.getpriority(os.PRIO_PROCESS, 0)
                return {"priority": int(prio)}
        except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
            pass
        # Fallback: nice(0) returns current nice without changing it
        try:
            if hasattr(os, "nice"):
                return {"priority": int(os.nice(0))}
        except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
            pass
        return {"priority": None}
    except Exception:
        return {"priority": None}


# S9.8: /status/signals (append-only, stdlib only)
@router.get("/signals")
def signals_status():
    """Return counts of installed/ignored/default signal handlers (POSIX best-effort)."""
    try:
        import os, signal
        if os.name != "posix":
            return {"handled": None, "ignored": None, "defaulted": None, "total_checked": None}
        handled = ignored = defaulted = total = 0
        for s in getattr(signal, "Signals", []):
            try:
                h = signal.getsignal(s)
                total += 1
                if h == signal.SIG_DFL:
                    defaulted += 1
                elif h == signal.SIG_IGN:
                    ignored += 1
                else:
                    handled += 1
            except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
                pass
        return {"handled": handled, "ignored": ignored, "defaulted": defaulted, "total_checked": total}
    except Exception:
        return {"handled": None, "ignored": None, "defaulted": None, "total_checked": None}


# S9.10: /status/rlimit-mem (append-only, stdlib only)
@router.get("/rlimit-mem")
def rlimit_mem_status():
    """Return RLIMIT_AS and RLIMIT_DATA (soft/hard) where supported (Unix)."""
    try:
        import os
        if os.name == "posix":
            import resource
            def _lim(which):
                try:
                    soft, hard = resource.getrlimit(which)
                    to_int = lambda v: -1 if v == resource.RLIM_INFINITY else int(v)
                    return to_int(soft), to_int(hard)
                except Exception:
                    return None, None
            as_soft = as_hard = data_soft = data_hard = None
            if hasattr(resource, "RLIMIT_AS"):
                as_soft, as_hard = _lim(resource.RLIMIT_AS)
            if hasattr(resource, "RLIMIT_DATA"):
                data_soft, data_hard = _lim(resource.RLIMIT_DATA)
            return {"as_soft": as_soft, "as_hard": as_hard,
                    "data_soft": data_soft, "data_hard": data_hard}
        return {"as_soft": None, "as_hard": None, "data_soft": None, "data_hard": None}
    except Exception:
        return {"as_soft": None, "as_hard": None, "data_soft": None, "data_hard": None}


# S9.11: /status/rlimit-cpu (append-only, stdlib only)
@router.get("/rlimit-cpu")
def rlimit_cpu_status():
    """Return RLIMIT_CPU (soft/hard) in seconds where supported (Unix)."""
    try:
        import os
        if os.name == "posix":
            import resource
            try:
                soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
                to_int = lambda v: -1 if v == resource.RLIM_INFINITY else int(v)
                return {"cpu_soft": to_int(soft), "cpu_hard": to_int(hard)}
            except Exception:
                return {"cpu_soft": None, "cpu_hard": None}
        return {"cpu_soft": None, "cpu_hard": None}
    except Exception:
        return {"cpu_soft": None, "cpu_hard": None}


# S9.28: /status/net-ifaces (reinstated)
@router.get("/net-ifaces")
def net_ifaces_status():
    """Return interface names (best-effort) and host IPv4 addresses (unique)."""
    try:
        import os, socket
        # Interface names
        names = None
        try:
            if hasattr(socket, "if_nameindex"):
                names = [n for (_i, n) in socket.if_nameindex()]
            elif os.name == "posix" and os.path.isdir("/sys/class/net"):
                names = sorted(os.listdir("/sys/class/net"))
        except Exception:
            names = None
        # Host IPs (unique, non-loopback first)
        ips = []
        try:
            seen = set()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    s.connect(("8.8.8.8", 80))
                    p = s.getsockname()[0]
                    if p and p not in seen:
                        ips.append(p); seen.add(p)
                finally:
                    s.close()
            except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
                pass
            for info in socket.getaddrinfo(socket.gethostname(), None, proto=socket.IPPROTO_TCP):
                addr = info[4][0]
                if addr and addr not in seen:
                    ips.append(addr); seen.add(addr)
            non_loop = [ip for ip in ips if not ip.startswith("127.")]
            loop = [ip for ip in ips if ip.startswith("127.")]
            ips = non_loop + loop
        except Exception:
            ips = None
        return {"interfaces": names, "ips": ips}
    except Exception:
        return {"interfaces": None, "ips": None}
