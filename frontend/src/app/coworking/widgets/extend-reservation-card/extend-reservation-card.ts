import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Extension } from '../../coworking.models';
import { Observable, map, mergeMap, timer } from 'rxjs';
import { Router } from '@angular/router';
import { ReservationService } from '../../reservation/reservation.service';
import { ExtensionService } from '../../reservation/extension/extension.service';

@Component({
  selector: 'extend-reservation-card',
  templateUrl: './extend-reservation-card.html',
  styleUrls: ['./extend-reservation-card.css']
})
export class ExtendReservationCard implements OnInit {
  @Input() extension!: Extension;

  public draftConfirmationDeadline$!: Observable<string>;

  constructor(
    public router: Router,
    public reservationService: ReservationService,
    public extensionService: ExtensionService
  ) {}

  ngOnInit(): void {
    this.draftConfirmationDeadline$ = this.initDraftConfirmationDeadline();
  }

  confirm() {
    this.extensionService.extend();
  }

  cancel() {}

  private initDraftConfirmationDeadline(): Observable<string> {
    const fiveMinutes =
      5 /* minutes */ * 60 /* seconds */ * 1000; /* milliseconds */

    const extensionDraftDeadline = (extension: Extension) =>
      extension.created_at.getTime() + fiveMinutes;

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
      map(() => this.extension),
      map(extensionDraftDeadline),
      map(deadlineString)
    );
  }
}
