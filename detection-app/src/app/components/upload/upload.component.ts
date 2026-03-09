import { Component, Output, EventEmitter, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DetectionService, DetectionResult } from '../../services/detection.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadComponent {
  @Output() detected = new EventEmitter<{ result: DetectionResult; previewUrl: string }>();
  @Output() cleared = new EventEmitter<void>();

  isDragging = signal(false);
  isLoading = signal(false);
  error = signal<string | null>(null);
  previewUrl = signal<string | null>(null);

  constructor(private detectionService: DetectionService) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(true);
  }

  onDragLeave() {
    this.isDragging.set(false);
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);
    const file = event.dataTransfer?.files[0];
    if (file) this.processFile(file);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) this.processFile(file);
    // Reset so the same file can be selected again
    input.value = '';
  }

  private processFile(file: File) {
    if (!file.type.startsWith('image/')) {
      this.error.set('Please select a valid image file.');
      return;
    }
    this.error.set(null);

    const reader = new FileReader();
    reader.onload = (e) => this.previewUrl.set(e.target?.result as string);
    reader.readAsDataURL(file);

    this.isLoading.set(true);
    this.detectionService.detectUpload(file).subscribe({
      next: (result) => {
        this.isLoading.set(false);
        this.detected.emit({ result, previewUrl: this.previewUrl()! });
      },
      error: (err) => {
        this.isLoading.set(false);
        this.error.set('Detection failed. Make sure the API server is running.');
      }
    });
  }

  clearPreview() {
    this.previewUrl.set(null);
    this.error.set(null);
    this.cleared.emit();
  }

  clearSilent() {
    this.previewUrl.set(null);
    this.error.set(null);
  }
}
