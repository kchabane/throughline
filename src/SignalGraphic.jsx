import React from "react";
import "./SignalGraphic.css";

export default function SignalGraphic({ varied = true, compact = false, snippets = [] }) {
  const incoming = [
    "M18 78 H168 C205 78 214 92 246 92 H316 C360 92 374 108 412 108 H486",
    "M26 104 H202 C238 104 250 122 286 122 H386 C424 122 440 138 486 138 H548",
    "M12 132 H178 C224 132 240 148 282 148 H420 C458 148 478 154 548 154",
    "M38 158 H230 C266 158 282 170 316 170 H446 C492 170 516 164 578 160",
    "M72 184 H248 C292 184 312 178 344 178 H466 C512 178 548 170 608 162",
    "M42 212 H214 C258 212 278 198 324 198 H468 C526 198 562 178 620 164",
    "M92 238 H278 C324 238 344 216 386 216 H500 C548 216 586 186 632 166",
    "M118 260 H328 C372 260 392 234 432 234 H530 C576 234 608 194 644 168",
    "M246 56 H356 C390 56 400 76 430 76 H502 C532 76 552 104 588 118 H632",
    "M310 86 H402 C438 86 448 106 480 106 H548 C578 106 600 132 640 146",
    "M354 196 H442 C474 196 496 184 526 184 H580 C606 184 622 174 652 164",
    "M420 236 H486 C522 236 548 212 574 202 C600 192 622 178 660 166"
  ];
  const converge = [
    "M486 108 C560 108 596 136 682 156",
    "M548 138 C600 138 626 148 682 156",
    "M548 154 C602 154 632 156 682 156",
    "M578 160 C620 160 646 158 682 156",
    "M608 162 C640 162 660 159 682 156",
    "M620 164 C646 164 664 160 682 156",
    "M632 166 C650 166 668 160 682 156",
    "M644 168 C658 166 670 160 682 156",
    "M632 118 C650 130 664 144 682 156",
    "M640 146 C654 148 666 152 682 156",
    "M652 164 C662 162 672 159 682 156",
    "M660 166 C668 162 674 159 682 156"
  ];
  const fullPaths = incoming.map((d,i) => `${d} ${converge[i].replace(/^M[\d.]+ [\d.]+/, "")}`);
  const textSnips = (snippets || []).filter(Boolean).slice(0, 4);
  return (
    <div className={`tl-ref-signal ${varied ? "tl-flow-varied" : ""} ${compact ? "is-compact" : ""}`} aria-hidden="true">
      <svg viewBox="0 0 1440 310" preserveAspectRatio="none" className="tl-ref-signal-svg">
        {varied && <g className="tl-flow-extra-lines">
          {[[0,1.12],[2,.86],[3,1.18],[5,.84],[6,.9],[7,1.15]].map(([index, spread], i) =>
            <path key={i} d={fullPaths[index]} transform={`translate(0 156) scale(1 ${spread}) translate(0 -156)`} />
          )}
        </g>}
        <g className="tl-ref-incoming-base">
          {incoming.map((d,i)=><path key={i} d={d} className={`rp rp-${i+1}`}/>)}
        </g>
        <g className="tl-ref-incoming-motion">
          {incoming.slice(0,8).map((d,i)=><path key={i} d={varied ? fullPaths[i] : d} pathLength={varied ? 100 : undefined} className={`rm rm-${i+1}`} style={varied ? { "--arrival-duration": `${3.8 + i * .34}s`, "--arrival-delay": `${i * -1.37}s`, "--arrival-width": `${2.3 + (i % 3) * .45}px`, "--arrival-length": `${7 + (i % 3) * 3}` } : undefined}/>)}
        </g>
        <g className="tl-ref-converge">
          {converge.map((d,i)=><path key={i} d={d} className={`rc rc-${i+1}`}/>)}
        </g>
        <path className="tl-ref-output" d="M754 156 C858 149 970 166 1088 163 C1202 160 1314 162 1448 162" />
        <path pathLength={varied ? 100 : undefined} className="tl-ref-output-pulse" d="M754 156 C858 149 970 166 1088 163 C1202 160 1314 162 1448 162" />
        <g className="tl-ref-ticks">
          {[1088,1198,1302,1392].map((x,i)=><line key={i} x1={x-4} y1="163" x2={x+4} y2="163"/>)}
        </g>
        <g className="tl-ref-microticks">
          <line x1="102" y1="78" x2="112" y2="78"/><line x1="172" y1="104" x2="182" y2="104"/>
          <line x1="240" y1="148" x2="250" y2="148"/><line x1="306" y1="184" x2="316" y2="184"/>
          <line x1="382" y1="216" x2="392" y2="216"/><line x1="454" y1="122" x2="464" y2="122"/>
          <line x1="520" y1="196" x2="530" y2="196"/>
        </g>
      </svg>
      <div className="tl-ref-hub">
        <span className="tl-ref-hub-mark"><i/><b/><i/></span>
      </div>
      {textSnips.length ? <div className="tl-ref-live-voices">
        {textSnips.map((t,i)=><span key={i} className={`lv lv-${i+1}`}>{t.length>58?`${t.slice(0,55)}…`:t}</span>)}
      </div> : null}
    </div>
  );
}

