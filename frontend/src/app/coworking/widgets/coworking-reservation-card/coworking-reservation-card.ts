import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { Reservation } from '../../coworking.models';
import { Observable, interval, map, mergeMap, shareReplay, timer } from 'rxjs';
import { Router } from '@angular/router';
import { ReservationService } from '../../reservation/reservation.service';
import { timeComponents } from './timeComponents';
import { formatDate } from '@angular/common';
import { MatSelect } from '@angular/material/select';

@Component({
  selector: 'coworking-reservation-card',
  templateUrl: './coworking-reservation-card.html',
  styleUrls: ['./coworking-reservation-card.css']
})
export class CoworkingReservationCard implements OnInit {
  @Input() reservation!: Reservation;
  @ViewChild('extendAmountElement') extendAmount!: MatSelect;

  public draftConfirmationDeadline$!: Observable<string>;
  public remainingTime: timeComponents = { hours: 0, minutes: 0, seconds: 0 };
  public thirtyMinutesLeft: boolean = false;
  public eligibleForExtension: boolean = false;
  public maxExtendAmount: number = 0;
  public extendPressed: boolean = false;

  constructor(
    public router: Router,
    public reservationService: ReservationService
  ) {}

  ngOnInit(): void {
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
    if (
      this.reservation.state !== 'CANCELLED' &&
      this.reservation.state !== 'CHECKED_OUT'
    ) {
      this.reservationService
        .watchRemainingTime(this.reservation.id, 1000)
        .subscribe((data) => {
          this.remainingTime = this.secondsToTimeComponent(data);
        });
    }
  }

  checkinDeadline(reservationStart: Date): Date {
    return new Date(reservationStart.getTime() + 10 * 60 * 1000);
  }

  cancel() {
    this.reservationService.cancel(this.reservation).subscribe();
  }

  confirm() {
    this.reservationService.confirm(this.reservation).subscribe();
  }

  checkout() {
    this.reservationService.checkout(this.reservation).subscribe();
  }

  extend() {
    this.reservationService
      .extend(this.reservation, this.extendAmount.value)
      .subscribe();
    window.location.reload();
  }

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

  private secondsToTimeComponent(totalSeconds: number): timeComponents {
    const hours = Math.floor((totalSeconds / (60 * 60)) % 24);
    const minutes = Math.floor((totalSeconds / 60) % 60);
    const seconds = Math.floor(totalSeconds) % 60;
    if (totalSeconds / 60 <= 30) {
      this.thirtyMinutesLeft = true;
      this.reservationService
        .getMaxExtensionTime(this.reservation.id)
        .subscribe((data) => {
          this.maxExtendAmount = data;
          this.eligibleForExtension = data > 0;
        });
    }
    return { seconds, minutes, hours };
  }

  getExtensionIntervals(): number[] {
    let intervals = [];
    for (let i = 15; i <= this.maxExtendAmount; i += 15) {
      intervals.push(i);
    }
    return intervals;
  }

  formatReservationTimes(start: Date, end: Date): string {
    const startTime = this.formatTime(start);
    const endTime = this.formatTime(end);

    if (
      (startTime.endsWith('AM') && endTime.endsWith('AM')) ||
      (startTime.endsWith('PM') && endTime.endsWith('PM'))
    ) {
      return `${startTime.slice(0, -3)} - ${endTime}`;
    }

    return `${startTime} - ${endTime}`;
  }

  private formatTime(date: Date): string {
    return formatDate(date, 'shortTime', 'en-US');
  }
}
