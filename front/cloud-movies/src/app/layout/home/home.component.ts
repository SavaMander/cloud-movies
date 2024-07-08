import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  items: any[] = [];
  

  constructor(private moviesService: MoviesService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.moviesService.getMoviesForPersonalizedFeed().subscribe({
      next: (response: any) => {
        if (response && response.length > 0) {
          for (const movie of response) {
            this.items.push(movie);
          }
          console.log("feed")
        } else {
          // If response is empty
          console.log("fetchAllMovies");

          this.fetchAllMovies();
        }
      },
      error: (err: any) => {
        console.error('Error fetching personalized feed movies:', err);
        this.fetchAllMovies();
      }
    });
  }
  
  fetchAllMovies(): void {
    this.moviesService.getAllMovies().subscribe({
      next: (response: any) => {
        for (const movie of response) {
          this.items.push(movie);
        }
      },
      error: (err: any) => {
        console.error('Error fetching all movies:', err);
      }
    });
  }
  
}
