# Food-recommandation

Bienvenue sur ce repository autour de la nourriture.
Pour construire ce projet nous sommes partis du constat que l'application Yuka ne permettait pas de comparer deux produits entre eux ni de rechercher des « top aliments » par catégories. Nous avons donc utilisé l'api de Open Food Facts (la base de données de Yuka) pour réaliser trois petits projets.

## Comment lancer notre outil

Voici les librairies à installer sur Python pour utiliser notre outil : pyzbar, tkinter, pandas, openfoodfacts et cv2.
Une fois les librairies installées, vous pouvez clone notre repository et lancer le fichier python "interface" afin de lancer notre outil. Vous aurez plusieurs choix qui s'offrent à vous : 
- un comparateur entre deux produits qui vous proposera soit d'insérer le chemin vers deux photos des codes barres de produits que vous souhaitez comparer soit d'insérer directement leurs codes barres. En fonction de votre objectif, vous obtiendrez une comparaison entre vos deux produits. Si vous souhaitez tester l'option avec l'entrée de chemins vers deux photos, vous pouvez enregistrer les photos que nous avons mis sur notre Repository sur votre ordinateur et récupérer le chemin lié à ces photos dans votre ordinateur.
- un outil qui vous donnera les cinq meilleurs produits de notre vaste base de données selon une catégorie d'aliments et un objectif santé.
- des résultats d'une étude de corrélation entre Nutriscore, ecoscore et Nova Group (indicateur du degré de transformation d'un aliment) ainsi que d'une étude entre sucres et gras.

## Organisation de notre repo

Vous pourrez trouver différents fichiers :
- interface.py qui correspond à l'interface utilisateur
- top_5.py qui reprendra le détail de l'outil de "top aliments"
- comparaison.py qui reprend le détail de l'outil comparaison
- data_analyse.py qui détaille les études de corrélation

Bonne navigation !
Lyna et Hakim
