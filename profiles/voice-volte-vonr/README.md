# Voice (VoLTE / VoNR) profile

Unified IMS voice analysis covering Voice over LTE, Voice over NR, and the common SIP+RTP machinery underneath. Wi-Fi calling shares the same signalling plane and is also covered here. There's a dedicated `voice-wifi-calling` profile when you specifically need the IKEv2 / IPsec access view.

## What it covers

- **SIP**: REGISTER, INVITE, ACK, BYE, CANCEL, UPDATE, PRACK, REFER, NOTIFY, MESSAGE; the full set of 1xx/2xx/3xx/4xx/5xx/6xx response classes; the IMS-specific `P-Asserted-Identity`, `P-Associated-URI`, `P-Access-Network-Info`, `P-Charging-Vector` headers.
- **RTP / RTCP**: heuristic decode picks up dynamic-port media, with payload-type filters for AMR-NB / AMR-WB / EVS, marker-bit detection for talk-spurt boundaries, and RTCP SR/RR/BYE filters.
- **Diameter Cx** (S-CSCF ↔ HSS, app-id 16777216): MAR (303), SAR (301), UAR (300), LIR (302), PPR (305), RTR (304).
- **Diameter Sh** (AS ↔ HSS, app-id 16777217): UDR (306), PUR (307), SNR (308), PNR (309).

## Telling VoLTE / VoNR / Wi-Fi calling apart

The signalling is identical SIP. The discriminator is the `P-Access-Network-Info` header on UE-originated requests:

- `3GPP-E-UTRAN-FDD; utran-cell-id-3gpp=...` → VoLTE
- `3GPP-NR; nr-cell-id-3gpp=...` → VoNR
- `IEEE-802.11; ...` → Wi-Fi calling (untrusted access via ePDG)

The toolkit ships filter buttons (`VoLTE`, `VoNR`, `Wi-Fi`) that key off this exact field.

## Column layout

The packet list shows Method or Status-Code, Call-ID (truncated), From-user, To-user, which is enough to follow a call by eye without opening dialogs.

## When to load this profile

Whenever your trace contains SIP. Wireshark's heuristic SIP detection is good, but if your IMS deployment uses non-default ports add them via `Decode As`.

## Verifying it works

```bash
python validate.py --profile voice-volte-vonr
```
