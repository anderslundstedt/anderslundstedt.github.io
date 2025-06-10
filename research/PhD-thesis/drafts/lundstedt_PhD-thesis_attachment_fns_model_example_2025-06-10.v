Require Import Arith.

Definition models_Q_p
  (M : Type) (O_M : M) (S_M : M -> M)
  :
  Prop
  :=
    (forall x, S_M x <> O_M)                    (* (Q1) *)
    /\
    (forall x y, S_M x = S_M y -> x = y)        (* (Q2) *)
    /\
    (forall x, x = O_M \/ exists y, x = S_M y). (* (Q3) *)

Definition models_Q_add
  (M : Type) (O_M : M) (S_M : M -> M) (add_M : M -> M -> M)
  :
  Prop
  :=
    models_Q_p M O_M S_M
    /\
    (forall x, add_M x O_M = x)                      (* (Q4) *)
    /\
    (forall x y, add_M x (S_M y) = S_M (add_M x y)). (* (Q5) *)

Definition models_Q
  (M      : Type)
  (O_M    : M)
  (S_M    : M -> M)
  (add_M  : M -> M -> M)
  (mult_M : M -> M -> M)
  :
  Prop
  :=
    models_Q_add M O_M S_M add_M
    /\
    (forall x, mult_M x O_M = O_M)                         (* (Q6) *)
    /\
    (forall x y, mult_M x (S_M y) = add_M (mult_M x y) x). (* (Q7) *)

Fact nat_models_Q : models_Q nat 0 S plus mult.
Proof.
  unfold models_Q. repeat split; auto.
  induction x as [| x IH].
  - left. reflexivity.
  - destruct IH as [IH1 | IH2]; right; eauto.
Qed.

Inductive A : Type :=
| a11 : A
| a12 : A
| a21 : A
| a22 : A.

Definition S_A (a : A) := match a with
| a11 => a12
| a12 => a11
| a21 => a22
| a22 => a21
end.

Definition fns_N : Type := nat + A.

Definition O_N : fns_N := inl 0.

Definition S_N (a : fns_N) : fns_N := match a with
| inl n => inl (S n)
| inr a => inr (S_A a)
end.

Fact fns_N_with_S_N_models_Q_p : models_Q_p fns_N O_N S_N.
Proof.
  unfold models_Q_p. repeat split.
  - intro α. destruct α as [n | a].
    + simpl. unfold O_N. injection. intros H2. inversion H2.
    + unfold O_N. destruct a; simpl; intro H; inversion H.
  - intros α β H. destruct α, β.
    + simpl in H. injection H. auto.
    + repeat unfold S_N in H. destruct a; simpl; inversion H.
    + repeat unfold S_N in H. destruct a; simpl; inversion H.
    + destruct a, a0; auto.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
      * simpl in H. inversion H.
  - intros α. destruct α as [n | a].
    + destruct n as [|n].
      * left. auto.
      * right. exists (inl n). reflexivity.
    + right. destruct a.
      * exists (inr a12); reflexivity.
      * exists (inr a11); reflexivity.
      * exists (inr a22); reflexivity.
      * exists (inr a21); reflexivity.
Qed.

Definition add_N_ns_std (a : A) (n : nat) :=
match a with
| a11 => if Nat.even n then a11 else a12
| a12 => if Nat.even n then a12 else a11
| a21 => if Nat.even n then a21 else a22
| a22 => if Nat.even n then a22 else a21
end.

Definition add_N_std_ns (n : nat) (a : A) : A := add_N_ns_std a n.

Definition add_N_ns_ns (a b : A) :=
match a, b with
| a11, a11 => a11
| a11, a12 => a12
| a11, a21 => a22
| a11, a22 => a21
| a12, a11 => a12
| a12, a12 => a11
| a12, a21 => a22
| a12, a22 => a21
| a21, a11 => a21
| a21, a12 => a22
| a21, a21 => a21
| a21, a22 => a22
| a22, a11 => a22
| a22, a12 => a21
| a22, a21 => a21
| a22, a22 => a22
end.

