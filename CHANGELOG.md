# Changelog

## 0.1.0 (2026-04-30)

Initial release. Eight Wireshark profiles covering 3G, 4G LTE, 5G NSA, 5G SA, IMS voice (VoLTE / VoNR), Wi-Fi calling, and the cross-generation user plane.

`validate.py` cross-checks every display-filter field reference against `tshark -G fields` so a Wireshark rename surfaces in CI rather than in the lab.

`install.sh` (Linux / macOS) and `install.ps1` (Windows) drop the profiles into the user's Wireshark configuration directory, with symlink and copy modes.

GitHub Actions CI runs the validator against the latest Wireshark stable and the 4.2 LTS line on every push.

MIT licensed.
