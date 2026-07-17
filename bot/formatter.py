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
    """Buyer view: harvest reports in one region, grouped per crop, showing
    how much stock is left (quantity − already sold)."""
    if not reports:
        return (f"📭 Belum ada laporan panen di *{region_label(region)}*.\n\n"
                f"_Pilih wilayah lain di bawah._")
    by_crop: dict[str, list] = {}
    for r in reports:
        by_crop.setdefault(r["crop"], []).append(r)
    lines = [f"📦 *Laporan Panen — {region_label(region)}:*"]
    for crop, rows in by_crop.items():
        remaining_total = sum(max(0, (r["quantity_kg"] or 0) - (r.get("sold_kg") or 0))
                              for r in rows)
        lines.append(f"\n🌱 *{crop_label(crop)}* ({len(rows)} laporan, "
                     f"sisa ±{remaining_total:g} kg)")
        for r in rows:
            qty = r["quantity_kg"] or 0
            remaining = qty - (r.get("sold_kg") or 0)
            if qty and remaining <= 0:
                stat = "🔴 TERJUAL HABIS"
            elif r.get("sold_kg"):
                stat = f"sisa {remaining:g}/{qty:g} kg"
            elif qty:
                stat = f"{qty:g} kg"
            else:
                stat = "jumlah -"
            lines.append(f"  • {stat}, panen {r['harvest_date']} — {r['farmer_name']}")
    lines.append("\n_Pilih wilayah lain, atau tekan 🛒 Beli di bawah._")
    return "\n".join(lines)


def format_fill_plan(region: str, target: float, allocations: list, shortfall: float) -> str:
    """EDF buy plan: which farmers to combine to fill `target` kg."""
    got = target - shortfall
    lines = [f"🛒 *Rencana pembelian* di {region_label(region)} — "
             f"diminta {target:g} kg, tersedia {got:g} kg:", ""]
    for a in allocations:
        r = a["report"]
        phone = f"`{r['farmer_phone']}`" if r.get("farmer_phone") else "_belum ada_"
        lines.append(f"• Ambil *{a['take_kg']:g} kg* dari *{r['farmer_name']}* "
                     f"(panen {r['harvest_date']}, stok {r['remaining_kg']:g} kg) — 📞 {phone}")
    if shortfall > 0:
        lines.append(f"\n⚠️ Kurang {shortfall:g} kg — stok di wilayah ini tidak mencukupi.")
    lines.append("\n_Urutan: panen paling awal didahulukan (paling cepat busuk)._")
    lines.append("Konfirmasi pembelian?")
    return "\n".join(lines)


def format_seller_sold_notification(crop, take_kg, remaining_kg, price) -> str:
    """Sent to a farmer when a buyer confirms buying part/all of their stock."""
    lines = ["💰 *Stok Anda Terjual!*",
             f"{crop_label(crop)}: *{take_kg:g} kg* dibeli oleh Pembeli Utama."]
    if price:
        lines.append(f"Harga pasar saat ini: *{rupiah(price)}/kg*.")
    if remaining_kg <= 0:
        lines.append("✅ Semua stok Anda sudah *TERJUAL HABIS*. Pembeli akan menghubungi Anda.")
    else:
        lines.append(f"Sisa stok Anda: *{remaining_kg:g} kg*. Pembeli akan menghubungi Anda.")
    return "\n".join(lines)


def format_purchase_result(rows: list) -> str:
    """After a confirmed buy: contacts + remaining/sold-out per farmer.
    `rows`: dicts with take_kg, farmer_name, farmer_phone, remaining_kg."""
    lines = ["✅ *Pembelian dikonfirmasi.* Silakan hubungi petani berikut:", ""]
    for a in rows:
        phone = f"`{a['farmer_phone']}`" if a.get("farmer_phone") else "_belum ada_"
        status = "🔴 TERJUAL HABIS" if a["remaining_kg"] <= 0 else f"sisa {a['remaining_kg']:g} kg"
        lines.append(f"• *{a['farmer_name']}* — beli {a['take_kg']:g} kg — "
                     f"📞 {phone} ({status})")
    return "\n".join(lines)


_STATUS_ID = {"pending": "⏳ menunggu", "confirmed": "✅ diterima", "declined": "❌ ditolak"}


def format_help() -> str:
    """User-facing command list. /admin is intentionally omitted."""
    return (
        "🌾 *Panen Pas — Daftar Perintah*\n\n"
        "/start — Mulai & pilih peran (Petani / Pembeli / Koordinator)\n"
        "/panen — _(Pembeli)_ Lihat laporan panen per wilayah\n"
        "/status — _(Koordinator)_ Lihat semua pencocokan\n"
        "/cancel — Batalkan proses yang sedang berjalan\n"
        "/help — Tampilkan pesan ini\n\n"
        "👨‍🌾 *Petani:* ketik /start lalu ikuti langkahnya untuk melaporkan panen "
        "dan menerima rekomendasi jual."
    )


def format_price_alert(crop: str, province: str, price: int, direction: str) -> str:
    """Broadcast sent to all users when an admin sets a price: spike (high),
    crash (low), or a reassuring stable note (normal)."""
    if direction == "high":
        return (f"🚨 *Peringatan Harga*\n\n"
                f"{crop_label(crop)} di {province_label(province)} *melonjak* ke "
                f"*{rupiah(price)}/kg* — jauh di ATAS harga normal.\n\n"
                f"📈 Peluang jual bagus. Pertimbangkan menjual sekarang selagi harga tinggi.")
    if direction == "low":
        return (f"🚨 *Peringatan Harga*\n\n"
                f"{crop_label(crop)} di {province_label(province)} *anjlok* ke "
                f"*{rupiah(price)}/kg* — jauh di BAWAH harga normal.\n\n"
                f"📉 Tahan penjualan bila memungkinkan; hubungi Pembeli Utama untuk opsi terbaik.")
    return (f"📊 *Info Harga*\n\n"
            f"{crop_label(crop)} di {province_label(province)} *stabil* di "
            f"*{rupiah(price)}/kg* — masih dalam rentang normal.\n\n"
            f"➖ Tidak ada tekanan pasar. Jual sesuai jadwal biasa Anda.")


def format_admin_summary(crop, province, price, stats, direction, n_sent) -> str:
    lines = [f"🔧 *Harga di-set:* {crop_label(crop)} — {province_label(province)}",
             f"Harga baru hari ini: *{rupiah(price)}/kg*"]
    if stats:
        low = max(0, stats["low"])
        lines.append(f"Normal (±2σ, {stats['n']} hari): {rupiah(low)}–{rupiah(stats['high'])}")
    if direction == "normal":
        lines.append(f"➖ Harga stabil (dalam rentang normal) — info disiarkan ke *{n_sent}* pengguna.")
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
