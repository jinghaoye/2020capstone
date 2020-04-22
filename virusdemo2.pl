tree(if_then_else('Do you have fever ', 
                /* level 1*/
                  if_then_else('It s been a week and it s getting worse', 
                  /* level 2*/
                               if_then_else('In contact with a large crowd recently',
                               /* level 3*/
                                            if_then_else('have difficulty breathing',
                                            /* level 4*/
                                                        if_then_else('Wether there is a persistent cough',
                                                        /* level 5*/
                                                                    if_then_else('anyone around you infected with covid-19',
                                                                    /* level 6*/
                                                                                virus(covid19),
                                                                                if_then_else('Do you feel very uncomfortable',
                                                                                            virus(covid19),
                                                                                            virus("fail to detect the virus"))),

                                                                    virus("fail to detect the virus")),

                                                        virus("fail to detect")),
                                            
                                            virus("fail to detect")),

                               if_then_else('The temperature rises to 39 degrees in short of period',
                               /* level 3*/
                                            if_then_else('Any vomiting, diarrhea, and rash',
                                            /* level 4*/
                                                        if_then_else('Sever headache, muscle and joint pain',
                                                        /* level 5*/
                                                                    if_then_else('accompanied by changes in consciousness, such as delirum, frowsiness, and bleeding',
                                                                    /* level 6*/
                                                                                virus(ebola),
                                                                                virus("fail to detect the virus")),

                                                                    virus("fail to detect the virus")),

                                                        if_then_else('feel muscle and joint pain, extreme fatigue and loss of appetite',
                                                        /* level 5*/
                                                                                if_then_else('got sore throat with persistent cough',
                                                                                /* level 6*/
                                                                                            virus(flu),
                                                                                            if_then_else('systemic symptom got imroved recently',
                                                                                            /* level 7*/
                                                                                                        virus(cold),
                                                                                                        virus("fail to detect the virus"))),

                                                                                virus("fail to detect the virus"))),

                                            if_then_else('Any vomiting, diarrhea, and rash',
                                            /* level 4*/
                                                        virus(ebola),
                                                          false))),

                  if_then_else('has nasal congestion, snot, sneeze',
                  /* level 2*/
                               if_then_else('has headache, joint pain, discomfort',
                                            virus(test1),
                                            virus("fail to detect the virus")),
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