import { useState } from "react";

export default function ChangePassword() {
    const [email, setEmail] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState<{ text: string, type: 'success' | 'error' } | null>(null);

    async function changePassword() {
        setIsLoading(true);
        setMessage(null);

        try {
            const res = await fetch("http://localhost:8000/auth/change-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    old_password: oldPassword,
                    new_password: newPassword
                })
            });

            const data = await res.json();

            if (res.ok) {
                setMessage({ text: "Password updated successfully!", type: "success" });
                setOldPassword("");
                setNewPassword("");
                // Store the new token
                if (data.access_token) {
                    localStorage.setItem("token", data.access_token);
                    console.log("Token refreshed");
                }
            } else {
                setMessage({ text: data.detail || "Update failed", type: "error" });
            }
        } catch (error) {
            console.error("Change password failed:", error);
            setMessage({ text: "Network error", type: "error" });
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="split-screen">
            {/* Left Side - Content */}
            <div className="content-side" style={{ background: 'var(--ink-black)', color: 'var(--bg-paper)' }}>
                <div style={{ maxWidth: '600px' }}>
                    <div className="comic-badge" style={{ background: 'var(--error-red)', color: 'var(--bg-paper)' }}>
                        SYSTEM OVERRIDE
                    </div>
                    <h1 style={{ fontSize: '5rem', marginBottom: '2rem', color: 'var(--bg-paper)' }}>
                        SECURITY<br />
                        <span style={{
                            color: 'var(--ink-black)',
                            backgroundColor: 'var(--accent-pop)',
                            padding: '0 1rem'
                        }}>UPDATE</span>
                    </h1>
                    <p style={{ fontSize: '1.5rem', lineHeight: '1.6', fontWeight: '600', opacity: 0.9 }}>
                        Rotate your keys. Maintain operational security.
                        The archive depends on your vigilance.
                    </p>
                </div>

                {/* Decorative Background Elements */}
                <div style={{
                    position: 'absolute',
                    top: '-50px',
                    right: '-50px',
                    width: '400px',
                    height: '400px',
                    border: '4px solid var(--bg-paper)',
                    borderRadius: '0',
                    transform: 'rotate(15deg)',
                    background: 'transparent',
                    zIndex: 0,
                    opacity: 0.2
                }} />
            </div>

            {/* Right Side - Form */}
            <div className="login-side">
                <div className="comic-card">
                    <h2 style={{ fontSize: '2rem', marginBottom: '2rem', textAlign: 'center' }}>
                        NEW CREDENTIALS
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
                        <label className="input-label">Current Access Key</label>
                        <input
                            type="password"
                            className="input-field"
                            placeholder="••••••••"
                            value={oldPassword}
                            onChange={(e) => setOldPassword(e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">New Access Key</label>
                        <input
                            type="password"
                            className="input-field"
                            placeholder="••••••••"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                        />
                    </div>

                    <button
                        className="btn-comic"
                        onClick={changePassword}
                        disabled={isLoading}
                    >
                        {isLoading ? 'UPDATING...' : 'CONFIRM UPDATE ->'}
                    </button>

                    <div style={{
                        marginTop: '2rem',
                        textAlign: 'center',
                        fontSize: '0.9rem',
                        fontWeight: '700'
                    }}>
                        <a href="/" style={{ color: 'var(--ink-black)', textDecoration: 'underline' }}>
                            &lt;- RETURN TO LOGIN
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
