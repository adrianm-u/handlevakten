USE handlevaktenDB;

-- passord for brukere er fornavn + 123, e.g. admin123, karl123
INSERT INTO users (email, password_hash, first_name, last_name, account_type) VALUES
('admin@handlevakten.no', 'scrypt:32768:8:1$dXFexsvvFn1OHaem$01b24f78e53740694c9cc98fd761ed538d2eb66cf9d30d221b6d08582e227a1e51aaef7ed5a28a615b86b88fa44189375914ca93878fb328f3457a776106d0cb', 'Admin', 'Bruker', 'admin'), 
('karl@epost.no', 'scrypt:32768:8:1$X6AiQlJidTMbZBY2$3d5d7b164ed749c901f0162da3894e289f106eff841e53d7be88d568148b956c9e03c11d58ea574c9bc43a3d213699dc2b8d1946d45c218b5b823e7c5c42d6ed', 'Karl', 'Knutsen', 'user'),
('celina@epost.no', 'scrypt:32768:8:1$HB742oMG8CJ4jo4Y$ef8440b05dddcbc01911359467b71e521dd5610b31281371c58aa90dbc0892c3e2da2c54cde7e4fd2a7b9b24f34efcba609cd2aed437d4c5b7187ce47090e621', 'Celina', 'Oftedal', 'user');


INSERT INTO categories (category_name) VALUES
('Meieri'),
('Brød'),
('Drikke'),
('Snacks'),
('Kjøtt'),
('Fisk');

INSERT INTO products (product_name, category_id, image_url, description) VALUES
('Meierismør 500g TINE', 1, 'static/images/tine_meierismor.jpg', 'TINE Meierismør er kjernet av fersk fløte.'),
('Kjøttdeig 400g Gilde', 2, 'static/images/gilde_kjottdeig.jpg', 'Gilde Kjøttdeig er laget av norsk storfekjøtt.'),
('Karbonader 2x100g Meny', 3, 'static/images/meny_karbonader.jpg', 'Meny Karbonader er laget av norsk storfekjøtt.'),
('Freia Melkesjokolade 200g', 4, 'static/images/freia_melkesjokolade.jpg', 'Ren Melkesjokolade av beste kvalitet fra Freia Melkejsokolade. Norges mest solgte sjokolade.'),
('Favorittsalami 150g Gilde', 5, 'static/images/favorittsalami_gilde.jpg', 'Gilde Favorittsalami er en saftig og smakfull salami.'),
('Mentos Fruktrull 40g', 6, 'static/images/mentos_fruktrull.png', 'Mentos drops med fruktsmak.');

INSERT INTO stores (store_name) VALUES
('Rema 1000'),
('KIWI'),
('Coop Extra'),
('Meny'),
('Joker'),
('SPAR'),
('Europris'),
('Bunnpris');

INSERT INTO prices (product_id, store_id, price) VALUES
(1, 1, 22), (1, 2, 23), (1, 3, 24),
(3, 1, 39), (3, 2, 37), (3, 3, 41),
(4, 1, 32), (4, 2, 30), (4, 3, 33),
(5, 1, 119), (5, 2, 125), (6, 1, 49),
(6, 3, 53);

INSERT INTO price_history (product_id, store_id, price, date) VALUES
(1, 1, 24.00, '2026-02-20'),
(1, 1, 23.00, '2026-02-21'),
(1, 1, 22.00, '2026-02-23'),

(3, 2, 39.00, '2026-02-18'),
(3, 2, 37.00, '2026-02-23'),

(4, 2, 31.00, '2026-02-22'),
(4, 2, 30.00, '2026-02-23'),

(5, 1, 129.00, '2026-02-20'),
(5, 1, 119.00, '2026-02-23'),

(6, 1, 55.00, '2026-02-21'),
(6, 1, 49.00, '2026-02-23');

INSERT INTO wishlist (user_id, wishlist_name) VALUES
(1, 'Admin test-liste'),
(2, 'Handleliste helg'),
(2, 'Fredagstaco'),
(3, 'Sunnere alternativer'),
(1, 'Studentbudsjett'),
(2, 'Protein');

INSERT INTO wishlist_items (wishlist_id, product_id) VALUES
(1, 1),
(1, 3),
(2, 4),
(2, 5),
(3, 2),
(4, 3),
(4, 4),
(5, 6),
(6, 6),
(6, 4);

INSERT INTO allergens (allergen_name) VALUES
('Melk'),
('Gluten'),
('Soya'),
('Egg'),
('Fisk'),
('Peanøtter'),
('Sesam'),
('Skalldyr');

INSERT INTO product_allergens (product_id, allergen_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 1),
(5, 2);