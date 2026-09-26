---
name: ping
description: Use when diagnosing agent execution latency, shell round-trip response times, process spawn overhead, or host environment clock skew. Don't use for network speed tests or application uptime monitoring.
---

# Ping

A connectivity and execution latency probe for the agent session. Output `pong` followed by empirical measurements rather than estimated numbers.

## Output contract

The first line of the reply must be exactly `pong` without conversational greetings. Output measured values immediately below. If any probe command fails, report the error output directly rather than guessing a number.

## Execution procedure

### 1. Measure tool round-trip latency

Run three high-resolution sleep delta samples and report the median:

```bash
python3 -c "import time; deltas = []; [(t0 := time.perf_counter(), time.sleep(0.100), deltas.append((time.perf_counter() - t0 - 0.100) * 1000)) for _ in range(3)]; print(f'overhead_ms={sorted(deltas)[1]:.2f}')"
```

### 2. Measure process spawn latency

Time execution of a real child process to measure the tool invocation floor:

```bash
python3 -c "import subprocess, time, sys; t0 = time.perf_counter(); subprocess.run([sys.executable, '-c', 'pass'], check=True); print(f'spawn_ms={(time.perf_counter() - t0) * 1000:.2f}')"
```

### 3. Collect host and session facts

Gather environment properties in a single invocation:

```bash
echo "cwd=$(pwd)"
echo "shell=${SHELL:-unknown}"
echo "user=${USER:-${USERNAME:-unknown}}"
echo "os=$(uname -s 2>/dev/null || echo windows)"
echo "arch=$(uname -m 2>/dev/null || echo unknown)"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 4. Optional network probe

Run only when the user explicitly requests network reachability:

```bash
ping -c 3 -W 2 1.1.1.1 2>/dev/null | tail -n 1 || echo "network unreachable"
```

## Report format

Format the final response as a compact block:

```text
pong

Latency
  harness overhead (median of 3)   1.8 ms
  process spawn                   12.4 ms

Session
  working directory   /Users/groundfox/agent-skills
  shell               /bin/zsh
  platform            Darwin / arm64
  utc                 2026-09-26T05:14:00Z

Verdict  responsive, no anomalies observed
```

## Diagnostic benchmarks

| Metric | Nominal range | Indicator |
|---|---|---|
| Harness overhead | < 10 ms | Standard local execution |
| Process spawn | 10 to 40 ms | Normal shell spawn overhead |
| Clock skew | Under 1 s variance | Healthy system clock |
| Overhead > 200 ms | High latency | Virtualization boundary or heavy system load |
