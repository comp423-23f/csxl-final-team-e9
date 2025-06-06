# Technical Specification

> Authors: <br>Isha Atre (https://github.com/Ishaatre) <br>Chloe Carroll (https://github.com/chloeecarroll) <br>Lauren Jones (https://github.com/laurennnjones) <br>Soumya Mahavadi (https://github.com/ssmahavadi) <br>_Last Updated: 12/12/2023_

## 1. Descriptions and sample data representations of new or modified model representation(s) and API routes

The only API routes we've made and implemented were for time remaining and extension eligibility. Time remaining was added as an attribute for the reservation object, so the API route passed this field to the frontend, where we can display it in the format of our timer. Extension eligibility was determined by backend methods created to check if there are reservations in the hour following a given reservation. This API route allows our frontend to make use of these methods and display the extension button accordingly.

## 2. Description of underlying database/entity-level representation decisions

We added the timeRemaining attribute to the reservation entity. We made it a dynamic property so that it can be re-evaluated and updated every second.

## 3. Technical and UX Design Choices

**Technical**:
We created a stopTime observable to stop getRemainingTime from running every second indefinitely to preserve efficiency. We used .next() to emit a new value to the observable in the reservation service's cancel() and checkout() methods. Using console logs, we determined that this did stop it. However, when you reload the page, it started calling getRemainingTime again. To fix this, we chose to imbed the call in an if statement to check the reservation's state.

We created a timeRemaining attribute to persist in backend instead of just calculating it in frontend. We originally had it only in frontend and was able to get our timer to function correctly, but moving it to backend allows it to persist after reloading the page.

Furthermore, despite having originally planned to create an additional boolean attribute titled is_eligible_for_extension which would handle the switch case of extension eligibility relative to timing, we were able to observe and account for that shift in the frontend utilizing existing functionality.

A focus of ours throughout the development process has been to prioritize long-term adaptability over short-term simplicity. An example of this is the functionality of the backend reservation service methods created to handle edge cases of reservation availability, or lack thereof, including check_extension_eligibility, check_extension_close, check_extension_overlap. In such methods, we opted for integer return values in our functions, rather than booleans, to allow for future scalability and detailed time management. While a boolean would suffice for current needs, representing simple yes-or-no scenarios, integers provide the flexibility to handle more complex, time-specific decisions in the future, such as managing 15-minute intervals. Additionally, we followed best practice by choosing a modular structure, constructing check_extension_eligibility to integrate the outputs of its two helper functions. This choice will be imperative in ensuring our system's adaptability and ease of maintenance, significantly aiding future development and debugging protocols.

**User Experience**:
When deciding how to differentiate between when a user can and cannot extend, we couldn't decide if we should have no button then have a button or have a disabled button then enabled button. Users can either not extend due to being outside of the 30 minute range or because there's a reservation after theirs. We decided that when a user was outside of the 30 minute range, there would be no button. Once they were within the 30 minute range, there would be a button, but it would be enabled/disabled depending on if there is a reservation after theirs. By implementing both differences, users are able to see that they can't extend and also determine why they are unable to extend.

## 4. Development Concerns

Most of the changes made to implement this feature have been made in the following files:

1. backend/services/coworking/reservation.py
2. frontend/src/app/coworking/reservation/reservation.service.ts
3. frontend/src/app/coworking/widgets/coworking-reservation-card/coworking-reservation-card.html

1 contains methods to draft, cancel, update reservations. It also has methods to retrieve the state of the CSXL at a given time. 2 contains API routes for the reservation component. 3 contains most of our frontend changes including new icons and buttons. Understanding how to manipulate reservation objects is crucial for understanding how to extend them.

![Checked In](images/checkedin.jpg)
Once a user has made a reservation and been checked in by an ambassador, they can see the time remaining on their reservation. Additionally, they see updated icons for the location, time, and user associated with their reservation.
![Able to Extend](images/canextend.jpg)
If they are within 30 minutes of the end of their reservation, and are elibigle to extend, they see an active blue Extend button.
![After Clicking Extend](images/emptydropdownfield.jpg)
Clicking on the Extend button causes a dropdown menu to appear for the amount of time they'd like to extend by.
![After Clicking In Dropdown](images/viewintervals.jpg)
![Unable to Extend](images/can'textend.jpg)
If I user cannot extend at least 15 minutes, they see a deactivated grey button as well as a message describing why they can't extend, either due to operating hours or an overlapping reservation with another user.
