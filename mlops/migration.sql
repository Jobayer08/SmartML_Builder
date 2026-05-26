-- Migration script to add missing columns for multi-user SaaS support

-- Add user_id and file_path to models table
ALTER TABLE models ADD COLUMN IF NOT EXISTS file_path TEXT;
ALTER TABLE models ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE models ADD CONSTRAINT IF NOT EXISTS fk_models_user_id FOREIGN KEY (user_id) REFERENCES users(id);

-- Add user_id to predictions table
ALTER TABLE predictions ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE predictions ADD CONSTRAINT IF NOT EXISTS fk_predictions_user_id FOREIGN KEY (user_id) REFERENCES users(id);

-- Add user_id to api_usage table if it exists
DO $$ 
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'api_usage') THEN
    ALTER TABLE api_usage ADD COLUMN IF NOT EXISTS user_id INTEGER;
    ALTER TABLE api_usage ADD CONSTRAINT IF NOT EXISTS fk_api_usage_user_id FOREIGN KEY (user_id) REFERENCES users(id);
  END IF;
END $$;

-- Update existing records to have user_id = 1 (default admin/first user)
UPDATE models SET user_id = COALESCE(user_id, 1) WHERE user_id IS NULL;
UPDATE predictions SET user_id = COALESCE(user_id, 1) WHERE user_id IS NULL;
UPDATE api_usage SET user_id = COALESCE(user_id, 1) WHERE user_id IS NULL;

-- Make user_id NOT NULL after updating
ALTER TABLE models ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE predictions ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE api_usage ALTER COLUMN user_id SET NOT NULL;
