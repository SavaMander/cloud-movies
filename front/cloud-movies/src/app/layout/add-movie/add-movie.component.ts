import { formatDate } from '@angular/common';
import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { MovieRequest } from 'src/app/model/MovieRequest';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-add-movie',
  templateUrl: './add-movie.component.html',
  styleUrls: ['./add-movie.component.css']
})
export class AddMovieComponent {
  genres: string[] = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller'];
  selectedFile?: File;
  selectedPhoto?: File;

  movieForm = new FormGroup({
    title: new FormControl('', Validators.required),
    description: new FormControl('', Validators.required),
    actors: new FormControl('', Validators.required),
    director: new FormControl('', Validators.required),
    genres: new FormArray([], Validators.required),
    moviePicture: new FormControl(null, Validators.required),
    movieFile: new FormControl(null, Validators.required)
  });

  constructor(private fb: FormBuilder, private moviesService: MoviesService, private snackBar: MatSnackBar,private router: Router) {}

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

  onFileChange(event: any): void {
    if (event.target.files.length > 0) {
      const file: File = event.target.files[0];
      const fileSizeInMb: number = file.size / (1024 * 1024);
      if (fileSizeInMb > 300) {
        alert('File size exceeds 300MB');
        this.movieForm.patchValue({ movieFile: null });
        return;
      }
      this.selectedFile = file;
      console.log(this.selectedFile);
    }
  }

  onPhotoChange(event: any): void {
    if (event.target.files.length > 0) {
      const photo: File = event.target.files[0];
      this.selectedPhoto = photo;

    }
  }

  onSubmit(): void {
    if (this.movieForm.valid && this.selectedFile && this.selectedPhoto) {
      const genresString = Array.isArray(this.movieForm.value.genres) ? this.movieForm.value.genres.join(',') : '';
      let date = new Date(this.selectedFile.lastModified).toDateString();
      const movieRequest: MovieRequest = {
        title: this.movieForm.value.title || '',
        description: this.movieForm.value.description || '',
        actors: this.movieForm.value.actors || '',
        director: this.movieForm.value.director || '',
        genres: genresString,
        name: this.selectedFile.name,
        type: this.selectedFile.type,
        size: (this.selectedFile.size/(1024*1024)).toFixed(2).toString(),
        dateCreated: date,
        dateModified: date
      }
      console.log(JSON.stringify(movieRequest));
      this.moviesService.addMovie(movieRequest).subscribe({
        next: (response: any) => {
          console.log(response);
          if(this.selectedFile && response.upload_url){
          this.moviesService.uploadFileToS3(this.selectedFile,response.upload_url).subscribe({
            next: (response: any) => {
              this.snackBar.open('Movie uploaded successfully!', 'Close', {
                duration: 3000,
              });
              this.router.navigate(['/home']);
            }
          })
        }
        }
      });
    } else {
      this.snackBar.open('Enter all required data', 'Close', {
        duration: 3000,
      });
    }
  }
  
}
