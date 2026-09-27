import React, { useState, useEffect } from 'react';
import { Activity, Compass, Eye, Radio } from 'lucide-react';
import { ConnectionState } from '../../services/websocket';

interface PerformanceHUDProps {
  isGoogle3DLoaded: boolean;
  connectionState: ConnectionState;
}

export const PerformanceHUD: React.FC<PerformanceHUDProps> = ({ isGoogle3DLoaded, connectionState }) => {
  const [fps, setFps] = useState(60);

  useEffect(() => {
    let frameCount = 0;
    let lastTime = performance.now();
    let animationId: number;

    const calculateFps = () => {
      frameCount++;
      const now = performance.now();
      if (now - lastTime >= 1000) {
        setFps(Math.min(60, Math.round((frameCount * 1000) / (now - lastTime))));
        frameCount = 0;
        lastTime = now;
      }
      animationId = requestAnimationFrame(calculateFps);
    };

    animationId = requestAnimationFrame(calculateFps);
    return () => cancelAnimationFrame(animationId);
  }, []);

  return (
    <div className="absolute top-18 right-6 z-20 flex items-center gap-3 px-3 py-1.5 rounded-lg bg-slate-950/80 border border-slate-800 text-[11px] font-mono text-slate-400 backdrop-blur-md">
      <div className="flex items-center gap-1.5">
        <Activity className={`w-3.5 h-3.5 ${fps >= 50 ? 'text-emerald-400' : 'text-amber-400'}`} />
        <span>{fps} FPS</span>
      </div>
      <div className="w-px h-3 bg-slate-800" />
      <div className="flex items-center gap-1.5" title="Simulated telemetry connection">
        <Radio className={`w-3.5 h-3.5 ${connectionState === 'connected' ? 'text-emerald-400' : 'text-amber-400'}`} />
        <span>{connectionState === 'connected' ? 'SIM STREAM' : connectionState.toUpperCase()}</span>
      </div>
      <div className="w-px h-3 bg-slate-800" />
      <div className="flex items-center gap-1.5">
        <Eye className="w-3.5 h-3.5 text-cyan-400" />
        <span className="text-slate-300">
          {isGoogle3DLoaded ? 'Google 3D Tiles' : 'Cesium 3D Terrain'}
        </span>
      </div>
      <div className="w-px h-3 bg-slate-800" />
      <div className="flex items-center gap-1.5">
        <Compass className="w-3.5 h-3.5 text-blue-400" />
        <span>19.076° N, 72.877° E</span>
      </div>
    </div>
  );
};
