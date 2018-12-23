# SpaceRetroWars

## Gruppe:	Oleg Kossjak, Artur Nowodworski
## Framework:	PyGame

## Funktionale Anforderungen
### a) Kern-Anforderungen (verbindlich)

/F10/ Vor dem Spielbeginn muss dem Spieler gewährleistet werden, eine von mindestens zwei Spielumgebungen auszuwählen.

/F20/ Das Spiel muss dem Spieler ermöglichen, am unteren Rand des Spielfeldes eine Kanone horizontal nach rechts und nach links zu steuern.

/F30/ Während des Spiels muss sich mehrere Reihen von Objekten (Aliens), die parallel zueinander angeordnet sind, horizontal von links nach rechts und zurück bewegen. Nach dem Erreichen eines Bereichs des linken bzw. des rechten Spielfeldrandes müssen die Reihen von Aliens um denselben Bereich nach unten verschoben werden. Wenn eine Reihe von Aliens einen unteren Bereich des Spielfeldes erreicht, verliert der Spieler eines seiner Leben.

/F40/ Das Spiel muss dem Spieler ermöglichen, mit der Kanone auf die Aliens zu schießen, um sie zu eliminieren. Wird ein Alien getroffen, bekommt der Spieler eine bestimmte Anzahl von Punkten.

/F50/ Die Aliens muss nach unten schießen. Wird dabei die Kanone getroffen, verliert der Spieler eines seiner Leben.

/F60/ Über der Kanone müssen sich Blöcke befinden, hinter denen sich die Kanone verstecken kann. Die Blöcke können durch ein Geschoss sowohl von den Aliens als auch von der Kanone getroffen werden, sodass sie letztendlich zerstört werden.

/F70/ Ab und zu muss im oberen Bereich des Spielfeldes ein Raumschiff erscheinen, das sich horizontal von einem Spielfeldrand bis zum anderen bewegt. Wird er durch die Kanone getroffen, bekommt der Spieler eine bestimmte Anzahl von Punkten.

/F80/ Während des Spiels muss die Anzahl der Leben des Spielers sowie die Anzahl der erreichten Punkte dargestellt werden.

/F90/ Es muss möglich sein, die Liste der besten Spielergebnisse aufzurufen (lokal).

### b) Nice-to-have – Anforderungen (fakultativ)

/F100/ Auf dem Spielfeld können sich schwarze Löcher befinden können. Befindet sich ein Alien an der Stelle eines schwarzen Loches, dann verschwindet er für eine gewisse Zeit, sodass man ihn nicht eliminieren kann.

/F110/ Der Spieler kann ein spezielles Geschoss in Form einer Bombe einsetzen können, die mehrere Gegner eliminieren kann.

/F130/ Mit De-castling kann die Formationsstellung, zur Schutz des Mutterschiffs, aufgelöst werden

/F140/ Es kann möglich sein, durch die Wahl der Anzahl der Aliens z.B. 5x5, 6x6, 7x7 (Reihen x Spalten) den Schwierigkeitsgrad festzulegen.

/F150/ Der Spieler kann einen Asteroidenregen, der Aliens aber auch die Kanone eliminieren kann, hervorrufen.

## Klassendiagramm

![alt text](https://github.com/mischart/SpaceRetroWars/blob/master/Klassendiagramm.PNG "Klassendiagramm")
