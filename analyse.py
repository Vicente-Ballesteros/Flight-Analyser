import math
import pandas as pd
from fetch_flights import fetch_flights

def isa_atmosphere(altitude_m):
    """Calculate ISA temperature and pressure at a given altitude in metres."""
    T0 = 288.15      # sea level temperature (K)
    P0 = 101325      # sea level pressure (Pa)
    L  = 0.0065      # temperature lapse rate (K/m)
    R  = 287.05      # gas constant for air
    g  = 9.80665     # gravity

    if altitude_m < 11000:
        T = T0 - L * altitude_m
        P = P0 * (T / T0) ** (g / (L * R))
    else:
        # stratosphere — constant temperature
        T = 216.65
        P = 22632 * math.exp(-g * (altitude_m - 11000) / (R * T))

    density = P / (R * T)
    return round(T, 2), round(P, 2), round(density, 4)

def true_airspeed(indicated_speed_ms, altitude_m):
    """Estimate true airspeed from ground speed and altitude."""
    _, _, density = isa_atmosphere(altitude_m)
    rho0 = 1.225  # sea level density kg/m3
    tas = indicated_speed_ms * math.sqrt(rho0 / density)
    return round(tas, 2)

def flight_phase(vertical_rate):
    """Detect flight phase from vertical rate (m/s)."""
    if vertical_rate > 1.5:
        return "climbing"
    elif vertical_rate < -1.5:
        return "descending"
    else:
        return "cruising"

def summarise_flight(callsign, flights):
    """Print a performance summary for a given callsign."""
    flight = flights[flights["callsign"] == callsign]

    if flight.empty:
        print(f"No flight found with callsign {callsign}")
        return

    row = flight.iloc[0]
    alt_m = row["baro_altitude"] if row["baro_altitude"] else 0
    spd   = row["velocity"] if row["velocity"] else 0
    vr    = row["vertical_rate"] if row["vertical_rate"] else 0

    T, P, rho = isa_atmosphere(alt_m)
    tas        = true_airspeed(spd, alt_m)
    phase      = flight_phase(vr)

    print(f"\n--- {callsign.strip()} ---")
    print(f"Country:        {row['origin_country']}")
    print(f"Position:       {row['latitude']:.4f}N, {row['longitude']:.4f}E")
    print(f"Altitude:       {alt_m:.0f} m ({alt_m*3.281:.0f} ft)")
    print(f"Ground speed:   {spd:.1f} m/s ({spd*1.944:.1f} kts)")
    print(f"True airspeed:  {tas:.1f} m/s ({tas*1.944:.1f} kts)")
    print(f"Vertical rate:  {vr:.1f} m/s")
    print(f"Flight phase:   {phase}")
    print(f"ISA temp:       {T - 273.15:.1f} °C")
    print(f"ISA pressure:   {P/100:.1f} hPa")
    print(f"Air density:    {rho:.4f} kg/m³")

if __name__ == "__main__":
    print("Fetching live flights over the UK...")
    flights = fetch_flights(49.9, 58.7, -8.2, 1.8)
    print(f"Found {len(flights)} flights\n")

    # show summary for first 3 flights
    for callsign in flights["callsign"].head(3):
        summarise_flight(callsign, flights)