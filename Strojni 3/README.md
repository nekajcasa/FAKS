# Preračini palanetno gonilo
Preračuni za strojne elemente 3 (datoteka planetno_vXX.xlsm). Za pravilno delovanje je potrebno omogočiti macro-te.

## Navodila za uporabo
Vrednosti se vpisuje v **rumeno** obarvane celice

Korak 1:
 - Izbere se skupino (celica B4)
 - Vnese se moč in frekvenco motorja
Korak 2:
 - Izpolne se vse rumeno obarvane celice razen E17 in F17
 - Klikne se gumb za željeni prenos moči (opis spodaj)
 - premika se sliderja za prestavno razmerje prve stopnje (zgornji) in velikost bobna (spodni), kombinacije ki ustrezajo vsem pogojem se obravajo vijolično
 - v E17 in F17 se vnese izbrano kombinacijo (s številom zob na sončniku posamezne stopnje)
Korak 3:
 - Izpolni se rumena polja (po potrebi še svetlo rumena)
 - Preverimo da so napetosti nižje od odpustnih (vrstica 47 in 55)

## Opis postavitev
###Prenos iz obroča
Moment se prenaša na boben iz obroča na drugi stopnji. Obroč prve stopnje in kletka druge stopnje sta blokirani.
###Prenos iz obroča 1 in 2
Moment se prenaša na boben iz obroča na drugi stopnji. Obroč prve stopnje je fiksiran na obroč druge stopnje, kletka druge stopnje je blokirana.
### Prenos iz kletke
Moment se prenaša na boben iz kletke na drugi stopnij. Obroča prve in druge stopnje sta blokirana.

#Pravilnost rezultatov
Fino bi bilo, se te rezultae primerja s drugimi izračuni da se najdejo napake v izračunih.
*Verjetnost da so napake pri izračunih Prenos iz obroča 1 in 2 je nekiliko večja.*

#Omejitve
Za enkrat je izračun možen samo za zobnike z ravnim ozobjem, do normalnega modula 5...
