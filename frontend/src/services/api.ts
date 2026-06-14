import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const getPorts = () => api.get('/ports');
export const createRoute = (sourceId: number, destId: number) => api.post('/routes', { source_id: sourceId, destination_id: destId });
export const getHistory = () => api.get('/routes');
export const login = (email: string, pass: string) => api.post('/auth/login', { email, password: pass });
export const register = (email: string, pass: string) => api.post('/auth/register', { email, password: pass });

export default api;
