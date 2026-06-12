# donut_playground

Demo ESP-IDF project (esp32c3) wired up so a **GitHub Copilot coding agent**
can build the firmware, flash it onto a **real devkit leased through
[Donut](https://gitlab.espressif.cn/services/donut)**, and run on-device
tests — all from the cloud.

The firmware prints a boot banner and a 1 Hz `tick N` counter;
`pytest_donut_playground.py` flashes it and asserts on the serial output.

## Local quickstart

```sh
# ESP-IDF env (esp32c3 toolchain installed)
. $IDF_PATH/export.sh        # or your `idfe` alias
pip install -r requirements-test.txt

idf.py build

# lease a real esp32c3 through Donut (keep running in another terminal)
donut connect --tags esp32c3
# → ESPPORT=rfc2217://127.0.0.1:NNNNN?ign_set_control

pytest --port "rfc2217://127.0.0.1:NNNNN?ign_set_control"
```

`donut` comes from `pip install esp-donut`; authenticate once with
`donut login` (or set `DONUT_TOKEN`).

## Copilot coding agent setup (one-time, repo settings)

1. **Push this repo to github.com** — the Copilot coding agent only runs there.
2. **Agent token:** mint an *agent* token in the Donut hub web UI
   (Leases view).
3. **Secret:** repo → *Settings → Secrets and variables → Agents* →
   *New repository secret* named `DONUT_TOKEN` with the minted token.
   The coding agent receives it as an environment variable. (The older
   "Actions environment named `copilot`" method is deprecated — secrets
   added there now are not picked up.)
4. **Firewall allowlist:** repo → *Settings → Code & automation → Copilot →
   Coding agent* → add `donut.espressif.tools` (and
   `https://donut.espressif.tools`) to the custom allowlist. The agent's
   egress firewall blocks the hub's WebSocket otherwise.
5. **Devices:** make sure a hands box with `esp32c3`-tagged devkits is
   connected to the hub and visible to the token (public, or owned by you).
6. `.github/workflows/copilot-setup-steps.yml` pre-installs ESP-IDF v6.0 +
   the esp32c3 toolchain into the agent's environment (cached between runs);
   `.github/copilot-instructions.md` teaches the agent the
   build → lease → flash → test workflow.

Then assign an issue to Copilot (or open the agents panel) and ask, e.g.:

> Change the tick period to 500 ms, update the on-device test accordingly,
> and verify on real hardware via Donut.

## Files

| Path | Purpose |
|------|---------|
| `main/donut_playground.c` | firmware: banner + chip info + tick counter |
| `pytest_donut_playground.py` | on-device smoke test (pytest-embedded) |
| `pytest.ini` | pytest-embedded services/target defaults |
| `requirements-test.txt` | pytest-embedded + esp-donut |
| `.github/copilot-instructions.md` | agent workflow (lease → flash → test) |
| `.github/workflows/copilot-setup-steps.yml` | agent env: ESP-IDF install |
