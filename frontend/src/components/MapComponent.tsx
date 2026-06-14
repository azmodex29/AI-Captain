import { MapContainer, TileLayer, Polyline, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIconRetina,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
    shadowSize: [41, 41]
});

// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIconRetina,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
});

interface MapComponentProps {
    route?: any;
    ports?: any[];
}

function ChangeView({ center, zoom }: { center: [number, number], zoom: number }) {
    const map = useMap();
    map.setView(center, zoom);
    return null;
}

const MapComponent = ({ route, ports }: MapComponentProps) => {
    const center: [number, number] = [20, 0];
    const zoom = 2;

    return (
        <MapContainer center={center} zoom={zoom} className="h-full w-full">
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {route && route.geometry && (
                <>
                    <Polyline 
                        positions={route.geometry.coordinates.map((c: any) => [c[1], c[0]])} 
                        color="blue" 
                        weight={4}
                    />
                    <ChangeView 
                        center={[route.geometry.coordinates[0][1], route.geometry.coordinates[0][0]]} 
                        zoom={4} 
                    />
                </>
            )}
            {ports?.map(port => (
                <Marker key={port.id} position={[port.lat, port.lon]}>
                    <Popup>{port.name}</Popup>
                </Marker>
            ))}
        </MapContainer>
    );
};

export default MapComponent;
