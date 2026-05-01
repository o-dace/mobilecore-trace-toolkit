# 5G NSA / EN-DC profile

For 5G Non-Standalone deployments where 5G NR is added as a secondary cell on top of an LTE anchor (Option 3, 3a, 3x in 3GPP terms).

## What it covers

- **X2-AP** between MeNB (master eNB) and SgNB (secondary gNB): secondary node addition, modification, release, and X2 handover.
- **S1-AP** for the LTE anchor leg: initial context setup, E-RAB modification (which is how the LTE bearer is reconfigured for split bearers), and path switch.
- **NAS-EPS** carrying ESM messages that update bearers when EN-DC is added or torn down.
- **LTE-RRC + NR-RRC** carried inside X2-AP `RRC-Container` IEs.

## The EN-DC tell

The signature of EN-DC is the X2 `SgNBAdditionRequest` procedure. Anywhere you see `x2ap.SgNBAdditionRequest_element` you're looking at a UE getting its 5G secondary cell. The associated `RRC-ConfigIndication` and `RRCReconfiguration` carry the NR cell parameters.

## When to load this profile

Load it when your trace has SCTP on ports 36412 (S1) and 36422 (X2). If you only see one or the other you don't need EN-DC view; use `4g-lte-epc` for S1 alone.

## Verifying it works

```bash
python validate.py --profile 5g-nsa-endc
```
