import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { MovieRequest } from '../model/MovieRequest';
import { environment } from '../env/env';
import { SearchRequest } from '../model/SearchRequest';
import { SubscriptionRequest } from '../model/SubscriptionRequest';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private searchResults = new BehaviorSubject<any[]>([]);

  constructor(private http: HttpClient) {
  }

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

  getAllMovies(): Observable<any> {
    return this.http.get<any>(environment.apiHost+"movies");
  }

  getMovie(title: string): Observable<any> {
    return this.http.get<any>(environment.apiHost+"movies/"+title)
  }

  downloadMovie(title: string): Observable<any> {
    return this.http.get<any>(environment.apiHost+"movies/download/"+title);
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
}
