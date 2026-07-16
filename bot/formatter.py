"""Bahasa Indonesia message formatting. Builds farmer-friendly text from the
recommendation *code* and the additive result keys (trend, cluster_size,
price_as_of, price_source) — never by parsing the English `reason` string
(ARCHITECTURE.md §2).
"""
from __future__ import annotations

CROP_LABELS = {"cabai_merah": "Cabai Merah", "bawang_merah": "Bawang Merah"}
REGION_LABELS = {"garut": "Garut", "cianjur": "Cianjur", "brebes": "Brebes"}

_HEADLINES = {
    "sell": "🟢 *REKOMENDASI: JUAL SEKARANG*",
    "hold": "🟡 *REKOMENDASI: JUAL SESUAI JADWAL BIASA*",
    "wait": "🔵 *REKOMENDASI: TUNGGU BEBERAPA HARI*",
}

_TREND_ID = {
    "rising": "harga sedang naik 📈",
    "falling": "harga sedang turun 📉",
    "flat": "harga stabil ➖",
}


def crop_label(key: str) -> str:
    return CROP_LABELS.get(key, key)


def region_label(key: str) -> str:
    return REGION_LABELS.get(key, key)


def format_recommendation_message(crop: str, region: str, days: int, rec: dict) -> str:
    lines = [_HEADLINES.get(rec["recommendation"], rec["recommendation"])]

    detail = []
    trend = rec.get("trend")
    if trend in _TREND_ID:
        detail.append(_TREND_ID[trend].capitalize())
    cluster = rec.get("cluster_size")
    if cluster and cluster > 1:
        detail.append(f"{cluster} petani panen {crop_label(crop).lower()} di "
                      f"{region_label(region)} dalam waktu berdekatan")
    if detail:
        lines.append("")
        lines.append("📊 " + ", dan ".join(detail) + ".")

    if rec["recommendation"] == "sell":
        lines.append("Jual sekarang sebelum pasokan menumpuk menekan harga.")
        if rec.get("match_request_id"):
            lines.append("✅ Penawaran Anda sudah diteruskan ke Pembeli Utama.")
    elif rec["recommendation"] == "wait":
        lines.append("Menunggu beberapa hari kemungkinan memberi harga lebih baik.")
    else:
        lines.append("Tidak ada tekanan pasar — jual sesuai rencana Anda.")

    as_of = rec.get("price_as_of")
    if as_of:
        src = "PIHPS (langsung)" if rec.get("price_source") == "pihps" else "data tersimpan"
        lines.append(f"\n_Harga per {as_of} ({src})._")
    return "\n".join(lines)


def format_buyer_match_message(match_id: int, farmer_name: str, crop: str,
                               region: str, harvest_date: str,
                               quantity_kg: float | None) -> str:
    qty = f"{quantity_kg:g} kg " if quantity_kg else ""
    return (
        f"📦 *Penawaran Panen Baru* (Match #{match_id})\n\n"
        f"Petani: *{farmer_name}*\n"
        f"Komoditas: *{qty}{crop_label(crop)}*\n"
        f"Wilayah: {region_label(region)}\n"
        f"Perkiraan panen: {harvest_date}\n\n"
        f"Terima penawaran ini?"
    )


_STATUS_ID = {"pending": "⏳ menunggu", "confirmed": "✅ diterima", "declined": "❌ ditolak"}


def format_coordinator_status(matches) -> str:
    if not matches:
        return "📋 Belum ada pencocokan tercatat."
    lines = ["📋 *Status Pencocokan:*\n"]
    for m in matches:
        qty = f"{m['quantity_kg']:g} kg " if m["quantity_kg"] else ""
        lines.append(
            f"#{m['id']} — {m['farmer_name']}: {qty}{crop_label(m['crop'])} "
            f"({region_label(m['region'])}, panen {m['harvest_date']}) — "
            f"{_STATUS_ID.get(m['status'], m['status'])}"
        )
    return "\n".join(lines)
