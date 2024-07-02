import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(): boolean {
    const userData = localStorage.getItem('user');

    if (userData) {
      return true;
    } else {
      window.location.href = 'https://kinoteka.auth.eu-central-1.amazoncognito.com/login?client_id=7k5pnltnj5n297ii67qoeu31lj&response_type=token&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fauth';
      return false;
    }
  }
}
