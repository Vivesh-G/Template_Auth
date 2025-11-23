import { useState } from "react";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    async function login() {
        setIsLoading(true);
        try {
            const res = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();
            console.log("Logged in:", data);
        } catch (error) {
            console.error("Login failed:", error);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="split-screen">
            {/* Left Side - Content */}
            <div className="content-side">
                <div style={{ maxWidth: '600px' }}>
                    <div className="comic-badge">AUTHENTICATION REQUIRED</div>
                    <h1 style={{ fontSize: '5rem', marginBottom: '2rem' }}>
                        ENTER THE<br />
                        <span style={{
                            color: 'var(--bg-paper)',
                            backgroundColor: 'var(--ink-black)',
                            padding: '0 1rem'
                        }}>ARCHIVE</span>
                    </h1>
                    <p style={{ fontSize: '1.5rem', lineHeight: '1.6', fontWeight: '600' }}>
                        Access the mainframe. Secure your data.
                        Don't forget to check your credentials before proceeding.
                    </p>
                </div>

                {/* Decorative Background Elements for the Left Side */}
                <div style={{
                    position: 'absolute',
                    bottom: '-50px',
                    left: '-50px',
                    width: '300px',
                    height: '300px',
                    border: '4px solid var(--ink-black)',
                    borderRadius: '50%',
                    background: 'var(--accent-pop)',
                    zIndex: -1,
                    opacity: 0.5
                }} />
            </div>

            {/* Right Side - Login Form */}
            <div className="login-side">
                <div className="comic-card">
                    <h2 style={{ fontSize: '2.5rem', marginBottom: '2rem', textAlign: 'center' }}>
                        LOGIN
                    </h2>

                    <div className="input-group">
                        <label className="input-label">User Identification</label>
                        <input
                            type="email"
                            className="input-field"
                            placeholder="user@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Access Code</label>
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
                        onClick={login}
                        disabled={isLoading}
                    >
                        {isLoading ? 'PROCESSING...' : 'AUTHENTICATE ->'}
                    </button>

                    <div style={{
                        marginTop: '2rem',
                        textAlign: 'center',
                        fontSize: '0.9rem',
                        fontWeight: '700'
                    }}>
                        <a href="#" style={{ color: 'var(--ink-black)', textDecoration: 'underline' }}>
                            LOST ACCESS KEY?
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
