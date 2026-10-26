create database if not exists burguer character set utf8mb4 collate utf8mb4_general_ci;
use burguer;

create table comidas (
	id int(10) unsigned not null auto_increment,
	nombre text not null,
	tiempo_preparacion time not null,
	tiempo_coccion time not null,
	primary key (id)
) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci;

create table pedidos (
	id int(11) unsigned not null auto_increment,
	fecha_pedido datetime not null default current_timestamp(),
	primary key (id)
) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci;

create table pedidos_detalles (
	id int(11) not null auto_increment,
	id_pedido int(11) not null,
	id_comida int(11) unsigned not null,
	cantidad int(10) unsigned not null default 1,
	primary key (id),
	key fk_detalle_comida (id_comida),
	constraint fk_detalle_comida foreign key (id_comida) references comidas (id)
) engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci;

