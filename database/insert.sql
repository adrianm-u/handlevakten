USE handlevaktenDB;


INSERT INTO users (email, first_name, last_name, account_type) VALUES
('admin@handlevakten.no', 'Admin', 'Bruker', 'admin'),
('karl@epost.no', 'Karl', 'Knutsen', 'user'),
('celina@epost.no', 'Celina', 'Oftedal', 'user'),
('ragnar@epost.no', 'Ragnar', 'Olsen', 'user'),
('kenneth@epost.no', 'Kenneth', 'Pedersen', 'user');

INSERT INTO categories (category_name) VALUES
('Meieri'),
('Brød'),
('Drikke'),
('Snacks'),
('Kjøtt'),
('Fisk');

INSERT INTO products (product_name, category_id) VALUES
('Melk 1L', 1),
('Yoghurt 500g', 1),
('Grovbrød', 2),
('Coca Cola 1.5L', 3),
('Maarud Potetgull Salt 240g', 4),
('Gilde Kjøttdeig 400g', 5),
('Laks Porsjoner u/Skinn 4x125g Lerøy', 6),
('Sliders Mini Brioche 480g', 2);

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
(7, 1, 119), (7, 2, 125), (8, 1, 49),
(8, 3, 53);

INSERT INTO price_history (product_id, store_id, price, date) VALUES
(1, 1, 24.00, '2026-02-20'),
(1, 1, 23.00, '2026-02-21'),
(1, 1, 22.00, '2026-02-23'),

(3, 2, 39.00, '2026-02-18'),
(3, 2, 37.00, '2026-02-23'),

(4, 2, 31.00, '2026-02-22'),
(4, 2, 30.00, '2026-02-23'),

(7, 1, 129.00, '2026-02-20'),
(7, 1, 119.00, '2026-02-23'),

(8, 1, 55.00, '2026-02-21'),
(8, 1, 49.00, '2026-02-23');

INSERT INTO wishlist (user_id, wishlist_name) VALUES
(1, 'Admin test-liste'),
(2, 'Handleliste helg'),
(2, 'Fredagstaco'),
(3, 'Sunnere alternativer'),
(4, 'Studentbudsjett'),
(5, 'Protein');

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
(6, 7);

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
(7, 5),
(8, 2);