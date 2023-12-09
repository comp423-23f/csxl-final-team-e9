import { AsyncPipe, CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

/* Coworking */
import { CoworkingRoutingModule } from './coworking-routing.module';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { CoworkingReservationCard } from './widgets/coworking-reservation-card/coworking-reservation-card';
import { CoworkingDropInCard } from './widgets/dropin-availability-card/dropin-availability-card.widget';
import { CoworkingHoursCard } from './widgets/operating-hours-panel/operating-hours-panel.widget';

/* Ambassador */
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';

/* Reservation */
import { ReservationComponent } from './reservation/reservation.component';

<<<<<<< HEAD
=======
/* Extension */
import { ExtensionComponent } from './reservation/extension/extension.component';
import { ExtendReservationCard } from './widgets/extend-reservation-card/extend-reservation-card';

>>>>>>> sprint-2
/* Material UI Dependencies */
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatSelectModule } from '@angular/material/select';

@NgModule({
  declarations: [
    CoworkingPageComponent,
    ReservationComponent,
    AmbassadorPageComponent,
    CoworkingDropInCard,
    CoworkingReservationCard,
    CoworkingHoursCard
  ],
  imports: [
    CommonModule,
    CoworkingRoutingModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatExpansionModule,
    MatButtonModule,
    MatTableModule,
    MatDatepickerModule,
    MatSelectModule,
    AsyncPipe
  ]
})
export class CoworkingModule {}
