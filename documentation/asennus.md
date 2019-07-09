# Asennusohje

## Paikallinen asennus

Oletetaan että git, python3 ja pip on asennettuna. Sovellus asennetaan ja käynnistetään paikallisesti seuraavilla komennoilla linuxissa:

```
git clone https://github.com/Laakeri/keskustelufoorumi.git
cd keskustelufoorumi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

Sovellus käynnistyy osoitteeseen ```localhost:5000```.

## Asennus Herokuun

Oletetaan että git ja heroku cli on asennettuna. Seuraavilla komennoilla sovelluksen saa herokuun

```
git clone https://github.com/Laakeri/keskustelufoorumi.git
cd keskustelufoorumi
heroku create sovelluksen-nimi
heroku addons:add heroku-postgresql:hobby-dev
git push heroku master
```

Sovellus käynnistyy osoitteeseen sovelluksen-nimi.herokuapp.com.

## Tietokanta

Sovellus käyttää lokaalisti application/db.db tiedostossa olevaa sqlite3 -tietokantaa. Herokussa se käyttää PostgreSQL:ää. Sovellus luo itse käynnistyessään tietokantataulut jos niitä ei ole, mutta taulut voi myös luoda seuraavilla komennoilla:

```SQL
CREATE TABLE Post (
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	message TEXT NOT NULL, 
	user_id INTEGER NOT NULL, 
	parent_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(parent_id) REFERENCES post (id)
);
```

```SQL
CREATE TABLE Account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	description TEXT, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id), 
	CHECK (is_admin IN (0, 1))
);
```

```SQL
CREATE TABLE favorite (
	user_id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	added_at DATETIME NOT NULL, 
	PRIMARY KEY (user_id, post_id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(post_id) REFERENCES post (id)
);
```