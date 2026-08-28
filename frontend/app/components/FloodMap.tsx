"use client";

import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { getRiskColor } from "../lib/riskColors";

interface StationWithPrediction {
  id: string;
  name: string;
  district: string;
  lat: number;
  lng: number;
  risk_percentage: number;
  risk_level: string;
}

export default function FloodMap({ stations }: { stations: StationWithPrediction[] }) {
  return (
    <div className="dark-map-wrapper h-full w-full">
      <MapContainer
        center={[30.9, 78.5]}
        zoom={8}
        style={{ height: "100%", width: "100%", borderRadius: "16px" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />

        {stations.map((station) => (
          <CircleMarker
            key={station.id}
            center={[station.lat, station.lng]}
            radius={14}
            pathOptions={{
              color: getRiskColor(station.risk_level),
              fillColor: getRiskColor(station.risk_level),
              fillOpacity: 0.7,
              weight: 2,
            }}
          >
            <Popup>
              <div style={{ fontFamily: "sans-serif" }}>
                <strong>{station.name}</strong>
                <br />
                {station.district}
                <br />
                Risk: <strong>{station.risk_level}</strong> ({station.risk_percentage}%)
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}