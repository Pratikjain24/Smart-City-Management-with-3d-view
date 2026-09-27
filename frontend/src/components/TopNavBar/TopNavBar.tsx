import React, { useState, useEffect, useRef } from 'react';
import { 
  Search, ShieldAlert, Wind, Zap, Car, 
  Clock, Sparkles, Navigation, X
} from 'lucide-react';
import { TemporalMode, CityMetrics } from '../../types/digital_twin';
import { api } from '../../services/api';

interface TopNavBarProps {
  temporalMode: TemporalMode;
  onSelectTemporalMode: (mode: TemporalMode) => void;
  cityMetrics: CityMetrics;
  onSearchResultSelected: (item: any) => void;
}

export const TopNavBar: React.FC<TopNavBarProps> = ({
  temporalMode,
  onSelectTemporalMode,
  cityMetrics,
  onSearchResultSelected
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  // Debounced Search
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const res = await api.search(searchQuery);
        setSearchResults(res.results || []);
        setShowDropdown(true);
      } catch (e) {
        console.error('Search error:', e);
      } finally {
        setIsSearching(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Click outside to dismiss search dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectResult = (item: any) => {
    setShowDropdown(false);
    setSearchQuery(item.title);
    onSearchResultSelected(item);
  };

  return (
    <header className="absolute top-3 left-4 right-4 z-30 flex items-center justify-between gap-4 px-5 py-2.5 rounded-xl bg-slate-950/85 border border-slate-800/80 backdrop-blur-xl shadow-2xl">
      {/* 1. Brand Identity */}
      <div className="flex items-center gap-3 select-none">
        <div className="relative flex items-center justify-center w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/25">
          <div className="w-4 h-4 border-2 border-white rounded-sm rotate-45" />
          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-slate-950 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-sm font-extrabold tracking-wider font-display text-white uppercase">
              MahaTwin Mumbai
            </h1>
            <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/20 border border-cyan-500/40 text-cyan-300">
              4D TWIN
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium">
            High-Fidelity Urban Command Twin
          </p>
        </div>
      </div>

      {/* 2. Global Search with Instant Suggestions */}
      <div ref={searchRef} className="relative flex-1 max-w-md mx-2">
        <div className="relative flex items-center">
          <Search className={`absolute left-3 w-4 h-4 ${isSearching ? 'text-cyan-400 animate-spin' : 'text-slate-400'}`} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onFocus={() => { if (searchResults.length > 0) setShowDropdown(true); }}
            placeholder="Search Mumbai roads, metro, water mains, hospitals, incidents..."
            className="w-full pl-9 pr-8 py-1.5 text-xs bg-slate-900/90 border border-slate-800 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-sans"
          />
          {searchQuery && (
            <button 
              onClick={() => { setSearchQuery(''); setSearchResults([]); setShowDropdown(false); }}
              className="absolute right-2.5 text-slate-400 hover:text-white"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Dropdown Results */}
        {showDropdown && searchResults.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-2 p-1.5 rounded-xl bg-slate-950/95 border border-slate-800 backdrop-blur-2xl shadow-2xl max-h-80 overflow-y-auto z-50">
            <div className="px-2 py-1 text-[10px] font-mono text-slate-500 uppercase tracking-wider">
              {searchResults.length} Results Found
            </div>
            {searchResults.map((item) => (
              <div
                key={item.id}
                onClick={() => handleSelectResult(item)}
                className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-cyan-500/10 hover:border hover:border-cyan-500/30 cursor-pointer transition-all text-left"
              >
                <div className="p-1.5 rounded-md bg-slate-900 border border-slate-800 text-cyan-400 mt-0.5">
                  <Navigation className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-semibold text-slate-200 truncate">{item.title}</h4>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-400">
                      {item.category}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 truncate mt-0.5">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 3. Temporal Mode Selector */}
      <div className="flex items-center p-0.5 rounded-lg bg-slate-900/90 border border-slate-800">
        <button
          onClick={() => onSelectTemporalMode('HISTORICAL')}
          className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
            temporalMode === 'HISTORICAL' 
              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5" />
            Historical
          </span>
        </button>

        <button
          onClick={() => onSelectTemporalMode('LIVE')}
          className={`relative px-3 py-1 text-xs font-semibold rounded-md transition-all ${
            temporalMode === 'LIVE' 
              ? 'bg-emerald-600 text-white shadow-md shadow-emerald-500/30 font-bold' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-300 animate-ping" />
            LIVE
          </span>
        </button>

        <button
          onClick={() => onSelectTemporalMode('FUTURE')}
          className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
            temporalMode === 'FUTURE' 
              ? 'bg-purple-600 text-white shadow-md shadow-purple-500/30' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Simulated 4D
          </span>
        </button>
      </div>

      {/* 4. Live City Status Metrics Pill */}
      <div className="hidden lg:flex items-center gap-4 pl-3 border-l border-slate-800/80 text-xs font-mono">
        <div className="flex items-center gap-1.5" title="Mumbai Traffic Congestion">
          <Car className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-400">Traffic:</span>
          <span className="font-bold text-amber-300">{cityMetrics.traffic_congestion_index}%</span>
        </div>

        <div className="flex items-center gap-1.5" title="SAFAR Mumbai AQI Average">
          <Wind className="w-3.5 h-3.5 text-orange-400" />
          <span className="text-slate-400">AQI:</span>
          <span className="font-bold text-orange-300">{cityMetrics.air_quality_index}</span>
        </div>

        <div className="flex items-center gap-1.5" title="Maharashtra Grid Mumbai Load">
          <Zap className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400">Grid:</span>
          <span className="font-bold text-cyan-300">{cityMetrics.grid_load_mw} MW</span>
        </div>

        <div className="flex items-center gap-1.5" title="Active Municipal Incidents">
          <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
          <span className="text-slate-400">Incidents:</span>
          <span className="font-bold text-rose-400">{cityMetrics.active_incidents_count}</span>
        </div>
      </div>
    </header>
  );
};
