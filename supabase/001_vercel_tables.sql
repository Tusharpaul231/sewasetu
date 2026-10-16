CREATE TABLE IF NOT EXISTS sms_messages (
    id          SERIAL PRIMARY KEY,
    to_number   VARCHAR(15) NOT NULL,
    text        TEXT        NOT NULL,
    sent_at     TIMESTAMP   NOT NULL,
    deliver_at  TIMESTAMP   NOT NULL
);
CREATE INDEX IF NOT EXISTS sms_messages_to_idx ON sms_messages (to_number, id);

CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    mobile      VARCHAR(15) NOT NULL,
    filename    TEXT,
    content     BYTEA       NOT NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT now()
);

DO $$
DECLARE t text;
BEGIN
  FOR t IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);
  END LOOP;
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
    REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon, authenticated;
    REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon, authenticated;
  END IF;
END $$;