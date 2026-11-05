#!/usr/bin/env python3
"""Stream a PCL 5 test page or caller-supplied printer data to RAW 9100."""

import argparse
import socket


CHUNK_SIZE = 4096
TEST_PAGE = b"\x1bE\x1b&l2A\x1b&l0O\x1b(s0p10h12v0s0b3TESP32-S3 HP LASERJET TEST\r\n\f"


def send_bytes(sock: socket.socket, data: bytes) -> int:
    sent = 0
    for offset in range(0, len(data), CHUNK_SIZE):
        chunk = data[offset : offset + CHUNK_SIZE]
        sock.sendall(chunk)
        sent += len(chunk)
    return sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Send print data unchanged to TCP RAW port 9100")
    parser.add_argument("host", help="ESP32 DHCP IPv4 address")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--file", help="stream this existing printer-data file unchanged")
    parser.add_argument("--port", type=int, default=9100)
    args = parser.parse_args()

    total = 0
    with socket.create_connection((args.host, args.port), timeout=15) as sock:
        sock.settimeout(30)
        if args.file:
            # The caller is responsible for supplying data suitable for this printer.
            with open(args.file, "rb") as source:
                while True:
                    chunk = source.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    total += len(chunk)
        else:
            total += send_bytes(sock, TEST_PAGE)
        sock.shutdown(socket.SHUT_WR)

    print(f"Sent {total} bytes to {args.host}:{args.port}; TCP write side closed")
    print("Check /api/status and the serial log for USB byte totals, then inspect the printer output.")


if __name__ == "__main__":
    main()
