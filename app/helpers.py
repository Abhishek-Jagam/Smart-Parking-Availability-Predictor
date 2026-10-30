"""
ParkWise - Consumer Parking App Helper Functions
Pure business logic for user-friendly name mappings, status translations,
predictive alternative suggestions, best arrival times, and hour profiles.
"""

from typing import Dict, List, Tuple, Any, Optional
import datetime
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Friendly Car Park Names & Metadata
# ---------------------------------------------------------------------------
FRIENDLY_NAMES: Dict[str, str] = {
    "BHMBCCMKT01": "Markets Car Park (Moat Lane)",
    "BHMBCCPST01": "Pershore Street Car Park",
    "BHMBCCSNH01": "Snow Hill Station Car Park",
    "BHMBCCTHL01": "Town Hall (Brunel Street)",
    "BHMBRCBRG01": "Bullring Centre (Moor Street)",
    "BHMBRCBRG02": "Bullring Centre (Edgbaston St)",
    "BHMBRCBRG03": "Bullring Centre (Park Street)",
    "BHMBRTARC01": "The Arcadian Centre (Hurst St)",
    "BHMEURBRD01": "Euro Car Park (Broad Street)",
    "BHMEURBRD02": "Euro Car Park (Bishopsgate)",
    "BHMMBMMBX01": "Mailbox Multi-Storey (Royal Mail)",
    "BHMNCPHST01": "NCP High Street Car Park",
    "BHMNCPLDH01": "NCP Londonderry House",
    "BHMNCPNHS01": "NCP New Street Station",
    "BHMNCPNST01": "NCP Navigation Street",
    "BHMNCPPLS01": "NCP Palace Multi-Storey",
    "BHMNCPRAN01": "NCP Royal Angus (St Chads)",
    "Broad Street": "Broad Street Central",
    "Bull Ring": "Bull Ring Underground",
    "NIA Car Parks": "Utilita Arena (Main Parking)",
    "NIA North": "Utilita Arena (North Car Park)",
    "NIA South": "Utilita Arena (South Car Park)",
    "Others-CCCPS105a": "Coventry Road Public Bay",
    "Others-CCCPS119a": "Digbeth High Street Bay",
    "Others-CCCPS133": "Jewellery Quarter (Vyse St)",
    "Others-CCCPS135a": "St Paul's Square Pay & Display",
    "Others-CCCPS202": "Ludgate Hill Parking",
    "Others-CCCPS8": "Aston University Visitor Bay",
    "Others-CCCPS98": "Gosta Green Public Bay",
    "Shopping": "Grand Central Shopping Parking",
}

REVERSE_FRIENDLY_NAMES: Dict[str, str] = {v: k for k, v in FRIENDLY_NAMES.items()}


def get_display_name(code: str) -> str:
    """Return friendly display name for a car park code."""
    return FRIENDLY_NAMES.get(code, code)


def get_system_code(display_name: str) -> str:
    """Return original system code for a friendly display name."""
    return REVERSE_FRIENDLY_NAMES.get(display_name, display_name)


# ---------------------------------------------------------------------------
# 2. Driver Status Translations & Formatting
# ---------------------------------------------------------------------------
# Consumer statuses:
# 1. "Easy to park" (Available / <50%)
# 2. "Filling up"   (Nearly Full / 50% - 79%)
# 3. "Likely full"  (Full / >=80%)

def translate_status(raw_class: str) -> Tuple[str, str, str, str]:
    """
    Translates raw ML target class into consumer-facing plain language.
    
    Returns:
        verdict: "Easy to park" | "Filling up" | "Likely full"
        chip_css: "status-easy" | "status-filling" | "status-full"
        badge_class: "status-pill-easy" | "status-pill-filling" | "status-pill-full"
        icon: Accessible symbol representing the state
    """
    if raw_class == "Available":
        return "Easy to park", "status-easy", "status-pill-easy", "●"
    elif raw_class == "Nearly Full":
        return "Filling up", "status-filling", "status-pill-filling", "▲"
    else:
        return "Likely full", "status-full", "status-pill-full", "■"


def get_typical_reason(hour: int, is_weekend: bool, verdict: str) -> str:
    """Provides a brief, natural language explanation for drivers."""
    if verdict == "Easy to park":
        if hour < 10:
            return "Early morning traffic is light, plenty of spaces remain open."
        elif hour >= 15:
            return "Afternoon rush has calmed down with steady vehicle departures."
        else:
            return "Steady turnover and consistent turnover across bays right now."
    elif verdict == "Filling up":
        if is_weekend:
            return "Weekend shoppers and visitors are arriving steadily."
        elif 11 <= hour <= 14:
            return "Midday lunch and business traffic is peaking around this time."
        else:
            return "Spaces are turning over, but finding a bay may take a few minutes."
    else:  # Likely full
        if 11 <= hour <= 14:
            return "Busiest hours of the day with very high demand and minimal turnover."
        elif is_weekend:
            return "Heavy weekend congestion in this area; spaces fill rapidly."
        else:
            return "Consistently near capacity during this time window."


