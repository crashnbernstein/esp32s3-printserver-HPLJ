# Help and diagnostic guide

Start with [README.md](README.md) for wiring, configuration, API reference, and Windows installation.

## Establish a baseline

1. Confirm the printer operates normally using its own self-test procedure, has paper, and supports PCL 5.
2. Confirm the ESP32-S3 board, correct power, GPIO 20 D+, GPIO 19 D-, USB VBUS, and common ground. Use UART console at 115200.
3. Copy the credential example, set a unique API key locally, and build the pinned PlatformIO environment.
4. Flash using UART. Record the first relevant serial error rather than only the final failure summary.
5. Provision Wi-Fi through the setup AP; note the station DHCP address privately.
6. Open `/api/status`. Confirm `wifi_connected` and `printer_ready_for_transfer` before submitting work.
7. Submit one browser test page, poll its job ID, and inspect the physical output.
8. Send one small RAW helper test. Compare before/after RAW counters and inspect paper.
9. Only after these pass, test Windows, large payloads, and reconnect behavior.

## Isolate the failing layer

- **Build:** copy the example if the local header is missing. Download failures differ from C compilation errors. Try the PlatformIO clean target when stale output is suspected.
- **Upload/serial:** confirm the port with `pio device list`, close competing monitors, and follow the board BOOT/RESET procedure. Native USB host pins cannot serve as a simultaneous serial console.
- **Wi-Fi:** NVS overrides compiled defaults. Configuration writes require connection through the setup AP address. A phone may abandon networks without internet.
- **USB:** capture descriptor logs. The printer connection must enumerate a USB Printer Class interface (class 0x07) with Bulk OUT. The connector on a network card may be a host/accessory port rather than a USB printer device port.
- **HTTP:** inspect the response status/error. An empty key denies printing. The test POST still needs `{}`. `202` means queued only.
- **RAW:** test the bundled PCL 5 page before custom files. Close the write side when done. An idle client can retain ownership until timeout. Interrupted streams can leave partial output.
- **Windows:** RAW 9100 forwards bytes unchanged. Use a PCL 5-capable HP LaserJet 4 driver and validate its output through the bridge.

## Recovery and acceptance checks

Reconnect USB and wait for readiness before resubmitting. After an uncertain request, inspect output before retrying to avoid duplicates. After partial RAW output, restore a known printer state using its documented procedure.

For Wi-Fi changes, make the saved network unavailable and join the fallback AP. Full flash erase is documented in README and intentionally destroys stored state/firmware; it is not a first troubleshooting step.

| Scenario | Expected observation |
| --- | --- |
| Wrong API key | `401`, no HTTP job accepted |
| Invalid text/newline/non-ASCII | `400` |
| Printer disconnected | Readiness false; new submission rejected or active job fails |
| Small RAW PCL page | Matching received/queued/USB increments; no new drops; inspect output |
| Large RAW test | Bounded streaming and eventual completion without new drops |
| HTTP during RAW ownership | `503`; retry after completion |
| Restart | History/counters reset; saved Wi-Fi reconnects |
| Station unavailable | Setup AP after connection timeout |

These are hardware acceptance procedures, not claims that each case has been tested on your board.

## Issue report template

```text
Summary:
Expected and actual behavior:
Exact reproduction steps:
Board model / flash size / connection:
Printer model / USB VID:PID:
PCL version / paper:
PlatformIO version / environment:
Firmware commit or source version:
Build result:
HTTP status/error or RAW command (redacted):
Before/after counters:
Relevant redacted serial excerpt:
Physical output:
```

Do not attach local credentials, API keys, passwords, `.pio`, firmware binaries, or unredacted setup AP logs. Report credential disclosures privately if the repository has private security reporting enabled, or through an available private owner contact.
