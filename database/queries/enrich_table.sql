ALTER TABLE players
ADD COLUMN AgeCategory TEXT CHECK(AgeCategory IN ('Young', 'MidAge', 'Old'));

ALTER TABLE players
ADD COLUMN GoalsPerClubGame FLOAT;

UPDATE players
SET AgeCategory = CASE
    WHEN age <= 23 THEN 'Young'
    WHEN age BETWEEN 24 AND 32 THEN 'MidAge'
    WHEN age >= 33 THEN 'Old'
    ELSE NULL
END;