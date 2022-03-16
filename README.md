# Logo3D

Pràctica de compiladors+Python de GEI-LP (edició 2020-2021 Q2).
Implementació d'un intèrpret d'un llenguatge de programació anomenat Logo3D el
qual permet pintar geometria 3D amb una tortuga en mitjançan el mòdul `vpython`.

## Especificació de Logo3D

Les instruccions de Logo3D són:

- l'assignació,
- la lectura,
- l'escriptura,
- el condicional,
- la iteració amb `WHILE`,
- la iteració amb `FOR`, i
- la invocació a un procediment.

Per entendre com funciona el llenguatge en profunditat consultar : https://github.com/jordi-petit/lp-logo3d-2021.

# Contingut

- `requirements.txt` fiter amb totes els requeriments del projecte.

- `logo3d.py`, el programa principal de l'intèrpret.

- `logo3d.g`, la gramàtica del llenguatge.

- `visitor.py`, el visitador de l'AST.

- `turtle3d.py`, la classe `Turtle3D`.

# Llibreries usades

- `vpython`

- `ANTLR4`

# Instalació

Per poder executar el programa es necessari tenir pyton3 i antlr4, per instalar
python3 executeu la comanda:

```bash
sudo apt-get install python3
```
I per antlr4 vegeu el seguent link el qual explica els passos de instalació:
https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

Tot seguit s'han de instalar les dependències, useu la comanda seguent per instalar-les totes:
```bash
python3 -m pip install -r requirements.txt
```
I per últim executeu la comanda de sota que generarà tots els arxius necessaris per l'intèrperet:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor logo3d.g
```

## Invocació

El intèrpret s'ha d'invocar amb la comanda `python3 logo3d.py` tot
passant-li com a paràmetre el nom del fitxer que conté el codi font
(l'extensió dels fitxsers per programes en Logo3D és `.l3d`). Per exemple:

```bash
python3 logo3d.py programa.l3d
```

Els programes poden començar des de qualsevol procediment.  Per defecte, es
comença pel procediment `main`.
Si es vol començar el programa des d'un procediment diferent de `main()`, cal donar el
seu nom com a segon paràmetre i es poden passar els valors dels seus paràmetres (nombre reals)
des de la linia de comandes.

```bash
python3 logo3d.py programa.l3d quadrats 10 20
```
