import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import {MaterialModule} from "../infrastructure/material/material.module";
import { NavbarComponent } from './navbar/navbar.component';
import { AddMovieComponent } from './add-movie/add-movie.component';
import { RouterModule } from '@angular/router';
import { MoviePageComponent } from './movie-page/movie-page.component';
@NgModule({
  declarations: [
    HomeComponent,
    NavbarComponent,
    AddMovieComponent,
    MoviePageComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule
  ],
  exports: [
    NavbarComponent
  ]
})
export class LayoutModule { }
