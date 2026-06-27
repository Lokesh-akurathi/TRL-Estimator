CREATE DATABASE trl;

CREATE TABLE papers (
    -- ── Layer 1: Core (stable, relational) ──────────────────
    paper_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title                   TEXT NOT NULL,
    research_title          TEXT,
    authors                 TEXT[],                          -- array, multiple authors           
    abstract                TEXT,
    published_year          INT,
    venue                   TEXT,
    doi                     TEXT UNIQUE,
    language                TEXT,
    country_of_origin       TEXT,                            -- fixed casing from v1
    source                  TEXT,                            -- "upload", "arxiv", "crawl"
    paper_type              TEXT,                            -- "survey","empirical","theoretical","benchmark","thesis"
    page_count              INT,
    created_at              TIMESTAMP DEFAULT now(),
    updated_at              TIMESTAMP DEFAULT now(),
    trl_level               INT DEFAULT NULL,

    -- ── Versioning columns (on papers table) ────────────────
    metadata_schema_version TEXT DEFAULT '1.0',             
	----- TRL specific -----------
    trl_specific        	JSONB
);

-- ALTER TABLE papers
-- ADD CONSTRAINT chk_trl_specific
-- CHECK (
--     trl_specific IS NOT NULL
-- );

