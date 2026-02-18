import React from "react";
import "./alphabetReference.css";

export default function AlphabetReference() {
  return (
    <div className="alphabet-ref">
      <div className="alphabet-chart">
        <img
          src="/images/all_signs.jpg"
          alt="ASL fingerspelling chart A to Z"
          className="alphabet-chart-img"
          draggable="false"
        />
      </div>
    </div>
  );
}
