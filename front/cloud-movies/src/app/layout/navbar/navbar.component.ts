import { Component, ElementRef, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { SearchComponent } from '../search/search.component';
import { AuthService } from 'src/app/infrastructure/auth.service';
import { MoviesService } from 'src/app/services/movies.service';
import { SearchRequest } from 'src/app/model/SearchRequest';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  user: string = '';
  searchValue: string = '';
  @ViewChild('selectElement')
  selectElement!: ElementRef;

  constructor(public dialog: MatDialog, private authService: AuthService, private movieService:MoviesService, private router:Router) {
    this.user = authService.getUsername();
  }
  openSearchDialog(): void {
    const dialogRef = this.dialog.open(SearchComponent, {
      height: "80%",
      width: "30%"
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  getSelectValue(): string {
    return this.selectElement.nativeElement.value;
  }

  getSearchValue(): string {
    return this.searchValue;
  }

  onSearch(){
    const search_type = this.getSelectValue().toLowerCase();
    const search_term = this.getSearchValue();
    const searchRequest : SearchRequest = {
      type: search_type,
      search_term: search_term
    }
    this.movieService.searchMovie(searchRequest);
    this.router.navigate(['/search']);
  }
}
