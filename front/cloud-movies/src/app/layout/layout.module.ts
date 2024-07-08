import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import {MaterialModule} from "../infrastructure/material/material.module";
import { NavbarComponent } from './navbar/navbar.component';
import { AddMovieComponent } from './add-movie/add-movie.component';
import { RouterModule } from '@angular/router';
import { MoviePageComponent } from './movie-page/movie-page.component';
import { SearchComponent } from './search/search.component';
import { SearchResultsComponent } from './search-results/search-results.component';
import { SubscriptionPageComponent } from './subscription-page/subscription-page.component';
import { FormsModule } from '@angular/forms';
@NgModule({
  declarations: [
    HomeComponent,
    NavbarComponent,
    AddMovieComponent,
    MoviePageComponent,
    SearchComponent,
    SearchResultsComponent,
    SubscriptionPageComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule,
    FormsModule
  ],
  exports: [
    NavbarComponent
  ]
})
export class LayoutModule { }
