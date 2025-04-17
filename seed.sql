-- qr_app_db.users definition

CREATE TABLE `users` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('USER','ADMIN') NOT NULL DEFAULT 'USER',
  `disabled` boolean NOT NULL DEFAULT false,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `IDX_97672ac88
  
  f789774dd47f7c8be` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO qr_app_db.users (id,name,email,password,`role`,created_at,updated_at) VALUES ('e070fd81-5b33-4f87-9504-474fb6e1471b','Ken Lee','john.doe@example.com','$2b$10$i9Pa4lXlIw.FMyX7go2/cew2Zel/epXdWXz.eXFJRKMpj.tmD6xPS','USER','2025-04-14 18:05:33.513000','2025-04-14 18:05:33.513000');
INSERT INTO qr_app_db.users (id,name,email,password,`role`,created_at,updated_at) VALUES ('e070fd81-5b33-4f87-9504-474fb6e1471c','Admin','admin@admin.com','$2b$10$i9Pa4lXlIw.FMyX7go2/cew2Zel/epXdWXz.eXFJRKMpj.tmD6xPS','ADMIN','2025-04-14 18:05:33.513000','2025-04-14 18:05:33.513000');


CREATE TABLE `qr` (
  `id` varchar(36) NOT NULL,
  `path` text NOT NULL,
  `data` text NOT NULL,
  `source` varchar(100) NOT NULL,
  `disabled` boolean NOT NULL DEFAULT FALSE,
  `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `user_id` varchar(36) NOT NULL,
  key `fk_qr_user` (`user_id`),
  CONSTRAINT `fk_qr_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  PRIMARY KEY (`id`)
 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO qr_app_db.qr (id,`path`,`data`,disabled,created_at,updated_at,user_id) VALUES
	 ('e079fd81-5b33-4f87-9504-474fb6e1471b','PATH','DATA',0,'2025-04-16 16:18:08.546739','2025-04-16 16:49:26.361552','e070fd81-5b33-4f87-9504-474fb6e1471b');
