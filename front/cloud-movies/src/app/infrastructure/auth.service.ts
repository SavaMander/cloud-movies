import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private jwtHelper: JwtHelperService) { }

  isLoggedIn(): boolean {
    return localStorage.getItem('user') != null;
  }

  getUsername(): any {
    if(this.isLoggedIn()){
      const accessToken: any=localStorage.getItem('user');
      const decodedToken = this.jwtHelper.decodeToken(accessToken);
      return decodedToken['cognito:username'];
    }
  }
}
