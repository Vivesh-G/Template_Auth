import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState<{ text: string, type: 'success' | 'error' } | null>(null);
    const navigate = useNavigate();

    async function signup() {
        setIsLoading(true);
        setMessage(null);

        try {
            const res = await fetch("http://localhost:8000/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (res.ok) {
                setMessage({ text: "Account created! Redirecting...", type: "success" });
                setTimeout(() => {
                    navigate("/");
                }, 1500);
            } else {
                setMessage({ text: data.detail || "Signup failed", type: "error" });
            }
        } catch (error) {
            console.error("Signup failed:", error);
            setMessage({ text: "Network error", type: "error" });
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="split-screen">
            {/* Left Side - Content */}
            <div className="content-side" style={{ background: 'var(--accent-pop)', color: 'var(--ink-black)' }}>
                <div style={{ maxWidth: '600px' }}>
                    <div className="comic-badge" style={{ background: 'var(--ink-black)', color: 'var(--bg-paper)' }}>
                        INITIATION SEQUENCE
                    </div>
                    <h1 style={{ fontSize: '5rem', marginBottom: '2rem' }}>
                        JOIN THE<br />
                        <span style={{
                            color: 'var(--bg-paper)',
                            backgroundColor: 'var(--ink-black)',
                            padding: '0 1rem'
                        }}>ARCHIVE</span>
                    </h1>
                    <p style={{ fontSize: '1.5rem', lineHeight: '1.6', fontWeight: '600' }}>
                        Create your identity. Secure your spot.
                        The database awaits your contribution.
                    </p>
                </div>

                {/* Decorative Background Elements */}
                <div style={{
                    position: 'absolute',
                    bottom: '-50px',
                    right: '-50px',
                    width: '300px',
                    height: '300px',
                    border: '4px solid var(--ink-black)',
                    borderRadius: '0',
                    background: 'var(--bg-paper)',
                    zIndex: -1,
                    opacity: 0.5,
                    transform: 'rotate(45deg)'
                }} />
            </div>

            {/* Right Side - Form */}
            <div className="login-side">
                <div className="comic-card">
                    <h2 style={{ fontSize: '2rem', marginBottom: '2rem', textAlign: 'center' }}>
                        NEW RECRUIT
                    </h2>

                    {message && (
                        <div style={{
                            marginBottom: '1.5rem',
                            padding: '1rem',
                            background: message.type === 'success' ? '#d4edda' : '#f8d7da',
                            color: message.type === 'success' ? '#155724' : '#721c24',
                            border: `2px solid ${message.type === 'success' ? '#c3e6cb' : '#f5c6cb'}`,
                            fontFamily: 'var(--font-headline)',
                            fontSize: '0.8rem',
                            fontWeight: '700'
                        }}>
                            {message.text}
                        </div>
                    )}

                    <div className="input-group">
                        <label className="input-label">Email Address</label>
                        <input
                            type="email"
                            className="input-field"
                            placeholder="recruit@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Set Password</label>
                        <input
                            type="password"
                            className="input-field"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button
                        className="btn-comic"
                        onClick={signup}
                        disabled={isLoading}
                    >
                        {isLoading ? 'PROCESSING...' : 'CREATE ACCOUNT ->'}
                    </button>

                    <div style={{
                        marginTop: '2rem',
                        textAlign: 'center',
                        fontSize: '0.9rem',
                        fontWeight: '700'
                    }}>
                        <a href="/" style={{ color: 'var(--ink-black)', textDecoration: 'underline' }}>
                            ALREADY HAVE AN ACCOUNT?
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
