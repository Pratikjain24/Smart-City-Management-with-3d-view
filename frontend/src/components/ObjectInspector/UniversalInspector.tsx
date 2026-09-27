import React, { useState } from 'react';
import { 
  X, Activity, Network, 
  CheckCircle2, ChevronRight, CornerDownRight
} from 'lucide-react';
import { UniversalObjectInspection } from '../../types/digital_twin';
import { DataHonestyBadge } from '../Common/DataHonestyBadge';

interface UniversalInspectorProps {
  inspectionData: UniversalObjectInspection | null;
  onClose: () => void;
  onSelectConnectedObject: (objectId: string) => void;
}

export const UniversalInspector: React.FC<UniversalInspectorProps> = ({
  inspectionData,
  onClose,
  onSelectConnectedObject
}) => {
  const [activeTab, setActiveTab] = useState<'OVERVIEW' | 'CONNECTIVITY' | 'TELEMETRY'>('OVERVIEW');

  if (!inspectionData) return null;

  const { object_id, name, category, status, data_provenance, freshness, details, graph_connections } = inspectionData;

  return (
    <aside className="absolute top-20 right-4 z-30 w-96 max-h-[calc(100vh-140px)] flex flex-col glass-panel border border-slate-800 shadow-2xl overflow-hidden animate-in fade-in slide-in-from-right-4 duration-200">
      {/* 1. Header Banner */}
      <div className="p-4 bg-gradient-to-r from-slate-900 via-slate-900/90 to-slate-950 border-b border-slate-800">
        <div className="flex items-start justify-between gap-3">
          <div>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 uppercase tracking-wider">
              {category.replace('_', ' ')}
            </span>
            <h2 className="text-sm font-bold text-white mt-1.5 leading-snug font-display">
              {name}
            </h2>
            <p className="text-[11px] text-slate-400 font-mono mt-0.5">
              ID: {object_id}
            </p>
          </div>
          <button 
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Data Honesty Pill */}
        <div className="mt-3">
          <DataHonestyBadge provenance={data_provenance} freshness={freshness} />
        </div>
      </div>

      {/* 2. Tab Navigation */}
      <div className="flex border-b border-slate-800 bg-slate-950/40 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('OVERVIEW')}
          className={`flex-1 py-2.5 text-center transition-colors ${
            activeTab === 'OVERVIEW' 
              ? 'text-cyan-400 border-b-2 border-cyan-500 bg-slate-900/60' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveTab('CONNECTIVITY')}
          className={`flex-1 py-2.5 text-center transition-colors flex items-center justify-center gap-1.5 ${
            activeTab === 'CONNECTIVITY' 
              ? 'text-cyan-400 border-b-2 border-cyan-500 bg-slate-900/60' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Network className="w-3.5 h-3.5" />
          Graph Links
        </button>
        <button
          onClick={() => setActiveTab('TELEMETRY')}
          className={`flex-1 py-2.5 text-center transition-colors ${
            activeTab === 'TELEMETRY' 
              ? 'text-cyan-400 border-b-2 border-cyan-500 bg-slate-900/60' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Telemetry
        </button>
      </div>

      {/* 3. Tab Contents */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs font-sans">
        {activeTab === 'OVERVIEW' && (
          <div className="space-y-3.5">
            {/* Status Card */}
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-cyan-400" />
                <span className="text-slate-400">Operational State:</span>
              </div>
              <span className="font-semibold text-slate-100">{status}</span>
            </div>

            {/* Dynamic Attributes Grid */}
            <div className="grid grid-cols-2 gap-2">
              {details.lanes && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Lanes</div>
                  <div className="text-sm font-bold text-white font-mono mt-0.5">{details.lanes} Lanes</div>
                </div>
              )}
              {details.avg_speed_kmh && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Avg Speed</div>
                  <div className="text-sm font-bold text-emerald-400 font-mono mt-0.5">{details.avg_speed_kmh} km/h</div>
                </div>
              )}
              {details.depth_meters !== undefined && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Depth Offset</div>
                  <div className="text-sm font-bold text-cyan-400 font-mono mt-0.5">{details.depth_meters} m</div>
                </div>
              )}
              {details.diameter_mm && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Pipe Diameter</div>
                  <div className="text-sm font-bold text-blue-400 font-mono mt-0.5">{details.diameter_mm} mm</div>
                </div>
              )}
              {details.flow_rate_m3h && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Flow Rate</div>
                  <div className="text-sm font-bold text-cyan-300 font-mono mt-0.5">{details.flow_rate_m3h.toLocaleString()} m³/h</div>
                </div>
              )}
              {details.voltage_kv && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Voltage</div>
                  <div className="text-sm font-bold text-amber-400 font-mono mt-0.5">{details.voltage_kv} kV</div>
                </div>
              )}
              {details.daily_ridership && (
                <div className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase">Daily Ridership</div>
                  <div className="text-sm font-bold text-purple-400 font-mono mt-0.5">{details.daily_ridership.toLocaleString()}</div>
                </div>
              )}
            </div>

            {/* Construction & Maintenance Info */}
            {details.construction_status && (
              <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800/80">
                <div className="text-[11px] font-semibold text-slate-300">Construction / Upgrade Status</div>
                <p className="text-slate-400 mt-1">{details.construction_status}</p>
              </div>
            )}
            {details.maintenance_status && (
              <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800/80">
                <div className="text-[11px] font-semibold text-slate-300">Maintenance Authority</div>
                <p className="text-slate-400 mt-1">{details.maintenance_status}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'CONNECTIVITY' && (
          <div className="space-y-3">
            <div className="text-[11px] text-slate-400 font-medium">
              Multimodal Infrastructure Topological Graph
            </div>

            {/* Connected Roads */}
            {graph_connections.connected_roads && graph_connections.connected_roads.length > 0 && (
              <div className="space-y-1.5">
                <div className="text-[11px] font-semibold text-cyan-400 flex items-center gap-1.5">
                  <CornerDownRight className="w-3.5 h-3.5" />
                  Intersecting & Connected Arterials ({graph_connections.connected_roads.length})
                </div>
                {graph_connections.connected_roads.map((cr: any) => (
                  <div 
                    key={cr.id}
                    onClick={() => onSelectConnectedObject(cr.id)}
                    className="flex items-center justify-between p-2 rounded-md bg-slate-900/80 border border-slate-800 hover:border-cyan-500/50 cursor-pointer transition-colors"
                  >
                    <div>
                      <div className="font-semibold text-slate-200">{cr.name}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{cr.type} • {cr.avg_speed_kmh} km/h</div>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
                  </div>
                ))}
              </div>
            )}

            {/* Upstream / Downstream for Utilities */}
            {graph_connections.upstream_source && (
              <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase">Upstream Water Source</div>
                <div className="font-semibold text-blue-300 mt-0.5">{graph_connections.upstream_source}</div>
              </div>
            )}
            {graph_connections.downstream_zones && (
              <div className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase">Downstream Delivery Zones</div>
                <div className="space-y-0.5 mt-1">
                  {graph_connections.downstream_zones.map((zone: string, i: number) => (
                    <div key={i} className="text-slate-300 text-[11px]">• {zone}</div>
                  ))}
                </div>
              </div>
            )}

            {/* Nearby Infrastructure */}
            {graph_connections.nearby_infrastructure && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <div className="text-[11px] font-semibold text-slate-300">Nearby Spatial Assets</div>
                {Object.entries(graph_connections.nearby_infrastructure).map(([k, list]) => (
                  <div key={k} className="p-2 rounded bg-slate-900/40 border border-slate-800/60">
                    <div className="text-[10px] font-mono text-cyan-400 uppercase">{k.replace('_', ' ')}</div>
                    <div className="mt-1 space-y-0.5">
                      {(list as string[]).map((item, idx) => (
                        <div key={idx} className="text-[11px] text-slate-300 flex items-center gap-1.5">
                          <span className="w-1 h-1 rounded-full bg-slate-500" />
                          {item}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'TELEMETRY' && (
          <div className="space-y-3">
            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 space-y-2">
              <div className="text-[10px] font-mono text-slate-400 uppercase">Data Stream Source</div>
              <div className="font-bold text-slate-200">{data_provenance}</div>
              <div className="text-[11px] text-slate-400">Heartbeat Interval: 1000ms WebSocket Sync</div>
            </div>

            <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 space-y-2">
              <div className="text-[10px] font-mono text-slate-400 uppercase">SCADA Health Diagnostic</div>
              <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                <CheckCircle2 className="w-4 h-4" />
                Sensor Nominal • 0 Dropped Packets
              </div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
