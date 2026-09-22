from typing import Dict, Any

class FareNormalizer:
    """
    Decomposes total fare into Base Fare, Statutory Taxes (UDF, PSF, Fuel Surcharges),
    and Convenience Fees across various airline and OTA quotes.
    """

    @staticmethod
    def normalize_quote(quote: Dict[str, Any]) -> Dict[str, Any]:
        total = quote.get("total_fare", 0.0)
        base = quote.get("base_fare", 0.0)
        taxes = quote.get("taxes_fees", 0.0)
        conv = quote.get("convenience_fee", 0.0)

        # If base fare or taxes are missing, estimate standard MoSPI breakdown
        if base == 0.0 and total > 0.0:
            conv = 300.0 if quote.get("source") not in quote.get("carrier") else 0.0
            net = max(0.0, total - conv)
            base = round(net * 0.75, 2)
            taxes = round(net * 0.25, 2)

        quote["base_fare"] = base
        quote["taxes_fees"] = taxes
        quote["convenience_fee"] = conv
        quote["total_fare"] = round(base + taxes + conv, 2)
        return quote

fare_normalizer = FareNormalizer()
