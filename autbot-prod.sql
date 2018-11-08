--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4
-- Dumped by pg_dump version 10.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: tb_admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_admins (
    discord_id bigint NOT NULL,
    server_id bigint NOT NULL,
    username text NOT NULL
);


ALTER TABLE public.tb_admins OWNER TO postgres;

--
-- Name: tb_commands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_commands (
    trigger text NOT NULL,
    response text NOT NULL,
    count bigint NOT NULL,
    server_id bigint NOT NULL,
    author_id bigint DEFAULT 0
);


ALTER TABLE public.tb_commands OWNER TO postgres;

--
-- Name: tb_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_roles (
    target_role_id bigint NOT NULL,
    server_id bigint NOT NULL,
    required_role_id bigint
);


ALTER TABLE public.tb_roles OWNER TO postgres;

--
-- Name: tb_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_settings (
    server_id bigint NOT NULL,
    json_blob text NOT NULL
);


ALTER TABLE public.tb_settings OWNER TO postgres;

--
-- Name: tb_users; Type: TABLE; Schema: public; Owner: autbot
--

CREATE TABLE public.tb_users (
    user_id integer NOT NULL,
    discord_id character varying(50),
    aut_score integer,
    norm_score integer,
    nice_score integer,
    toxic_score integer,
    awareness_score integer
);


ALTER TABLE public.tb_users OWNER TO autbot;

-- johny big gay

CREATE TABLE public.tb_active_listeners (
    caller_message_id character varying(20),
    target_message_id character varying(20)
);

ALTER TABLE public.tb_active_listeners OWNER TO autbot;

--
-- Name: tb_users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: autbot
--

CREATE SEQUENCE public.tb_users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tb_users_user_id_seq OWNER TO autbot;

--
-- Name: tb_users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autbot
--

ALTER SEQUENCE public.tb_users_user_id_seq OWNED BY public.tb_users.user_id;


--
-- Name: tb_users user_id; Type: DEFAULT; Schema: public; Owner: autbot
--

ALTER TABLE ONLY public.tb_users ALTER COLUMN user_id SET DEFAULT nextval('public.tb_users_user_id_seq'::regclass);


--
-- Data for Name: tb_admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_admins (discord_id, server_id, username) FROM stdin;
471864040998699011	436189230390050826	ghost
\.


--
-- Data for Name: tb_commands; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_commands (trigger, response, count, server_id, author_id) FROM stdin;
436189230390050826help	hello	3	436189230390050826	214037134477230080
436189230390050826hi	test	0	436189230390050826	214037134477230080
hi	hi	3	436189230390050826	0
johnyjohnyisbetterthanmember	):]	0	436189230390050826	0
436189230390050826hello*this*isatest	hello	2	436189230390050826	0
test	[:smile:]	1	436189230390050826	0
johny	johny is better than [member][:grinning_face_with_smiling_eyes:]	1	436189230390050826	0
436189230390050826Hello	hiiiiiiiiii	1	436189230390050826	0
436189230390050826hellothissnatohueisatest	remove	0	436189230390050826	0
436189230390050826owl	[:owl:][owl] is bad	1	436189230390050826	0
436189230390050826hellothis*isatest	this [capture] is a test?	6	436189230390050826	0
436189230390050826santoheusntoahusntoahuoau*asohusoatuhoanuehoantuheou*euaoeuoauaouoau	natoehusntoahuesnautoaheu	0	436189230390050826	0
436189230390050826chris	[member] is [sleepwalken, a [adj] bot] [test, hello]	11	436189230390050826	0
436189230390050826snathueo	sntahoue	0	436189230390050826	0
436189230390050826saonthuou	sanothuoauenth	0	436189230390050826	0
436189230390050826aou	aoue	0	436189230390050826	0
436189230390050826asonuth	asonetuh	1	436189230390050826	0
436189230390050826test	[:shrug:]	1	436189230390050826	0
436189230390050826shrug	[:person_shrugging:]	1	436189230390050826	0
436189230390050826urabot	no u	3	436189230390050826	0
436189230390050826ura*	[capture] more like idiot	5	436189230390050826	0
\.


