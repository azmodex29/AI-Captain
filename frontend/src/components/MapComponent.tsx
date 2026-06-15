import { MapContainer, TileLayer, Polyline, Marker, Popup, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect, useState } from 'react';

// Vessel Icon
const portIcon = L.divIcon({
    className: 'custom-div-icon',
    html: `<div style="background-color: #3b82f6; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px rgba(59,130,246,0.8);"></div>`,
    iconSize: [12, 12],
    iconAnchor: [6, 6]
});

const vesselIcon = L.divIcon({
    className: 'vessel-icon',
    html: `<div style="transform: rotate(45deg);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 22l10-4 10 4Z"></path></svg></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
});

interface MapComponentProps {
    route: any;
    ports: any[];
}

const MapComponent = ({ route, ports }: MapComponentProps) => {
    const [piracyZones, setPiracyZones] = useState<any>(null);

    useEffect(() => {
        // Fetch piracy zones for visualization
        fetch('/backend/app/data/piracy/piracy_zones.geojson')
            .then(res => res.json())
            .then(data => setPiracyZones(data))
            .catch(() => {
                // Fallback for demo if local fetch fails in dev
                setPiracyZones(null);
            });
    }, []);

    // CartoDB Dark Matter tiles for the Command Center look
    const tileUrl = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";
    const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';

    return (
        <MapContainer 
            center={[20, 0]} 
            zoom={3} 
            style={{ height: '100%', width: '100%', background: '#020617' }}
            zoomControl={false}
        >
            <TileLayer url={tileUrl} attribution={attribution} />

            {/* Piracy Zones */}
            {piracyZones && (
                <GeoJSON 
                    data={piracyZones} 
                    style={(feature) => ({
                        fillColor: feature?.properties.risk_level === 'High' ? '#ef4444' : '#f59e0b',
                        weight: 1,
                        opacity: 0.5,
                        color: feature?.properties.risk_level === 'High' ? '#ef4444' : '#f59e0b',
                        fillOpacity: 0.1,
                        className: 'piracy-zone-glow'
                    })}
                />
            )}

            {/* Ports */}
            {ports.map(port => (
                <Marker 
                    key={port.id} 
                    position={[port.lat, port.lon]} 
                    icon={portIcon}
                >
                    <Popup className="dark-popup">
                        <div className="bg-slate-900 text-white p-2 rounded">
                            <h4 className="font-bold text-blue-400 uppercase text-[10px] tracking-widest">{port.name}</h4>
                            <p className="text-[9px] text-slate-400">Lat: {port.lat}, Lon: {port.lon}</p>
                        </div>
                    </Popup>
                </Marker>
            ))}

            {/* Calculated Route */}
            {route && (
                <>
                    {/* Background glow path */}
                    <Polyline 
                        positions={route.geometry.coordinates.map((c: any) => [c[1], c[0]])} 
                        pathOptions={{ color: '#3b82f6', weight: 8, opacity: 0.1 }} 
                    />
                    {/* Animated foreground path */}
                    <Polyline 
                        positions={route.geometry.coordinates.map((c: any) => [c[1], c[0]])} 
                        pathOptions={{ 
                            color: '#60a5fa', 
                            weight: 3, 
                            opacity: 0.8,
                            className: 'route-path-animated'
                        }} 
                    />
                    
                    {/* Vessel at start point */}
                    <Marker 
                        position={[route.geometry.coordinates[0][1], route.geometry.coordinates[0][0]]} 
                        icon={vesselIcon} 
                    />
                </>
            )}
        </MapContainer>
    );
};

export default MapComponent;
