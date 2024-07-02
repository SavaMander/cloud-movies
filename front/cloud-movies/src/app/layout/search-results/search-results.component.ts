import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent {
  items: any[] = [];

  constructor(private moviesService: MoviesService, private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.moviesService.getSearchResults().subscribe({
      next: (response: any) => {
        this.items = response;
      },
      error: (err: any) => {
        console.error('Error fetching search results:', err);
      }
    });
  }
}
