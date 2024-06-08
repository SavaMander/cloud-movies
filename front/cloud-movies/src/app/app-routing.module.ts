import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './layout/home/home.component';
import { AddMovieComponent } from './layout/add-movie/add-movie.component';
import { MoviePageComponent } from './layout/movie-page/movie-page.component';

const routes: Routes = [
  { component: HomeComponent, path:"home" },
  { component: AddMovieComponent, path:"add-movie"},
  { component: MoviePageComponent, path:"movie-page/:name"},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: '**', redirectTo: '/home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
