import { useState, useEffect } from 'react';
import MapComponent from '../components/MapComponent';
import { getPorts, createRoute } from '../services/api';
import { Ship, ShieldAlert, Navigation, Compass, Wind, Anchor } from 'lucide-react';

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
            alert("Routing failed. The grid-based engine couldn't find a navigable path.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen w-screen bg-[#020617] text-slate-100 overflow-hidden font-sans">
            {/* Command Sidebar */}
            <div className="w-[420px] glass h-full flex flex-col p-8 z-20 shadow-[20px_0_50px_rgba(0,0,0,0.5)] border-r border-white/5">
                <div className="flex items-center gap-4 mb-10">
                    <div className="p-3 bg-blue-600 rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.4)]">
                        <Ship className="text-white" size={28} />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black tracking-tighter text-white uppercase italic">AI Captain</h1>
                        <p className="text-[10px] text-blue-400 font-bold tracking-[0.2em] uppercase opacity-80">Next-Gen Bridge System</p>
                    </div>
                </div>

                <div className="space-y-6 flex-1">
                    <section className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest ml-1">Departure Port</label>
                            <div className="relative group">
                                <Anchor className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={18} />
                                <select 
                                    value={source} 
                                    onChange={(e) => setSource(e.target.value)}
                                    className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all appearance-none cursor-pointer"
                                >
                                    <option value="">Select Origin...</option>
                                    {ports.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                                </select>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest ml-1">Arrival Port</label>
                            <div className="relative group">
                                <Navigation className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={18} />
                                <select 
                                    value={destination} 
                                    onChange={(e) => setDestination(e.target.value)}
                                    className="w-full bg-slate-900/50 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all appearance-none cursor-pointer"
                                >
                                    <option value="">Select Destination...</option>
                                    {ports.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                                </select>
                            </div>
                        </div>

                        <button 
                            onClick={handleCalculate}
                            disabled={loading}
                            className="w-full relative group overflow-hidden bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 py-5 rounded-xl transition-all duration-300 shadow-[0_4px_20px_rgba(37,99,235,0.3)] hover:shadow-[0_4px_25px_rgba(37,99,235,0.5)] active:scale-[0.98]"
                        >
                            <div className="flex items-center justify-center gap-3 relative z-10 font-black uppercase tracking-widest text-xs">
                                {loading ? "Computing Grid..." : <><Compass className="animate-spin-slow" size={20} /> Engage Pathfinding</>}
                            </div>
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-shimmer" />
                        </button>
                    </section>

                    {route && (
                        <div className="space-y-6 pt-6 border-t border-white/5 animate-in fade-in slide-in-from-bottom-4 duration-700">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-white/5 border border-white/5 p-4 rounded-2xl hover:bg-white/10 transition-colors">
                                    <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-1">Distance</p>
                                    <p className="text-2xl font-black text-white">{route.distance.toLocaleString()} <span className="text-xs font-normal text-slate-400">nm</span></p>
                                </div>
                                <div className="bg-white/5 border border-white/5 p-4 rounded-2xl hover:bg-white/10 transition-colors">
                                    <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-1">Duration</p>
                                    <p className="text-2xl font-black text-white">{route.eta} <span className="text-xs font-normal text-slate-400">days</span></p>
                                </div>
                            </div>

                            <div className="bg-white/5 border border-white/5 p-5 rounded-2xl space-y-4">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className={`p-2 rounded-lg ${route.risk_score > 50 ? 'bg-red-500/20 text-red-500' : 'bg-green-500/20 text-green-500'}`}>
                                            <ShieldAlert size={18} />
                                        </div>
                                        <span className="text-[10px] font-black uppercase tracking-widest text-slate-300">Composite Risk</span>
                                    </div>
                                    <span className={`text-xl font-black ${route.risk_score > 50 ? 'text-red-500' : 'text-green-500'}`}>
                                        {route.risk_score}%
                                    </span>
                                </div>
                                <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                                    <div 
                                        className={`h-full rounded-full transition-all duration-1000 ease-out ${route.risk_score > 50 ? 'bg-red-500' : 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]'}`} 
                                        style={{ width: `${route.risk_score}%` }}
                                    ></div>
                                </div>
                            </div>

                            <div className="bg-blue-600/10 border border-blue-500/20 p-5 rounded-2xl relative overflow-hidden group">
                                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                    <Wind size={48} />
                                </div>
                                <h3 className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
                                    Strategic Analysis
                                </h3>
                                <p className="text-sm text-slate-300 leading-relaxed italic border-l-2 border-blue-500/30 pl-4 mb-4">
                                    "{route.recommendation.summary}"
                                </p>
                                <ul className="space-y-2">
                                    {route.recommendation.advice.map((a: string, i: number) => (
                                        <li key={i} className="flex gap-3 text-xs text-slate-400">
                                            <div className="mt-1 h-1.5 w-1.5 rounded-full bg-blue-500 shrink-0" />
                                            {a}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>

                <div className="mt-auto pt-6 border-t border-white/5 flex items-center justify-between opacity-50">
                    <p className="text-[9px] uppercase tracking-widest font-bold">Status: Nominal</p>
                    <p className="text-[9px] uppercase tracking-widest font-bold">Grid: v2.0-RiskAware</p>
                </div>
            </div>

            {/* Tactical Display (Map) */}
            <div className="flex-1 relative bg-[#020617]">
                <MapComponent route={route} ports={ports} />
            </div>
        </div>
    );
};

export default Dashboard;
