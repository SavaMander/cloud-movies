import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  items: any[] = [];

  constructor(private moviesService: MoviesService, private router: Router) {}

  ngOnInit(): void {
    this.moviesService.getAllMovies().subscribe({
      next: (response: any) => {
        for (const movie of response) {
          this.items.push(movie);
        }
      },
      error: (err: any) => {
        console.error('Error fetching movies:', err);
      }
    });
  }
}
