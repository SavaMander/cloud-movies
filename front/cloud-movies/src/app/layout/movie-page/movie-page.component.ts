import { Component, OnInit } from '@angular/core';
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
  constructor(private moviesService: MoviesService,private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.title=params["name"];
      this.moviesService.getMovie(this.title).subscribe({
        next: (response: any) => {
          this.movie=response.data;
        }
      })
    })
  }

  onDownload(){
    this.moviesService.downloadMovie(this.title).subscribe({
      next: (response: any) => {
        console.log(response);
        if(response.download_url){
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
          })
        }
      }
    })
  }
}
