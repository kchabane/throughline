import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import "./EntryFlow.css";
import "./design.css";
import "./MotionStudy.css";
import StudySignal from "./SignalGraphic";


function MotionStudy() {
  const [paused, setPaused] = useState(false);
  const [focused, setFocused] = useState(true);
  const [run, setRun] = useState(0);
  return <main className={`motion-study ${focused ? "study-focus" : ""}`} data-paused={paused}>
    <header className="motion-study-header">
      <div><p className="study-eyebrow">Throughline · motion study</p><h1>A clearer sense of flow.</h1><p>Stronger moving strokes. Quieter background lines. The same clean logo.</p></div>
      <div className="study-controls"><button type="button" aria-pressed={!focused} onClick={() => setFocused(v=>!v)}>{focused ? "Compare with original" : "Focus on B"}</button><button type="button" aria-pressed={paused} onClick={() => setPaused(v=>!v)}>{paused ? "Play motion" : "Pause motion"}</button><button type="button" onClick={() => { setRun(v=>v+1); setPaused(false); }}>{focused ? "Restart motion" : "Restart both"}</button></div>
    </header>
    <div className="study-comparison" key={run}>
      <section className="study-version study-original" aria-labelledby="study-original-title">
        <p className="study-eyebrow">A · Baseline</p><h2 id="study-original-title">Original rhythm</h2><p>Regular traveling signals at the original speeds.</p><StudySignal varied={false} />
      </section>
      <section className="study-version study-varied" aria-labelledby="study-varied-title">
        <p className="study-eyebrow">B · Motion refinement</p><h2 id="study-varied-title">Varied flow</h2><p>More fine threads add depth; the bolder signals gather into one clear throughline.</p><StudySignal varied />
      </section>
    </div>
    <footer className="study-footer">Watch for a few cycles. The selected B animation is now used on the homepage.<a href="/">Back to the product</a></footer>
  </main>;
}
ReactDOM.createRoot(document.getElementById("root")).render(<MotionStudy />);
