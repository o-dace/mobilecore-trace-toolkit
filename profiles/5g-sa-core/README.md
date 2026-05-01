# 5G SA Core profile

For analyzing 5G Standalone control-plane traces between gNB, AMF, SMF, NRF, AUSF, UDM, and PCF.

## What it covers

- **NGAP** (N2 / gNB ↔ AMF): registrations, handovers, PDU session resource setup, UE context release.
- **NAS-5GS**: both 5GMM (mobility) and 5GSM (PDU sessions), surfaced via dedicated filters and a custom column.
- **HTTP/2 SBI**: `/namf-*`, `/nsmf-*`, `/nausf-*`, `/nudm-*`, `/nnrf-*`, `/npcf-*`. JSON bodies are decoded automatically.

## When to load this profile

Load it when your trace is dominated by SCTP (port 38412) or HTTP/2 traffic between core network functions. If you're looking at packet data on N3 or N9, use `user-plane` instead. If your packets show X2-AP or S1-AP, your trace is 4G or 5G NSA, so switch to `4g-lte-epc` or `5g-nsa-endc`.

## Highlights

- Custom column shows whichever of 5GMM, 5GSM, or NGAP message type is present, so the packet list reads like a call flow.
- Coloring rules surface failures (5GMM / 5GSM cause IEs and any NGAP unsuccessful outcome) before bulk signalling.
- Filter buttons for the common slice-and-dice operations: `Registration`, `Auth`, `SecMode`, `PDU Sess`, `Failures`.

## Verifying it works

```bash
python validate.py --profile 5g-sa-core
```

Field names like `nas-5gs.mm.message_type` and `ngap.procedureCode` are verified against the Wireshark dissector reference shipped with this repo. Running the validator against your local Wireshark installation will warn if any field has been renamed in your version.
