CREATE TABLE "Users" (
  "user_id" SERIAL UNIQUE PRIMARY KEY,
  "first_name" string,
  "last_name" string,
  "created_at" timestamp,
  "country_code" int,
  "region_code" int,
  "state_code" int,
  "province_code" int,
  "city_code" int,
  "auth_id" int NOT NULL,
  "email" varchar,
  "gender_id" int NOT NULL,
  "details" string,
  "confirmation_code" string NOT NULL,
  "confirmation_time" timestamp,
  "genres_liked_id" int
);

CREATE TABLE "Authentication" (
  "auth_id" int UNIQUE PRIMARY KEY,
  "username" string NOT NULL,
  "password_hash" string NOT NULL,
  "password_salt" string NOT NULL,
  "created_at" timestamp NOT NULL,
  "city_id" int
);

CREATE TABLE "Country" (
  "id" int UNIQUE PRIMARY KEY,
  "name" string NOT NULL,
  "city_id" int,
  "region_id" int,
  "state_id" int,
  "province_id" int
);

CREATE TABLE "City" (
  "id" int UNIQUE PRIMARY KEY,
  "name" string NOT NULL
);

CREATE TABLE "Region" (
  "id" int UNIQUE PRIMARY KEY,
  "name" string NOT NULL
);

CREATE TABLE "State" (
  "id" int UNIQUE PRIMARY KEY,
  "name" string NOT NULL
);

CREATE TABLE "Province" (
  "id" int UNIQUE PRIMARY KEY,
  "name" string NOT NULL
);

CREATE TABLE "Movies" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" string,
  "API_used" string NOT NULL,
  "API_id" string NOT NULL
);

CREATE TABLE "TV_Shows" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" string,
  "API_used" string NOT NULL,
  "API_id" string NOT NULL
);

CREATE TABLE "Queue" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "movie_id" int,
  "tv_show_id" int
);

CREATE TABLE "User_Photos" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "image" image,
  "user_id" int NOT NULL
);

CREATE TABLE "Genres" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" string NOT NULL,
  "details" string
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

ALTER TABLE "Users" ADD FOREIGN KEY ("genres_liked_id") REFERENCES "Genres" ("id");

ALTER TABLE "Authentication" ADD FOREIGN KEY ("auth_id") REFERENCES "Users" ("auth_id");

ALTER TABLE "Authentication" ADD FOREIGN KEY ("city_id") REFERENCES "City" ("id");

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
