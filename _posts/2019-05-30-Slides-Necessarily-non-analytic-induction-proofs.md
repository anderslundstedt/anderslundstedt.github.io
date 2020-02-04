---
layout: post
tags: research academia
title: "Slides: Necessarily non-analytic induction proofs"
---
I recently gave two talks on the research project "Necessarily non-analytic
induction proofs".
The first talk was in Gothenburg at the
[FLoV logic seminar](https://flov.gu.se/english/research/seminars/logic).
The second talk was in New York at
[JAF 38](https://jaf2019nyc.com).
I have uploaded slides for each talk to the research page.

At both talks I received useful feedback. Some feedback pointed out some
problems with our definitions. Instead of modifying the slides I will address
those problems here.

**UPDATE 2019-08-29:** *In the latest summary that I have uploaded to the
research page, the following problem has been addressed.*  
At the FLoV talk,
[Mattias Granberg Olsson](https://flov.gu.se/english/about/linguistics--logic-and-theory-of-science-unit/linguistics--logic-and-theory-of-science-unit?languageId=100001&userId=xgranb)
pointed out a problem with our definition of first-order languages of arithmetic
and their corresponding standard models. The problem is that a language of
arithmetic (as we defined it) can have at most one function symbol (or predicate
symbol) for each function (or relation) in the standard model. This makes it
very inconvenient (though not impossible) to model proofs showing that two
distinct definitions define the same function (or relation). To address this at
the JAF 38 talk I simplified our definition of a first-order language of
arithmetic and removed the definition of what constitutes the standard model for
a first-order language of arithmetic. Since it would still be nice to be able to
define the standard model for any language of arithmetic, we will probably have
to come up with some other solution.

**UPDATE 2020-02-02:** *I have uploaded to the research page a note reflecting
on terminology. This note includes a discussion of the following problem.*  
At the FLoV talk, [Graham Leigh](https://flov.gu.se/english/about/linguistics--logic-and-theory-of-science-unit/linguistics--logic-and-theory-of-science-unit?languageId=100001&userId=xleigr)
pointed out that the terminology "necessarily non-analytic" might be a bit
unfortunate. The reason is that we can construct cases where we have "ψ(x)
witnesses that T proves ∀x.φ(x) by necessarily non-analytic induction" and where
ψ(x) is a subformula of φ(x). Since analytic proofs are usually taken to be
those satisfying a subformula property (in some sense), it might be a bit
misleading to use the terminology "non-analytic" when the proof does satisfy a
subformula property. We will have to think more about what terminology to use.

I also want to mention a piece of feedback that did not concern any problem. At
JAF 38, [Matt Kaufmann](https://www.cs.utexas.edu/~kaufmann/) gave me an example
of a non-analytic induction proof. For reasons of efficiency one might want to
define the factorial on the natural numbers such that the definition is
"tail-recursive". Showing that this definition is equivalent to the standard one
seems to require a non-analytic induction proof. This seems indeed to be the
case. I have not verified all the details yet but when I have I will add this
example to our summary document (on the research page).
