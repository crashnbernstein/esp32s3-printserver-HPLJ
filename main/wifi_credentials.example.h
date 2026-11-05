#pragma once

// Copy to wifi_credentials.h (excluded by .gitignore).
// Leave Wi-Fi empty to provision through the setup access point.
#define WIFI_SSID ""
#define WIFI_PASSWORD ""
// Optional DHCP hostname (1-32 chars, letters/digits/hyphen). Defaults to hplj-printserver.
// #define DEVICE_HOSTNAME "hplj-printserver"
// Empty disables HTTP printing. Set a unique random key before building.
// Generate one with: python -c "import secrets; print(secrets.token_hex(32))"
#define X_API_KEY ""
