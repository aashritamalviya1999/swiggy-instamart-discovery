-- Reviews Table (Raw & Cleaned Ingested Data)
CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    platform TEXT,
    author TEXT,
    raw_content TEXT,
    cleaned_content TEXT,
    rating INTEGER,
    created_at TIMESTAMP,
    url TEXT,
    language TEXT,
    primary_purchased_category TEXT,
    willing_to_try_new TEXT,
    new_categories_of_interest TEXT,
    barrier_reason TEXT,
    is_spam INTEGER DEFAULT 0
);

-- AI Analysis Table
CREATE TABLE IF NOT EXISTS analysis_results (
    review_id TEXT PRIMARY KEY,
    sentiment TEXT,
    summary TEXT,
    intent TEXT,
    barriers TEXT,                 -- JSON array of barrier strings
    motivations TEXT,              -- JSON array of motivation strings
    pain_points TEXT,              -- JSON array
    feature_requests TEXT,         -- JSON array
    shopping_behavior TEXT,        -- Routine Buyer, Experiment Seeker, etc.
    user_segment TEXT,
    detected_categories TEXT,      -- JSON array of categories
    FOREIGN KEY(review_id) REFERENCES reviews(id)
);

-- Clusters Table
CREATE TABLE IF NOT EXISTS clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subtheme TEXT,
    description TEXT,
    size INTEGER
);

-- Review-to-Cluster Map
CREATE TABLE IF NOT EXISTS review_clusters (
    review_id TEXT,
    cluster_id INTEGER,
    distance REAL,
    PRIMARY KEY(review_id, cluster_id),
    FOREIGN KEY(review_id) REFERENCES reviews(id),
    FOREIGN KEY(cluster_id) REFERENCES clusters(id)
);

-- Insights Table
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    confidence_score REAL,
    supporting_reviews_count INTEGER,
    supporting_quotes TEXT,        -- JSON array
    platforms TEXT,                -- JSON array
    contradicting_opinions TEXT,   -- JSON array
    confidence_explanation TEXT
);

-- Opportunities Table
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    problem TEXT,
    evidence TEXT,
    representative_quotes TEXT,    -- JSON array
    frequency TEXT,
    impact REAL,                   -- 1-10
    confidence REAL,               -- 1-10
    opportunity_score REAL,
    business_value TEXT
);
