CREATE TABLE "Users" (
  "user_id" SERIAL UNIQUE PRIMARY KEY,
  "first_name" text,
  "last_name" text,
  "created_at" timestamp,
  "country_code" int,
  "region_code" int,
  "state_code" int,
  "province_code" int,
  "city_code" int,
  "email" varchar,
  "gender_id" int NOT NULL,
  "details" text,
  "confirmation_code" text NOT NULL,
  "confirmation_time" timestamp,
  "genres_liked_id" int
);

CREATE TABLE "Authentication" (
  "auth_id" int UNIQUE PRIMARY KEY,
  "username" text NOT NULL,
  "password_hash" text NOT NULL,
  "password_salt" text NOT NULL,
  "created_at" timestamp NOT NULL,
  "user_id" int
);

CREATE TABLE "Country" (
  "id" int UNIQUE PRIMARY KEY,
  "name" text NOT NULL,
  "city_id" int,
  "region_id" int,
  "state_id" int,
  "province_id" int
);

CREATE TABLE "City" (
  "id" int UNIQUE PRIMARY KEY,
  "name" text NOT NULL
);

CREATE TABLE "Region" (
  "id" int UNIQUE PRIMARY KEY,
  "name" text NOT NULL
);

CREATE TABLE "State" (
  "id" int UNIQUE PRIMARY KEY,
  "name" text NOT NULL
);

CREATE TABLE "Province" (
  "id" int UNIQUE PRIMARY KEY,
  "name" text NOT NULL
);

CREATE TABLE "Movies" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text,
  "API_used" text NOT NULL,
  "API_id" text NOT NULL
);

CREATE TABLE "TV_Shows" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text,
  "API_used" text NOT NULL,
  "API_id" text NOT NULL
);

CREATE TABLE "Queue" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "movie_id" int,
  "tv_show_id" int
);

CREATE TABLE "User_Photos" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "image" bytea,
  "user_id" int NOT NULL
);

CREATE TABLE "Genres" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text NOT NULL,
  "details" text
);

CREATE TABLE "Friends" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "friend_user_id" int NOT NULL,
  "date_start" date NOT NULL
);

CREATE TABLE "Likes" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "user_id" int,
  "liked" boolean,
  "watched" boolean,
  "movie_id" int,
  "tv_show_id" int,
  "date_liked" timestamp NOT NULL
);

ALTER TABLE "Country" ADD FOREIGN KEY ("id") REFERENCES "Users" ("country_code");

ALTER TABLE "Region" ADD FOREIGN KEY ("id") REFERENCES "Users" ("region_code");

ALTER TABLE "State" ADD FOREIGN KEY ("id") REFERENCES "Users" ("state_code");

ALTER TABLE "Province" ADD FOREIGN KEY ("id") REFERENCES "Users" ("province_code");

ALTER TABLE "Users" ADD FOREIGN KEY ("genres_liked_id") REFERENCES "Genres" ("id");

ALTER TABLE "Authentication" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Country" ADD FOREIGN KEY ("city_id") REFERENCES "City" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("region_id") REFERENCES "Region" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("state_id") REFERENCES "State" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("province_id") REFERENCES "Province" ("id");

ALTER TABLE "Queue" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Queue" ADD FOREIGN KEY ("movie_id") REFERENCES "Movies" ("id");

ALTER TABLE "Queue" ADD FOREIGN KEY ("tv_show_id") REFERENCES "TV_Shows" ("id");

ALTER TABLE "User_Photos" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Friends" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Friends" ADD FOREIGN KEY ("friend_user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Likes" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Likes" ADD FOREIGN KEY ("movie_id") REFERENCES "Movies" ("id");

ALTER TABLE "Likes" ADD FOREIGN KEY ("tv_show_id") REFERENCES "TV_Shows" ("id");

COMMENT ON COLUMN "Authentication"."created_at" IS 'when pasword and username created';
