"use client";

import { useState } from "react";

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}

export default function Page() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);

    const [loginId, setLoginId] = useState("");
    const [loginPwd, setLoginPwd] = useState("");
    const [startDate, setStartDate] = useState(formatDate(today));
    const [endDate, setEndDate] = useState(formatDate(tomorrow));

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const inputStyle = {
        width: "100%",
        marginTop: "5px",
        padding: "10px 12px",
        boxSizing: "border-box",
        border: "1px solid #d1d5db",
        borderRadius: "6px",
        backgroundColor: "#ffffff",
        fontSize: "15px",
    };

    const labelStyle = {
        fontWeight: "bold",
        display: "block",
        marginBottom: "5px",
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);
        setMessage("");

        try {
            const response = await fetch("/api/stayout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    loginId,
                    loginPwd,
                    start_date: startDate,
                    end_date: endDate,
                }),
            });

            const result = await response.json();

            if (result.success) {
                setMessage("✅ " + result.message);
            } else {
                setMessage("❌ " + result.message);
            }
        } catch (error) {
            console.error(error);
            setMessage("❌ 서버 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "100vh",
                backgroundColor: "#f3f4f6",
            }}
        >
            <form
                onSubmit={handleSubmit}
                style={{
                    width: "420px",
                    backgroundColor: "#ffffff",
                    padding: "32px",
                    borderRadius: "10px",
                    boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
                }}
            >
                <h2
                    style={{
                        textAlign: "center",
                        marginBottom: "30px",
                    }}
                >
                    기숙사 외박 신청
                </h2>

                <div style={{ marginBottom: "18px" }}>
                    <label style={labelStyle}>아이디</label>
                    <input
                        type="text"
                        value={loginId}
                        onChange={(e) => setLoginId(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>

                <div style={{ marginBottom: "18px" }}>
                    <label style={labelStyle}>비밀번호</label>
                    <input
                        type="password"
                        value={loginPwd}
                        onChange={(e) => setLoginPwd(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>

                <div style={{ marginBottom: "18px" }}>
                    <label style={labelStyle}>시작 날짜</label>
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>

                <div style={{ marginBottom: "24px" }}>
                    <label style={labelStyle}>종료 날짜</label>
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        width: "100%",
                        padding: "12px",
                        border: "none",
                        borderRadius: "6px",
                        backgroundColor: loading ? "#9ca3af" : "#2563eb",
                        color: "#ffffff",
                        fontSize: "16px",
                        fontWeight: "bold",
                        cursor: loading ? "default" : "pointer",
                        transition: "0.2s",
                    }}
                >
                    {loading ? "신청 중..." : "외박 신청"}
                </button>

                {message && (
                    <div
                        style={{
                            marginTop: "20px",
                            textAlign: "center",
                            fontWeight: "bold",
                        }}
                    >
                        {message}
                    </div>
                )}
            </form>
        </main>
    );
}