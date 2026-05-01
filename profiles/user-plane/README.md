# User-plane profile

A cross-generation view of the data plane: PFCP on N4 (5G), GTPv2-C on S11/S5/S8 (4G), GTPv1 on Gn (3G), and GTP-U everywhere underneath.

## What it covers

- **PFCP**: full message-type table (1, 2, 5–12, 50–57), Apply Action flags (`forw` / `drop` / `buff` / `nocp` / `dupl`) so you can see at a glance whether a UPF is being told to forward or buffer, and rule-ID filters (PDR / FAR / QER / URR).
- **GTP-U**: G-PDU (255), Echo (1/2), Error Indication (26), with helpers to peek at the inner protocol (`gtp and tcp`, `gtp and dns`, etc.).
- **GTPv2-C**: Create / Modify / Delete Session and Bearer, which establish and tear down the GTP-U tunnels.

## When to load this profile

When you need to debug data flow, missing user traffic, or PFCP rule installation. Anywhere you'd otherwise be staring at a wall of UDP packets on ports 8805, 2123, or 2152.

## Notable: PFCP message-type field is `pfcp.msg_type`

The Wireshark dissector field is `pfcp.msg_type`, **not** `pfcp.message_type`. This is one of the easiest mistakes to make when copying filters from 3GPP specs (which use the long form). The validator catches this.

## Verifying it works

```bash
python validate.py --profile user-plane
```
