# 4G LTE EPC profile

For analyzing LTE Evolved Packet Core control-plane traces. S1, S11, S5/S8, and S6a all in one view.

## What it covers

- **S1-AP** between eNodeB and MME (SCTP 36412).
- **NAS-EPS** EMM and ESM, surfaced via dedicated filters and a custom column. The dissector field names are `nas_eps.nas_msg_emm_type` and `nas_eps.nas_msg_esm_type`. Note the underscore form differs from the 5G profile, which uses dotted `nas-5gs.mm.message_type`.
- **GTPv2-C** on S11 (MME ↔ SGW) and S5/S8 (SGW ↔ PGW): Create Session, Modify Bearer, Delete Session, Create / Update / Delete Bearer.
- **Diameter S6a** (Application-Id 16777251) for the MME ↔ HSS interface, with command codes for ULR (316), AIR (318), CLR (317), IDR (319), NOR (323), PUR (321).

## Column layout

The packet list shows separate columns for EMM/ESM message type, S1AP procedure code or GTPv2 message type, and Diameter command code, so an attach flow reads as a single annotated story.

## When to load this profile

Whenever your trace is dominated by S1-AP signalling and the NAS layer is EPS rather than 5GS. If you also see X2-AP and `RRCConnectionReconfiguration` with secondary cell config, switch to `5g-nsa-endc`.

## Verifying it works

```bash
python validate.py --profile 4g-lte-epc
```
