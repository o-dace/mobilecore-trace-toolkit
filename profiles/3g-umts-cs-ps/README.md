# 3G UMTS profile (CS + PS domains)

For analyzing 3G UMTS / WCDMA core traces. Iu interface (RANAP), MAP between core elements (HLR, VLR, MSC, SGSN), and GTPv1 on Gn for the packet domain.

## What it covers

- **RANAP** (Iu): initial UE message, direct transfer (NAS), RAB assignment, Iu release, paging, security mode.
- **MAP**: HLR signalling (Update Location 2, Send Authentication Info 56, Cancel Location 3, Insert Subscriber Data 7), SMS routing (SRI-for-SM 45, MO/MT-Forward 46/44), and Update GPRS Location 23. Operation codes are filterable via `gsm_old.opCode`. The Wireshark dissector keeps MAP opcodes under the legacy `gsm_old` namespace.
- **GTPv1-C** (Gn): Create / Update / Delete PDP Context (16/17, 18/19, 20/21), plus GTP-U (255) and Error Indication (26).
- **SCCP / M3UA**: the SS7-over-IP transport that carries MAP and RANAP.

## When to load this profile

When your trace is from a UMTS / 3G core. If your packets are SCTP-only with no SCCP / M3UA below RANAP, the dissector chain may need a Decode As nudge (see `decode_as_entries`).

## Verifying it works

```bash
python validate.py --profile 3g-umts-cs-ps
```