# ---------------------------------------------------------------------------
# 3. Model Feature Builder
# ---------------------------------------------------------------------------
def build_feature_row(
    carpark_code: str,
    target_dt: datetime.datetime,
    capacity: int,
    carpark_mapping: Dict[str, int],
    occupancy_pct: float,
    lag_1: Optional[float] = None,
    lag_2: Optional[float] = None,
    lag_3: Optional[float] = None
) -> pd.DataFrame:
    """Builds a single-row feature vector matching the trained scikit-learn pipeline."""
    h = target_dt.hour
    m = target_dt.minute
    dow = target_dt.weekday()
    is_wknd = 1 if dow >= 5 else 0
    woy = target_dt.isocalendar()[1]
    
    time_decimal = h + m / 60.0
    h_sin = np.sin(time_decimal / 24.0 * 2 * np.pi)
    h_cos = np.cos(time_decimal / 24.0 * 2 * np.pi)
    c_enc = carpark_mapping.get(carpark_code, 0)
    
    # Defaults for lag features if not supplied
    l1 = lag_1 if lag_1 is not None else occupancy_pct
    l2 = lag_2 if lag_2 is not None else l1
    l3 = lag_3 if lag_3 is not None else l2
    
    rolling_m = float(np.mean([l1, l2, l3]))
    rolling_s = float(np.std([l1, l2, l3]))
    
    row = {
        "Capacity": capacity,
        "occupancy_pct": occupancy_pct,
        "hour": h,
        "minute": m,
        "dayofweek": dow,
        "is_weekend": is_wknd,
        "weekofyear": woy,
        "hour_sin": h_sin,
        "hour_cos": h_cos,
        "SystemCodeNumber_enc": c_enc,
        "lag_1": l1,
        "lag_2": l2,
        "lag_3": l3,
        "rolling_mean_3": rolling_m,
        "rolling_std_3": rolling_s
    }
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# 4. Actionable Driver Advice: Best Alternative & Best Time
# ---------------------------------------------------------------------------
def find_best_alternative(
    current_code: str,
    target_dt: datetime.datetime,
    model: Any,
    carpark_mapping: Dict[str, int],
    facility_capacities: Dict[str, int],
    historical_hourly_means: Dict[Tuple[str, int], float]
) -> Optional[Dict[str, Any]]:
    """
    Finds the best alternative car park at the specified time by evaluating
    all other facilities and choosing the one with lowest predicted fill level.
    """
    candidates = []
    
    for other_code, cap in facility_capacities.items():
        if other_code == current_code:
            continue
            
        typical_occ = historical_hourly_means.get((other_code, target_dt.hour), 45.0)
        X_cand = build_feature_row(
            carpark_code=other_code,
            target_dt=target_dt,
            capacity=cap,
            carpark_mapping=carpark_mapping,
            occupancy_pct=typical_occ
        )
        
        proba = model.predict_proba(X_cand)[0]
        # proba order: [Available, Nearly Full, Full]
        p_avail = proba[0]
        p_full = proba[2]
        
        candidates.append({
            "code": other_code,
            "name": get_display_name(other_code),
            "p_avail": p_avail,
            "p_full": p_full,
            "est_occ": typical_occ,
            "capacity": cap
        })
        
    if not candidates:
        return None
        
    # Sort candidates: highest availability probability first, then lowest fill
    candidates.sort(key=lambda x: (-x["p_avail"], x["p_full"], x["est_occ"]))
    return candidates[0]


def find_best_time_to_arrive(
    current_code: str,
    target_date: datetime.date,
    model: Any,
    carpark_mapping: Dict[str, int],
    capacity: int,
    historical_hourly_means: Dict[Tuple[str, int], float]
) -> str:
    """
    Evaluates operating hours (8:00 to 16:00) for this car park to recommend
    the optimal arrival window.
    """
    best_hour = 8
    best_p_avail = -1.0
    
    for h in [8, 9, 10, 11, 12, 13, 14, 15, 16]:
        eval_dt = datetime.datetime.combine(target_date, datetime.time(h, 0))
        typical_occ = historical_hourly_means.get((current_code, h), 40.0)
        
        X_cand = build_feature_row(
            carpark_code=current_code,
            target_dt=eval_dt,
            capacity=capacity,
            carpark_mapping=carpark_mapping,
            occupancy_pct=typical_occ
        )
        proba = model.predict_proba(X_cand)[0]
        p_avail = proba[0]
        
        if p_avail > best_p_avail:
            best_p_avail = p_avail
            best_hour = h
            
    if best_hour <= 10:
        return f"before {best_hour + 1}:00 AM"
    elif best_hour >= 15:
        return f"after {best_hour - 12}:00 PM"
    else:
        return f"around {best_hour - 12 if best_hour > 12 else best_hour}:00 {'PM' if best_hour >= 12 else 'AM'}"


# ---------------------------------------------------------------------------
# 5. Hourly Profile Generation for "Busy Times" Screen
# ---------------------------------------------------------------------------
def get_hourly_profile_for_facility(
    code: str,
    dow: int,
    historical_hourly_means: Dict[Tuple[str, int], float]
) -> List[Dict[str, Any]]:
    """
    Returns an hour-by-hour occupancy profile from 08:00 to 16:00 for the selected facility.
    """
    profile = []
    hours = list(range(8, 17))
    for h in hours:
        occ = historical_hourly_means.get((code, h), 45.0)
        if occ < 50.0:
            status_text = "Easy"
            css = "status-easy"
        elif occ < 80.0:
            status_text = "Moderate"
            css = "status-filling"
        else:
            status_text = "Busy"
            css = "status-full"
            
        time_label = f"{h}:00" if h <= 12 else f"{h-12}:00 PM"
        if h == 12:
            time_label = "12:00 PM"
        elif h < 12:
            time_label = f"{h}:00 AM"
            
        profile.append({
            "hour": h,
            "label": time_label,
            "occupancy_pct": round(occ, 1),
            "status": status_text,
            "css": css
        })
    return profile

