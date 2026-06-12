# On-device test issues report

Date: 2026-06-12

## Environment

- Repository: `kumekay/donut_playground`
- Target: `esp32c3`
- Test command: `pytest --port "$ESPPORT" --junitxml=test-results.xml`

## Issue 1: Flash/connect step fails over leased RFC2217 port

The lease was established successfully and provided an RFC2217 serial URL, but `pytest-embedded`/`esptool` could not complete the chip sync during setup.

### Log samples

```text
ESPPORT=rfc2217://127.0.0.1:38933?ign_set_control
lease L_gFy2v0dAPkAwRTltGykLE active — point idf.py at $ESPPORT; Ctrl-C to release
```

```text
2026-06-12 08:15:26 Serial port rfc2217://127.0.0.1:38933?ign_set_control:
2026-06-12 08:15:27 Connecting...
2026-06-12 08:15:29 ...............
esptool.util.FatalError: Failed to connect to ESP32-C3: Download mode successfully detected, but getting no sync reply: The serial TX path seems to be down.
For troubleshooting steps visit: https://docs.espressif.com/projects/esptool/en/latest/troubleshooting.html
```

### Observed impact

- Test aborts during fixture setup (`ERROR at setup of test_boot_banner_and_ticks`).
- No firmware boot/banner assertions run because flashing/connection fails first.

## Additional notes from test run

- `pytest` reported RFC2217-related deprecation warnings from `pyserial` (`setDaemon()` / `setName()`), but these were warnings only and not the test-stopping failure.
