# Voice (Wi-Fi calling) profile

For analyzing untrusted-WLAN access to the IMS, what 3GPP calls VoWi-Fi or EPC integrated Wi-Fi, through an Evolved Packet Data Gateway (ePDG).

## What it covers

- **IKEv2** on the SWu interface (UE ↔ ePDG, UDP 500 or 4500 with NAT-T): IKE_SA_INIT (34), IKE_AUTH (35), CREATE_CHILD_SA (36), INFORMATIONAL (37), plus a curated list of error Notify codes (NO_PROPOSAL_CHOSEN, AUTHENTICATION_FAILED, INVALID_SYNTAX, INTERNAL_ADDRESS_FAILURE).
- **EAP-AKA / EAP-AKA'** (Type 23 / 50) carried inside IKE_AUTH for UE authentication against the HSS.
- **GTPv2-C on S2b** (ePDG ↔ PGW): the bearer that hangs the Wi-Fi attachment off the EPC. RAT type is WLAN (3).
- **ESP** for the ciphered tunnel content. With a debug PGW you can match on `esp.protocol` to see the inner protocol.
- **SIP** filtered specifically when carrying `P-Access-Network-Info: IEEE-802.11`, so REGISTER / INVITE traffic over Wi-Fi is highlighted.

## When to load this profile

When troubleshooting Wi-Fi calling registration or call setup. Common signs you're in the right place:

- Lots of UDP 4500 (ESP-in-UDP after NAT-T detection)
- IKE_SA_INIT followed by IKE_AUTH carrying EAP payloads
- A subsequent GTPv2 Create Session Request from the ePDG to the PGW with `gtpv2.rat_type == 3` (WLAN)

If voice over Wi-Fi is set up via a trusted access path (S2a) instead, the GTPv2 RAT type and IE set are similar but the IKEv2 layer is replaced. Load `voice-volte-vonr` instead.

## Verifying it works

```bash
python validate.py --profile voice-wifi-calling
```
