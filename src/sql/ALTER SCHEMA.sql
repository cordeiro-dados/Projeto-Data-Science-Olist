select default_character_set_name from information_schema.SCHEMATA S where schema_name = 'olist';

ALTER DATABASE `olist` CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_unicode_ci;