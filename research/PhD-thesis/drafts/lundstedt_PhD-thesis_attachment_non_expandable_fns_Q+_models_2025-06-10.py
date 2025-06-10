#! /usr/bin/env python3.13

# IMPORTS

import dataclasses

from itertools import product
from typing import Final as F, NewType, Self, TypeAlias



# NEWTYPES T_CORRECT_EQS AND T_INCORRECT_EQS

t_correct_eqs     = NewType('t_correct_eqs',     list[str])
t_incorrect_eqs   = NewType('t_incorrect_eqs',   list[str])



# DATA CLASS C_ELEMENT

@dataclasses.dataclass(frozen=True,kw_only=True)
class c_element:
    ci : F[int] # cycle index
    ri : F[int] # right index
    def __post_init__(self) -> None:
        assert self.ci >= 1, self.ci
        assert self.ri >= 1, self.ri
    def __repr__(self) -> str:
        return f'a[{self.ci},{self.ri}]'



# DATA CLASS C_CYCLE

@dataclasses.dataclass(frozen=True,kw_only=True)
class c_cycle:
    ci       : F[int]
    length   : F[int]
    elements : F[tuple[c_element,...]] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        assert self.ci     >= 1, self.ci
        assert self.length >= 1, self.length
        elements : F[tuple[c_element,...]] = \
            tuple(c_element(ci=self.ci,ri=ri) for ri in range(1,self.length+1))
        object.__setattr__(self,'elements',elements)

    def element(self, ri: int) -> c_element:
        assert ri <= self.length, (ri,self.length)
        return self.elements[ri-1]

    def S(self, a: c_element) -> c_element:
        assert a.ci == self.ci, (a,self.ci)
        assert a.ri <= self.length
        if a.ri == self.length:
            return self.elements[0]
        else:
            return self.elements[a.ri]

    def P(self, a: c_element) -> c_element:
        assert a.ci == self.ci, (a,self.ci)
        assert a.ri <= self.length
        if a.ri == 1:
            return self.elements[-1]
        else:
            return self.elements[a.ri-2]

    def it_S(self, a: c_element, iterations: int) -> c_element:
        if iterations < 0:
            return self.it_P(a,-iterations)
        assert a.ci == self.ci, (a,self.ci)
        assert a.ri <= self.length
        return self.elements[(a.ri-1+iterations) % self.length]

    def it_P(self, a: c_element, iterations: int) -> c_element:
        if iterations < 0:
            return self.it_S(a,-iterations)
        assert a.ci == self.ci, (a, self.ci)
        assert a.ri <= self.length
        return self.elements[(a.ri-1-iterations) % self.length]

    def __repr__(self) -> str:
        return \
            f'A[{self.ci}]' +                                   \
            ' = '           +                                   \
            '{' + ', '.join(str(a) for a in self.elements) + '}'



# DATA CLASS CYCLE STRUCTURE

@dataclasses.dataclass(frozen=True,kw_only=True,eq=False)
class c_cycle_structure:
    cycle_lengths : F[tuple[int,...]]
    cycles        : F[tuple[c_cycle,...]]
    elements      : F[tuple[c_element,...]]
    no_of_cycles  : F[int]
    size          : F[int]

    def __init__(self, *, cycle_lengths: tuple[int,...]) -> None:
        no_of_cycles : F[int]                  = len(cycle_lengths)
        cycles       : F[tuple[c_cycle,...]]   = tuple(
            c_cycle(ci=ci,length=𝓁) for (ci,𝓁) in enumerate(cycle_lengths,1)
        )
        elements     : F[tuple[c_element,...]] = tuple(
            a for c in cycles for a in c.elements
        )
        assert no_of_cycles >= 1
        assert all(𝓁 >= 1 for 𝓁 in cycle_lengths), cycle_lengths
        assert \
            all(𝓁1 >= 𝓁2 for 𝓁1,𝓁2 in zip(cycle_lengths,cycle_lengths[1:])),\
            cycle_lengths
        object.__setattr__(self,'cycle_lengths',cycle_lengths)
        object.__setattr__(self,'cycles',       cycles)
        object.__setattr__(self,'elements',     elements)
        object.__setattr__(self,'no_of_cycles', no_of_cycles)
        object.__setattr__(self,'size',         len(self.elements))

    def cycle(self, ci: int) -> c_cycle:
        assert 1 <= ci <= self.no_of_cycles, (ci,self.no_of_cycles)
        return self.cycles[ci-1]

    def element(self, *, ci: int, ri: int) -> c_element:
        assert 1 <= ci <= self.no_of_cycles, (ci,self.no_of_cycles)
        assert \
            1 <= ri <= self.cycles[ci-1].length,\
            (ci, ri, self.cycles[ci-1].length)
        return self.cycles[ci-1].elements[ri-1]

    def S(self, a: c_element) -> c_element:
        assert a.ci <= self.no_of_cycles, (a,self.no_of_cycles)
        return self.cycles[a.ci-1].S(a)

    def P(self, a: c_element) -> c_element:
        assert a.ci <= self.no_of_cycles, (a,self.no_of_cycles)
        return self.cycles[a.ci-1].P(a)

    def it_S(self, a: c_element, iterations: int) -> c_element:
        assert a.ci <= self.no_of_cycles, (a,self.no_of_cycles)
        return self.cycles[a.ci-1].it_S(a,iterations)

    def it_P(self, a: c_element, iterations: int) -> c_element:
        assert a.ci <= self.no_of_cycles, (a,self.no_of_cycles)
        return self.cycles[a.ci-1].it_P(a,iterations)

    def __repr__(self) -> str:
        return \
            'A = '                                                     +\
            '+'.join(f'A[{ci}]' for ci in (c.ci for c in self.cycles)) +\
            '\n'                                                       +\
            '\n'.join(str(cycle) for cycle in self.cycles)             +\
            '\n'                                                       +\
            '\n'.join(
                '\n'.join(f'S{a} = {self.S(a)}' for a in cycle.elements)
                for cycle in self.cycles
            )



