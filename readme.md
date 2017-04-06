# WIFI-QR-Code latex document creator

This small cli-tool creates a simple latex-document containing wifi information.
Especially it creates a qr-code which could later be scanned by a smartphone to connect to the wifi.

## QR-Code

The qr-code is created containing the following string:

```
WIFI:S:{};T:{};P:{};;
```

The brackets are replaced by:

1. SSID
2. Password
3. Encryption (WEP or WPA)

## Usage

```bash
./wifi-qr-tex.py wifi-qr-tex.py [-h] [-e {WPA,WEP}] [-d DESTINATION] [-l {de,en}] SSID PASSWORD
```
