
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
DELIMITER //
DROP FUNCTION IF EXISTS TrouverClient;
CREATE FUNCTION
    TrouverClient(ID_client INT(50))
    RETURNS VARCHAR(100)
    DETERMINISTIC
BEGIN
DECLARE @NomClient VARCHAR(100);
SET @NomClient = (SELECT COUNT (DISTINCT nom_complet) FROM Client WHERE nom_complet = @NomClient);
RETURN @NomClient;
END; //
DELIMITER ;
select TrouverClient(5);




# Procedure pour chercher toutes les commandes et livraisons d'un client, la SP prend le ClientID en argument.
DELIMITER //
CREATE PROCEDURE HistoriqueParClient (IN IDClient INT)
BEGIN
SELECT C.nom_complet, M.ID_commande, P.montant_total, L.date_livraison, L.statut_livraison
FROM Client C, Commande M, Livraison L, Paiement P
WHERE IDClient = C.ID_client AND C.ID_client = M.ID_client AND L.ID_commande = M.ID_commande;
END //
DELIMITER ;
call HistoriqueParClient(66);




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