import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.core.config import settings

# Route Distance & Base Price Multipliers
ROUTE_BASE_PAIRS = {
    ("DEL", "BOM"): {"base_min": 3600, "base_max": 5200, "dist_km": 1150},
    ("DEL", "BLR"): {"base_min": 4200, "base_max": 6100, "dist_km": 1740},
    ("BOM", "BLR"): {"base_min": 2800, "base_max": 4100, "dist_km": 840},
    ("DEL", "CCU"): {"base_min": 3400, "base_max": 4900, "dist_km": 1305},
    ("BLR", "HYD"): {"base_min": 2200, "base_max": 3300, "dist_km": 500},
    ("MAA", "DEL"): {"base_min": 4100, "base_max": 5900, "dist_km": 1760},
    ("CCU", "BLR"): {"base_min": 3800, "base_max": 5400, "dist_km": 1560},
    ("DEL", "HYD"): {"base_min": 3300, "base_max": 4700, "dist_km": 1250},
    ("BOM", "GOI"): {"base_min": 2100, "base_max": 3200, "dist_km": 440},
    ("BLR", "MAA"): {"base_min": 1800, "base_max": 2700, "dist_km": 290},
    ("DEL", "PNQ"): {"base_min": 3500, "base_max": 5000, "dist_km": 1170},
    ("BOM", "AMD"): {"base_min": 2000, "base_max": 2900, "dist_km": 440},
}

CARRIER_PREMIUMS = {
    "IndiGo": 1.00,
    "Air India": 1.15,        # Full Service Carrier (meals/bags included)
    "Air India Express": 0.96,
    "Akasa Air": 0.94,        # Competitive new LCC
    "SpiceJet": 0.97
}

OTA_CONVENIENCE_FEES = {
    "Direct Airline": 0.0,
    "MakeMyTrip": 349.0,
    "Yatra": 325.0,
    "EaseMyTrip": 0.0,       # Zero convenience fee policy marketing
    "Cleartrip": 300.0,
    "Ixigo": 275.0
}

class HighFidelityAirfareGenerator:
    """
    Generates realistic, dynamic, time-series compliant Indian domestic airfare quotes.
    Models advance booking surge curves, airport UDF/PSF taxes, fuel surcharges,
    and carrier/OTA dynamic pricing behavior.
    """

    @staticmethod
    def calculate_advance_multiplier(advance_days: int) -> float:
        """
        Advance purchase lead-time elasticity curve:
        T+1: High last-minute surge (1.85x)
        T+7: Moderate surge (1.35x)
        T+15: Standard baseline (1.00x)
        T+30: Advance discount (0.85x)
        T+45: Early bird discount (0.75x)
        """
        if advance_days == 1:
            return random.uniform(1.70, 2.10)
        elif advance_days == 7:
            return random.uniform(1.25, 1.45)
        elif advance_days == 15:
            return random.uniform(0.95, 1.05)
        elif advance_days == 30:
            return random.uniform(0.80, 0.90)
        elif advance_days == 45:
            return random.uniform(0.70, 0.80)
        return 1.0

    def generate_quote(
        self,
        origin: str,
        destination: str,
        advance_days: int,
        carrier: str,
        source: str,
        target_date: datetime = None
    ) -> Dict[str, Any]:
        
        if target_date is None:
            target_date = datetime.utcnow() + timedelta(days=advance_days)

        pair_info = ROUTE_BASE_PAIRS.get((origin, destination), {"base_min": 3000, "base_max": 4500, "dist_km": 1000})
        
        # 1. Base fare calculation with distance & market variation
        raw_base = random.uniform(pair_info["base_min"], pair_info["base_max"])
        
        # 2. Advance booking multiplier
        adv_mult = self.calculate_advance_multiplier(advance_days)
        
        # 3. Carrier multiplier
        carrier_mult = CARRIER_PREMIUMS.get(carrier, 1.0)
        
        # 4. Day-of-week multiplier (Friday/Sunday weekend surge)
        dep_day = target_date.weekday()
        day_mult = 1.12 if dep_day in [4, 6] else (0.95 if dep_day == 1 else 1.0)

        # Base Fare calculation
        base_fare = round(raw_base * adv_mult * carrier_mult * day_mult, 2)

        # 5. Taxes & Statutory Surcharges (Fuel Surcharge ~ 22%, Airport UDF/PSF ~ ₹450, GST ~ 5%)
        fuel_surcharge = round(base_fare * 0.22, 2)
        udf_psf_tax = random.choice([380.0, 450.0, 520.0])
        gst_tax = round((base_fare + fuel_surcharge) * 0.05, 2)
        taxes_fees = round(fuel_surcharge + udf_psf_tax + gst_tax, 2)

        # 6. OTA Convenience Fee
        convenience_fee = OTA_CONVENIENCE_FEES.get(source, random.choice([250.0, 350.0]))

        # 7. Total fare
        total_fare = round(base_fare + taxes_fees + convenience_fee, 2)

        # Inject occasional synthetic outlier (0.5% probability) to test cleaner pipeline
        is_synthetic_glitch = random.random() < 0.005
        if is_synthetic_glitch:
            total_fare = total_fare * random.choice([10.0, 0.05]) # Extreme spike or zero fare error

        flight_num_prefix = {"IndiGo": "6E", "Air India": "AI", "Air India Express": "IX", "Akasa Air": "QP", "SpiceJet": "SG"}.get(carrier, "6E")
        flight_number = f"{flight_num_prefix}-{random.randint(101, 999)}"

        return {
            "source": source,
            "carrier": carrier,
            "origin": origin,
            "destination": destination,
            "flight_number": flight_number,
            "departure_date": target_date,
            "advance_days": advance_days,
            "base_fare": base_fare,
            "taxes_fees": taxes_fees,
            "convenience_fee": convenience_fee,
            "total_fare": total_fare,
            "currency": "INR",
            "fare_class": "Economy Standard"
        }

    def generate_full_basket_snapshot(self, scrape_date: datetime = None) -> List[Dict[str, Any]]:
        """
        Generates a comprehensive snapshot across all 12 city pairs, 5 advance lead-times,
        5 carriers, and 5 OTAs (over 1,500+ raw price quotes per execution batch).
        """
        quotes = []
        if scrape_date is None:
            scrape_date = datetime.utcnow()

        for pair in settings.CITY_PAIRS:
            origin = pair["origin"]
            destination = pair["destination"]

            for adv in settings.ADVANCE_WINDOWS:
                target_dep = scrape_date + timedelta(days=adv)

                for carrier in settings.AIRLINES:
                    # Direct Airline Quote
                    q_direct = self.generate_quote(origin, destination, adv, carrier, carrier, target_dep)
                    q_direct["scraped_at"] = scrape_date
                    quotes.append(q_direct)

                    # 1-2 Random OTA Quotes for parity checking
                    ota = random.choice(settings.OTAS)
                    q_ota = self.generate_quote(origin, destination, adv, carrier, ota, target_dep)
                    q_ota["scraped_at"] = scrape_date
                    quotes.append(q_ota)

        return quotes

mock_scraper = HighFidelityAirfareGenerator()
