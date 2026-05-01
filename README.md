# mobilecore-trace-toolkit

Wireshark profiles for analyzing mobile core traces across 3G, 4G, 5G NSA, 5G SA, IMS voice (VoLTE / VoNR), and Wi-Fi calling. Includes a small validator that catches dissector field renames in CI before they ruin a debugging session.

Each profile ships with curated display filters, color rules, filter buttons, capture filters, decode-as overrides, and a column layout tuned to the protocols it covers.

## What's in here

| Profile | Covers | Reach for it when |
|:---|:---|:---|
| [`5g-sa-core`](profiles/5g-sa-core) | NGAP, NAS-5GS, HTTP/2 SBI | SCTP on 38412 or HTTP/2 between AMF/SMF/NRF/AUSF/UDM |
| [`5g-nsa-endc`](profiles/5g-nsa-endc) | X2-AP, S1-AP, LTE-RRC, NR-RRC | EN-DC traces; the giveaway is X2 `SgNBAdditionRequest` |
| [`4g-lte-epc`](profiles/4g-lte-epc) | S1-AP, NAS-EPS, GTPv2-C, Diameter S6a | LTE attach, TAU, bearer setup, HSS auth |
| [`3g-umts-cs-ps`](profiles/3g-umts-cs-ps) | RANAP (Iu), MAP, SCCP/M3UA, GTPv1 | UMTS / WCDMA core |
| [`voice-volte-vonr`](profiles/voice-volte-vonr) | SIP, RTP/RTCP, Diameter Cx/Sh | IMS voice on any access. P-Access-Network-Info filters split VoLTE / VoNR / Wi-Fi |
| [`voice-wifi-calling`](profiles/voice-wifi-calling) | IKEv2, EAP-AKA', ESP, GTPv2 S2b | ePDG / SWu untrusted-WLAN access |
| [`user-plane`](profiles/user-plane) | PFCP (N4), GTP-U, GTPv2-C | Data-plane debugging across generations |
| [`all-in-one`](profiles/all-in-one) | Highlights from every profile | Triaging an unknown trace |

## Install

### Linux / macOS

```bash
git clone https://github.com/o-dace/mobilecore-trace-toolkit.git
cd mobilecore-trace-toolkit
./install.sh             # symlinks profiles into ~/.config/wireshark/profiles
./install.sh --copy      # frozen copies instead of symlinks
./install.sh --uninstall
```

### Windows

```powershell
git clone https://github.com/o-dace/mobilecore-trace-toolkit.git
cd mobilecore-trace-toolkit
.\install.ps1            # copies to %APPDATA%\Wireshark\profiles
.\install.ps1 -Uninstall
```

After installing, open Wireshark and pick a profile from the bottom-right of the status bar.

## Validate

`validate.py` parses every display-filter expression across every profile, extracts each `proto.field` token, and cross-checks it against your local `tshark -G fields` output. CI runs the same check on every push against the `tshark` package available on the GitHub Actions Ubuntu runner and prints the exact version it used.

```bash
python validate.py                  # every profile
python validate.py --profile 5g-sa-core
python validate.py --no-tshark      # parser-only sanity check
```

This catches the most common breakage mode for shared Wireshark profiles: a field name renamed or removed across versions, which fails silently in the GUI (the filter just never matches).

## Wireshark dissector field naming gotchas

Wireshark's field names aren't always what you'd guess from the 3GPP spec. A few that catch people out, all enforced by the validator:

- 5G NAS uses dotted dashes: `nas-5gs.mm.message_type`
- 4G NAS uses a dashed protocol prefix and underscored message fields: `nas-eps.nas_msg_emm_type`
- PFCP message type is `pfcp.msg_type`, not `pfcp.message_type`
- 3G MAP operation codes live under the legacy namespace `gsm_old.opCode`, not `gsm_map.opCode`
- NGAP / S1AP / X2AP procedures use `_element` suffixes (e.g. `ngap.InitialUEMessage_element`) rather than encoding procedure presence as `procedureCode == N`

If your filters silently match nothing in newer Wireshark, run the validator. It will tell you which field name moved.

## Supported Wireshark versions

Designed for modern Wireshark 4.x releases. The safest compatibility check is to run `python validate.py` against the exact `tshark` version installed on the workstation or trace-analysis VM where you will use the profiles. Older versions may be missing fields like `x2ap.SgNBAdditionRequest_element` (added when EN-DC dissection landed) or much of `pfcp.*` (added in 2.6+).

## Contributing

PRs welcome. The validator runs in CI, so you'll get immediate feedback if a field name needs adjusting against the version it tests on.

## License

MIT, see [LICENSE](LICENSE).