Definition add_N (α β : fns_N) : fns_N :=
match α, β with
| inl n, inl m => inl (n+m)
| inl n, inr a => inr (add_N_std_ns n a)
| inr a, inl n => inr (add_N_ns_std a n)
| inr a, inr b => inr (add_N_ns_ns a b)
end.

Lemma fns_N_with_S_N_add_N_models_Q4 : forall (α : fns_N), add_N α (inl 0) = α.
Proof.
  destruct α as [n | a].
  + simpl. rewrite <- plus_n_O. reflexivity.
  + simpl. destruct a; reflexivity.
Qed.

Lemma fns_N_with_S_N_add_N_models_Q5_ns_std
  : forall (a : A) (n : nat), add_N_ns_std a (S n) = S_A (add_N_ns_std a n).
Proof.
  intros a n.
  unfold add_N_ns_std.
  remember (Nat.even    n ) as   n_even eqn:eq_n_even.
  remember (Nat.even (S n)) as S_n_even eqn:eq_S_n_even.
  destruct n_even; destruct S_n_even.
  - absurd (true = Nat.even (S n)).
    + symmetry in eq_n_even, eq_S_n_even.
      rewrite Nat.even_spec in eq_n_even, eq_S_n_even.
      rewrite Nat.Even_succ in eq_S_n_even.
      apply (Nat.Even_Odd_False n eq_n_even) in eq_S_n_even.
      auto.
    + auto.
  - destruct a; reflexivity.
  - destruct a; reflexivity.
  - absurd (false = Nat.even (S n)).
    + symmetry in eq_n_even, eq_S_n_even.
      rewrite <- eq_S_n_even in eq_n_even.
      rewrite Nat.even_succ in eq_n_even, eq_S_n_even.
      rewrite <- Nat.negb_odd in eq_n_even.
      rewrite eq_S_n_even in eq_n_even.
      simpl in eq_n_even.
      inversion eq_n_even.
    + auto.
Qed.

Fact fns_N_with_S_N_add_N_models_Q_add : models_Q_add fns_N O_N S_N add_N.
Proof.
  unfold models_Q_add.
  split; [apply fns_N_with_S_N_models_Q_p | ].
  split.
  - simpl. unfold O_N. apply fns_N_with_S_N_add_N_models_Q4.
  - intros α β.
    + destruct α as [n | a]; [destruct β as [m | a] | destruct β as [n | b]].
      * simpl. rewrite <- plus_n_Sm. reflexivity.
      * simpl. destruct a; simpl; destruct (Nat.even n); reflexivity.
      * simpl. rewrite <- fns_N_with_S_N_add_N_models_Q5_ns_std. reflexivity.
      * simpl. unfold add_N_ns_ns. destruct a; destruct b; reflexivity.
Qed.

Fixpoint it_add_right_N (β α : fns_N) (n : nat) : fns_N :=
match n with
| 0   => α
| S n => add_N (it_add_right_N β α n) β
end.

Definition mult_N_ns_std (a : A) (n : nat) : fns_N :=
  it_add_right_N (inr a) (inl 0) n.

Lemma fns_N_with_S_N_add_N_mult_N_models_ns
  : forall (a : A), mult_N_ns_std a 0 = inl 0.
Proof. intro a. unfold mult_N_ns_std. reflexivity. Qed.

Lemma mult_N_a11_fixpoint : forall (n : nat), mult_N_ns_std a11 (S n) = inr a11.
Proof.
  intro n. induction n as [|n IHn].
  - reflexivity.
  - change
      (mult_N_ns_std a11 (S (S n)))
    with
      (add_N (mult_N_ns_std a11 (S n)) (inr a11)).
    rewrite IHn.
    reflexivity.
Qed.

