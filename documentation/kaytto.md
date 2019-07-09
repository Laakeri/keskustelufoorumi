# Käyttötapaukset

Tässä olevat SQL kyselyt eivät välttämättä ole täysin samoja kuin implementaatio, koska implementaatio on tehty suureksi osaksi SQLAlchemy ORM:ää käyttäen.

## Kuka tahansa vierailija sivulla voi:

### Rekisteröityä

```SQL
INSERT INTO Account (username, password) VALUES (:username, :password);
```

### Kirjautua sisään

```SQL
SELECT * FROM Account WHERE username = :username AND password = :password;
```

### Selata viestejä

* Etusivu näyttää viestejä järjestyksessä uudesta vanhimpaan
* Viestiketjujen laajennus ja pienennys toimii javascriptillä
* Yhdellä kertaa ladataan korkeintaan 4 peräkkäistä viestiä, lisää voi ladata painamalla "Näytä lisää" (4 on pieni luku, mutta tätä on helppo demota)
* Viestejä voi selata myös alkaen jostain viestiketjusta painaen "Linkki"-linkkiä

Seuraavaa kyselyä käytetään kaikessa viestien selaamisessa. Se kyselee annetun parent-viestin lapsiviestien kaikki tarpeelliset tiedot. Lapsiviestejä listataan korkeintaan :posts_limit määrä, ja offsettiä käytetään selaamisen mahdollistamiseen. Hyvä trikki on käyttää limittinä 5 viestiä kun halutaan listata 4 viestiä, koska sitten tiedetään suoraan onko neljän seuraavan jälkeen vielä lisää viestejä.
```SQL
SELECT 
	Post.message, 
	Post.id, 
	Post.created_at, 
	Account.username, 
	(SELECT COUNT(*) FROM Post Child WHERE Child.parent_id = Post.id), 
	Favorite.post_id 
FROM Post Post 
INNER JOIN Account ON Account.id = Post.user_id 
LEFT JOIN Favorite ON Favorite.post_id = Post.id AND Favorite.user_id = :current_user_id 
WHERE Post.parent_id = :parent_id 
ORDER BY Post.created_at DESC 
LIMIT :posts_limit OFFSET :offset;
```

### Katsoa käyttäjien profiilia

* Profiilissa näkyy milloin käyttäjä on rekisteröitynyt, montako viestiä hän on lähettänyt ja mahdollisesti kuvaus
* Jokaisen viestin yhteydessä on linkki käyttäjän profiiliin

```SQL
SELECT
	Account.date_created,
	Account.description,
	(SELECT COUNT(*) FROM Post WHERE Account.id = Post.user_id)
FROM Account Account
WHERE Account.username = :username;
```

## Rekisteröityneet käyttäjät voivat:

### Lähettää viestejä

* Uusi viesti tai vastauksena johonkin viestiin

```SQL
INSERT INTO Post (message, user_id, parent_id) VALUES (:message, :current_user_id, :parent_id);
```

### Muokata lähettämiään viestejä

```SQL
UPDATE Post SET message = :message WHERE id = :id AND user_id = :current_user_id;
```

### Poistaa lähettämiään viestejä

```SQL
DELETE FROM Post WHERE id = :id AND user_id = :current_user_id;
```

### Lisätä viestejä suosikeiksi

```SQL
INSERT INTO Favorite (user_id, post_id) VALUES (:current_user_id, :post_id);
```

### Poistaa viestejä suosikeista

```SQL
DELETE FROM Favorite WHERE user_id = :current_user_id AND post_id = :post_id;
```

### Selata omia suosikkiviestejä

```SQL
SELECT post_id FROM Favorite WHERE user_id = :current_user_id;
```

### Muokata kuvausta omassa profiilissa

```SQL
UPDATE Account SET description = :description WHERE id = :current_user_id;
```

### Kirjautua ulos


# Puuttuvat ominaisuudet

Näitä on suunniteltu jossain kohtaa, mutta ei toteutettu:

* Admin käyttäjä joka voi poistaa kaikkien viestejä
* Viestejä voi järjestää jonkun muun kriteerin mukaan
* Viesteihin voi liittää mediaa