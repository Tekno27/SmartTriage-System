import AppIcon from "./AppIcon";

export default function AIRecommendationPanel({ data, loading }) {
  if (loading) {
    return (
      <div className="ai-panel loading">
        <div className="ai-panel-header">
          <AppIcon name="sparkles" size={18} className="ai-sparkle" />
          <strong>AI is analysing…</strong>
        </div>
        <div className="ai-shimmer" />
      </div>
    );
  }

  if (!data) return null;

  const isDiagnosis = data.type === "diagnosis";

  return (
    <div className="ai-panel">
      <div className="ai-panel-header">
        <AppIcon name="sparkles" size={18} className="ai-sparkle" />
        <div>
          <strong>AI Recommendations</strong>
          <span className="ai-confidence">{data.confidence}% confidence</span>
        </div>
      </div>

      <p className="ai-summary">{data.summary}</p>

      {isDiagnosis ? (
        <>
          <div className="ai-section">
            <h4>Differential Diagnosis</h4>
            <ul className="ai-list">
              {data.differential_diagnosis?.map((d, i) => (
                <li key={i}>
                  <strong>{d.condition}</strong>
                  <span className={`likelihood ${d.likelihood}`}>{d.likelihood}</span>
                </li>
              ))}
            </ul>
          </div>
          {data.suggested_tests?.length > 0 && (
            <div className="ai-section">
              <h4>Suggested Tests</h4>
              <ul className="ai-list simple">
                {data.suggested_tests.map((t, i) => (
                  <li key={i}>{t}</li>
                ))}
              </ul>
            </div>
          )}
          {data.recommended_medications?.length > 0 && (
            <div className="ai-section">
              <h4>Suggested Medications</h4>
              <ul className="ai-list meds">
                {data.recommended_medications.map((m, i) => (
                  <li key={i}>
                    <strong>{m.name}</strong>
                    <span className="muted">{m.dosage}</span>
                    {m.for_condition && <span className="for-cond">for {m.for_condition}</span>}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      ) : (
        <>
          {data.possible_conditions?.length > 0 && (
            <div className="ai-section">
              <h4>Possible Conditions</h4>
              <div className="ai-chips">
                {data.possible_conditions.map((c, i) => (
                  <span key={i} className="ai-chip">{c}</span>
                ))}
              </div>
            </div>
          )}
          {data.recommended_actions?.length > 0 && (
            <div className="ai-section">
              <h4>Recommended Actions</h4>
              <ul className="ai-list simple">
                {data.recommended_actions.map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </div>
          )}
          {data.suggested_urgency && (
            <div className="ai-urgency-hint">
              Suggested urgency: <strong>{data.suggested_urgency}</strong>
            </div>
          )}
        </>
      )}

      <p className="ai-disclaimer">{data.disclaimer}</p>
    </div>
  );
}
