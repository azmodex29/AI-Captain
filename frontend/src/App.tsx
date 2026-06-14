import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
    const token = localStorage.getItem('token');
    return token ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route 
                    path="/" 
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    } 
                />
            </Routes>
        </Router>
    );
}

export default App;