# TYPE ALIAS T_PLUS

ta_plus  : TypeAlias = dict[tuple[c_element,c_element],c_element]



# C_PLUS_REDUCT

@dataclasses.dataclass(frozen=True, kw_only=True)
class c_plus_reduct(c_cycle_structure):

    _plus : F[ta_plus]

    def __init__(self, *, cycle_lengths: tuple[int,...], plus: ta_plus) -> None:
        super().__init__(cycle_lengths=cycle_lengths)
        assert \
            set(plus.keys()) == set(product(self.elements, repeat=2)),\
            (set(plus.keys()), set(product(self.elements, repeat=2)))
        object.__setattr__(self, '_plus', plus)

    @classmethod
    def from_cycle_structure(
        cls,
        cycle_structure : c_cycle_structure,
        plus            : ta_plus,
    ) -> Self:
        return cls(cycle_lengths=cycle_structure.cycle_lengths, plus=plus)

    def plus(self, a: c_element, b: c_element) -> c_element:
        assert a.ci <= self.no_of_cycles,       (a.ci, self.no_of_cycles)
        assert b.ci <= self.no_of_cycles,       (b.ci, self.no_of_cycles)
        assert a.ri <= self.cycle(a.ci).length, (a.ri, self.cycle(a.ci).length)
        assert b.ri <= self.cycle(b.ci).length, (b.ri, self.cycle(b.ci).length)
        return self._plus[(a,b)]

    def it_right_plus(
        self, *, add_to: c_element, add_with: c_element, iterations: int,
    ) -> c_element:
        assert iterations >= 0, iterations
        if iterations == 0:
            return add_to
        return self.it_right_plus(
            add_to     = self.plus(add_to,add_with),
            add_with   = add_with,
            iterations = iterations-1,
        )

    def __repr__(self) -> str:
        return \
            super().__repr__() +                                     \
            '\n' +                                                   \
            '\n'.join(
                '\n'.join(
                    f'{a}+{b} = {self.plus(a,b)}'
                    for b,a in product(cycle.elements, self.elements)
                )
                for cycle in self.cycles
            )



# FUNCTION MODELS_Q5

def models_Q5(pr : c_plus_reduct) -> tuple[t_correct_eqs,t_incorrect_eqs]:
    correct_eqs   : t_correct_eqs   = t_correct_eqs([])
    incorrect_eqs : t_incorrect_eqs = t_incorrect_eqs([])
    for α in pr.elements:
        for β in pr.elements:
            α_Sβ : F[c_element] = pr.plus(α, pr.S(β))
            S_αβ : F[c_element] = pr.S(pr.plus(α,β))
            eq   : str          = f'{α}+S({β}) = {α}+{pr.S(β)} = {α_Sβ}'
            if α_Sβ == S_αβ:
                eq += ' = '
            else:
                eq += f' ≠ {S_αβ} = '
            eq += f'S({pr.plus(α,β)}) = S({α}+{β})'
            if α_Sβ == S_αβ:
                correct_eqs.append(eq)
            else:
                incorrect_eqs.append(eq)
    return (correct_eqs,incorrect_eqs)



# FUNCTION IS_COMMUTATIVE

