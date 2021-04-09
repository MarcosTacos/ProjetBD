#  create database testProjet;
use testProjet;


# ID_client et email unique ici
CREATE TABLE IF NOT EXISTS Client
(
  ID_client INT NOT NULL AUTO_INCREMENT,
  nom_complet VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  telephone VARCHAR(12) NOT NULL,
  adresse VARCHAR(100) NOT NULL,
  mot_de_passe VARCHAR(100) NOT NULL,
  UNIQUE(email),
  PRIMARY KEY (ID_client)
);

# ID_produit unique
CREATE TABLE IF NOT EXISTS Produit
(
  ID_produit INT NOT NULL AUTO_INCREMENT,
  nom_du_produit VARCHAR(100) NOT NULL,
  description VARCHAR(100) NOT NULL,
  ID_typeProduit INT NOT NULL,
  prix INT NOT NULL,
  PRIMARY KEY (ID_produit)
);

# ID_commande redondant, probablement mieux de le supprimer ou
# de le remplacer par un autre attribut comme ID_panier.
# quantite, ID_client et ID_produit ne sont pas uniques
# Table a modifier
CREATE TABLE IF NOT EXISTS Panier
(
  quantite INT NOT NULL,
  ID_client INT NOT NULL,
  ID_produit INT NOT NULL,
  ID_commande INT NOT NULL,
  PRIMARY KEY (ID_client),
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE
);


# ID_commande et ID_paiement uniques ici
CREATE TABLE IF NOT EXISTS Commande
(
  ID_commande INT NOT NULL AUTO_INCREMENT,
  prix_commande INT NOT NULL,
  statut_commande INT NOT NULL,
  ID_client INT NOT NULL,
  ID_paiement INT NOT NULL,
  PRIMARY KEY (ID_commande),
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_paiement) REFERENCES Paiement(ID_paiement) ON UPDATE CASCADE ON DELETE CASCADE
);

# ID_paiement et ID_commande uniques ici
CREATE TABLE IF NOT EXISTS Paiement
(
  ID_paiement INT NOT NULL AUTO_INCREMENT,
  mode_paiement VARCHAR(100) NOT NULL,
  montant_total FLOAT NOT NULL,
  ID_commande INT NOT NULL,
  ID_client INT NOT NULL,
  PRIMARY KEY (ID_paiement),
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE
);

# ID_livraison, ID_commande et ID_paiement sont uniques ici
CREATE TABLE IF NOT EXISTS Livraison
(
  ID_livraison INT NOT NULL AUTO_INCREMENT,
  date_livraison DATE NOT NULL,
  statut_livraison INT NOT NULL,
  ID_commande INT NOT NULL,
  ID_paiement INT NOT NULL,
  PRIMARY KEY (ID_livraison),
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_paiement) REFERENCES Paiement(ID_paiement) ON UPDATE CASCADE ON DELETE CASCADE
);


