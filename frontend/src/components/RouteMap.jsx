import { useEffect } from "react";
import {
  CircleMarker,
  MapContainer,
  Polyline,
  TileLayer,
  Tooltip,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

function FitRoute({ positions }) {
  const map = useMap();

  useEffect(() => {
    if (positions.length > 1) {
      map.fitBounds(positions, { padding: [32, 32] });
    }
  }, [map, positions]);

  return null;
}

function RouteMap({ optimization }) {
  if (!optimization?.geometry?.length) return null;

  const positions = optimization.geometry.map(([longitude, latitude]) => [
    latitude,
    longitude,
  ]);

  return (
    <section className="bg-white rounded-2xl shadow-lg p-4 mt-8">
      <h2 className="text-2xl font-bold px-4 py-2">Road route</h2>
      <MapContainer center={positions[0]} zoom={10} className="h-96 w-full rounded-xl">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Polyline positions={positions} pathOptions={{ color: "#2563eb", weight: 5 }} />
        {optimization.route.map((location, index) => (
          <CircleMarker
            key={`${location.latitude}-${location.longitude}`}
            center={[location.latitude, location.longitude]}
            radius={8}
            pathOptions={{ color: index === 0 ? "#16a34a" : "#dc2626" }}
          >
            <Tooltip>{`${index + 1}. ${location.name}`}</Tooltip>
          </CircleMarker>
        ))}
        <FitRoute positions={positions} />
      </MapContainer>
    </section>
  );
}

export default RouteMap;
