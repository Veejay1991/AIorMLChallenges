import { Component, signal, ViewChild } from '@angular/core';
import { UploadComponent } from './components/upload/upload.component';
import { AssetsGalleryComponent } from './components/assets-gallery/assets-gallery.component';
import { ResultsComponent } from './components/results/results.component';
import { DetectionResult } from './services/detection.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [UploadComponent, AssetsGalleryComponent, ResultsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  @ViewChild(UploadComponent) uploadComponent!: UploadComponent;

  result = signal<DetectionResult | null>(null);
  previewUrl = signal<string | null>(null);

  onDetected(event: { result: DetectionResult; previewUrl: string }) {
    this.uploadComponent?.clearSilent();
    this.result.set(event.result);
    this.previewUrl.set(event.previewUrl);
  }

  clearResults() {
    this.result.set(null);
    this.previewUrl.set(null);
    this.uploadComponent?.clearPreview();
  }

  onUploadCleared() {
    this.result.set(null);
    this.previewUrl.set(null);
  }
}
