import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoworkingPageComponent } from './coworking-home/coworking-home.component';
import { AmbassadorPageComponent } from './ambassador-home/ambassador-home.component';
import { ReservationComponent } from './reservation/reservation.component';
import { ExtensionComponent } from './reservation/extension/extension.component';

const routes: Routes = [
  CoworkingPageComponent.Route,
  ReservationComponent.Route,
  AmbassadorPageComponent.Route,
  ExtensionComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoworkingRoutingModule {}
