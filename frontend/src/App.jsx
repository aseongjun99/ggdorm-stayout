import { useState } from "react";
import api from "./api/api";

function App() {

    const today = new Date();
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);

    const formatDate = (date) => {
        return date.toISOString().split("T")[0];
    };

    const [loginId, setLoginId] = useState("");
    const [loginPwd, setLoginPwd] = useState("");
    const [startDate, setStartDate] = useState(formatDate(today));
    const [endDate, setEndDate] = useState(formatDate(tomorrow));

    const handleSubmit = async () => {

        const formData = new FormData();

        formData.append("loginId", loginId);
        formData.append("loginPwd", loginPwd);
        formData.append("start_date", startDate);
        formData.append("end_date", endDate);

        try {

            const response = await api.post(
                "/login-test",
                formData
            );

            alert("외박 신청 완료!");
            console.log(response.data);

        } catch (error) {

            console.error(error);

            alert("외박 신청 실패");

        }

    };

    return (
        <div>

            <h1>외박 자동 신청</h1>

            <div>
                <label>아이디</label>
                <br />

                <input
                    type="text"
                    value={loginId}
                    onChange={(e) => setLoginId(e.target.value)}
                />
            </div>

            <br />

            <div>
                <label>비밀번호</label>
                <br />

                <input
                    type="password"
                    value={loginPwd}
                    onChange={(e) => setLoginPwd(e.target.value)}
                />
            </div>

            <br />

            <div>
                <label>외박 시작일</label>
                <br />

                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </div>

            <br />

            <div>
                <label>외박 종료일</label>
                <br />

                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>

            <br />

            <button onClick={handleSubmit}>
                외박 신청
            </button>

        </div>
    );
}

export default App;