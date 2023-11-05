import { Component, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Reservation } from '../../coworking.models';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { ExtensionService } from './extension.service';
import { ReservationService } from '../reservation.service';

const titleResolver: ResolveFn<string> = (
  route: ActivatedRouteSnapshot
): Observable<string> => {
  let reservationService = inject(ReservationService);
  let reservationTitle = (reservation: Reservation): string => {
    return `Reservation #${reservation.id}`; // TODO: Include State of Reservation in future version
    // of this application when the fix for this bug lands: https://github.com/angular/angular/issues/51401
  };
  return reservationService
    .get(parseInt(route.params['id']))
    .pipe(map(reservationTitle));
};

@Component({
  selector: 'app-coworking-extension',
  templateUrl: './extension.component.html',
  styleUrls: ['./extension.component.css']
})
export class ExtensionComponent {
  public static Route: Route = {
    path: 'reservation/:id/extension',
    component: ExtensionComponent,
    title: titleResolver,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };
  public id: number;
  public reservation$: Observable<Reservation>;

  constructor(
    public route: ActivatedRoute,
    public extensionService: ExtensionService,
    public router: Router
  ) {
    this.id = parseInt(route.snapshot.params['id']);
    this.reservation$ = extensionService.get(this.id);
  }
}
