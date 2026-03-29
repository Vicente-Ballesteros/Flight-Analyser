import matplotlib.pyplot as plt
import folium
from fetch_flights import fetch_flights
from analyse import isa_atmosphere, flight_phase

def plot_altitude_speed(flights):
    """Scatter plot of altitude vs speed, coloured by flight phase."""
    flights = flights.dropna(subset=["baro_altitude", "velocity", "vertical_rate"])
    
    colours = flights["vertical_rate"].apply(
        lambda vr: "green" if vr > 1.5 else "red" if vr < -1.5 else "blue"
    )

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        flights["velocity"] * 1.944,
        flights["baro_altitude"] * 3.281,
        c=colours,
        alpha=0.7,
        edgecolors="none"
    )

    plt.xlabel("Ground speed (kts)")
    plt.ylabel("Altitude (ft)")
    plt.title("UK flights — altitude vs speed")

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="green", label="Climbing"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="blue",  label="Cruising"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="red",   label="Descending"),
    ]
    plt.legend(handles=handles)
    plt.tight_layout()
    plt.savefig("altitude_speed.png", dpi=150)
    plt.show()
    print("Saved altitude_speed.png")

def plot_flight_map(flights):
    """Plot all flights on an interactive map and save as HTML."""
    flights = flights.dropna(subset=["latitude", "longitude"])

    m = folium.Map(location=[54.0, -2.0], zoom_start=6)

    for _, row in flights.iterrows():
        phase  = flight_phase(row["vertical_rate"] or 0)
        colour = "green" if phase == "climbing" else "red" if phase == "descending" else "blue"
        alt_ft = (row["baro_altitude"] or 0) * 3.281
        spd_kt = (row["velocity"] or 0) * 1.944

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            color=colour,
            fill=True,
            fill_opacity=0.8,
            popup=folium.Popup(
                f"<b>{row['callsign']}</b><br>"
                f"Country: {row['origin_country']}<br>"
                f"Altitude: {alt_ft:.0f} ft<br>"
                f"Speed: {spd_kt:.0f} kts<br>"
                f"Phase: {phase}",
                max_width=200
            )
        ).add_to(m)

    m.save("flight_map.html")
    print("Saved flight_map.html — open this in your browser!")

if __name__ == "__main__":
    print("Fetching live flights over the UK...")
    flights = fetch_flights(49.9, 58.7, -8.2, 1.8)
    print(f"Found {len(flights)} flights\n")

    print("Generating altitude vs speed plot...")
    plot_altitude_speed(flights)

    print("Generating interactive map...")
    plot_flight_map(flights)
