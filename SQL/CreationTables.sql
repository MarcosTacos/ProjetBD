CREATE DATABASE PJT2;
USE PJT2;



-- # ID_client et email uniques ici
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
-- # ID_produit unique
CREATE TABLE IF NOT EXISTS Produit
(
  ID_produit INT NOT NULL AUTO_INCREMENT,
  nom_du_produit VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  quantite_produit INT NOT NULL,
  taille INT NOT NULL,
  couleur VARCHAR(20) NOT NULL,
  genre VARCHAR(20) NOT NULL,
  prix INT NOT NULL,
  PRIMARY KEY (ID_produit)
);

-- # Id-panier se genere dans Panier, et dans Commande il refere a Panier comme foreign key
-- #  ID_client et ID_produit ne sont pas uniques--> Id_Client =  Clé etrangere a Client, Id_Produit = Clé etrangere vers Produit.
CREATE TABLE IF NOT EXISTS Panier
(
  ID_panier INT NOT NULL AUTO_INCREMENT,
  ID_client INT,
  statut_panier INT NOT NULL,
  PRIMARY KEY (ID_panier),
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS ItemsPanier (
#     ID_itemsPanier INT,
    ID_panier INT,
    ID_produit INT,
    quantite_items INT NOT NULL,
    prix_totalProduits INT NOT NULL,
    PRIMARY KEY(ID_panier, ID_produit),
    FOREIGN KEY (ID_panier) REFERENCES Panier(ID_panier) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit) ON UPDATE CASCADE ON DELETE CASCADE
);


-- # ID_commande et ID_paiement uniques ici --> Id-Paiement de Paiement va referer a ID-Paiement dans Commande
CREATE TABLE IF NOT EXISTS Commande
(
  ID_commande INT NOT NULL AUTO_INCREMENT,
  ID_client INT,
  statut_commande INT NOT NULL,
  prix_parCommande INT NOT NULL,
  PRIMARY KEY (ID_commande),
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS ItemsCommande
(
  ID_itemsCommande INT NOT NULL AUTO_INCREMENT,
  ID_commande INT,
  ID_produit INT,
  prix_duProduit INT,
  quantite_itemsCommande INT,
  PRIMARY KEY (ID_itemsCommande),
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit) ON UPDATE CASCADE ON DELETE CASCADE
);


-- # ID_paiement et ID_commande uniques ici, Id-PAIEMENT REFERE A ID-Paiement de Commande, c'est dans cette table qu'il est instanciÃ© par AUTO_INCREMENT
CREATE TABLE IF NOT EXISTS Paiement
(
  ID_paiement INT NOT NULL AUTO_INCREMENT,
  mode_paiement VARCHAR(100) NOT NULL,
  statut_paiement INT NOT NULL,
  ID_commande INT,
  ID_client INT,
  PRIMARY KEY (ID_paiement),
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_client) REFERENCES Client(ID_client) ON UPDATE CASCADE ON DELETE CASCADE
);

-- # ID_livraison, ID_commande et ID_paiement sont uniques ici
CREATE TABLE IF NOT EXISTS Livraison
(
  ID_livraison INT NOT NULL AUTO_INCREMENT,
  date_livraison DATE NOT NULL,
  statut_livraison INT NOT NULL,
  ID_commande INT,
  ID_paiement INT,
  PRIMARY KEY (ID_livraison),
  FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ID_paiement) REFERENCES Paiement(ID_paiement) ON UPDATE CASCADE ON DELETE CASCADE
);


-- # Pour supprimer les tables pour les recreer apres une correction, supprimez dans l'ordre suivant.

-- # set foreign_key_checks = 0;
DROP TABLE Livraison;
DROP TABLE Paiement;
DROP TABLE ItemsCommande;
DROP TABLE Commande;
DROP TABLE ItemsPanier;
DROP TABLE Panier;
DROP TABLE Produit;
DROP TABLE Client;

show tables;
