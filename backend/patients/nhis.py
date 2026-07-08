"""Simulated NHIS (National Health Insurance Scheme) verification."""

from datetime import date, timedelta

from datetime import date

from django.utils import timezone


def verify_nhis(nhis_number: str) -> dict:
    """
    Mock NHIS lookup. In production this would call the NHIA API.
    Demo rules:
      - Empty → invalid
      - Contains 'EXP' or ends with '000' → expired
      - Otherwise → active, renewed for 1 year
    """
    nhis = (nhis_number or "").strip().upper()
    if not nhis or len(nhis) < 6:
        return {
            "valid": False,
            "status": "unknown",
            "message": "NHIS number not found. Please check and try again.",
            "expiry_date": None,
            "member_name": None,
        }

    if "EXP" in nhis or nhis.endswith("000"):
        return {
            "valid": False,
            "status": "expired",
            "message": "NHIS membership has expired. Please renew at any NHIS office.",
            "expiry_date": (date.today() - timedelta(days=30)).isoformat(),
            "member_name": None,
        }

    expiry = date.today() + timedelta(days=365)
    return {
        "valid": True,
        "status": "active",
        "message": "NHIS membership is active and renewed.",
        "expiry_date": expiry.isoformat(),
        "member_name": None,
    }


def apply_nhis_verification(profile, nhis_number: str) -> dict:
    result = verify_nhis(nhis_number)
    profile.nhis_number = nhis_number
    profile.nhis_status = result["status"]
    if result["expiry_date"]:
        profile.nhis_expiry_date = date.fromisoformat(result["expiry_date"])
    if result["valid"]:
        profile.nhis_verified_at = timezone.now()
    profile.save()
    return result
