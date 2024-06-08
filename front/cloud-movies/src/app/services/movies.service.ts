import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MovieRequest } from '../model/MovieRequest';
import { environment } from '../env/env';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {

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
}
