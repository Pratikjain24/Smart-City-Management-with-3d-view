export type TelemetryCallback = (data: any) => void;
export type ConnectionState = 'connecting' | 'connected' | 'disconnected';
export type ConnectionCallback = (state: ConnectionState) => void;

class MahaTwinTelemetryStream {
  private ws: WebSocket | null = null;
  private listeners: Set<TelemetryCallback> = new Set();
  private connectionListeners: Set<ConnectionCallback> = new Set();
  private reconnectTimeout: any = null;
  private isExplicitlyClosed = false;

  public connect() {
    this.isExplicitlyClosed = false;
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/live-stream`;

    this.notifyConnectionState('connecting');
    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        this.notifyConnectionState('connected');
        console.log('[MahaTwin WS] Connected to live telemetry stream');
      };

      this.ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          this.listeners.forEach((callback) => callback(payload));
        } catch (err) {
          console.error('[MahaTwin WS] Error parsing message:', err);
        }
      };

      this.ws.onclose = () => {
        this.notifyConnectionState('disconnected');
        if (!this.isExplicitlyClosed) {
          console.warn('[MahaTwin WS] Disconnected. Reconnecting in 3s...');
          this.reconnectTimeout = setTimeout(() => this.connect(), 3000);
        }
      };

      this.ws.onerror = (err) => {
        console.error('[MahaTwin WS] Error:', err);
        this.ws?.close();
      };
    } catch (e) {
      console.error('[MahaTwin WS] Connection exception:', e);
      this.reconnectTimeout = setTimeout(() => this.connect(), 3000);
    }
  }

  public subscribe(callback: TelemetryCallback): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  public subscribeConnection(callback: ConnectionCallback): () => void {
    this.connectionListeners.add(callback);
    return () => this.connectionListeners.delete(callback);
  }

  private notifyConnectionState(state: ConnectionState) {
    this.connectionListeners.forEach((callback) => callback(state));
  }

  public disconnect() {
    this.isExplicitlyClosed = true;
    this.notifyConnectionState('disconnected');
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const telemetryStream = new MahaTwinTelemetryStream();