def is_commutative(pr: c_plus_reduct) -> tuple[t_correct_eqs,t_incorrect_eqs]:
    correct_eqs   : t_correct_eqs   = t_correct_eqs([])
    incorrect_eqs : t_incorrect_eqs = t_incorrect_eqs([])
    for α in pr.elements:
        for β in pr.elements:
            αβ : F[c_element] = pr.plus(α,β)
            βα : F[c_element] = pr.plus(β,α)
            eq : str = f'{α}+{β} = {αβ}'
            if αβ == βα:
                eq += ' = '
            else:
                eq += f' ≠ {βα} = '
            eq += f'{β}+{α}'
            if αβ == βα:
                correct_eqs.append(eq)
            else:
                incorrect_eqs.append(eq)
    return (correct_eqs,incorrect_eqs)



# FUNCTION IS_ASSOCIATIVE

def is_associative(pr: c_plus_reduct) -> tuple[t_correct_eqs, t_incorrect_eqs]:
    correct_eqs   : t_correct_eqs   = t_correct_eqs([])
    incorrect_eqs : t_incorrect_eqs = t_incorrect_eqs([])
    for α in pr.elements:
        for β in pr.elements:
            for γ in pr.elements:
                αβ   : F[c_element] = pr.plus(α,β)
                αβ_γ : F[c_element] = pr.plus(αβ,γ)
                βγ   : F[c_element] = pr.plus(β,γ)
                α_βγ : F[c_element] = pr.plus(α,βγ)
                eq : str = f'({α}+{β})+{γ} = {αβ}+{γ} = {αβ_γ}'
                if αβ_γ == α_βγ:
                    eq += ' = '
                else:
                    eq += f' ≠ {α_βγ} = '
                eq += f'{α}+{βγ} = {α}+({β}+{γ})'
                if αβ_γ == α_βγ:
                    correct_eqs.append(eq)
                else:
                    incorrect_eqs.append(eq)
    return (correct_eqs,incorrect_eqs)



# FUNCTION IS_EXPANDABLE

def is_expandable(pr: c_plus_reduct) -> tuple[t_correct_eqs,t_incorrect_eqs]:
    correct_eqs   : t_correct_eqs   = t_correct_eqs([])
    incorrect_eqs : t_incorrect_eqs = t_incorrect_eqs([])
    for a in pr.elements:
        for ci in range(1,pr.no_of_cycles+1):
            for b in pr.elements:
                a_plus_b_cycle_length_times : F[c_element] = pr.it_right_plus(
                    add_to=a,add_with=b,iterations=pr.cycle(ci).length
                )
                alternative_found : F[bool] = b == a_plus_b_cycle_length_times
                eq : str = \
                    f'{a}×{pr.element(ci=ci,ri=1)} ≔ {b}'   \
                    +                                       \
                    (' = ' if alternative_found else ' ≠ ') \
                    +                                       \
                    '('*pr.cycle(ci).length                 \
                    +                                       \
                    f'{a}+'
                for _ in range(pr.cycle(ci).length-1):
                    eq += f'{b})+'
                eq += f'{b})'
                if alternative_found:
                    correct_eqs.append(eq)
                else:
                    incorrect_eqs.append(eq)
    return (correct_eqs,incorrect_eqs)



# MAIN

## OUR PLUS REDUCTS

### ELEMENTS USED

a11 : F[c_element] = c_element(ci=1,ri=1)
a12 : F[c_element] = c_element(ci=1,ri=2)
a21 : F[c_element] = c_element(ci=2,ri=1)
a31 : F[c_element] = c_element(ci=3,ri=1)

### PR_NOT_COMMUTATIVE_EXPANDABLE

# this one just to test that function is_expandable works as expected
pr_not_commutative_expandable : F[c_plus_reduct] = c_plus_reduct(
    cycle_lengths = (2,),
    plus          = {
        (a11,a11): a11,
        (a12,a11): a11,
        (a11,a12): a12,
        (a12,a12): a12,
    }
)

### PR_COMMUTATIVE_ASSOCIATIVE

pr_commutative_associative : F[c_plus_reduct] = c_plus_reduct(
    cycle_lengths = (1,1),
    plus          = {
        (a11,a11): a11,
        (a21,a11): a21,
        (a11,a21): a21,
        (a21,a21): a11,
    }
)

### PR_COMMUTATIVE_NOT_ASSOCIATIVE

pr_commutative_not_associative : F[c_plus_reduct] = c_plus_reduct(
    cycle_lengths = (1,1),
    plus          = {
        (a11,a11): a21,
        (a21,a11): a11,
        (a11,a21): a11,
        (a21,a21): a11,
    }
)

