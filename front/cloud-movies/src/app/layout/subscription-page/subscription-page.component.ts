import { Component, OnInit } from '@angular/core';
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
  subscriptions: string[] = [];

  constructor(public movieService: MoviesService, private authService: AuthService, private snackbar: MatSnackBar){

  }

  ngOnInit(): void {
    this.loadSubscriptions();
  }

  loadSubscriptions(): void {
    this.movieService.getSubscriptions().subscribe({
      next: (subscriptions: string[]) => {
        this.subscriptions = subscriptions;
      },
      error: (err) => {
        console.error('Error loading subscriptions:', err);
        this.snackbar.open('Failed to load subscriptions. Please try again later.', 'Close', {
          duration: 3000,
        });
      }
    });
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

  onDeleteSubscription(subscription: string) {
    this.movieService.deleteSubscription(subscription).subscribe({
      next: (response: any) => {
        this.snackbar.open('Subscription deleted.', 'Close', {
          duration: 3000,
        });
      },
      error: (err) => {
        console.error('Failed to delete subscription:', err);
        this.snackbar.open('Failed to delete subscription. Please try again later.', 'Close', {
          duration: 3000,
        });
      }
    });
  }
  
}
