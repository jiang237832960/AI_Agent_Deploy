# -*- coding: utf-8 -*-
import subprocess
import sys

def get_wmi_value(query):
    try:
        result = subprocess.run(
            ['wmic', 'os', 'get', query, '/value'],
            capture_output=True, text=True, timeout=10,
            encoding='utf-8', errors='ignore'
        )
        for line in result.stdout.split('\n'):
            if '=' in line:
                return line.split('=')[1].strip()
    except:
        pass
    return None

def get_counter(counter_name):
    try:
        cmd = f"$c = Get-Counter '{counter_name}' -ErrorAction SilentlyContinue; if($c){{[math]::Round($c.CounterSamples[0].CookedValue/1MB,0)}}"
        result = subprocess.run(
            ['powershell', '-Command', cmd],
            capture_output=True, text=True, timeout=10,
            encoding='utf-8', errors='ignore'
        )
        return result.stdout.strip()
    except:
        return None

print("=" * 60)
print("              内存使用情况详细检测")
print("=" * 60)
print()

total_mem = get_wmi_value('TotalVisibleMemorySize')
free_mem = get_wmi_value('FreePhysicalMemory')

if total_mem and free_mem:
    total_mb = int(total_mem) // 1024
    free_mb = int(free_mem) // 1024
    used_mb = total_mb - free_mb
    used_pct = (used_mb * 100) // total_mb

    print("[1] 物理内存 (操作系统报告)")
    print(f"    总内存:      {total_mb} MB ({total_mb//1024} GB)")
    print(f"    已使用:      {used_mb} MB ({used_mb//1024} GB) - {used_pct}%")
    print(f"    可用内存:    {free_mb} MB ({free_mb//1024} GB)")
    print()

nonpaged = get_counter('\\Memory\\Pool Nonpaged Bytes')
paged = get_counter('\\Memory\\Pool Paged Bytes')
cache = get_counter('\\Memory\\Cache Bytes')

kernel_total = 0
if nonpaged and nonpaged.isdigit():
    print("[2] 系统内存 (内核/缓存)")
    print(f"    非分页池:    {nonpaged} MB")
    kernel_total += int(nonpaged)

if paged and paged.isdigit():
    print(f"    分页池:      {paged} MB")
    kernel_total += int(paged)

if cache and cache.isdigit():
    print(f"    系统缓存:    {cache} MB")
    kernel_total += int(cache)

if kernel_total > 0:
    print(f"    小计:        {kernel_total} MB")
print()

result = subprocess.run(
    ['wmic', 'pagefile', 'get', 'AllocatedBaseSize,CurrentUsage'],
    capture_output=True, text=True, timeout=10
)
lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
if len(lines) >= 2:
    parts = lines[1].split()
    if len(parts) >= 2:
        page_total = int(parts[0])
        page_used = int(parts[1])
        page_pct = (page_used * 100) // page_total
        print("[3] 分页文件 (虚拟内存)")
        print(f"    总大小:      {page_total} MB")
        print(f"    已使用:      {page_used} MB ({page_pct}%)")
print()

cmd = 'Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 | ForEach-Object { $_.ProcessName + "," + [math]::Round($_.WorkingSet/1MB,0) }'
result = subprocess.run(
    ['powershell', '-Command', cmd],
    capture_output=True, text=True, timeout=30,
    encoding='utf-8', errors='ignore'
)

processes = []
for line in result.stdout.strip().split('\n'):
    if ',' in line:
        parts = line.rsplit(',', 1)
        if len(parts) == 2:
            try:
                name = parts[0].strip()
                mem = int(parts[1].strip())
                processes.append((name, mem))
            except:
                pass

print("[4] 进程内存排行 Top 15")
print("    " + "-" * 40)
for i, (name, mem) in enumerate(processes, 1):
    print(f"    {i:2}. {name[:26]:<26} {mem:>5} MB")
print("    " + "-" * 40)

if processes:
    proc_total = sum(mem for _, mem in processes)
    print(f"    Top 15 进程总内存: {proc_total} MB")
print()

cmd = '(Get-Process | Measure-Object WorkingSet -Sum).Sum / 1MB'
result = subprocess.run(
    ['powershell', '-Command', cmd],
    capture_output=True, text=True, timeout=30,
    encoding='utf-8', errors='ignore'
)
all_proc_total = int(float(result.stdout.strip()))

print("[5] 内存平衡检查")
print(f"    操作系统报告已使用: {used_mb:>6} MB")
print(f"    内核/缓存:          {kernel_total:>6} MB")
print(f"    所有进程总和:       {all_proc_total:>6} MB")
print(f"    合计 (内核+进程):   {kernel_total + all_proc_total:>6} MB")
print(f"    差异:               {used_mb - (kernel_total + all_proc_total):>6} MB")
print()

print("=" * 60)
