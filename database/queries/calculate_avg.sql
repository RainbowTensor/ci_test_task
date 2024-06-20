SELECT 
    CurrentClub,
    AVG(Age) AS AverageAge,
    AVG(NumberOfAppearancesInTheCurrentClub) AS AverageAppearances,
    COUNT(*) AS TotalPlayers
FROM players
WHERE NumberOfAppearancesInTheCurrentClub IS NOT NULL
GROUP BY CurrentClub;