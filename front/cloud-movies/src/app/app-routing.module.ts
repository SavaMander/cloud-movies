import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './layout/home/home.component';
import { AddMovieComponent } from './layout/add-movie/add-movie.component';
import { MoviePageComponent } from './layout/movie-page/movie-page.component';
import { AuthGuard } from './infrastructure/auth.guard';
import { AuthCallbackComponent } from './infrastructure/auth-callback/auth-callback.component';
import { SearchComponent } from './layout/search/search.component';
import { SearchResultsComponent } from './layout/search-results/search-results.component';
import { SubscriptionPageComponent } from './layout/subscription-page/subscription-page.component';

const routes: Routes = [
  { component: HomeComponent, path:"home", canActivate: [AuthGuard]},
  { component: AddMovieComponent, path:"add-movie"},
  { component: MoviePageComponent, path:"movie-page/:name"},
  { component: AuthCallbackComponent, path:"auth"},
  { component: SearchResultsComponent, path: "search"},
  { component: SubscriptionPageComponent, path: "subscriptions"},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: '**', redirectTo: '/home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
