"""TCMB Rates: today's official exchange rates from the Central Bank of the Republic of Turkey.

Adds the tool `tcmb_rates` (source: https://www.tcmb.gov.tr/kurlar/today.xml). Rates are in TRY.
"""
import xml.etree.ElementTree as ET

import httpx

from ada import kernel

URL = "https://www.tcmb.gov.tr/kurlar/today.xml"


def _num(node, tag):
    v = (node.findtext(tag) or "").strip()
    try:
        return float(v)
    except ValueError:
        return None


def parse(xml_text: str, codes: list[str] | None = None) -> str:
    root = ET.fromstring(xml_text)
    date = root.get("Date") or root.get("Tarih") or ""
    want = {c.strip().upper() for c in codes or [] if c.strip()}
    rows = []
    for cur in root.findall("Currency"):
        code = (cur.get("CurrencyCode") or cur.get("Kod") or "").upper()
        if want and code not in want:
            continue
        unit = cur.findtext("Unit") or "1"
        rows.append(f"| {code} | {unit} | {_num(cur, 'ForexBuying') or '-'} | {_num(cur, 'ForexSelling') or '-'} "
                    f"| {_num(cur, 'BanknoteSelling') or '-'} | {(cur.findtext('CurrencyName') or '').strip()} |")
    if not rows:
        return f"No rates found for: {', '.join(sorted(want))}" if want else "TCMB returned no rates."
    head = (f"TCMB indicative rates ({date}), TRY per unit\n\n| Code | Unit | Forex buying | Forex selling "
            "| Banknote selling | Name |\n|---|---|---|---|---|---|")
    return head + "\n" + "\n".join(rows)


@kernel.tool(
    "tcmb_rates",
    "Today's official TCMB (Central Bank of Turkey) exchange rates in TRY. Optionally filter by currency codes.",
    {"codes": {"type": "array", "items": {"type": "string"}, "description": "e.g. [\"USD\", \"EUR\"]; empty = all"}},
)
async def tcmb_rates(codes: list[str] | None = None) -> str:
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as c:
        r = await c.get(URL)
        r.raise_for_status()
    return parse(r.text, codes)
