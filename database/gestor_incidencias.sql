--
-- PostgreSQL database dump
--

\restrict gI7e1njib63pduEitS7gUCMm4FYQq9zmDdqJx0aVpcVvkNcYwttOizTS1FPMOSp

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-11-07 22:42:54

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 221 (class 1255 OID 16410)
-- Name: actualizar_fecha_incidencia(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.actualizar_fecha_incidencia() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.actualizar_fecha_incidencia() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16388)
-- Name: incidencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.incidencias (
    id bigint NOT NULL,
    titulo character varying(150) NOT NULL,
    descripcion text NOT NULL,
    prioridad character varying(10) DEFAULT 'Media'::character varying NOT NULL,
    estado character varying(20) DEFAULT 'Pendiente'::character varying NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_incidencias_descripcion_no_vacia CHECK ((length(TRIM(BOTH FROM descripcion)) > 0)),
    CONSTRAINT chk_incidencias_estado CHECK (((estado)::text = ANY ((ARRAY['Pendiente'::character varying, 'En proceso'::character varying, 'Resuelta'::character varying])::text[]))),
    CONSTRAINT chk_incidencias_prioridad CHECK (((prioridad)::text = ANY ((ARRAY['Baja'::character varying, 'Media'::character varying, 'Alta'::character varying])::text[]))),
    CONSTRAINT chk_incidencias_titulo_no_vacio CHECK ((length(TRIM(BOTH FROM titulo)) > 0))
);


ALTER TABLE public.incidencias OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16387)
-- Name: incidencias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.incidencias ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.incidencias_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4917 (class 0 OID 16388)
-- Dependencies: 220

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 219

--
-- TOC entry 4767 (class 2606 OID 16409)
-- Name: incidencias incidencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incidencias
    ADD CONSTRAINT incidencias_pkey PRIMARY KEY (id);


--
-- TOC entry 4764 (class 1259 OID 16412)
-- Name: idx_incidencias_estado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_incidencias_estado ON public.incidencias USING btree (estado);


--
-- TOC entry 4765 (class 1259 OID 16413)
-- Name: idx_incidencias_prioridad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_incidencias_prioridad ON public.incidencias USING btree (prioridad);


--
-- TOC entry 4768 (class 2620 OID 16411)
-- Name: incidencias trg_actualizar_fecha_incidencia; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_actualizar_fecha_incidencia BEFORE UPDATE ON public.incidencias FOR EACH ROW EXECUTE FUNCTION public.actualizar_fecha_incidencia();


-- Completed on 2026-11-07 22:42:55

--
-- PostgreSQL database dump complete
--

\unrestrict gI7e1njib63pduEitS7gUCMm4FYQq9zmDdqJx0aVpcVvkNcYwttOizTS1FPMOSp

