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
      window.location.href = 'https://kinoteka-cdk.auth.eu-central-1.amazoncognito.com/login?client_id=61vvarcscpr7ico82i2u0b8veo&response_type=token&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fauth';
      return false;
    }
  }
}
