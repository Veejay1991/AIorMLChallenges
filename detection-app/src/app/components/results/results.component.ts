import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DetectionResult } from '../../services/detection.service';

const LABEL_META: Record<string, { icon: string; color: string }> = {
  person: { icon: '🧍', color: '#4f46e5' },
  dog:    { icon: '🐕', color: '#d97706' },
  cat:    { icon: '🐈', color: '#059669' },
};

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent {
  @Input() result: DetectionResult | null = null;
  @Input() previewUrl: string | null = null;
  @Output() cleared = new EventEmitter<void>();

  labelMeta(label: string) {
    return LABEL_META[label.toLowerCase()] ?? { icon: '🎯', color: '#6b7280' };
  }

  confidencePercent(conf: number): number {
    return Math.round(conf * 100);
  }

  clear() {
    this.cleared.emit();
  }
}
