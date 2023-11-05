import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { Observable } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Reservation } from '../../coworking.models';

@Component({
  selector: 'app-coworking-extension',
  templateUrl: './extension.component.html',
  styleUrls: ['./extension.component.css']
})
export class ExtensionComponent {}
