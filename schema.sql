-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS indeed_ads;
DROP TABLE IF EXISTS linkedin_ads;

PRAGMA foreign_keys=ON;

-- Create the tables

-- Table for the indeed-ads
CREATE TABLE indeed_ads (
    date            DATETIME DEFAULT (datetime('now','localtime')),
    title           TEXT,
    company         TEXT,
    location        TEXT,
    link            TEXT,
    PRIMARY KEY (title,company,location)
);

-- Table for the linkedin-ads
CREATE TABLE linkedin_ads (
    date            DATETIME DEFAULT (datetime('now','localtime')),
    title           TEXT,
    company         TEXT,
    location        TEXT,
    link            TEXT,
    PRIMARY KEY (title,company,location)
);
