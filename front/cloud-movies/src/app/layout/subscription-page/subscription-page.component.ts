import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from 'src/app/infrastructure/auth.service';
import { SubscriptionRequest } from 'src/app/model/SubscriptionRequest';
import { MoviesService } from 'src/app/services/movies.service';

@Component({
  selector: 'app-subscription-page',
  templateUrl: './subscription-page.component.html',
  styleUrls: ['./subscription-page.component.css']
})
export class SubscriptionPageComponent {
  subscriptionValue: string = "";

  constructor(public movieService: MoviesService, private authService: AuthService, private snackbar: MatSnackBar){

  }

  onSubscribe(){
    const subscription: SubscriptionRequest = {
      username: this.authService.getUsername(),
      subscription: this.subscriptionValue
    }

    this.movieService.subcribe(subscription).subscribe({
      next: (response: any) => {
        this.snackbar.open('Successfully subscribed!', 'Close', {
          duration: 3000,
        });
      },
      error: (err) => {
        console.error('Subscription error:', err);
        this.snackbar.open('Subscription failed. Please try again later.', 'Close', {
          duration: 3000,
        });
      }
    })
  }
}
