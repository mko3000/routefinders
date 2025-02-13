# Toteutusdokumentti

## Käyttö
Ohjemassa on komentorivikäyttöliittymä, jossa voi valita tyhjän tai valmiin kartan tai algoritmivertailun. Jos käyttäjä valitsee kartan, graafinen pygame-käyttöliittymä aukeaa. Karttaan voi piirtää itse seiniä ja kartassa voi käynnistää jonkun kolmesta reitinhakualgoritmista, jolloin niiden toiminta esitetään kartalla. Reitinhakualgoritmin suorituksesta tulostetaan tietoja komentorivikäyttöliittymään. Algoritmivertailua ajaa kaikki vertailtavat algoritmit suurehkolla kartalla ja tulostaa suorituksesta tietoja komentorivikäyttöliittymään. Vertailussa käytetään Moving AI:n reitinhakualgoritmien arviointiin tarkoitettuja karttoja (https://movingai.com/benchmarks/grids.html).

## Rakenne
Ohjelman rakenne on jaettu käyttöliittymään ja sovelluslogiikkaan. Käyttöliittymässä on kaksi pääluokkaa: ui ha gui. Ui hallitsee tekstikäyttöliittymää, josta voi käynnistää graafisen esityksen algoritmien toiminnasta. Graafisen esityksen toiminnallisuutta ohjataan gui-luokasta.

Sovelluslogiikassa on luokka ruudukolle (Grid) ja ruudelle (Tile). Ruutujen toiminta eroaa hieman riippuen käytetystä reitinhakualgoritmista, joten ruudulle on kolme aliluokkaa (Dijkstra_tile, Astar_tile, JPS_tile). Jokaiselle kolmelle reitinhakualgoritmille (Dijkstra, A*, Jump Point Search) on oma luokkansa. Lisäksi on luokka karttojen hallinnointiin.

## Suorituskykyvertailu
Vaikka Jump Point Search -algoritmi kävikin huomattavasti vähemmässä määrässä ruutuja kuin muut algoritmit, kesti sen suoritus useimmiten hieman pidempää kuin A*:n. Dijkstra oli hitain.

## Laajojen kielimallien käyttö
Käytin ChatGTP 4o -kielimallia tekstikäyttöliittymässä näkyvän taulukon muotoiluun ja toiminnallisuuden, jolla karttoja voi poistaa karttamuistista (json-tiedosto), tekemiseen. Reitinhakualgormien, tai muunkaan oleellisen ohjemalogiikan toteuttamiseen, ei ole käytetty kielimalleja.

## Viitteet:
- Harabor, D., & Grastien, A. (2011). Online Graph Pruning for Pathfinding On Grid Maps. Proceedings of the AAAI Conference on Artificial Intelligence, 25(1), 1114-1119. https://doi.org/10.1609/aaai.v25i1.7994
- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://movingai.com/benchmarks/grids.html
- https://zerowidth.com/2013/a-visual-explanation-of-jump-point-search/