import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Extension, Reservation } from '../../coworking.models';
import { ReservationService } from '../reservation.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExtensionService {
  public reservation$: Observable<Reservation> | undefined;

  constructor(
    private http: HttpClient,
    private reservationService: ReservationService
  ) {}

  get(id: number): Observable<Reservation> {
    return this.reservationService.get(id);
  }

  extendable(id: number) {
    let endpoint = `/api/coworking/reservation/${id}`;
    return this.http.get<boolean>(endpoint);
  }
  cancel() {}

  extend() {}
}
