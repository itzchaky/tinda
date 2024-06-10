--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chats; Type: TABLE; Schema: public; Owner: mvq
--

CREATE TABLE public.chats (
    chatid integer NOT NULL,
    message text,
    "timestamp" timestamp without time zone,
    senderid integer,
    recipientid integer
);


ALTER TABLE public.chats OWNER TO mvq;

--
-- Name: chats_chatid_seq; Type: SEQUENCE; Schema: public; Owner: mvq
--

ALTER TABLE public.chats ALTER COLUMN chatid ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.chats_chatid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: matches; Type: TABLE; Schema: public; Owner: mvq
--

CREATE TABLE public.matches (
    matchid integer NOT NULL,
    matchdate date,
    active boolean,
    dislike boolean,
    matcher integer,
    matchee integer
);


ALTER TABLE public.matches OWNER TO mvq;

--
-- Name: matches_matchid_seq; Type: SEQUENCE; Schema: public; Owner: mvq
--

ALTER TABLE public.matches ALTER COLUMN matchid ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.matches_matchid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pictures; Type: TABLE; Schema: public; Owner: mvq
--

CREATE TABLE public.pictures (
    filename character varying(255) NOT NULL,
    userid integer NOT NULL
);


ALTER TABLE public.pictures OWNER TO mvq;

--
-- Name: users; Type: TABLE; Schema: public; Owner: mvq
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(20),
    description text,
    password character varying(255) NOT NULL,
    datebirth date,
    location character varying(255)
);


ALTER TABLE public.users OWNER TO mvq;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: mvq
--

ALTER TABLE public.users ALTER COLUMN userid ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_userid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: mvq
--

COPY public.chats (chatid, message, "timestamp", senderid, recipientid) FROM stdin;
22	hey	2024-06-09 18:36:09.144235	4	5
\.


--
-- Data for Name: matches; Type: TABLE DATA; Schema: public; Owner: mvq
--

COPY public.matches (matchid, matchdate, active, dislike, matcher, matchee) FROM stdin;
4	2024-06-08	t	f	4	5
5	2024-06-08	t	f	4	6
6	2024-06-08	t	f	5	6
10	2024-06-08	f	f	7	5
11	2024-06-08	f	f	7	6
9	2024-06-08	t	f	7	4
\.


--
-- Data for Name: pictures; Type: TABLE DATA; Schema: public; Owner: mvq
--

COPY public.pictures (filename, userid) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: mvq
--

COPY public.users (userid, email, name, description, password, datebirth, location) FROM stdin;
4	a@gmail.com	Andreas	hey	$2b$12$AL1aAG.9gjSAShbOTCGjHOAUJMIt8K5rGOWddtH8ntRrz/skSAZ9W	2024-06-21	Denmark
5	b@gmail.com	michaela	a	$2b$12$0gJv4T6eMSabJlY5MKPO8OX.CXjIXNcnxyIHFA94IWptQlTFxCTNG	2024-06-23	Denmark
6	c@gmail.com	Christian	1	$2b$12$eP4ztAlM/33tSq2qvhkKQOetdmKhHIc50O1UKBKQEkqZt6s/UvrLO	2024-05-29	Denmark
7	d@gmail.com	Rune	a	$2b$12$IiixjyJbB4dTMRTeZ9rrKOcCH/UJmoPr1XXzWRsYxZkZJ2hD.9oc.	2024-07-07	Denmark
\.


--
-- Name: chats_chatid_seq; Type: SEQUENCE SET; Schema: public; Owner: mvq
--

SELECT pg_catalog.setval('public.chats_chatid_seq', 22, true);


--
-- Name: matches_matchid_seq; Type: SEQUENCE SET; Schema: public; Owner: mvq
--

SELECT pg_catalog.setval('public.matches_matchid_seq', 11, true);


--
-- Name: users_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: mvq
--

SELECT pg_catalog.setval('public.users_userid_seq', 7, true);


--
-- Name: chats chats_pkey; Type: CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (chatid);


--
-- Name: matches matches_pkey; Type: CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (matchid);


--
-- Name: pictures pictures_pkey; Type: CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.pictures
    ADD CONSTRAINT pictures_pkey PRIMARY KEY (filename);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: chats chats_recipientid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_recipientid_fkey FOREIGN KEY (recipientid) REFERENCES public.users(userid);


--
-- Name: chats chats_senderid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_senderid_fkey FOREIGN KEY (senderid) REFERENCES public.users(userid);


--
-- Name: matches matches_matchee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_matchee_fkey FOREIGN KEY (matchee) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- Name: matches matches_matcher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.matches
    ADD CONSTRAINT matches_matcher_fkey FOREIGN KEY (matcher) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- Name: pictures pictures_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mvq
--

ALTER TABLE ONLY public.pictures
    ADD CONSTRAINT pictures_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

