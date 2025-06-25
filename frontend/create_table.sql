-- SQL script to create contacts table in Supabase
CREATE TABLE IF NOT EXISTS contacts (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  company VARCHAR(255),
  message TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Add RLS (Row Level Security) policy to allow insertions
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows anonymous inserts
CREATE POLICY "Allow anonymous inserts" ON contacts
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Create a policy that allows authenticated users to view all
CREATE POLICY "Allow authenticated select" ON contacts
  FOR SELECT
  TO authenticated
  USING (true);