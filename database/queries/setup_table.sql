CREATE TABLE IF NOT EXISTS players (
    PlayerID TEXT PRIMARY KEY,
    URL TEXT UNIQUE,
    Name TEXT,
    FullName TEXT,
    DateOfBirth TEXT,
    Age INTEGER,
    PlaceOfBirth TEXT,
    CountryOfBirth TEXT,
    Position TEXT,
    CurrentClub TEXT,
    NationalTeam TEXT,
    NumberOfAppearancesInTheCurrentClub INTEGER,
    GoalsInTheCurrentClub INTEGER,
    ScrapingTimestamp TEXT
);
