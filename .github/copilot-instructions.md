# donut_playground — instructions for coding agents

This is an ESP-IDF project for the **esp32c3**. You have access to a **real
esp32c3 devkit** over the network through **Donut** (a remote-hands service):
you lease a device, get a local rfc2217 serial port, and `idf.py` / `esptool` /
pytest work against it exactly like a locally plugged board.

## Environment

`copilot-setup-steps.yml` pre-installs ESP-IDF at `~/esp-idf` (with the
esp32c3 toolchain) and the Python test dependencies. Start every shell with:

```sh
source ~/esp-idf/export.sh
```

The Donut agent token is provided as the `DONUT_TOKEN` environment variable
(a repository secret — never print it).

## Workflow: build, lease a device, flash, test

```sh
source ~/esp-idf/export.sh
pip install -q -r requirements-test.txt   # into the IDF python env

# 1. Build
idf.py build

# 2. Lease an esp32c3 (runs until killed; ESPPORT appears on stdout).
#    PYTHONUNBUFFERED is required: with stdout redirected, the ESPPORT line
#    otherwise sits in Python's block buffer and never reaches the file.
PYTHONUNBUFFERED=1 donut connect --tags esp32c3 > /tmp/donut.out 2> /tmp/donut.err &
DONUT_PID=$!
for i in $(seq 1 30); do grep -q ESPPORT /tmp/donut.out && break; sleep 1; done
export $(grep ESPPORT /tmp/donut.out)
echo "leased port: $ESPPORT"

# 3. Run the on-device tests (pytest-embedded flashes the built app itself)
pytest --port "$ESPPORT" --junitxml=test-results.xml

# 4. Release the lease when done
kill $DONUT_PID
```

Notes:

- `donut ls` lists available devices if the lease fails — a device must carry
  **all** requested tags.
- Killing the `donut connect` process releases the lease; always do it when
  finished so the device frees up for others.
- Hold **one lease at a time**.
- To flash without pytest: `idf.py -p "$ESPPORT" flash`. Avoid bare
  `idf.py monitor` (interactive, never exits); to read console output
  non-interactively, prefer the pytest flow above.
- If `donut connect` exits immediately, check `/tmp/donut.err` — common causes
  are a missing/revoked `DONUT_TOKEN` or no device matching the tags.

## Project layout

- `main/donut_playground.c` — the firmware: prints a boot banner, chip info,
  then a 1 Hz `tick N` counter.
- `pytest_donut_playground.py` — on-device smoke test (pytest-embedded).
- Tests assert on serial output via `dut.expect(...)`; keep new firmware
  output line-oriented and deterministic so tests can match it.

## Conventions

- Target stays `esp32c3` (`sdkconfig.defaults`); don't change the target.
- Any firmware change must keep `pytest --port "$ESPPORT"` green on real
  hardware before you finish.
