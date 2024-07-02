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
        if (idToken) {
          localStorage.setItem('user', idToken);
          this.router.navigate(['/home']);
        } else {
          window.location.href = 'https://kinoteka.auth.eu-central-1.amazoncognito.com/login?client_id=7k5pnltnj5n297ii67qoeu31lj&response_type=token&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fauth';
        }
      }
    });
  }
}
