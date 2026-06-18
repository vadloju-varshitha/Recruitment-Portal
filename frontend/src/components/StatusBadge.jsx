const STATUS_COLORS = {
  applied: 'bg-blue-100 text-blue-800',
  shortlisted: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  on_hold: 'bg-yellow-100 text-yellow-800',
  interview: 'bg-purple-100 text-purple-800',
  offered: 'bg-indigo-100 text-indigo-800',
  hired: 'bg-emerald-100 text-emerald-800',
};

export default function StatusBadge({ status }) {
  const color = STATUS_COLORS[status] || 'bg-gray-100 text-gray-800';
  return (
    <span className={`badge ${color}`}>
      {status?.replace('_', ' ').toUpperCase()}
    </span>
  );
}
