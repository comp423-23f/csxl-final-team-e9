import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Reservation } from '../../coworking.models';
import { Observable, interval, map, mergeMap, shareReplay, timer } from 'rxjs';
import { Router } from '@angular/router';
import { ReservationService } from '../../reservation/reservation.service';
import { ExtensionService } from '../../reservation/extension/extension.service';
import { timeComponents } from './timeComponents';

@Component({
  selector: 'coworking-reservation-card',
  templateUrl: './coworking-reservation-card.html',
  styleUrls: ['./coworking-reservation-card.css']
})
export class CoworkingReservationCard implements OnInit {
  @Input() reservation!: Reservation;

  public draftConfirmationDeadline$!: Observable<string>;
  public reservationCountdown$!: Observable<timeComponents>;
  public thirtyMinutes: boolean = false;

  constructor(
    public router: Router,
    public reservationService: ReservationService,
    public extensionService: ExtensionService
  ) {}

  ngOnInit(): void {
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
  }

  checkinDeadline(reservationStart: Date): Date {
    return new Date(reservationStart.getTime() + 10 * 60 * 1000);
  }

  cancel() {
    this.reservationService.cancel(this.reservation).subscribe();
  }

  confirm() {
    this.reservationService.confirm(this.reservation).subscribe();
    this.reservationCountdown$ = this.initReservationCountdown();
  }

  checkout() {
    this.reservationService.checkout(this.reservation).subscribe();
  }

  /*extend() {
    this.extensionService.extend(this.reservation).subscribe();
  }*/

  private initDraftConfirmationDeadline(): Observable<string> {
    const fiveMinutes =
      5 /* minutes */ * 60 /* seconds */ * 1000; /* milliseconds */

    const reservationDraftDeadline = (reservation: Reservation) =>
      reservation.created_at.getTime() + fiveMinutes;

    const deadlineString = (deadline: number): string => {
      const now = new Date().getTime();
      const delta = (deadline - now) / 1000; /* milliseconds */
      if (delta > 60) {
        return `Confirm in ${Math.ceil(delta / 60)} minutes`;
      } else if (delta > 0) {
        return `Confirm in ${Math.ceil(delta)} seconds`;
      } else {
        this.cancel();
        return 'Cancelling...';
      }
    };

    return timer(0, 1000).pipe(
      map(() => this.reservation),
      map(reservationDraftDeadline),
      map(deadlineString)
    );
  }

  private initReservationCountdown(): Observable<timeComponents> {
    const twoHours =
      2 /* hours */ *
      60 /* minutes */ *
      60 /* seconds */ *
      1000; /* milliseconds */

    //const reservationDeadline = (reservation: Reservation) =>
    //  reservation.created_at.getTime() + twoHours;
    const reservationDeadline = (reservation: Reservation) =>
      reservation.end.getTime();

    const countdownString = (deadline: number): timeComponents => {
      const now = new Date().getTime();
      const delta = (deadline - now) / 1000; /* seconds */
      const hours = Math.floor((delta / (60 * 60)) % 24);
      const minutes = Math.floor((delta / 60) % 60);
      const seconds = Math.floor(delta) % 60;
      if (delta / 60 <= 30) {
        this.thirtyMinutes = true;
      }
      return { seconds, minutes, hours };
    };

    return timer(0, 1000).pipe(
      map(() => this.reservation),
      map(reservationDeadline),
      map(countdownString)
    );
  }
}
