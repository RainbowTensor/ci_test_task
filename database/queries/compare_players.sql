SELECT p1.Name, COUNT(*)
FROM players p1
    CROSS JOIN players p2
WHERE p1.CurrentClub = 'Liverpool'
    AND p1.Age > p2.Age
    AND p1.Position = p2.Position
    AND p1.NumberOfAppearancesInTheCurrentClub <  p2.NumberOfAppearancesInTheCurrentClub
GROUP BY p1.PlayerID;