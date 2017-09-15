////////////////Beliefs
//waypoint(sequence,latitude,longitude, altitute relative to ground)

!start.

////////////////Plans

//wait for a confirmation if all is set up
+!start : .my_name(N)
  <-  .send(bob,tell,iam(N)).

+!start
  <-  !start.
