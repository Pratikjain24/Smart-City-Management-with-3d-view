import React, { useState, useEffect } from 'react';
import { 
  Play, Pause, RotateCcw, Clock
} from 'lucide-react';
import { TemporalScenario, TemporalMode } from '../../types/digital_twin';

interface TimeMachineBarProps {
  currentYear: number;
  temporalMode: TemporalMode;
  scenarios: Record<string, TemporalScenario>;
  onYearChange: (year: number) => void;
  onSelectScenario: (scenarioKey: string) => void;
}

export const TimeMachineBar: React.FC<TimeMachineBarProps> = ({
  currentYear,
  scenarios,
  onYearChange,
  onSelectScenario
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<1 | 5 | 20>(1);

  // Auto-play timeline progression
  useEffect(() => {
    let interval: any;
    if (isPlaying) {
      interval = setInterval(() => {
        onYearChange(currentYear >= 2030 ? 2020 : currentYear + 1);
      }, 2500 / playbackSpeed);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentYear, playbackSpeed, onYearChange]);

  const scenarioKey = currentYear <= 2021 ? 'historical_2020' 
    : currentYear <= 2024 ? 'historical_2023' 
    : currentYear <= 2026 ? 'live_2026' 
    : currentYear <= 2028 ? 'future_2028' 
    : 'future_2030';

  const activeScenario = scenarios[scenarioKey];

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 w-full max-w-4xl px-4 select-none">
      <div className="glass-panel p-3.5 border border-slate-800 shadow-2xl space-y-3">
        {/* Top Controls Header */}
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-cyan-500/20 text-cyan-400">
              <Clock className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-extrabold font-display uppercase tracking-wider text-white">
                  4D Time Machine
                </span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                  currentYear < 2026 ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  : currentYear === 2026 ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                }`}>
                  {currentYear < 2026 ? 'HISTORICAL' : currentYear === 2026 ? 'LIVE' : 'SIMULATED FUTURE'}
                </span>
              </div>
            </div>
          </div>

          {/* Active Scenario Title */}
          {activeScenario && (
            <div className="text-right hidden md:block">
              <div className="text-xs font-semibold text-slate-200">
                {activeScenario.title}
              </div>
              <div className="text-[11px] text-slate-400 truncate max-w-md">
                {activeScenario.description}
              </div>
            </div>
          )}

          {/* Playback Controls */}
          <div className="flex items-center gap-1.5 bg-slate-900/80 p-1 rounded-lg border border-slate-800">
            <button
              onClick={() => onYearChange(2026)}
              title="Return to LIVE 2026"
              className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-2.5 py-1 rounded bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 flex items-center gap-1.5 text-xs font-semibold transition-all"
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Pause' : 'Play'}</span>
            </button>

            <button
              onClick={() => setPlaybackSpeed(playbackSpeed === 1 ? 5 : playbackSpeed === 5 ? 20 : 1)}
              className="px-2 py-1 rounded text-xs font-mono font-bold text-slate-300 hover:bg-slate-800"
            >
              {playbackSpeed}x
            </button>
          </div>
        </div>

        {/* Timeline Slider with Year Milestones */}
        <div className="space-y-1.5 pt-1">
          <input
            type="range"
            min={2020}
            max={2030}
            step={1}
            value={currentYear}
            onChange={(e) => onYearChange(parseInt(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
          />

          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 px-1">
            <span 
              onClick={() => { onYearChange(2020); onSelectScenario('historical_2020'); }}
              className={`cursor-pointer hover:text-cyan-300 ${currentYear === 2020 ? 'text-blue-400 font-bold' : ''}`}
            >
              2020 (Baseline)
            </span>
            <span 
              onClick={() => { onYearChange(2023); onSelectScenario('historical_2023'); }}
              className={`cursor-pointer hover:text-cyan-300 ${currentYear === 2023 ? 'text-blue-400 font-bold' : ''}`}
            >
              2023 (Tunnels)
            </span>
            <span 
              onClick={() => { onYearChange(2026); onSelectScenario('live_2026'); }}
              className={`cursor-pointer hover:text-emerald-300 font-bold ${currentYear === 2026 ? 'text-emerald-400 scale-110' : ''}`}
            >
              • 2026 LIVE •
            </span>
            <span 
              onClick={() => { onYearChange(2028); onSelectScenario('future_2028'); }}
              className={`cursor-pointer hover:text-purple-300 ${currentYear === 2028 ? 'text-purple-400 font-bold' : ''}`}
            >
              2028 (Bullet Train)
            </span>
            <span 
              onClick={() => { onYearChange(2030); onSelectScenario('future_2030'); }}
              className={`cursor-pointer hover:text-purple-300 ${currentYear === 2030 ? 'text-purple-400 font-bold' : ''}`}
            >
              2030 (Climate Resilient)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
