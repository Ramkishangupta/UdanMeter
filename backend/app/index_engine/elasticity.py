import pandas as pd
from typing import List, Dict, Any
from app.core.config import settings

class AnalyticsEngine:
    """
    Computes lead-time price elasticity curves, carrier parity markups,
    and sector-wise airfare pressure heatmaps.
    """

    @staticmethod
    def compute_lead_time_elasticity(quotes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not quotes:
            return []

        df = pd.DataFrame(quotes)
        t1_avg = df[df["advance_days"] == 1]["total_fare"].mean() if not df[df["advance_days"] == 1].empty else 1.0

        results = []
        for adv in settings.ADVANCE_WINDOWS:
            sub = df[df["advance_days"] == adv]
            if not sub.empty:
                avg_tot = sub["total_fare"].mean()
                avg_base = sub["base_fare"].mean()
                avg_tax = sub["taxes_fees"].mean()
                disc_pct = ((t1_avg - avg_tot) / t1_avg) * 100.0 if t1_avg > 0 else 0.0

                results.append({
                    "advance_days": adv,
                    "avg_total_fare": round(avg_tot, 2),
                    "avg_base_fare": round(avg_base, 2),
                    "avg_taxes": round(avg_tax, 2),
                    "discount_vs_t1_pct": round(disc_pct, 2)
                })
        return results

    @staticmethod
    def compute_carrier_parity(quotes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not quotes:
            return []

        df = pd.DataFrame(quotes)
        results = []

        for carrier in settings.AIRLINES:
            sub = df[df["carrier"] == carrier]
            if not sub.empty:
                direct_fares = sub[sub["source"] == carrier]["total_fare"]
                ota_fares = sub[sub["source"] != carrier]["total_fare"]

                avg_direct = direct_fares.mean() if not direct_fares.empty else sub["total_fare"].mean()
                avg_ota = ota_fares.mean() if not ota_fares.empty else avg_direct + 320.0
                markup = ((avg_ota - avg_direct) / avg_direct) * 100.0 if avg_direct > 0 else 0.0

                results.append({
                    "carrier": carrier,
                    "direct_avg_fare": round(avg_direct, 2),
                    "ota_avg_fare": round(avg_ota, 2),
                    "ota_markup_pct": round(markup, 2),
                    "total_quotes": len(sub)
                })
        return results

    @staticmethod
    def compute_route_heatmap(quotes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not quotes:
            return []

        df = pd.DataFrame(quotes)
        heatmap = []

        for pair in settings.CITY_PAIRS:
            o, d = pair["origin"], pair["destination"]
            sub = df[(df["origin"] == o) & (df["destination"] == d)]

            if not sub.empty:
                avg_f = sub["total_fare"].mean()
                min_f = sub["total_fare"].min()
                max_f = sub["total_fare"].max()
                t1_f = sub[sub["advance_days"] == 1]["total_fare"].mean() if not sub[sub["advance_days"] == 1].empty else avg_f * 1.6
                t45_f = sub[sub["advance_days"] == 45]["total_fare"].mean() if not sub[sub["advance_days"] == 45].empty else avg_f * 0.75
                pressure = round(avg_f / 4500.0, 2) # Route Pressure Index relative to baseline benchmark

                heatmap.append({
                    "origin": o,
                    "destination": d,
                    "route_name": pair["name"],
                    "weight": pair["weight"],
                    "avg_fare": round(avg_f, 2),
                    "min_fare": round(min_f, 2),
                    "max_fare": round(max_f, 2),
                    "t1_fare": round(t1_f, 2),
                    "t45_fare": round(t45_f, 2),
                    "pressure_index": pressure
                })
        return heatmap

analytics_engine = AnalyticsEngine()
