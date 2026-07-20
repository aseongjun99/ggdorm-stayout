"use client";

import { useState } from "react";

export default function ApplyForm() {
    // yyyy-MM-dd 형태로 변환
    const formatDate = (date) => {
        return date.toISOString().split("T")[0];
    };

    // 오늘 / 내일 날짜 생성
    const today = new Date();
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);

    // Form 데이터
    const [formData, setFormData] = useState({
        loginId: "",
        loginPwd: "",
        startDate: formatDate(today),
        endDate: formatDate(tomorrow),
    });

    // 입력값 변경
    const handleChange = (e) => {
        const { name, value } = e.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    // 신청 버튼 클릭
    const handleSubmit = () => {
        console.log(formData);
    };

    return (
        <div>
            <h2>외박 신청</h2>

            <div>
                <label>아이디</label>
                <br />
                <input
                    type="text"
                    name="loginId"
                    value={formData.loginId}
                    onChange={handleChange}
                    placeholder="아이디"
                />
            </div>

            <br />

            <div>
                <label>비밀번호</label>
                <br />
                <input
                    type="password"
                    name="loginPwd"
                    value={formData.loginPwd}
                    onChange={handleChange}
                    placeholder="비밀번호"
                />
            </div>

            <br />

            <div>
                <label>외박 시작일</label>
                <br />
                <input
                    type="date"
                    name="startDate"
                    value={formData.startDate}
                    onChange={handleChange}
                />
            </div>

            <br />

            <div>
                <label>외박 종료일</label>
                <br />
                <input
                    type="date"
                    name="endDate"
                    value={formData.endDate}
                    onChange={handleChange}
                />
            </div>

            <br />

            <button onClick={handleSubmit}>
                외박 신청
            </button>
        </div>
    );
}