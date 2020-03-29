tree(if_then_else('has fever',
                  if_then_else('It s been a week and it s getting worse',
                               virus(covid19),
                               if_then_else(' The temperature rises to 39 degrees in one or two days',
                                            virus(flu),
                                            if_then_else('Any vomiting, diarrhea, and rash',
                                                        virus(ebola),
                                                        false))),
                  if_then_else('has nasal congestion, snot, sneeze',
                               if_then_else('has headache, joint pain, discomfort',
                                            false,
                                            virus(cold)),
                               false))).
                               
is_true(Q) :-
        format("~w?\n", [Q]),
        read(yes).

virus(A) :-
        tree(T),
        tree_animal(T, A).

tree_animal(virus(A), A).

tree_animal(if_then_else(Cond,Then,Else), A) :-
        (   is_true(Cond) ->
            tree_animal(Then, A)
        ;   tree_animal(Else, A)
        ).