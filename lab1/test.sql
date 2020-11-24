DELETE from message where dep_id not
 in (select dep_id from department where actual is not null)