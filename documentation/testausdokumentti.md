# Testausdokumentti
## Testien ajo
Aja testit komennolla
```
poetry run pytest
```

## Testikattavuus
Testikattavuus reitinhakualgoritmeille coverage-rapotin mukaan on seuraava:
```
Name                          Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------
src/dijkstra.py                  51      0     16      1    99% 
src/astar.py                     69      0     16      0   100%
src/jps.py                      156      2     72      3    98%

```

## Testit
Reitinhakualgoritmien yksikkötestit testaavat, että algoritmit löytävät oikean pituisen reitin tai eivät löydä reittiä, kun se ei ole mahdollista. 

A*- ja JPS-algoritmeja verrataan Dijkstran toimintaan. Ensin Dijkstra etsii reitin satunnaisesti valitulla Moving AI -kartalla, jonka alku- ja loppupisteet on arvottu. A*:n ja JPS:n pitää löytää saman pituinen reitti, mutta nopeammin kuin Dijkstra.