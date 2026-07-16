"""
Rule Engine Interface.
Contains the get_recommendation function. When Developer A's engine is ready,
you can import the real implementation here or swap the call in get_recommendation().
"""

def _mock_get_recommendation(crop: str, days_to_harvest: int) -> dict:
    """Mock implementation of the rule engine recommendation logic."""
    crop_lower = crop.lower().strip()
    
    if "padi" in crop_lower or "rice" in crop_lower:
        if days_to_harvest > 60:
            return {
                "recommendation": "Lakukan pemupukan pertama menggunakan Urea dan SP-36.",
                "reason": f"Tanaman padi Anda masih dalam fase vegetatif awal ({days_to_harvest} hari menuju panen), membutuhkan nutrisi nitrogen yang cukup untuk pertumbuhan daun."
            }
        elif 20 < days_to_harvest <= 60:
            return {
                "recommendation": "Kurangi debit air sawah dan lakukan pemupukan susulan NPK.",
                "reason": f"Fase ini ({days_to_harvest} hari menuju panen) adalah fase pengisian bulir padi, membutuhkan kalium tinggi untuk kualitas gabah."
            }
        else:
            return {
                "recommendation": "Keringkan sawah sepenuhnya dan siapkan alat panen.",
                "reason": f"Hanya tersisa {days_to_harvest} hari menuju panen. Pengeringan sawah mempercepat pematangan bulir secara seragam."
            }
            
    elif "cabai" in crop_lower or "chili" in crop_lower:
        if days_to_harvest > 30:
            return {
                "recommendation": "Semprotkan pestisida nabati secara berkala dan jaga kelembapan tanah.",
                "reason": f"Tanaman cabai berumur {days_to_harvest} hari sebelum panen rentan terhadap serangan hama kutu daun."
            }
        else:
            return {
                "recommendation": "Hentikan penyemprotan pestisida kimia dan lakukan pemetikan buah matang saja.",
                "reason": f"Mendekati masa panen ({days_to_harvest} hari), residu pestisida kimia pada cabai harus dihindari demi kesehatan konsumen."
            }
            
    # Default recommendation for other crops
    if days_to_harvest > 30:
        return {
            "recommendation": "Lakukan penyiraman rutin di pagi hari dan berikan pupuk kompos.",
            "reason": f"Tanaman {crop} memiliki sisa waktu tumbuh yang cukup lama ({days_to_harvest} hari), nutrisi organik membantu pertumbuhan akar."
        }
    else:
        return {
            "recommendation": "Jaga sanitasi lahan dan bersiap untuk pemanenan.",
            "reason": f"Masa panen tanaman {crop} kurang dari sebulan ({days_to_harvest} hari). Menjaga kebersihan lahan mencegah penularan penyakit pasca-panen."
        }

def get_recommendation(crop: str, days_to_harvest: int) -> dict:
    """
    Main entry point for recommendation engine.
    Contract: Returns dict with keys 'recommendation' and 'reason'.
    """
    # TODO: Once Developer A's rule engine is ready, swap the line below with:
    # from developer_a_module import get_recommendation as real_get_recommendation
    # return real_get_recommendation(crop, days_to_harvest)
    
    return _mock_get_recommendation(crop, days_to_harvest)
