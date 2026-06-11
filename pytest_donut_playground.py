"""On-device smoke test, run against a real esp32c3 leased through Donut.

The DUT serial port is a Donut rfc2217 URL, e.g.:

    pytest --port "rfc2217://127.0.0.1:46211?ign_set_control"
"""
import time

FOUR_INTERVALS_MIN_DURATION_SEC = 3.0
FOUR_INTERVALS_MAX_DURATION_SEC = 3.5


def test_boot_banner_and_ticks(dut):
    dut.expect_exact("donut-playground ready", timeout=30)
    dut.expect(r"target: esp32c3, cores: \d+", timeout=10)
    start_tick = int(dut.expect(r"tick (\d+)", timeout=10).group(1))
    start_time = time.monotonic()

    prev_tick = start_tick
    for _ in range(4):
        current_tick = int(dut.expect(r"tick (\d+)", timeout=10).group(1))
        assert current_tick == prev_tick + 1, "tick counter must increment by 1"
        prev_tick = current_tick

    elapsed = time.monotonic() - start_time

    assert prev_tick == start_tick + 4, "expected tick counter to increase by exactly 4"
    assert FOUR_INTERVALS_MIN_DURATION_SEC <= elapsed <= FOUR_INTERVALS_MAX_DURATION_SEC, (
        f"expected 4 intervals in ~3.2s at 800 ms period, observed {elapsed:.2f}s"
    )
