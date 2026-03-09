import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Detection {
  label: string;
  confidence: number;
}

export interface DetectionResult {
  detections: Detection[];
  message: string;
}

@Injectable({ providedIn: 'root' })
export class DetectionService {
  private readonly apiBase = 'http://localhost:8000/api';
  private http = inject(HttpClient);

  getAssets(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiBase}/assets`);
  }

  detectUpload(file: File): Observable<DetectionResult> {
    const form = new FormData();
    form.append('file', file, file.name);
    return this.http.post<DetectionResult>(`${this.apiBase}/detect/upload`, form);
  }

  detectAsset(filename: string): Observable<DetectionResult> {
    return this.http.post<DetectionResult>(`${this.apiBase}/detect/asset/${encodeURIComponent(filename)}`, {});
  }

  getAssetUrl(filename: string): string {
    return `http://localhost:8000/assets/${encodeURIComponent(filename)}`;
  }
}
