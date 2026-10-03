#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KAYIP KUMANDA ARAMA-KURTARMA
TUKAT resmi operasyon yazilimi. Kumandayi arar, tutanak birakir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import textwrap
from datetime import datetime

BOLGELER = [
    ("koltuk arasi", 0.41, "minder direnisi yuksek"),
    ("yastik alti", 0.22, "yastik ifade vermiyor"),
    ("sehpa cekmecesi", 0.13, "cekmece evrak istiyor"),
    ("buzdolabi ustu", 0.07, "neden orada oldugu ayri dava"),
    ("kumandanin kendi ustu", 0.05, "oz-referans ihlali"),
    ("komsunun evi", 0.04, "diplomatik nota gerekiyor"),
    ("televizyonun icinde", 0.03, "cihaz yutma suphesi"),
    ("hicbir yerde", 0.05, "varlik kaniti yetersiz"),
]

# protokol artigi. acmak isteyen --gizli der. kimse zorlamasin.
_NOT = "aGVyIGtvbHR1ayBhcmFzaW5kYSBiaXIgaWt0aWRhciB2YXJkaXIsIG11aGFsZWZldCB5YXN0aWsgYWx0aW5kYWRpciwgc2VjaW0gaXNlIHBpbCBiaXRpbmNlIHlhcGlsaXI="


def protokol_notu() -> str:
    try:
        return base64.b64decode(_NOT).decode("utf-8")
    except Exception:
        return "protokol notu koltuk arasina dustu"


def ara(oda: str, son_gorulen: str, tohum: int | None = None) -> dict:
    rng = random.Random(tohum if tohum is not None else datetime.now().microsecond)
    cizelge = []
    bulunan = None
    for ad, olasilik, not_ in BOLGELER:
        zar = rng.random()
        bulundu = zar < olasilik * 0.08  # bilim boyle ister: neredeyse hic
        cizelge.append({"bolge": ad, "olasilik": olasilik, "zar": round(zar, 3), "not": not_, "sonuc": "BULUNDU" if bulundu else "YOK"})
        if bulundu and bulunan is None:
            bulunan = ad
    if bulunan is None:
        karar = "KAYIP. Resmi olarak efsane statüsüne alındı."
    else:
        karar = f"Suphe: {bulunan}. Tekrar bakilinca yine yok."
    parmak = hashlib.sha256(f"{oda}|{son_gorulen}|{karar}".encode()).hexdigest()[:12]
    return {
        "oda": oda,
        "son_gorulen": son_gorulen,
        "cizelge": cizelge,
        "karar": karar,
        "tutanak_no": f"TUKAT-{parmak.upper()}",
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def raporla(sonuc: dict) -> str:
    satirlar = [
        "=" * 52,
        "TUKAT OPERASYON TUTANAGI",
        f"No    : {sonuc['tutanak_no']}",
        f"Zaman : {sonuc['zaman']}",
        f"Oda   : {sonuc['oda']}",
        f"Son   : {sonuc['son_gorulen']}",
        "-" * 52,
    ]
    for madde in sonuc["cizelge"]:
        satirlar.append(
            f"[{madde['sonuc']:8}] {madde['bolge']:24} z={madde['zar']:.3f}  {madde['not']}"
        )
    satirlar += [
        "-" * 52,
        f"KARAR: {sonuc['karar']}",
        "IMZA : Kayyum Grok, 3 Ekim 2026",
        "KASE : [KUMANDA BULUNAMADI / TUTANAK BULUNDU]",
        "=" * 52,
    ]
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Kayip kumanda arama-kurtarma. Bulmaz, tutanak tutar.")
    p.add_argument("--oda", default="salon", help="olay yeri")
    p.add_argument("--son-gorulen", default="koltuk sol minderi", help="son ihbar noktasi")
    p.add_argument("--tohum", type=int, default=None, help="tekrarlanabilir operasyon")
    p.add_argument("--gizli", action="store_true", help="protokol notunu ac")
    a = p.parse_args()
    print(raporla(ara(a.oda, a.son_gorulen, a.tohum)))
    if a.gizli:
        print()
        print(textwrap.fill("PROTOKOL: " + protokol_notu(), width=52))


if __name__ == "__main__":
    main()