### PR_NOT_COMMUTATIVE_ASSOCIATIVE

pr_not_commutative_associative : F[c_plus_reduct] = c_plus_reduct(
    cycle_lengths = (2,1,1),
    plus          = {
        (a11,a11): a11,
        (a12,a11): a11,
        (a21,a11): a21,
        (a31,a11): a31,
        (a11,a12): a12,
        (a12,a12): a12,
        (a21,a12): a21,
        (a31,a12): a31,
        (a11,a21): a21,
        (a12,a21): a21,
        (a21,a21): a21,
        (a31,a21): a31,
        (a11,a31): a31,
        (a12,a31): a31,
        (a21,a31): a31,
        (a31,a31): a21,
    }
)

### PR_NOT_COMMUTATIVE_NOT_ASSOCIATIVE

pr_not_commutative_not_associative : F[c_plus_reduct] = c_plus_reduct(
    cycle_lengths = (2,),
    plus          = {
        (a11,a11): a12,
        (a12,a11): a12,
        (a11,a12): a11,
        (a12,a12): a11,
    }
)




## FUNCTION CHECK_PR

def check_pr(pr: c_plus_reduct) -> None:
    print(pr)
    print()
    print('Models (Q5)?',end=' ')
    models_Q5_res           : F[tuple[t_correct_eqs,t_incorrect_eqs]] = \
        models_Q5(pr)
    models_Q5_correct_eqs   : F[t_correct_eqs]                        = \
       models_Q5_res[0]
    models_Q5_incorrect_eqs : F[t_incorrect_eqs]                      = \
       models_Q5_res[1]
    if models_Q5_incorrect_eqs != []:
        print('No, a counterexample:')
        print(models_Q5_incorrect_eqs[0])
    else:
        print('Yes:')
        for correct_eq in models_Q5_correct_eqs:
            print(correct_eq)
    print()
    print('Is expandable?',end=' ')
    is_expandable_res           : F[tuple[t_correct_eqs,t_incorrect_eqs]] = \
        is_expandable(pr)
    is_expandable_correct_eqs   : F[t_correct_eqs]                        = \
       is_expandable_res[0]
    is_expandable_incorrect_eqs : F[t_incorrect_eqs]                      = \
       is_expandable_res[1]
    if is_expandable_incorrect_eqs != []:
        print('No:')
        for incorrect_eq in is_expandable_incorrect_eqs:
            print(incorrect_eq)
    else:
        print('Yes, alternatives:')
        for correct_eq in is_expandable_correct_eqs:
            print(correct_eq)
    print()
    print('Is commutative?',end=' ')
    is_commutative_res           : F[tuple[t_correct_eqs,t_incorrect_eqs]] = \
        is_commutative(pr)
    is_commutative_correct_eqs   : F[t_correct_eqs]                        = \
       is_commutative_res[0]
    is_commutative_incorrect_eqs : F[t_incorrect_eqs]                      = \
       is_commutative_res[1]
    if is_commutative_incorrect_eqs != []:
        print('No, a counterexample:')
        print(is_commutative_incorrect_eqs[0])
    else:
        print('Yes:')
        for correct_eq in is_commutative_correct_eqs:
            print(correct_eq)
    print()
    print('Is associative?',end=' ')
    is_associative_res           : F[tuple[t_correct_eqs,t_incorrect_eqs]] = \
        is_associative(pr)
    is_associative_correct_eqs   : F[t_correct_eqs]                        = \
       is_associative_res[0]
    is_associative_incorrect_eqs : F[t_incorrect_eqs]                      = \
       is_associative_res[1]
    if is_associative_incorrect_eqs != []:
        print('No, a counterexample:')
        print(is_associative_incorrect_eqs[0])
    else:
        print('Yes:')
        for correct_eq in is_associative_correct_eqs:
            print(correct_eq)


## IF __NAME__ == '__MAIN__':

if __name__ == '__main__':
    print('A non-commutative expandable non-standard part:')
    print()
    check_pr(pr_not_commutative_expandable)
    print()
    print('---')
    print()
    print('A commutative associative non-expandable non-standard part:')
    print()
    check_pr(pr_commutative_associative)
    print()
    print('---')
    print()
    print('A commutative non-associative non-expandable non-standard part:')
    print()
    check_pr(pr_commutative_not_associative)
    print()
    print('---')
    print()
    print('A non-commutative associative non-expandable non-standard part:')
    check_pr(pr_not_commutative_associative)
    print()
    print('---')
    print()
    print('A non-commutative non-associative non-expandable non-standard part:')
    print()
    check_pr(pr_not_commutative_not_associative)
