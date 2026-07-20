import { BASE_URL, DEFAULT_HEADERS } from "./constants";
import { getInputValue } from "./parser";

export async function login(loginId, loginPwd) {
    const response = await fetch(BASE_URL + "/user/login", {
        method: "POST",
        headers: {
            ...DEFAULT_HEADERS
        },
        body: new URLSearchParams({
            retUrl: "/ko/index/mypage/stayout/",
            loginId,
            loginPwd,
        }),
        redirect: "follow",
    });

    const html = await response.text();
    
    const registrationNo = getInputValue(
        html,
        "registrationNo"
    );

    const jsessionid = response.url.match(/jsessionid=([^?;]+)/)?.[1];

    if (!registrationNo) {
        throw new Error("로그인에 실패했습니다.");
    }

    return {
        registrationNo,
        jsessionid
    };
}

export async function fetchUserInfo(jsessionid, registrationNo) {
    const response = await fetch(
        BASE_URL + "/ko/index/mypage/stayout/",
        {
            method: "POST",
            headers: {
                ...DEFAULT_HEADERS,
                Cookie: `JSESSIONID=${jsessionid}`,
            },
            body: new URLSearchParams({
                registrationNo,
                mode: "write",
            })
        }
    );

    const html = await response.text();

    return {
        registrationNo,
        studentId: getInputValue(html, "stno"),
        studentName: getInputValue(html, "namekor"),
        gender: getInputValue(html, "sex"),
        roomInfo: getInputValue(html, "roominfo"),
        phone: getInputValue(html, "cellno"),
    };
}

export async function submitStayout(
    jsessionid,
    user,
    startDate,
    endDate
) {
    await fetch(
        BASE_URL + "/ko/index/mypage/stayout/",
        {
            method: "POST",
            headers: {
                ...DEFAULT_HEADERS,
                Cookie: `JSESSIONID=${jsessionid}`,
            },
            body: new URLSearchParams({
                startYmd: startDate,
                endYmd: endDate,
                reason: "본가",
                mode: "regist",
                type: "write",
                campus: "1",
                registrationNo: user.registrationNo,
                seq: "",
                stno: user.studentId,
                namekor: user.studentName,
                sex: user.gender,
                roominfo: user.roomInfo,
                cellno: user.phone,
                startHh: "00",
                endHh: "00",
            }),
        }
    );
}