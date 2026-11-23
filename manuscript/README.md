# Three-leaf connected-forcing counterexamples

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National
University of Singapore; ChronoAI Pte Ltd, Singapore). 20 November 2026.
CC BY 4.0 (`cc-by-4.0`).

## Mathematical content

For integers `a,b >= 4`, let `A = S_(1,a,b)` and
`B = S_(2,2,a+b-3)` be three-armed trees, where arm lengths count edges.
Both have `n = a+b+2` vertices and three leaves. Their connected zero
forcing coefficient differences at sizes `4,6,n-2` are `-2,1,-1`.
Consequently neither ordering admits the cutoff in Mukherjee and Ray's
Problem 5.3, arXiv:2611.10985v1, Section 5, page 21.
Taking `a=4, b=n-6` gives a pair at every order `n >= 10`.

The enumeration is Brimkov's May 2017 Rice thesis, Proposition 7.11,
pages 168–169, subsequently expressed polynomially by Mukherjee and Ray
in Lemma 3.3. The path and cycle formulas are Brimkov's Propositions 7.7
and 7.8; the star follows by specialization. These formulas are credited
and reproved, not presented as new enumerations.

The note also proves the smallest literal ordered counterexample has
order four, gives the path–star reversed cutoff, the one-long-arm
formula and the starlike minimum-size count. For Problem 5.2 it classifies
all five-vertex unicyclic graphs with two leaves: their two polynomials
are `4x^3+4x^4+x^5` and `2x^2+5x^3+3x^4+x^5`. Thus that entire class has
neither a coefficientwise least nor a greatest element. General unicyclic
enumeration and Conjecture 5.1 remain outside these conclusions.

## Files and PDF build

- `note.tex`: the main source, with its bibliography included.
- `note.pdf`: the mathematical note, supplied separately from the source ZIP.
- `metadata.json`: the note identity, creators, license and formal source link.
- `verify.py`: a Python standard-library exact finite checker.
- `verification.json`: expected checker output.
- `SOURCE-SHA256SUMS`: source-archive member hashes.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, with the LaTeX packages listed in `note.tex`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

No separate BibTeX step is necessary. Engine versions and PDF metadata
can affect PDF bytes.

## Exact finite checks

Python 3.8 or later suffices:

```sh
python3 verify.py > verification.actual.json
cmp verification.json verification.actual.json
```

The checker enumerates all initial vertex subsets and tests induced
connectivity and ordinary forcing. It compares sequential and simultaneous
forcing closures. The selected graph families comprise paths and stars
at orders 2–10, cycles at orders 3–10, and the three-leaf pairs at
orders 10–14: 36 graphs and 69,616 subsets. It also checks all 21 labeled
trees at orders 1–4, accounting for 286 further subsets.

For the unicyclic classification it exhausts all 1,024 labeled simple
graphs on five vertices. Exactly 90 are connected with five edges and
two leaves. Explicit vertex permutations identify the two classes, of
sizes 30 and 60; their 2,880 initial subsets are all checked. No member
is coefficientwise least or greatest. In total, 72,782 initial subsets
are tested. Polynomial arithmetic additionally checks all 378 pairs
`4 <= a <= b <= 30` and 72 one-long-arm identities.

Arrays are indexed by subset size, including index zero. For `n=10`
the three-leaf coefficient vectors are
`[0,0,0,3,5,7,9,7,5,3,1]` and
`[0,0,0,3,7,8,8,8,6,3,1]`; both cutoff lists are empty.
All-parameter claims follow from the written proofs, not extrapolation.

## Formal statement coverage

The pinned mathematical source is:

https://github.com/the-omega-institute/trureturing/blob/a165df4cad5a5538260a4e40d6b865a3db48795d/D5/S3/Combinatorics/Graph/ZeroForcing/ConnectedForcingCrossingRefutation.lean

In namespace
`D5.S3.Combinatorics.Graph.ZeroForcing.ConnectedForcingCrossingRefutation`,
`connectedForcing` requires ordinary forcing and initially induced
connectivity; `coefficient` counts subsets of a specified size; `claim`
is the full ordered universal assertion. The declaration `result : ¬ claim`
establishes its negation with the four-vertex path and star. The three-leaf
family, unicyclic classification, general enumeration, minimality and
other all-order statements have the written proofs in the note.

The imported ordinary forcing definitions `Black.init`, `Black.force`
and `IsZeroForcing` are pinned at the same commit:
https://github.com/the-omega-institute/trureturing/blob/a165df4cad5a5538260a4e40d6b865a3db48795d/D5/S3/Combinatorics/GeneralizedPetersen/ZeroForcingThree.lean
Their role here is definitional, not an additional theorem about the
three-leaf or unicyclic families.

## Scientific sources

1. S. Mukherjee and P. Ray, *On the connected zero forcing polynomial of
   finite trees*, arXiv:2611.10985v1 (7 November 2026), Lemma 3.3 and
   Sections 4–5. https://arxiv.org/abs/2611.10985v1
2. B. Brimkov, *Graph Coloring, Zero Forcing, and Related Problems*,
   Ph.D. thesis, Rice University, May 2017, Chapter 7, especially
   Propositions 7.7, 7.8 and 7.11, pages 165–169.
   https://repository.rice.edu/server/api/core/bitstreams/c29c77d5-534a-4c5d-bd83-09121784af53/content
3. B. Brimkov and R. Davila, *Characterizations of the Connected Forcing
   Number of a Graph*, arXiv:1604.00740v1 (4 April 2016), Section 1,
   Theorem 13 and Corollary 14. https://arxiv.org/abs/1604.00740v1
4. T. Newton and B. Brimkov, *Zero forcing is not unimodal*,
   arXiv:2611.11352v1 (8 November 2026), Corollary 2 and Section 3.
   https://arxiv.org/abs/2611.11352v1
