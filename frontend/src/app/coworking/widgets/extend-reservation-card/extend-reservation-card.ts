import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Reservation } from '../../coworking.models';
import { Observable, map, mergeMap, timer } from 'rxjs';
import { Router } from '@angular/router';
import { ReservationService } from '../../reservation/reservation.service';

@Component({
  selector: 'extend-reservation-card',
  templateUrl: './extend-reservation-card.html',
  styleUrls: ['./extend-reservation-card.css']
})
export class ExtendReservationCard {
  @Input() reservation!: Reservation;
  // implements OnInit

  constructor(
    public router: Router,
    public reservationService: ReservationService
  ) {}

  confirm() {
    // this.reservationService.extend(this.reservation, ).subscribe();
    this.router.navigate(['/coworking/reservation/', this.reservation.id]);
  }

  cancel() {
    this.router.navigate(['/coworking/reservation/', this.reservation.id]);
  }
}
