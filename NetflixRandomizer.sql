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
  "auth_id" int NOT NULL,
  "email" varchar,
  "gender_id" int NOT NULL,
  "details" text,
  "confirmation_cod" text NOT NULL,
  "confirmation_time" timestamp,
  "genres_liked_id" int
);

CREATE TABLE "Authentication" (
  "auth_id" int UNIQUE PRIMARY KEY,
  "username" text NOT NULL,
  "password" text NOT NULL,
  "created_at" timestamp NOT NULL,
  "city_id" int
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
  "movie_id" SERIAL PRIMARY KEY NOT NULL,
  "name" text,
  "details" text,
  "date_released" date,
  "runtime" int
);

CREATE TABLE "TV_Shows" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text,
  "details" text,
  "date_released" date,
  "runtime_total" int,
  "num_of_episodes" int
);

CREATE TABLE "Recommendation" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "user_id" int,
  "movie_id" int,
  "tv_show_id" int,
  "watched" boolean DEFAULT false,
  "liked" boolean DEFAULT null,
  "date_liked" timestamp
);

CREATE TABLE "User_Photos" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "image" image,
  "user_id" int NOT NULL
);

CREATE TABLE "User_Social_Networks" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "social_network_id" int NOT NULL,
  "user_id" int NOT NULL
);

CREATE TABLE "Social_Networks" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text NOT NULL,
  "url" text NOT NULL,
  "details" text
);

CREATE TABLE "Genres" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" text NOT NULL,
  "details" text
);

CREATE TABLE "User_Movies_Watched" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "movie_id" int
);

CREATE TABLE "User_TVShows_Watched" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int NOT NULL,
  "tv_show_id" int
);

ALTER TABLE "Users" ADD FOREIGN KEY ("genres_liked_id") REFERENCES "Genres" ("id");

ALTER TABLE "Authentication" ADD FOREIGN KEY ("auth_id") REFERENCES "Users" ("auth_id");

ALTER TABLE "Authentication" ADD FOREIGN KEY ("city_id") REFERENCES "City" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("city_id") REFERENCES "City" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("region_id") REFERENCES "Region" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("state_id") REFERENCES "State" ("id");

ALTER TABLE "Country" ADD FOREIGN KEY ("province_id") REFERENCES "Province" ("id");

ALTER TABLE "Recommendation" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "Recommendation" ADD FOREIGN KEY ("movie_id") REFERENCES "Movies" ("movie_id");

ALTER TABLE "Recommendation" ADD FOREIGN KEY ("tv_show_id") REFERENCES "TV_Shows" ("id");

ALTER TABLE "User_Photos" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "User_Social_Networks" ADD FOREIGN KEY ("social_network_id") REFERENCES "Social_Networks" ("id");

ALTER TABLE "User_Social_Networks" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "User_Movies_Watched" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "User_Movies_Watched" ADD FOREIGN KEY ("movie_id") REFERENCES "Movies" ("movie_id");

ALTER TABLE "User_TVShows_Watched" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("user_id");

ALTER TABLE "User_TVShows_Watched" ADD FOREIGN KEY ("tv_show_id") REFERENCES "TV_Shows" ("id");

COMMENT ON COLUMN "Authentication"."created_at" IS 'when pasword and username created';
