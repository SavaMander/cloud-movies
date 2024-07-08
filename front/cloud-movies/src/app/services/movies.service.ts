import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { MovieRequest } from '../model/MovieRequest';
import { environment } from '../env/env';
import { SearchRequest } from '../model/SearchRequest';
import { SubscriptionRequest } from '../model/SubscriptionRequest';
import { AuthService } from '../infrastructure/auth.service';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private searchResults = new BehaviorSubject<any[]>([]);

  constructor(private http: HttpClient, private authService: AuthService) {
  }
  username: string = this.authService.getUsername();

  addMovie(movieRequest: MovieRequest): Observable<any> {
    return this.http.post<any>(environment.apiHost+"movies", movieRequest);
  }

  uploadFileToS3(file: File, presignedURL: string): Observable<any> {
    return this.http.put<any>(presignedURL, file, {
      headers: {
        'Content-Type': file.type
      }
    });
  }

  getMoviesForPersonalizedFeed(): Observable<any> {
    const apiUrl = `${environment.apiHost}movies/feed?username=${this.username}`;
    return this.http.get<any>(apiUrl);
  }

  getAllMovies(): Observable<any> {
    return this.http.get<any>(environment.apiHost+"movies");
  }

  getMovie(title: string): Observable<any> {
    return this.http.get<any>(environment.apiHost+"movies/"+title)
  }

  downloadMovie(title: string): Observable<any> {
    const apiUrl = `${environment.apiHost}movies/download/${title}?username=${this.username}`;
    return this.http.get<any>(apiUrl);
  }

  downloadFileFromS3(presignedURL: string): Observable<Blob> {
    return this.http.get(presignedURL, { responseType: 'blob' });
  }

  deleteMovie(title: string): Observable<any> {
    return this.http.delete<any>(environment.apiHost+"movies/"+title);
  }

  searchMovie(searchRequest: SearchRequest): void {
    this.http.post<any[]>(environment.apiHost+"movies/search",searchRequest).subscribe(
      results => {
        this.searchResults.next(results);
      }
    );
  }

  getSearchResults(): Observable<any[]> {
    return this.searchResults.asObservable();
  }

  subcribe(subscriptionRequest: SubscriptionRequest): Observable<any> {
    return this.http.post<any>(environment.apiHost+"subscribe",subscriptionRequest);
  }

  rateMovie(rating: number, title: string): Observable<any> {
    const body = { rating };
    return this.http.post<any>(`${environment.apiHost}movies/rate/${title}?username=${this.username}`, body);
  }
}
