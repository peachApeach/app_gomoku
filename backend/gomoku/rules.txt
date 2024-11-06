"""
https://www.renju.net/rules/

So, here are the three rules that make renju different from gomoku:


Black player is not allowed to make the 3x3 fork.
Black player is not allowed to make the 4x4 fork.
Black player is not allowed to make an overline (6 or more stones in a row).


Endgame Capture:
◦ A player who manages to line up five stones wins only if the opponent cannot
break this line by capturing a pair.
◦ If the player has already lost four pairs and the opponent can capture one
more, the opponent wins by capture.
◦ If there is no possibility of this happening, there is no need to continue the
game.

• No double-threes : It is forbidden to play a move that introduces two free-three
alignments, which would guarantee a win by alignment (See the appendix).
== The rule of three and three bans a move that simultaneously forms two open rows of three stones (rows not blocked by an opponent's stone at either end).
"""

"""
Règles de restriction du premier joueur : Le premier joueur est souvent limité dans ses choix pour les premiers coups, par exemple, en lui imposant des zones ou en l'obligeant à varier ses placements pour éviter une victoire immédiate.

Règle de "Renju" : Une règle très connue, utilisée au Japon, interdit au premier joueur de former des motifs spécifiques comme deux rangées ouvertes de trois pions, ou deux rangées de quatre, ce qui limite ses possibilités de gagner trop vite.

Règle de "Swap" : Une autre approche consiste à faire jouer les trois premiers coups par le premier joueur. Ensuite, le deuxième joueur peut décider de changer de rôle et de devenir le premier joueur. Cela incite le premier joueur à ne pas trop avantager sa propre position pour éviter que son adversaire ne prenne l’avantage.

Plateau plus grand : Augmenter la taille du plateau peut aussi réduire l'avantage du premier joueur en offrant plus d'options de jeu.
"""