--
-- Data for Name: tb_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_roles (target_role_id, server_id, required_role_id) FROM stdin;
\.


--
-- Data for Name: tb_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_settings (server_id, json_blob) FROM stdin;
470626250046832640	{"admins": ["214037134477230080"], "bot_commands": []}
477356784982556675	{"admins": ["214037134477230080"], "bot_commands": []}
436189230390050826	{"admins": ["214037134477230080"], "default_role": "436189456962289674", "bot_commands": ["436189230390050830"], "aut_emoji": "<:pech:450372220611461121>", "edit_emoji": "\\ud83d\\udcdd"}
113121129882783744	{"admins": ["214037134477230080"], "bot_commands": []}
146017081593167872	{"admins": ["214037134477230080"], "bot_commands": []}
218757502773231616	{"admins": ["214037134477230080"], "bot_commands": []}
278226556923674624	{"admins": ["214037134477230080"], "bot_commands": []}
345955252987494400	{"admins": ["214037134477230080"], "bot_commands": []}
416020909531594752	{"admins": ["214037134477230080"], "bot_commands": []}
463772890886701058	{"admins": ["214037134477230080"], "bot_commands": []}
470461719127392257	{"admins": ["214037134477230080"], "bot_commands": []}
\.


--
-- Data for Name: tb_users; Type: TABLE DATA; Schema: public; Owner: autbot
--

COPY public.tb_users (user_id, discord_id, aut_score, norm_score, nice_score, toxic_score, awareness_score) FROM stdin;
4	186304444378382336	2	2	2	2	0
5	124733533661954050	2	4	2	2	0
12	131776062739841024	2	2	2	2	0
13	179636744818262016	2	2	2	2	0
7	189528269547110400	2	2	2	2	0
14	131857650676793345	2	2	2	2	0
9	130959008587710464	3	2	2	2	0
15	97544912039342080	2	2	2	2	0
11	245298512755949569	2	2	2	5	0
17	131294120399470602	14	2	2	9	0
16	103027947786473472	2	2	2	2	0
2	218157264333307905	2	2	2	2	0
18	95674839217475584	2	2	2	5	0
1	168722115447488512	12	7	2	4	0
10	250802771068977153	3	2	2	4	0
6	178700066091958273	6	2	7	9	0
19	142750185380904960	2	2	2	4	0
20	74646589213257728	2	2	2	2	0
8	257260785258987530	2	2	2	2	0
3	214037134477230080	6	2	2	9	3
\.


--
-- Name: tb_users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: autbot
--

SELECT pg_catalog.setval('public.tb_users_user_id_seq', 20, true);


--
-- Name: tb_admins tb_admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_admins
    ADD CONSTRAINT tb_admins_pkey PRIMARY KEY (discord_id);


--
-- Name: tb_commands tb_commands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_commands
    ADD CONSTRAINT tb_commands_pkey PRIMARY KEY (trigger);


--
-- Name: tb_roles tb_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_roles
    ADD CONSTRAINT tb_roles_pkey PRIMARY KEY (target_role_id);


--
-- Name: tb_settings tb_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_settings
    ADD CONSTRAINT tb_settings_pkey PRIMARY KEY (server_id);


--
-- Name: tb_users tb_users_pkey; Type: CONSTRAINT; Schema: public; Owner: autbot
--

ALTER TABLE ONLY public.tb_users
    ADD CONSTRAINT tb_users_pkey PRIMARY KEY (user_id);


--
-- Name: TABLE tb_admins; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tb_admins TO autbot;


--
-- Name: TABLE tb_commands; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tb_commands TO autbot;


--
-- Name: TABLE tb_roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tb_roles TO autbot;


--
-- Name: TABLE tb_settings; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tb_settings TO autbot;


--
-- Name: TABLE tb_users; Type: ACL; Schema: public; Owner: autbot
--

GRANT ALL ON TABLE public.tb_users TO autbot;


--
-- PostgreSQL database dump complete
--

