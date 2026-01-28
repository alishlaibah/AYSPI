import React from "react";
import "./headerbar.css";

export default function HeaderBar() {
    return (
        <header className="topbar">
            <div className="brand">
                <div className="logoMark" aria-hidden="true">
                    <span className="logoGlow" />
                    <svg
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M2 12C4.7 7.5 8 5 12 5C16 5 19.3 7.5 22 12C19.3 16.5 16 19 12 19C8 19 4.7 16.5 2 12Z"
                            stroke="rgba(234,240,255,0.92)"
                            strokeWidth="1.6"
                        />
                        <path
                            d="M12 15.2C13.767 15.2 15.2 13.767 15.2 12C15.2 10.233 13.767 8.8 12 8.8C10.233 8.8 8.8 10.233 8.8 12C8.8 13.767 10.233 15.2 12 15.2Z"
                            stroke="rgba(77,225,255,0.92)"
                            strokeWidth="1.6"
                        />
                    </svg>
                </div>

                <div className="brandText">
                    <div className="brandName">AYSPI</div>
                </div>
            </div>
        </header>
    );
}
