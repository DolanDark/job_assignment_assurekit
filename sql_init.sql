CREATE EXTENSION pgcrypto;

CREATE TABLE public.assurekit_users (
  userid character varying(250) PRIMARY KEY,
  username character varying(250) NOT NULL,
  email character varying(100) NOT NULL,
  isadmin boolean NOT NULL,
  );
