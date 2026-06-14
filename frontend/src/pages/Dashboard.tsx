import { useState, useEffect } from 'react';
import MapComponent from '../components/MapComponent';
import { getPorts, createRoute } from '../services/api';
import { Ship, ShieldAlert, Navigation } from 'lucide-react';

const Dashboard = () => {
    const [ports, setPorts] = useState<any[]>([]);
    const [source, setSource] = useState('');
    const [destination, setDestination] = useState('');
    const [route, setRoute] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getPorts().then(res => setPorts(res.data)).catch(err => console.error(err));
    }, []);

    const handleCalculate = async () => {
        if (!source || !destination) return;
        setLoading(true);
        try {
            const res = await createRoute(parseInt(source), parseInt(destination));
            setRoute(res.data);
        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 404) {
                alert("No maritime route found between these ports in the current network database.");
            } else {
                alert("Failed to calculate route. Make sure you are logged in.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen w-screen bg-slate-900 text-white overflow-hidden">
            {/* Sidebar */}
            <div className="w-96 bg-slate-800 p-6 flex flex-col gap-6 shadow-xl z-10 overflow-y-auto">
                <div className="flex items-center gap-2">
                    <Ship className="text-blue-400" size={32} />
                    <h1 className="text-2xl font-bold tracking-tight">AI CAPTAIN</h1>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-400 mb-1">Source Port</label>
                        <select 
                            value={source} 
                            onChange={(e) => setSource(e.target.value)}
                            className="w-full bg-slate-700 border-none rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Select source</option>
                            {ports.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-400 mb-1">Destination Port</label>
                        <select 
                            value={destination} 
                            onChange={(e) => setDestination(e.target.value)}
                            className="w-full bg-slate-700 border-none rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Select destination</option>
                            {ports.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                        </select>
                    </div>
                    <button 
                        onClick={handleCalculate}
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-bold py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                        {loading ? "Calculating..." : <><Navigation size={20} /> Calculate Route</>}
                    </button>
                </div>

                {route && (
                    <div className="space-y-6 mt-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-slate-700 p-4 rounded-xl border border-slate-600">
                                <p className="text-xs text-slate-400 uppercase font-bold">Distance</p>
                                <p className="text-xl font-bold">{route.distance} nm</p>
                            </div>
                            <div className="bg-slate-700 p-4 rounded-xl border border-slate-600">
                                <p className="text-xs text-slate-400 uppercase font-bold">ETA</p>
                                <p className="text-xl font-bold">{route.eta} days</p>
                            </div>
                        </div>

                        <div className="bg-slate-700 p-4 rounded-xl border border-slate-600 space-y-4">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <ShieldAlert className="text-red-400" size={20} />
                                    <span className="font-bold">Risk Score</span>
                                </div>
                                <span className={`text-xl font-black ${route.risk_score > 50 ? 'text-red-500' : 'text-green-500'}`}>
                                    {route.risk_score}%
                                </span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-2">
                                <div 
                                    className={`h-2 rounded-full ${route.risk_score > 50 ? 'bg-red-500' : 'bg-green-500'}`} 
                                    style={{ width: `${route.risk_score}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="bg-blue-900/30 p-4 rounded-xl border border-blue-500/30">
                            <h3 className="font-bold text-blue-400 mb-2 flex items-center gap-2">
                                <Ship size={18} /> Advisor Recommendation
                            </h3>
                            <p className="text-sm text-slate-300 italic mb-2">"{route.recommendation.summary}"</p>
                            <ul className="text-xs space-y-1">
                                {route.recommendation.advice.map((a: string, i: number) => (
                                    <li key={i} className="flex gap-2">
                                        <span className="text-blue-400">•</span> {a}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>

            {/* Main Content (Map) */}
            <div className="flex-1 relative">
                <MapComponent route={route} ports={ports} />
            </div>
        </div>
    );
};

export default Dashboard;
