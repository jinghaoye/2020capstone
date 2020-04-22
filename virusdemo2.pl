tree(if_then_else('Do you have fever ', 
                /* level 1*/
                  if_then_else('It s been a week and it s getting worse', 
                  /* level 2*/
                               if_then_else('In contact with a large crowd recently',
                               /* level 3*/
                                            if_then_else('have difficulty breathing',
                                            /* level 4*/
                                                            virus(test1),
                                                            virus("fail to detect")),
                                            
                                            virus("fail to detect")),

                               if_then_else(' The temperature rises to 39 degrees in one or two days',
                                            virus(flu),
                                            if_then_else('Any vomiting, diarrhea, and rash',
                                                        virus(ebola),
                                                          false))),

                  if_then_else('has nasal congestion, snot, sneeze',
                  /* level 2*/
                               if_then_else('has headache, joint pain, discomfort',
                                            virus("fail to detect the virus"),
                                            virus(cold)),
                               false))).
                               
is_true(Q) :-
        format("~w?\n", [Q]),
        read(yes).

virus(Virus) :-
        tree(T),
        tree_virus(T, Virus).

tree_virus(virus(Virus), Virus).

tree_virus(if_then_else(Cond,Then,Else), Virus) :-
        (   is_true(Cond) ->
            tree_virus(Then, Virus)
        ;   tree_virus(Else, Virus)
        ).