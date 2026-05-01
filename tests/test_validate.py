from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate import PROFILES_DIR, collect_fields

CI_REPORTED_STALE_FIELDS = {
    "gtp.imsi",
    "gtp.msisdn",
    "gtpv2.msisdn",
    "nas_eps.emm.cause",
    "nas_eps.esm.cause",
    "nas_eps.nas_msg_emm_type",
    "nas_eps.nas_msg_esm_type",
    "ngap.UnsuccessfulOutcome_element",
    "x2ap.NeweNB_UE_X2AP_ID",
    "x2ap.OldeNB_UE_X2AP_ID",
}


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


def test_profiles_do_not_reference_ci_reported_stale_fields() -> None:
    offenders: dict[str, list[str]] = {}
    for profile_dir in PROFILES_DIR.iterdir():
        if not profile_dir.is_dir():
            continue
        stale = sorted(collect_fields(profile_dir) & CI_REPORTED_STALE_FIELDS)
        if stale:
            offenders[profile_dir.name] = stale

    assert offenders == {}
