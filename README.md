# ConstalationDreamer

Tento projekt umo��uje vytvo�it r�zn� hv�zdn� soustavy na z�klad� zadan�ho textov�ho �et�zce. Ten je rozd�len do jednotliv�ch ��st� a z nich jsou pak p�e�etny r�zn� informace o dan� soustav�. Tyto informace budou pozd�ji objasn�ny (pozd�ji je my�leno �asov� ne te� v textu).

Krom� generov�n� samotn�ch soustav se pro jednoduchost vytvo�� i zjednodu�en� pohled na planety, kter� v dan�m syst�mu jsou. Ty mohou b�t v n�kolika z�kladn�ch form�ch. Op�t je v�e �teno z p�vodn�ho zadan�ho �et�zce.

N�sleduje n�kolik uk�zek samotn�ch soustav a n�sledn� dosavadn� stav tvorby biom�.

<p float="middle">
<img src="./examples/star_system_Jan_Tislick�.png" width="350">
<img src="./examples/star_system_Petr_�epn��ek.png" width=350>
<img src="./examples/star_system_Qvido_Ostravan.png" width=350>
<img src="./examples/star_system_Martin_Nov�k.png" width=350>
</p>
<p float="middle">
<img src="./examples/biom_generator_1.png" width=300>
<img src="./examples/biom_generator_1000.png" width=300>
<img src="./examples/biom_generator_3684.png" width=300>
<img src="./examples/biom_generator_658731.png" width=300>
</p>

[ ] - Refaktorovat vykreslovani objektu, pokusit se vymyslet takov� p��stup, aby nebylo nutne rozli�ovat jednolive instance a pouze se volalo draw, zde bude nejv�t�� probl�m s p�sem asteroid�.
[ ] - Refaktorovat zp�sob vykreslovani planet. C�lem bude, p�edat p�edem p�ipravenou kreslici plochu, do ktere se vykresl� vzhled planety a po pot�ebnych upravach se vlo�� na specifikovane misto
[ ] - Sjednotit p�ed�van� objekty do draw, aby to v�e bylo bu� kreslici plocha (ImageDraw) nebo jen Image