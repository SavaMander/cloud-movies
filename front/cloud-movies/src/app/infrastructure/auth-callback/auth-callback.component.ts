import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-auth-callback',
  templateUrl: './auth-callback.component.html',
  styleUrls: ['./auth-callback.component.css']
})
export class AuthCallbackComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.route.fragment.subscribe((fragment: string | null) => {
      if (fragment) {
        const params = new URLSearchParams(fragment);
        const idToken = params.get('id_token');
        console.log(idToken);
        if (idToken) {
          localStorage.setItem('user', idToken);
          this.router.navigate(['/home']);
        } else {
          window.location.href = 'https://kinoteka-cdk.auth.eu-central-1.amazoncognito.com/login?client_id=61vvarcscpr7ico82i2u0b8veo&response_type=token&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fauth';
        }
      }
    });
  }
}
