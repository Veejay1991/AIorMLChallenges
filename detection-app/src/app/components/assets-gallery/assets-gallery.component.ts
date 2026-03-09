import { Component, Output, EventEmitter, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DetectionService, DetectionResult } from '../../services/detection.service';

@Component({
  selector: 'app-assets-gallery',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './assets-gallery.component.html',
  styleUrl: './assets-gallery.component.css'
})
export class AssetsGalleryComponent implements OnInit {
  @Output() detected = new EventEmitter<{ result: DetectionResult; previewUrl: string }>();

  assets = signal<string[]>([]);
  loadingAsset = signal<string | null>(null);
  error = signal<string | null>(null);

  constructor(private detectionService: DetectionService) {}

  ngOnInit() {
    this.detectionService.getAssets().subscribe({
      next: (list) => this.assets.set(list),
      error: () => this.error.set('Could not load examples. Make sure the API server is running.')
    });
  }

  detectAsset(filename: string) {
    this.loadingAsset.set(filename);
    this.detectionService.detectAsset(filename).subscribe({
      next: (result) => {
        this.loadingAsset.set(null);
        this.detected.emit({ result, previewUrl: this.detectionService.getAssetUrl(filename) });
      },
      error: () => {
        this.loadingAsset.set(null);
        this.error.set(`Detection failed for "${filename}".`);
      }
    });
  }

  getAssetUrl(filename: string): string {
    return this.detectionService.getAssetUrl(filename);
  }

  labelFromFilename(filename: string): string {
    return filename.replace(/\.[^.]+$/, '').replace(/_/g, ' ');
  }
}
