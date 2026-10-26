use burguer;

insert into comidas (id, nombre, tiempo_preparacion, tiempo_coccion) values
	(2, 'Cheese Burguer', '00:01:30', '00:04:00'),
	(3, 'Clasica Burguer', '00:01:30', '00:04:00'),
	(4, 'Bel Burguer', '00:01:30', '00:04:00'),
	(5, 'Fer Lomito', '00:01:30', '00:04:00'),
	(6, 'Isais Burguer', '00:01:30', '00:04:00'),
	(7, 'Kento Burguer', '00:01:30', '00:04:00');

insert into pedidos (id, fecha_pedido) values
	(3, '2026-10-15 14:28:59'),
	(4, '2026-10-15 14:31:03'),
	(5, '2026-10-16 15:08:10'),
	(6, '2026-10-16 15:11:48'),
	(7, '2026-10-16 15:22:25'),
	(8, '2026-10-16 19:34:21');

insert into pedidos_detalles (id, id_pedido, id_comida, cantidad) values
	(1, 3, 2, 1),
	(2, 4, 2, 3),
	(3, 4, 3, 1),
	(4, 5, 2, 4),
	(5, 5, 4, 5),
	(6, 6, 2, 2),
	(7, 6, 3, 1),
	(8, 6, 4, 2),
	(9, 6, 5, 1),
	(10, 6, 6, 1),
	(11, 6, 7, 1),
	(12, 7, 7, 1);

