:- initialization(main).

println(X) :-
    write(X),
    write('\n').

sum_with_step(N, Step, R) :-
    N @=< 0 -> R is 0;
    (
        M is N - Step,
        sum_with_step(M, Step, Other),
        R is N + Other
    ).

pow(N, M, R) :-
    M == 0 -> R is 1;
    (
        (M > 0 -> P is M - 1; P is M + 1),
        pow(N, P, Other),
        (M > 0 -> R is N * Other; R is Other / N)
    ).

tree_pow(N, M, R) :-
    M == 0 -> R is 1;
    (
        Div is truncate(M / 2),
        Mod is M mod 2,
        (Mod == 1 -> P is N; P is 1),
        tree_pow(N, Div, Other),
        (M > 0 -> R is Other * Other * P; R is Other * Other / P)
    ).

sum_n(N, R) :-
    N == 0 -> R is 0;
    (
        M is N - 1,
        sum_n(M, Other),
        R is N + Other
    ).

pi2_by_6(N, R) :-
    N == 1 -> R is 1;
    (
        M is N - 1,
        pi2_by_6(M, Other),
        R is 1 / N / N + Other
    ).

main :-
    Var_step is 6,
    Var_n is 215,
    Var_a is 0.2511,
    Var_m is -6,
    Var_N is 43,
    Var_k is 1,
    
    sum_with_step(Var_n, Var_step, Task_1_Result),
    pow(Var_a, Var_m, Task_2_method_1_result),
    tree_pow(Var_a, Var_m, Task_2_method_2_result),
    sum_n(Var_N, Task_3_Result),
    pi2_by_6(Var_k, Task_4_Result),
    
    println(Task_1_Result),
    println(Task_2_method_1_result),
    println(Task_2_method_2_result),
    println(Task_3_Result),
    println(Task_4_Result).
