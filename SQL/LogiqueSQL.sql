
# Trigger pour valider le courriel inclut le @ avant insertion nouveau client.
# Si a l'inscription du client le format email est mauvais il retourne un message d'erreur
DELIMITER //
CREATE TRIGGER ValiderEmail
BEFORE INSERT ON Client
FOR EACH ROW
BEGIN
IF INSTR('@', new.email) <= 0
THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Courriel Invalide';
END IF;
END;//
DELIMITER ;
show triggers;



# Fonction qui prend en argument ID_client et retourne le nom complet du client
SET GLOBAL log_bin_trust_function_creators = 1;
DELIMITER //
CREATE FUNCTION TrouverClient(IDClient INTEGER) RETURNS VARCHAR(50)
BEGIN
    DECLARE NomClient VARCHAR(50);
    IF EXISTS (SELECT * FROM CLIENT C WHERE C.ID_client = IDClient) THEN
        SET NomClient = (SELECT DISTINCT C.nom_complet  FROM CLIENT C WHERE C.ID_client = IDClient);
        #ELSE SET  NomClient = 'not found';
    END IF;
    RETURN NomClient;
END //
DELIMITER ;
select TrouverClient(5);




# Procedure pour chercher toutes les commandes et livraisons d'un client, la SP prend le ClientID en argument.
DELIMITER //
CREATE PROCEDURE HistoriqueParIDClient (IN IDClient INT)
BEGIN
    SELECT C.nom_complet, M.ID_commande, M.prix_commande, L.date_livraison, L.statut_livraison
    FROM Client C, Commande M, Livraison L
    WHERE IDClient = C.ID_client AND C.ID_client = M.ID_client AND L.ID_commande = M.ID_commande;
END //
DELIMITER ;
call HistoriqueParIDClient(66);



# ------------************ PROCEDURE pour retourner l'historiques des commandes d'un client, avec son courriel recu en entrée.*********-----------------
DELIMITER //
CREATE PROCEDURE HistoriqueParEmailClient(IN courriel CHAR(30))

BEGIN
DECLARE IDC integer;
        SELECT C.ID_Client INTO IDC  FROM Client C WHERE courriel = C.email;
SELECT C.nom_complet, M.ID_commande, M.prix_parcommande, L.date_livraison, L.statut_livraison
FROM Client C, Commande M, Livraison L
WHERE IDC = C.ID_client AND C.ID_client = M.ID_client AND L.ID_commande = M.ID_commande;
END //
DELIMITER ;

call HistoriqueParEmailClient('aodeeganj@wired.com');
DROP PROCEDURE HistoriqueParEmailClient;
select * from Livraison;
select * from Commande;



# ----------------- ************** Trigger pour valider le mot de passe a au moins 9 caracteres avant insertion nouveau client.
DELIMITER //
CREATE TRIGGER ValiderMotDePasse BEFORE INSERT ON Client FOR EACH ROW
BEGIN
DECLARE msg VARCHAR(50);
        SET msg = 'OK';
IF length(new.mot_de_passe) < 9  THEN
SET msg = 'Mot de passe doit avoir au moins 9 caracteres!';
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END IF;
END //
DELIMITER ;

insert into Client (nom_complet, email, telephone, adresse, mot_de_passe) values ('Costa Smith', 'costa@hotmail.com', '840-607-7741', '0707 Di Loreto Drive', 'U37');
DROP TRIGGER ValiderMotDePasse;

















# Procedure a completer:
# Insere des ID_typeProduit, prix des produits, date_livraison et statut_livraison  aleatoires (ranged)
DELIMITER //
CREATE PROCEDURE RandomIDs(IN valeurMin INT, IN valeurMax INT)
    BEGIN
        DECLARE @compteur , @booleen , @interval INT;
        DECLARE @DateL DATE;
        SET @compteur := 0;
        SET @randLivre := FLOOR(RAND()*(20-5+1))+5;
        SET @DateL := DATE_ADD(CURDATE(), INTERVAL @randLivre DAY);
        START TRANSACTION;
        WHILE @compteur < 100 DO
	    SET @booleen := FLOOR(RAND());
	    SET @DateL = CAST(NOW() + (365 * 2 * RAND() â€“ 365) AS DATE);
            INSERT INTO Produit(ID_typeProduit, prix) VALUES (valeurMin + CEIL(RAND() * (valeurMax - valeurMin)));
	    INSERT INTO Livraison(date_livraison, statut_livraison) VALUES (@DateL, @booleen);
            SET @compteur := @compteur + 1;
        END WHILE;
	COMMIT;
    END//
DELIMITER ;
call RandomIDs(5,5);    # Ne pas executer pour l'instant, servira pour nouveaux clients seulement



# Securite du mot de passe, ne peut etre vu en telechargeant la database autre que par les users autorises
CREATE VIEW protected_info AS SELECT ID_client FROM Client;
GRANT ALL PRIVILEGES ON  testProjet.* TO 'etienne/marc/reda'@'localhost';
GRANT SELECT TO testProjet.protected_info, testProjet.Panier, testProjet.paiement, testProjet.produit, testProjet.Livraison, testProjet.Commande
TO 'read-only_user_name'@'%' identified by 'password';