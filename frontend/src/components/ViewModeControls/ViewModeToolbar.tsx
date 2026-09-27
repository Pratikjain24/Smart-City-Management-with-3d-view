import React, { useState } from 'react';
import { 
  Globe2, ArrowDownCircle, Filter, Bookmark, 
  RotateCcw, Maximize2, Minimize2, ChevronUp
} from 'lucide-react';
import { ViewMode, UtilityType } from '../../types/digital_twin';
import { MUMBAI_BOOKMARKS } from '../../services/cesium/CesiumViewerManager';

interface ViewModeToolbarProps {
  viewMode: ViewMode;
  onSetViewMode: (mode: ViewMode) => void;
  undergroundDepth: number;
  onSetUndergroundDepth: (depth: number) => void;
  activeUtilityIsolation: UtilityType | 'ALL' | null;
  onSelectUtilityIsolation: (type: UtilityType | 'ALL' | null) => void;
  onSelectBookmark: (key: string) => void;
  onResetHome: () => void;
}

export const ViewModeToolbar: React.FC<ViewModeToolbarProps> = ({
  viewMode,
  onSetViewMode,
  undergroundDepth,
  onSetUndergroundDepth,
  activeUtilityIsolation,
  onSelectUtilityIsolation,
  onSelectBookmark,
  onResetHome
}) => {
  const [showUtilityMenu, setShowUtilityMenu] = useState(false);
  const [showBookmarksMenu, setShowBookmarksMenu] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => console.error(err));
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
        setIsFullscreen(false);
      }
    }
  };

  const utilityOptions: { id: UtilityType | 'ALL'; name: string; color: string }[] = [
    { id: 'ALL', name: 'All Utilities', color: '#06b6d4' },
    { id: 'water', name: '💧 Water Supply Mains', color: '#38bdf8' },
    { id: 'sewer', name: '🚰 Sewer Deep Tunnels', color: '#10b981' },
    { id: 'drainage', name: '🌧️ Storm Drainage', color: '#818cf8' },
    { id: 'electricity', name: '⚡ High-Voltage Power', color: '#f59e0b' },
    { id: 'telecom', name: '📡 Optical Dark Fiber', color: '#ec4899' }
  ];

  return (
    <div className="absolute bottom-24 right-4 z-20 flex flex-col items-end gap-2.5">
      {/* 1. Utility Isolation Flyout Menu */}
      {showUtilityMenu && (
        <div className="glass-panel p-2 border border-slate-800 shadow-2xl rounded-xl space-y-1 w-56 mb-1 animate-in fade-in slide-in-from-bottom-2">
          <div className="px-2 py-1 text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            Isolate Utility Network
          </div>
          {utilityOptions.map((opt) => (
            <button
              key={opt.id}
              onClick={() => {
                onSelectUtilityIsolation(opt.id === 'ALL' ? null : opt.id);
                setShowUtilityMenu(false);
              }}
              className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center justify-between transition-colors ${
                (activeUtilityIsolation === opt.id) || (opt.id === 'ALL' && !activeUtilityIsolation)
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                  : 'text-slate-300 hover:bg-slate-800'
              }`}
            >
              <span>{opt.name}</span>
            </button>
          ))}
        </div>
      )}

      {/* 2. Camera Tour Bookmarks Menu */}
      {showBookmarksMenu && (
        <div className="glass-panel p-2 border border-slate-800 shadow-2xl rounded-xl space-y-1 w-64 mb-1 animate-in fade-in slide-in-from-bottom-2">
          <div className="px-2 py-1 text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            Cinematic Camera Bookmarks
          </div>
          {Object.entries(MUMBAI_BOOKMARKS).map(([key, bm]) => (
            <button
              key={key}
              onClick={() => {
                onSelectBookmark(key);
                setShowBookmarksMenu(false);
              }}
              className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:bg-cyan-500/20 hover:text-cyan-300 transition-colors flex items-center gap-2"
            >
              <Bookmark className="w-3.5 h-3.5 text-cyan-400" />
              <span className="truncate">{bm.name}</span>
            </button>
          ))}
        </div>
      )}

      {/* 3. Underground Depth Control (Only active in underground view) */}
      {viewMode === 'UNDERGROUND' && (
        <div className="glass-panel px-3 py-2 border border-slate-800 shadow-xl rounded-xl flex items-center gap-3 mb-1">
          <span className="text-[11px] font-mono text-slate-300">Subsurface: {undergroundDepth}m</span>
          <input
            type="range"
            min={5}
            max={50}
            step={5}
            value={undergroundDepth}
            onChange={(e) => onSetUndergroundDepth(parseInt(e.target.value))}
            className="w-24 h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
          />
        </div>
      )}

      {/* 4. Main Floating Action Toolbar */}
      <div className="glass-panel p-1.5 border border-slate-800 shadow-2xl rounded-xl flex items-center gap-1.5">
        {/* Surface View Button */}
        <button
          onClick={() => onSetViewMode('SURFACE')}
          className={`btn-command text-xs ${viewMode === 'SURFACE' ? 'active' : ''}`}
          title="Surface Photorealistic 3D View"
        >
          <Globe2 className="w-4 h-4 text-cyan-400" />
          <span className="hidden sm:inline">Surface</span>
        </button>

        {/* Underground View Button */}
        <button
          onClick={() => onSetViewMode(viewMode === 'UNDERGROUND' ? 'SURFACE' : 'UNDERGROUND')}
          className={`btn-command text-xs ${viewMode === 'UNDERGROUND' ? 'active' : ''}`}
          title="Underground Utility & Subsurface Cutaway"
        >
          <ArrowDownCircle className="w-4 h-4 text-indigo-400" />
          <span className="hidden sm:inline">Underground</span>
        </button>

        {/* Utility Isolation Button */}
        <button
          onClick={() => setShowUtilityMenu(!showUtilityMenu)}
          className={`btn-command text-xs ${activeUtilityIsolation ? 'active' : ''}`}
          title="Utility Isolation Filter"
        >
          <Filter className="w-4 h-4 text-emerald-400" />
          <span className="hidden sm:inline">
            {activeUtilityIsolation ? activeUtilityIsolation.toUpperCase() : 'Utilities'}
          </span>
          <ChevronUp className="w-3 h-3 text-slate-400" />
        </button>

        {/* Bookmarks Tour Button */}
        <button
          onClick={() => setShowBookmarksMenu(!showBookmarksMenu)}
          className="btn-command text-xs"
          title="Cinematic Landmark Bookmarks"
        >
          <Bookmark className="w-4 h-4 text-amber-400" />
          <span className="hidden sm:inline">Landmarks</span>
        </button>

        {/* Home Mumbai Button */}
        <button
          onClick={onResetHome}
          className="btn-command text-xs"
          title="Home Mumbai View"
        >
          <RotateCcw className="w-4 h-4 text-slate-300" />
        </button>

        {/* Fullscreen Toggle */}
        <button
          onClick={toggleFullscreen}
          className="btn-command text-xs"
          title="Toggle Fullscreen"
        >
          {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
        </button>
      </div>
    </div>
  );
};
