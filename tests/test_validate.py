from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate import PROFILES_DIR, collect_fields


def test_collect_fields_ignores_dotted_strings(tmp_path: Path) -> None:
    profile = tmp_path / "profile"
    profile.mkdir()
    (profile / "dfilters").write_text(
        '"Wi-Fi hint" sip.P-Access-Network-Info contains "IEEE-802.11"\n'
        '"IMS host" sip.r-uri.host contains "ims.mnc"\n'
    )
    (profile / "colorfilters").write_text(
        '@Wi-Fi error@sip.Status-Code >= 400 and '
        'sip.P-Access-Network-Info contains "IEEE-802.11"@[0,0,0][65535,0,0]\n'
    )
    (profile / "dfilter_buttons").write_text(
        '"TRUE","Wi-Fi","sip.P-Access-Network-Info contains \\"IEEE-802.11\\"","hint"\n'
    )

    fields = collect_fields(profile)

    assert "sip.P-Access-Network-Info" in fields
    assert "sip.r-uri.host" in fields
    assert "IEEE-802.11" not in fields
    assert "ims.mnc" not in fields


def test_user_plane_gtpv2_filters_use_current_field_names() -> None:
    fields = collect_fields(PROFILES_DIR / "user-plane")

    assert "gtpv2.f_teid.ipv4" not in fields
    assert "gtpv2.f_teid.ipv6" not in fields
    assert "gtpv2.bearer_id" not in fields
    assert "gtpv2.imsi" not in fields

    assert "gtpv2.f_teid_ipv4" in fields
    assert "gtpv2.f_teid_ipv6" in fields
    assert "gtpv2.ebi" in fields
