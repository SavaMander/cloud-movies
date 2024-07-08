import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-movie-page',
  templateUrl: './movie-page.component.html',
  styleUrls: ['./movie-page.component.css']
})
export class MoviePageComponent implements OnInit {
  title: any;
  movie: any;
  rating: number = 0;

  constructor(
    private moviesService: MoviesService,
    private route: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.title = params["name"];
      this.moviesService.getMovie(this.title).subscribe({
        next: (response: any) => {
          this.movie = response.data;
        }
      });
    });
  }

  onDownload() {
    this.moviesService.downloadMovie(this.title).subscribe({
      next: (response: any) => {
        if (response.download_url) {
          this.moviesService.downloadFileFromS3(response.download_url).subscribe({
            next: (response: Blob) => {
              const url = window.URL.createObjectURL(response);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'movie.mp4';
              document.body.appendChild(a);
              a.click();
              window.URL.revokeObjectURL(url);
              document.body.removeChild(a);
            }
          });
        }
      }
    });
  }

  onDelete() {
    this.moviesService.deleteMovie(this.title).subscribe({
      next: (response: any) => {
        this.router.navigate(['/home']);
      }
    });
  }

  onRate() {
    this.moviesService.rateMovie(this.rating, this.title).subscribe({
      next: (response: any) => {
        this.snackbar.open('Rated successfully!', 'Close', { duration: 3000 });
      },
      error: (error: any) => {
        this.snackbar.open('Error rating the movie.', 'Close', { duration: 3000 });
      }
    });
  }

  onRateLikes(liked: boolean) {
    this.rating = liked ? 4 : 2;
    this.onRate();
    this.rating = 0;
  }
}
