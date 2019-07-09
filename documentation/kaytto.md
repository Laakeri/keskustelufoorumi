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

```SQL
SELECT Post.message, Post.id, Post.created_at, Account.username, (SELECT COUNT(*) FROM Post Child WHERE Child.parent_id = Post.id), Favorite.post_id FROM Post Post INNER JOIN Account ON Account.id = Post.user_id LEFT JOIN Favorite ON Favorite.post_id = Post.id AND Favorite.user_id = :current_user_id WHERE Post.parent_id = :parent_id ORDER BY Post.created_at DESC LIMIT :posts_limit OFFSET :offset;
```

* Etusivu näyttää viestejä järjestyksessä uudesta vanhimpaan
* Viestiketjujen laajennus ja pienennys toimii javascriptillä
* Yhdellä kertaa ladataan korkeintaan 4 peräkkäistä viestiä, lisää voi ladata painamalla "Näytä lisää" (4 on pieni luku, mutta tätä on helppo demota)
* Viestejä voi selata myös alkaen jostain viestiketjusta painaen "Linkki"-linkkiä

### Katsoa käyttäjien profiilia

* Profiilissa näkyy milloin käyttäjä on rekisteröitynyt, montako viestiä hän on lähettänyt ja mahdollisesti kuvaus
* Jokaisen viestin yhteydessä on linkki käyttäjän profiiliin

## Sivuston käyttäjät voivat:

### Lähettää viestejä

* Uusi viesti tai vastauksena johonkin viestiin

### Muokata lähettämiään viestejä

### Poistaa lähettämiään viestejä

### Lisätä viestejä suosikeiksi

### Poistaa viestejä suosikeista

### Selata omia suosikkiviestejä

### Muokata kuvausta omassa profiilissa

### Kirjautua ulos


# Puuttuvat ominaisuudet

Näitä on suunniteltu jossain kohtaa, mutta ei toteutettu:

* Admin käyttäjä joka voi poistaa kaikkien viestejä
* Viestejä voi järjestää jonkun muun kriteerin mukaan
* Viesteihin voi liittää mediaa