Lemma mult_N_a21_fixpoint : forall (n : nat), mult_N_ns_std a21 (S n) = inr a21.
Proof.
  intro n. induction n as [|n IHn].
  - reflexivity.
  - change
      (mult_N_ns_std a21 (S (S n)))
    with
      (add_N (mult_N_ns_std a21 (S n)) (inr a21)).
    rewrite IHn.
    reflexivity.
Qed.

Lemma mult_N_a22_fixpoint : forall (n : nat), mult_N_ns_std a22 (S n) = inr a22.
Proof.
  intro n. induction n as [|n IHn].
  - reflexivity.
  - change
      (mult_N_ns_std a22 (S (S n)))
    with
      (add_N (mult_N_ns_std a22 (S n)) (inr a22)).
    rewrite IHn.
    reflexivity.
Qed.

Lemma mult_N_a12_even_odd
  : forall n : nat,
    (Nat.Even (S n) -> mult_N_ns_std a12 (S n) = inr a11)
    /\
    (Nat.Odd  (S n) -> mult_N_ns_std a12 (S n) = inr a12).
Proof.
  intro n. induction n as [|n IHn].
  - split.
    + intros H_even_1.
      exfalso.
      rewrite <- Nat.even_spec in H_even_1.
      rewrite Nat.even_1 in H_even_1.
      inversion H_even_1.
    + reflexivity.
  - split.
    + intros H_even_SSn.
      destruct IHn as [_ IHn].
      rewrite Nat.Even_succ in H_even_SSn.
      specialize (IHn H_even_SSn).
      change
        (mult_N_ns_std a12 (S (S n)))
      with
        (add_N (mult_N_ns_std a12 (S n)) (inr a12)).
      rewrite IHn.
      simpl.
      reflexivity.
    + intros H_odd_SSn.
      destruct IHn as [IHn _].
      rewrite Nat.Odd_succ in H_odd_SSn.
      specialize (IHn H_odd_SSn).
      change
        (mult_N_ns_std a12 (S (S n)))
      with
        (add_N (mult_N_ns_std a12 (S n)) (inr a12)).
      rewrite IHn.
      simpl.
      reflexivity.
Qed.

Lemma mult_N_a12_even
  : forall n : nat,
      n <> 0 -> Nat.Even n -> mult_N_ns_std a12 n = inr a11.
Proof.
  intro n. destruct n as [|n].
  - intro H_0_neq_0. exfalso. apply H_0_neq_0. reflexivity.
  - intros _ H_even_Sn.
    pose (mult_N_a12_even_odd n) as H. destruct H as [H _].
    apply (H H_even_Sn).
Qed.

Lemma mult_N_a12_odd
  : forall n : nat, Nat.Odd n -> mult_N_ns_std a12 n = inr a12.
Proof.
  intro n. destruct n as [|n].
  - intro H_odd_0.
    rewrite <- Nat.odd_spec in H_odd_0.
    rewrite Nat.odd_0 in H_odd_0.
    inversion H_odd_0.
  - intros H_odd_Sn.
    pose (mult_N_a12_even_odd n) as H. destruct H as [_ H].
    apply (H H_odd_Sn).
Qed.

Lemma Sn_neq_0 : forall n : nat, S n <> 0.
  intros n. symmetry. apply Nat.neq_0_succ.
Qed.

Lemma fns_N_with_S_N_add_N_mult_N_models_Q7_ns_std
  : forall (a : A) (n : nat),
      mult_N_ns_std a (S n) = add_N (mult_N_ns_std a n) (inr a).
Proof.
  intro a. destruct a.
  - destruct n as [|n].
    + reflexivity.
    + repeat rewrite mult_N_a11_fixpoint. reflexivity.
  - intro n.
    destruct (Nat.Even_or_Odd (S n)) as [H_even_Sn | H_odd_Sn].
    + rewrite (mult_N_a12_even (S n) (Sn_neq_0 n) H_even_Sn).
      rewrite Nat.Even_succ in H_even_Sn.
      rewrite (mult_N_a12_odd n H_even_Sn).
      simpl.
      reflexivity.
    + rewrite (mult_N_a12_odd (S n) H_odd_Sn).
      destruct n as [|n].
      * simpl. reflexivity.
      * rewrite Nat.Odd_succ in H_odd_Sn.
        rewrite (mult_N_a12_even (S n) (Sn_neq_0 n) H_odd_Sn).
        simpl.
        reflexivity.
  - destruct n as [|n].
    + reflexivity.
    + repeat rewrite mult_N_a21_fixpoint. reflexivity.
  - destruct n as [|n].
    + reflexivity.
    + repeat rewrite mult_N_a22_fixpoint. reflexivity.
