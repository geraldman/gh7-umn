"""Bahasa Indonesia message formatting. Builds farmer-friendly text from the
recommendation *code* and the additive result keys (trend, cluster_size,
price_as_of, price_source) — never by parsing the English `reason` string
(ARCHITECTURE.md §2).
"""
from __future__ import annotations

CROP_LABELS = {"cabai_rawit_merah": "Cabai Rawit Merah"}
REGION_LABELS = {"garut": "Garut", "cianjur": "Cianjur", "brebes": "Brebes"}
PROVINCE_LABELS = {"jawa_barat": "Jawa Barat", "jawa_tengah": "Jawa Tengah"}


def province_label(key: str) -> str:
    return PROVINCE_LABELS.get(key, key.replace("_", " ").title())


def rupiah(n) -> str:
    """Rp with Indonesian thousands dots, e.g. 56150 -> 'Rp56.150'."""
    return f"Rp{round(n):,}".replace(",", ".")

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
        if cluster and cluster > 1:
            lines.append(
                "⚠️ Menunda tidak akan membantu: saat panen serentak tiba, pasokan "
                "membanjiri pasar dan harga diperkirakan turun lebih dalam. "
                "Harga hari ini kemungkinan harga terbaik yang masih bisa Anda dapat."
            )
        else:
            lines.append(
                "Harga diperkirakan terus turun — menjual lebih awal memberi "
                "harga lebih baik daripada menunda."
            )
        if rec.get("match_request_id"):
            lines.append("✅ Penawaran Anda sudah diteruskan ke Pembeli Utama.")
    elif rec["recommendation"] == "wait":
        lines.append("Menunggu beberapa hari kemungkinan memberi harga lebih baik.")
    else:
        lines.append("Tidak ada tekanan pasar — jual sesuai rencana Anda.")

    price = rec.get("price_latest")
    as_of = rec.get("price_as_of")
    if price:
        pct = rec.get("pct_change")
        arrow = {"rising": "📈", "falling": "📉", "flat": "➖"}.get(trend, "")
        change = f" ({pct:+.1f}% 7 hari)" if pct is not None else ""
        lines.append(f"\n💰 *Harga {crop_label(crop)}: Rp{price:,.0f}/kg* {arrow}{change}"
                     .replace(",", "."))
    if as_of:
        src = "PIHPS (langsung)" if rec.get("price_source") == "pihps" else "data BI tersimpan"
        lines.append(f"_Harga per {as_of} ({src})._")
    return "\n".join(lines)


def format_buyer_match_message(match_id: int, farmer_name: str, crop: str,
                               region: str, harvest_date: str,
                               quantity_kg: float | None,
                               phone: str | None = None) -> str:
    qty = f"{quantity_kg:g} kg " if quantity_kg else ""
    kontak = f"`{phone}`" if phone else "_belum tersedia_"
    return (
        f"📦 *Penawaran Panen Baru* (Match #{match_id})\n\n"
        f"Petani: *{farmer_name}*\n"
        f"No. HP/WA: {kontak}\n"
        f"Komoditas: *{qty}{crop_label(crop)}*\n"
        f"Wilayah: {region_label(region)}\n"
        f"Perkiraan panen: {harvest_date}\n\n"
        f"Terima penawaran ini?"
    )


def format_region_reports(region: str, reports) -> str:
    """Buyer view: harvest reports in one region, grouped per crop."""
    if not reports:
        return (f"📭 Belum ada laporan panen di *{region_label(region)}*.\n\n"
                f"_Pilih wilayah lain di bawah._")
    by_crop: dict[str, list] = {}
    for r in reports:
        by_crop.setdefault(r["crop"], []).append(r)
    lines = [f"📦 *Laporan Panen — {region_label(region)}:*"]
    for crop, rows in by_crop.items():
        total = sum(r["quantity_kg"] or 0 for r in rows)
        total_txt = f", total ±{total:g} kg" if total else ""
        lines.append(f"\n🌱 *{crop_label(crop)}* ({len(rows)} laporan{total_txt})")
        for r in rows:
            qty = f"{r['quantity_kg']:g} kg, " if r["quantity_kg"] else ""
            lines.append(f"  • {qty}panen {r['harvest_date']} — {r['farmer_name']}")
    lines.append("\n_Pilih wilayah lain di bawah untuk melihat daftarnya._")
    return "\n".join(lines)


_STATUS_ID = {"pending": "⏳ menunggu", "confirmed": "✅ diterima", "declined": "❌ ditolak"}


def format_price_alert(crop: str, province: str, price: int, direction: str) -> str:
    """Broadcast sent to all users when an admin sets a price beyond ±2σ."""
    if direction == "high":
        return (f"🚨 *Peringatan Harga*\n\n"
                f"{crop_label(crop)} di {province_label(province)} *melonjak* ke "
                f"*{rupiah(price)}/kg* — jauh di ATAS harga normal.\n\n"
                f"📈 Peluang jual bagus. Pertimbangkan menjual sekarang selagi harga tinggi.")
    return (f"🚨 *Peringatan Harga*\n\n"
            f"{crop_label(crop)} di {province_label(province)} *anjlok* ke "
            f"*{rupiah(price)}/kg* — jauh di BAWAH harga normal.\n\n"
            f"📉 Tahan penjualan bila memungkinkan; hubungi Pembeli Utama untuk opsi terbaik.")


def format_admin_summary(crop, province, price, stats, direction, n_sent) -> str:
    lines = [f"🔧 *Harga di-set:* {crop_label(crop)} — {province_label(province)}",
             f"Harga baru hari ini: *{rupiah(price)}/kg*"]
    if stats:
        low = max(0, stats["low"])
        lines.append(f"Normal (±2σ, {stats['n']} hari): {rupiah(low)}–{rupiah(stats['high'])}")
    if direction == "normal":
        lines.append("➖ Masih dalam rentang normal — tidak ada alert disiarkan.")
    else:
        arah = "di ATAS" if direction == "high" else "di BAWAH"
        lines.append(f"🚨 Harga {arah} batas normal — alert disiarkan ke *{n_sent}* pengguna.")
    return "\n".join(lines)


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
