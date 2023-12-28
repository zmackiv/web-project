DROP TABLE IF EXISTS objednavka;
DROP TABLE IF EXISTS stroj;
DROP TABLE IF EXISTS typy_stroje;
DROP TABLE IF EXISTS typy_uzivatele;
DROP TABLE IF EXISTS uzivatel;
DROP TABLE IF EXISTS uzivatel_objednavka;

CREATE TABLE objednavka (
    id_objednavka       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    timestamp           TIMESTAMP NOT NULL,
    cas_od              INTEGER NOT NULL,
    cas_do              INTEGER NOT NULL,
    adresa_doruceni     TEXT NOT NULL,
    vzdalenost_doruceni TEXT NOT NULL,
    cena                INTEGER NOT NULL,
    potvrzeni           CHAR(1) NOT NULL,
    stroj_id_stroj      INTEGER NOT NULL,
    FOREIGN KEY (stroj_id_stroj) REFERENCES stroj (id_stroj)
);

CREATE TABLE stroj (
    id_stroj                 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    model                    TEXT NOT NULL,
    popis                    TEXT NOT NULL,
    hodinova_cena            INTEGER NOT NULL,
    cena_dopravy_km          INTEGER NOT NULL,
    foto                     TEXT NOT NULL,
    typy_stroje_id_typstroje INTEGER NOT NULL,
    FOREIGN KEY (typy_stroje_id_typstroje) REFERENCES typy_stroje (id_typstroje)
);

CREATE TABLE typy_stroje (
    id_typstroje INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nazev        TEXT NOT NULL
);

CREATE TABLE typy_uzivatele (
    id_typuzivatele INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nazev           TEXT NOT NULL
);

CREATE TABLE uzivatel (
    id_uzivatele                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    jmeno                          TEXT NOT NULL,
    prijmeni                       TEXT NOT NULL,
    email                          TEXT NOT NULL,
    heslo                          TEXT NOT NULL,
    cena_prace                     INTEGER,
    typy_uzivatele_id_typuzivatele INTEGER NOT NULL,
    FOREIGN KEY (typy_uzivatele_id_typuzivatele) REFERENCES typy_uzivatele (id_typuzivatele)
);

CREATE TABLE uzivatel_objednavka (
    uzivatel_id_uzivatele    INTEGER NOT NULL,
    objednavka_id_objednavka INTEGER NOT NULL,
    FOREIGN KEY (objednavka_id_objednavka) REFERENCES objednavka (id_objednavka),
    FOREIGN KEY (uzivatel_id_uzivatele) REFERENCES uzivatel (id_uzivatele)
);

INSERT INTO typy_uzivatele (id_typuzivatele, nazev) VALUES (1, 'admin');
INSERT INTO typy_uzivatele (id_typuzivatele, nazev) VALUES (2, 'dispecer');
INSERT INTO typy_uzivatele (id_typuzivatele, nazev) VALUES (3, 'klient');
INSERT INTO typy_uzivatele (id_typuzivatele, nazev) VALUES (4, 'technik');

INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES ('Admin', 'Admin', 'admin', '74baeb21265087ea11e1555f2b1489ae16c00cbdd5b78f0c3eedd6c0c8be3a41', 1);
INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES ('Dispecer', 'Dispecer', 'dispecer', '9d9ad6bf6984657b3ccf9efb93bcc2154ae9fdf2ac6cf2e221b9f7661845f8d1', 2);
INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES ('Klient', 'Klient', 'klient', 'f44fe2b0f77381eb7d8cd895b73f19a95126576fe5cb0521dfb1aa1baed03f9c', 3);
INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES ('Technik', 'Technik', 'technik', '2aa76a551815c813cb581ac374549265bf16720c0910d8472a425344889d82ca', 4);

INSERT INTO stroj (model, popis, hodinova_cena, cena_dopravy_km, foto, typy_stroje_id_typstroje) VALUES ('New Holland 5.2', 'Zbrusu nový traktor.', 170, 50, 'https://www.mascus.cz/_next/image?url=https%3A%2F%2Fst.mascus.com%2Fimagetilewm%2Fproduct%2F72704d0e%2Flindner-traktor-lintrac-80-4-h%2C8a5c8ba8.jpg&w=1920&q=75', 1);
INSERT INTO stroj (model, popis, hodinova_cena, cena_dopravy_km, foto, typy_stroje_id_typstroje) VALUES ('Matador MO', 'Zbrusu nový secí stroj.', 120, 30, 'https://www.kuhncenter.cz/file/sdff-get?id=998', 2);
INSERT INTO stroj (model, popis, hodinova_cena, cena_dopravy_km, foto, typy_stroje_id_typstroje) VALUES ('KÖCKERLING VITU', 'Zbrusu nový secí stroj.', 130, 30, 'https://www.pal.cz/getattachment/de759566-e2a7-4bf1-9593-f7518b01262e/PhotoSmall?maxsidesize=660', 2);

INSERT INTO typy_stroje(id_typstroje, nazev) VALUES (1, 'traktor');
INSERT INTO typy_stroje(id_typstroje, nazev) VALUES (2, 'secí stroj');