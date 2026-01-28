import React from "react";
import "./alphabetReference.css";

export default function AlphabetReference() {
    return (
        <div className="refBody">
            <div className="chartArea">
                <img
                    src="/images/all_signs.jpg"
                    alt="ASL fingerspelling chart A to Z"
                    className="chartImg"
                    draggable="false"
                />
            </div>

            <div className="refFooterNote">
                Use this chart to verify hand shapes while testing predictions.
            </div>
        </div>
    );
}