Qed.

Definition mult_N_std_ns (n : nat) (a : A) : A :=
match a with
| a11 => a11
| a21 => a21
| a12 => if Nat.even n then a11 else a12
| a22 => if Nat.even n then a21 else a22
end.

Definition mult_N_ns_ns (a b : A) : A :=
match a, b with
| a11, a11 => a11
| a12, a11 => a11
| a21, a11 => a21
| a22, a11 => a22
| a11, a12 => a11
| a12, a12 => a12
| a21, a12 => a21
| a22, a12 => a22
| a11, a21 => a11
| a12, a21 => a11
| a21, a21 => a21
| a22, a21 => a22
| a11, a22 => a11
| a12, a22 => a12
| a21, a22 => a21
| a22, a22 => a22
end.

Lemma fns_N_with_S_N_add_N_mult_N_models_Q7_ns_ns
  : forall (a b : A), mult_N_ns_ns a (S_A b) = add_N_ns_ns (mult_N_ns_ns a b) a.
Proof.
  intros a b; destruct a; destruct b; simpl; reflexivity.
Qed.

Definition mult_N (α β : fns_N) : fns_N :=
match α, β with
| inl n, inl m => inl (n*m)
| inl n, inr a => inr (mult_N_std_ns n a)
| inr a, inl n =>     (mult_N_ns_std a n)
| inr a, inr b => inr (mult_N_ns_ns a b)
end.

Fact fns_N_with_S_N_add_N_mult_N_models_Q
  : models_Q fns_N O_N S_N add_N mult_N.
Proof.
  unfold models_Q. split; [| split].
  - apply fns_N_with_S_N_add_N_models_Q_add.
  - intro α. destruct α as [n | a].
    + unfold mult_N. simpl. rewrite <- mult_n_O. reflexivity.
    + destruct a;
        unfold mult_N; simpl; unfold mult_N_ns_std; simpl; reflexivity.
  - intros α β.
    destruct α as [n | a]; [destruct β as [m | a] | destruct β as [n | b]].
    + unfold add_N, mult_N. simpl. rewrite <- mult_n_Sm. reflexivity.
    + destruct a.
      * reflexivity.
      * simpl. destruct (Nat.Even_or_Odd n) as [n_even | n_odd].
        {
          rewrite <- Nat.even_spec in n_even.
          rewrite n_even. simpl. rewrite n_even.
          reflexivity.
        }
        {
          rewrite <- Nat.odd_spec in n_odd.
          set (Nat.negb_odd n) as n_not_even.
          rewrite n_odd in n_not_even. simpl in n_not_even.
          rewrite <- n_not_even. simpl.
          rewrite <- n_not_even. reflexivity.
        }
      * reflexivity.
      * simpl. destruct (Nat.Even_or_Odd n) as [n_even | n_odd].
        {
          rewrite <- Nat.even_spec in n_even.
          rewrite n_even. simpl. rewrite n_even.
          reflexivity.
        }
        {
          rewrite <- Nat.odd_spec in n_odd.
          set (Nat.negb_odd n) as n_not_even.
          rewrite n_odd in n_not_even. simpl in n_not_even.
          rewrite <- n_not_even. simpl.
          rewrite <- n_not_even. reflexivity.
        }
    + apply fns_N_with_S_N_add_N_mult_N_models_Q7_ns_std.
    + simpl. rewrite fns_N_with_S_N_add_N_mult_N_models_Q7_ns_ns. reflexivity.
Qed.
