import React from 'react';

interface DataHonestyBadgeProps {
  provenance?: string;
  freshness?: string;
  source?: string;
}

export const DataHonestyBadge: React.FC<DataHonestyBadgeProps> = ({
  provenance = 'SAMPLE_BUNDLED_DATA',
  freshness = 'Data availability unknown'
}) => {
  const getBadgeStyle = () => {
    const prov = provenance.toUpperCase();
    if (prov.includes('SAMPLE') || prov.includes('BUNDLED')) {
      return {
        bg: 'bg-amber-500/15',
        border: 'border-amber-500/40',
        text: 'text-amber-400',
        dot: 'bg-amber-400',
        label: 'SAMPLE DATA'
      };
    }
    if (prov.includes('LIVE') || prov.includes('IOT') || prov.includes('SCADA')) {
      return {
        bg: 'bg-emerald-500/15',
        border: 'border-emerald-500/40',
        text: 'text-emerald-400',
        dot: 'bg-emerald-400 animate-ping',
        label: 'LIVE STREAM'
      };
    }
    if (prov.includes('HISTORICAL')) {
      return {
        bg: 'bg-blue-500/15',
        border: 'border-blue-500/40',
        text: 'text-blue-400',
        dot: 'bg-blue-400',
        label: 'HISTORICAL'
      };
    }
    if (prov.includes('SIMULATED') || prov.includes('FUTURE')) {
      return {
        bg: 'bg-purple-500/15',
        border: 'border-purple-500/40',
        text: 'text-purple-400',
        dot: 'bg-purple-400 animate-pulse',
        label: 'SIMULATED'
      };
    }
    return {
      bg: 'bg-amber-500/15',
      border: 'border-amber-500/40',
      text: 'text-amber-400',
      dot: 'bg-amber-400',
      label: 'AUTHORITATIVE SAMPLE'
    };
  };

  const badge = getBadgeStyle();

  return (
    <div className={`inline-flex items-center gap-2 px-2.5 py-1 rounded-full border text-xs font-mono ${badge.bg} ${badge.border} ${badge.text}`}>
      <span className="relative flex h-2 w-2">
        <span className={`absolute inline-flex h-full w-full rounded-full opacity-75 ${badge.dot}`} />
        <span className={`relative inline-flex rounded-full h-2 w-2 ${badge.dot.replace('animate-ping', '').replace('animate-pulse', '')}`} />
      </span>
      <span className="font-semibold">{badge.label}</span>
      <span className="text-slate-400">|</span>
      <span className="text-slate-300 font-sans">{freshness}</span>
    </div>
  );
};
