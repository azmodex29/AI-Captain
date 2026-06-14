import { useState } from 'react';
import { login, register } from '../services/api';
import { Ship, Lock, Mail } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (isRegister) {
                await register(email, password);
                alert("Account created! Please login.");
                setIsRegister(false);
            } else {
                const res = await login(email, password);
                localStorage.setItem('token', res.data.token);
                navigate('/');
            }
        } catch (err) {
            console.error(err);
            alert("Authentication failed.");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white p-4">
            <div className="max-w-md w-full bg-slate-800 rounded-2xl p-8 shadow-2xl border border-slate-700">
                <div className="flex flex-col items-center gap-4 mb-8">
                    <div className="bg-blue-600 p-4 rounded-full shadow-lg">
                        <Ship size={48} />
                    </div>
                    <h2 className="text-3xl font-black tracking-tight">AI CAPTAIN</h2>
                    <p className="text-slate-400 text-center">Maritime Decision Support Platform</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-400 mb-1">Email Address</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                            <input 
                                type="email" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-slate-700 border-none rounded-lg py-3 pl-10 pr-4 text-white focus:ring-2 focus:ring-blue-500"
                                placeholder="captain@vessel.com"
                                required
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-400 mb-1">Password</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                            <input 
                                type="password" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-slate-700 border-none rounded-lg py-3 pl-10 pr-4 text-white focus:ring-2 focus:ring-blue-500"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button 
                        type="submit"
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors shadow-lg shadow-blue-900/20"
                    >
                        {isRegister ? "Create Account" : "Access Bridge"}
                    </button>
                </form>

                <div className="mt-6 text-center">
                    <button 
                        onClick={() => setIsRegister(!isRegister)}
                        className="text-blue-400 hover:text-blue-300 text-sm font-medium"
                    >
                        {isRegister ? "Already have access? Login" : "No account? Register as Captain"}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Login;
