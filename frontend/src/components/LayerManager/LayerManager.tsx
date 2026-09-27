import React, { useState } from 'react';
import { 
  Layers, Eye, EyeOff, ChevronDown, ChevronRight,
  Car, Droplets, Waves, Zap, Radio, Building2, 
  AlertTriangle, Wind, Filter
} from 'lucide-react';
import { LayerItem } from '../../types/digital_twin';

interface LayerManagerProps {
  layers: LayerItem[];
  onToggleLayer: (layerId: string) => void;
  onIsolateLayer: (layerId: string) => void;
}

export const LayerManager: React.FC<LayerManagerProps> = ({
  layers,
  onToggleLayer,
  onIsolateLayer
}) => {
  const [isOpen, setIsOpen] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    TRANSPORTATION: true,
    WATER: true,
    SEWERAGE: false,
    DRAINAGE: false,
    ELECTRICITY: false,
    TELECOM: false,
    CIVIC: false,
    INCIDENTS: true,
    ENVIRONMENT: true
  });

  const toggleCategory = (cat: string) => {
    setExpandedCategories(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  const categories = [
    { id: 'TRANSPORTATION', name: 'Transportation & Roads', icon: Car, color: 'text-cyan-400' },
    { id: 'WATER', name: 'Water Distribution Network', icon: Droplets, color: 'text-blue-400' },
    { id: 'SEWERAGE', name: 'Sewerage & MSDP Deep Tunnels', icon: Waves, color: 'text-emerald-400' },
    { id: 'DRAINAGE', name: 'Storm Water Drainage (SWD)', icon: Waves, color: 'text-indigo-400' },
    { id: 'ELECTRICITY', name: 'High-Voltage Power Grid', icon: Zap, color: 'text-amber-400' },
    { id: 'TELECOM', name: 'Optical Dark Fiber Backbone', icon: Radio, color: 'text-pink-400' },
    { id: 'CIVIC', name: 'Civic & Emergency Facilities', icon: Building2, color: 'text-purple-400' },
    { id: 'INCIDENTS', name: 'Live Incidents & Road Damage', icon: AlertTriangle, color: 'text-rose-400' },
    { id: 'ENVIRONMENT', name: 'SAFAR AQI & Flood Risk', icon: Wind, color: 'text-teal-400' },
  ];

  return (
    <aside className={`absolute top-20 left-4 z-20 transition-all duration-300 ${
      isOpen ? 'w-80' : 'w-12'
    }`}>
      <div className="glass-panel overflow-hidden border border-slate-800 shadow-2xl">
        {/* Header */}
        <div 
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between px-4 py-3 bg-slate-900/80 border-b border-slate-800 cursor-pointer select-none hover:bg-slate-800/60 transition-colors"
        >
          <div className="flex items-center gap-2.5">
            <Layers className="w-4 h-4 text-cyan-400" />
            {isOpen && (
              <span className="text-xs font-bold font-display uppercase tracking-wider text-slate-200">
                Layer Manager
              </span>
            )}
          </div>
          {isOpen && (
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-300">
              {layers.filter(l => l.visible).length}/{layers.length} Active
            </span>
          )}
        </div>

        {/* Content Body */}
        {isOpen && (
          <div className="max-h-[calc(100vh-260px)] overflow-y-auto p-2 space-y-2">
            {categories.map((cat) => {
              const catLayers = layers.filter(l => l.category === cat.id);
              if (catLayers.length === 0) return null;

              const isExpanded = expandedCategories[cat.id];
              const Icon = cat.icon;

              return (
                <div key={cat.id} className="rounded-lg bg-slate-900/50 border border-slate-800/80 overflow-hidden">
                  {/* Category Header */}
                  <div 
                    onClick={() => toggleCategory(cat.id)}
                    className="flex items-center justify-between px-3 py-2 cursor-pointer hover:bg-slate-800/50 transition-colors text-left"
                  >
                    <div className="flex items-center gap-2">
                      <Icon className={`w-3.5 h-3.5 ${cat.color}`} />
                      <span className="text-xs font-semibold text-slate-300">
                        {cat.name}
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <span className="text-[10px] font-mono">({catLayers.length})</span>
                      {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                    </div>
                  </div>

                  {/* Layer Items */}
                  {isExpanded && (
                    <div className="px-2 pb-2 pt-1 space-y-1 border-t border-slate-800/50">
                      {catLayers.map((layer) => (
                        <div 
                          key={layer.id}
                          className="flex items-center justify-between px-2.5 py-1.5 rounded-md hover:bg-slate-800/70 transition-colors group"
                        >
                          <div 
                            onClick={() => onToggleLayer(layer.id)}
                            className="flex items-center gap-2.5 flex-1 cursor-pointer"
                          >
                            <span 
                              className="w-2.5 h-2.5 rounded-full flex-shrink-0" 
                              style={{ backgroundColor: layer.color }} 
                            />
                            <span className={`text-xs ${layer.visible ? 'text-slate-200' : 'text-slate-500 line-through'}`}>
                              {layer.name}
                            </span>
                          </div>

                          <div className="flex items-center gap-1 opacity-80 group-hover:opacity-100">
                            {/* Isolate Button */}
                            <button
                              onClick={(e) => { e.stopPropagation(); onIsolateLayer(layer.id); }}
                              title="Isolate this layer"
                              className="p-1 rounded text-slate-400 hover:text-cyan-300 hover:bg-slate-700/60 transition-colors text-[10px]"
                            >
                              <Filter className="w-3 h-3" />
                            </button>

                            {/* Visibility Toggle */}
                            <button
                              onClick={(e) => { e.stopPropagation(); onToggleLayer(layer.id); }}
                              className="p-1 rounded text-slate-400 hover:text-white transition-colors"
                            >
                              {layer.visible ? (
                                <Eye className="w-3.5 h-3.5 text-cyan-400" />
                              ) : (
                                <EyeOff className="w-3.5 h-3.5 text-slate-600" />
                              )}
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </aside>
  );
};
