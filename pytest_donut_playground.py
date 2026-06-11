"""On-device smoke test, run against a real esp32c3 leased through Donut.

The DUT serial port is a Donut rfc2217 URL, e.g.:

    pytest --port "rfc2217://127.0.0.1:46211?ign_set_control"
"""

import time


def test_boot_banner_and_ticks(dut):
    dut.expect_exact("donut-playground ready", timeout=30)
    dut.expect(r"target: esp32c3, cores: \d+", timeout=10)

    first_match = dut.expect(r"tick (\d+)", timeout=10)
    first = int(first_match.group(1))
    first_time = time.monotonic()

    second_match = dut.expect(r"tick (\d+)", timeout=10)
    second = int(second_match.group(1))
    second_time = time.monotonic()

    assert second == first + 1, "tick counter must increase monotonically"

    interval = second_time - first_time
    assert 0.3 <= interval <= 0.8, f"expected ~0.5 s tick interval, got {interval:.3f} s"
