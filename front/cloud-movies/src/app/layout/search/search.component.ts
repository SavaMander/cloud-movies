import { Component } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  constructor(public dialogRef: MatDialogRef<SearchComponent>) {}

  genres: string[] = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller'];

  movieForm = new FormGroup({
    title: new FormControl('', Validators.required),
    description: new FormControl('', Validators.required),
    actors: new FormControl('', Validators.required),
    director: new FormControl('', Validators.required),
    genres: new FormArray([], Validators.required),
    movieFile: new FormControl(null, Validators.required)
  });

  onClose(): void {
    this.dialogRef.close();
  }

  onCheckboxChange(event: any) {
    const genres: FormArray = this.movieForm.get('genres') as FormArray;
    if (event.source.checked) {
      genres.push(new FormControl(event.source.value));
    } else {
      const index = genres.controls.findIndex((x) => x.value === event.source.value);
      if (index !== -1) {
        genres.removeAt(index);
      }
    }
  }
}
