# Feature: Extending a Drop-in Reservation

> Written by Isha Atre, Chloe Carroll, Lauren Jones, and Soumya Mahavadi<br> > _Last Updated: 11/01/2023_

## Overview

This feature allows students who have 30 minutes or less left in their current drop-in reservation to be able to extend it for up to an additional hour, only if no other student has reserved their current seat immediately after.

## Key Personas

**Sally Student** wants to know if her drop-in reservation can be extended and have the ability to extend it by up to an hour if so.

**Amy Ambassador** and **Rhonda Root** wants the ability to extend Sally Student's drop-in reservation if there is no reservation immediately following it.

## User Stories

**Story A:**
As Sally Student, if the following time slot for my current seat is available, I want the ability to extend my drop-in seat reservation by up to 1 additional hour, in increments of 15 minutes. If the following time slot is reserved, I want to know that I cannot extend and see the time remaining on my reservation.

**Story B:**
As Sally Student, if the time slot following mine is originally reserved, but that reservation is cancelled, the option to extend my current reservation should reappear.

**Story C:**
As Amy Ambassador or Rhonda Root, if the time slot following Sally Student's original time slot is available for booking, I want the ability to extend the reservation on behalf of Sally Student, upon their request.

**Story D:**
As Sally Student, if I want to spend more or less time in the CSXL Lab than my reservation is automatically calculated for, I want to be able to alter the time slots of my reservation. The initial reservation should be between 15 minutes and 2 hours.

## Wireframes

Based on our wireframe, the initial landing page in the CSXL Lab is titled "Make a Reservation." Here, we haveintegrated image icons alongside key information such as "First Name," "Last Name," "Sitterson 011," "Monitor #," the date, and start-stop clock icons. These enhancements not only add to the visual appeal of the website. but also provide users with more intuitive information compared to the original CSXL Reservation page. Notably, we have separated the "Confirm" button and the "Time Remaining to Cancel" feature to make it more user friendly.

Moving on to the second page, "Reservation Confirmation," users are presented with text labels paired with image icons, including "First Name," "Last Name," "Sitterson 011," "Monitor #," "Day and Date," and "Start and End Time." On this page, users have the option to click the button “Extend”in order to extend their reservation. This button should only appear when there is 30 minutes left. This design decision aligns with a logical user flow, because the option to edit should follow the reservation confirmation since it is the final page the user has open.

Once the “Extend” button is clicked, it will direct the user to the last page, "Extend a Reservation," which has the same design as the "Make a Reservation" page's appearance. Here, users can adjust their reservation times in 15-minute increments. This specific time interval was chosen because 5 minutes appeared too brief, and 30 minutes felt excessive for users looking to extend their original reservations.

## Technical Implementation Opportunities and Planning

**What specific areas of the existing code base will you directly depend upon, extend, or integrate with?**

We will directly depend upon the reservation models defined in backend/models/coworking/reservation.py as well as the API routes to retrieve and update existing reservations. Ideally, we'd like to utilize the update_reservation method in backend/api/coworking/reservation.py, but because entending should route the user to a new page, we may have to create a new one with a route involving the extension page rather than @api.put("/reservation/{id}", tags=["Coworking"]).

In the frontend, we will be adding a new extension component which will have a route from the current reservation component. We will also need to extend the current widgets used for the reservation card. We plan to add an extend method within the ReservationService located at frontend/src/app/coworking/reservation/reservation.service.ts.

**What planned page components and widgets, per the assigned reading, do you anticipate needing in your feature’s frontend?**

First, we anticipate editing the coworking-reservation-card located at frontend/src/app/coworking/widgets/coworking-reservation-card by adding an "extend" button that would only show up if an extension was permitted, as well as a countdown timer to reveal how much time is left in Sally Student's current reservation on the reservation confirmation page. We also plan to add a new page component for an extension form/page that Sally Student can navigate to if an extension is permitted, so that they can decide how much time to extend their current reservation by. In addition, we plan on adding a time picker widget (https://m3.material.io/components/time-pickers/overview, https://stackoverflow.com/questions/45791339/how-to-implement-a-datetime-picker-in-ionic-2-to-select-time-range) to coworking-reservation-card to improve the current UI in terms of selecting start and end times when creating a new reservation.

**What additional models, or changes to existing models, do you foresee needing (if any)?**

We do not foresee the need to create or change any models for this feature. We plan to utilize the ReservationDetails class predefined in backend/models/coworking/reservation.py, which already contains three attributes concerning extensions that are needed for our feature. We can use the SeatAvailability class located in backend/models/coworking/availability.py to determine whether or not Sally Student's seat is reserved for the next time slot. For Story D, we plan to update the current functionality of creating reservations to allow students to be able to reserve a seat for up to 2 hours in increments of 15 minutes. However, this will not require a change to the existing backend reservation model since the ReservationPartial class has fields to store the start and end times of the reservation.

**Considering your most-frequently used and critical user stories, what API / Routes do you foresee modifying or needing to add?**

We foresee calling upon the PUT API route found in backend/api/coworking/reservation.py to update Sally Student's current reservation with a new end time when they request an extension. We will also need a new route in the frontend for the extension page component we will add.

**What concerns exist for security and privacy of data? Should the capabilities you are implementing be specific to only certain users or roles?**

When Sally Student makes a reservation, only Sally Student, Amy Ambassador, and Rhonda Root should be able to cancel or extend the reservation. Other students should not be able to cancel, extend, or even view Sally Student's reservation. If Sally Student wants to extend their reservation but cannot because the next time slot is already reserved by another student, Sally should not be able to see exactly who has a reservation after them, just that they cannot extend theirs. Only Amy Ambassador and Rhonda Root should be able to see which students have current and scheduled reservations.
