# All-in-one profile

The default profile to load when you don't yet know what's in your trace. Combines highlights from every specialized profile so a mixed-generation capture renders correctly without having to switch profiles.

## What it covers

Filters and color rules for: 5G SA (NGAP, NAS-5GS, HTTP/2 SBI), 5G NSA (X2-AP), 4G LTE (S1-AP, NAS-EPS, GTPv2), 3G UMTS (RANAP, MAP, GTPv1), user plane (PFCP, GTP-U), IMS voice (SIP, RTP/RTCP, Diameter Cx/Sh), and Wi-Fi calling (IKEv2, EAP-AKA, S2b GTPv2).

## When to use this vs a specialized profile

Use this when you're triaging an unknown trace or chasing a problem that crosses generations (VoLTE call dropping during 4G→5G handover, or a Wi-Fi-to-LTE switch). Switch to a specialized profile once you've localized the issue. The specialized ones have richer per-protocol filters and tighter coloring.

## Color scheme

Failures across all generations are red. Each generation gets its own background tint so the packet list reads as colored stripes by access type: 5G blue, 4G green, 3G purple, voice teal, user plane yellow, Wi-Fi calling indigo. Notable accept events (Registration Accept, Attach Accept, SIP 200) are green.
