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
    potvzeni            CHAR(1) NOT NULL,
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

INSERT INTO uzivatel (jmeno, prijmeni, email, heslo, typy_uzivatele_id_typuzivatele) VALUES ('admin', 'admin','admin@admin','admin',1);
