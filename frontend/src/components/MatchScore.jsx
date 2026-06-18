export default function MatchScore({ score, breakdown }) {
  const parsed = breakdown ? (typeof breakdown === 'string' ? JSON.parse(breakdown) : breakdown) : null;

  const getColor = (s) => {
    if (s >= 80) return 'text-green-600';
    if (s >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full ${score >= 80 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`}
            style={{ width: `${Math.min(score, 100)}%` }}
          ></div>
        </div>
        <span className={`font-bold text-sm ${getColor(score)}`}>{score}%</span>
      </div>
      {parsed && (
        <div className="text-xs text-gray-500 space-y-1">
          <p>Matched: {parsed.matched_skills?.join(', ') || 'None'}</p>
          {parsed.missing_skills?.length > 0 && (
            <p>Missing: {parsed.missing_skills.join(', ')}</p>
          )}
        </div>
      )}
    </div>
  );
}
