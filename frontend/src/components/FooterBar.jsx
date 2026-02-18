import React from "react";
import "./footerbar.css";

export default function FooterBar() {
  return (
    <footer className="footer" role="contentinfo">
      <div className="footer-inner container">
        <span className="footer-credit">Built by Ali Shlaibah</span>
        <span className="footer-date">Last updated Feb 2026</span>
      </div>
    </footer>
  );
}
