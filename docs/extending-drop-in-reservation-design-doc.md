0. Extending a Drop-in Reservation : Isha Atre, Chloe Carroll, Lauren Jones, Soumya Mahavadi

1. Overview: This feature allows students who are currently in a drop-in reservation to extend for 1 additional hour if no other student has a reservation immediately after.

2. Key Personas: Describe the key personas your feature serves. What are their needs and goals with your feature?

   Sally Student - wants to know if her drop-in reservation can be extended and the ability to extend by 1 hour if so.

   Amy Ambassador - wants the ability to extend Sally Student's drop-in reservation if there's no reservation following it.

3. User Stories organized by persona, necessity for a minimum-viable feature, and frequency/importance of use.

   Story A.
   As Sally Student, if the following time slot is open, I want the ability to extend my drop-in seat reservation by 1 hour. If the following time slot is reserved, I to know that I cannot extend and see the time remaining on my reservation.

   Story B.
   As Sally Student, if the time slot following mine is originally reserved, but that reservation is cancelled, the option to extend should reappear.

   Story C.
   As Amy Ambassador, if the time slot following Sally Student's original time slot is available for booking, I want the ability to extend the reservation on behalf of Sally Student, upon their request.

   Story D.
   As Sally Student, if I do not want to spend 2 hours in the CSXL Lab, I should be able to input the time I want to spend in CSXL Lab.

4. Wireframes / Mockups: Include rough wireframes of your feature’s user interfaces for the most critical user stories, along with brief descriptions of what is going on. These can be hand-drawn, made in PowerPoint/KeyNote, or created with a tool like Figma. To see an example of a detailed wireframe Kris made this summer before building the drop-in feature, see this Figma board. You will notice the final implementation is not 1:1 with the original wireframe!

5. Technical Implementation Opportunities and Planning

What specific areas of the existing code base will you directly depend upon, extend, or integrate with?

    Currently, drop-in reservations are limited to 2-hour periods. When a drop-in reservation’s end time is within the next 30 minutes, another student is able to claim the next turn on the seat by creating a drop-in reservation that starts between 1 and 30 minutes into the future.

What planned page components and widgets, per the assigned reading, do you anticipate needing in your feature’s frontend?

    An icon (green?) if extending is permitted. If not, a progress spinner or clock to show time remaining on the reservation.

What additional models, or changes to existing models, do you foresee needing (if any)?
Considering your most-frequently used and critical user stories, what API / Routes do you foresee modifying or needing to add?

What concerns exist for security and privacy of data? Should the capabilities you are implementing be specific to only certain users or roles?

    When Sally Student makes a reservation, only Sally Student or Amy Ambassador should be able to cancel or extend the reservation. Other students should not be able to cancel or extend Sally's reservation. If Sally attempts to extend but cannot, she should not be able to see who has a reservation after her, just that there is a student who reserved the following time slot. Only Amy Ambassador should be able to see which students have current/scheduled reservations.
