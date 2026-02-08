/* ============================================================
   CRICSHEET MATCH DATA ANALYSIS – SQL QUERIES
   Database : cricsheet_db
   ============================================================ */


/* 1. Total Matches by Format */

SELECT 
    match_type,
    COUNT(*) AS total_matches
FROM matches
GROUP BY match_type
ORDER BY total_matches DESC;



/* 2. Toss Decision Distribution */

SELECT 
    toss_decision,
    COUNT(*) AS decision_count
FROM matches
GROUP BY toss_decision;



/* 3. Matches Won by Each Team */

SELECT 
    winner,
    COUNT(*) AS matches_won
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY matches_won DESC
LIMIT 10;



/* 4. Top 10 Venues by Number of Matches */

SELECT 
    venue,
    COUNT(*) AS total_matches
FROM matches
GROUP BY venue
ORDER BY total_matches DESC
LIMIT 10;



/* 5. Total Runs Scored in Dataset */

SELECT 
    SUM(runs_batsman) AS total_runs
FROM deliveries;



/* 6. Total Wickets Taken */

SELECT 
    COUNT(*) AS total_wickets
FROM deliveries
WHERE wicket = 1;



/* 7. Top 10 Batsmen by Total Runs */

SELECT 
    batsman,
    SUM(runs_batsman) AS total_runs
FROM deliveries
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;



/* 8. Top 10 Bowlers by Wickets */

SELECT 
    bowler,
    COUNT(*) AS wickets_taken
FROM deliveries
WHERE wicket = 1
GROUP BY bowler
ORDER BY wickets_taken DESC
LIMIT 10;



/* 9. Strike Rate of Batsmen (Min 500 Runs) */

SELECT 
    batsman,
    SUM(runs_batsman) AS total_runs,
    COUNT(ball) AS balls_faced,
    ROUND((SUM(runs_batsman) / COUNT(ball)) * 100, 2) AS strike_rate
FROM deliveries
GROUP BY batsman
HAVING total_runs >= 500
ORDER BY strike_rate DESC
LIMIT 10;



/* 10. Economy Rate of Bowlers (Min 300 Balls) */

SELECT 
    bowler,
    SUM(runs_total) AS runs_conceded,
    COUNT(ball) AS balls_bowled,
    ROUND((SUM(runs_total) / COUNT(ball)) * 6, 2) AS economy_rate
FROM deliveries
GROUP BY bowler
HAVING balls_bowled >= 300
ORDER BY economy_rate ASC
LIMIT 10;



/* 11. Matches Played in Each City */

SELECT 
    city,
    COUNT(*) AS total_matches
FROM matches
GROUP BY city
ORDER BY total_matches DESC
LIMIT 10;



/* 12. Win Margin Type Distribution */

SELECT 
    win_margin,
    COUNT(*) AS occurrences
FROM matches
GROUP BY win_margin;



/* 13. Number of Unique Teams */

SELECT 
    COUNT(DISTINCT team1) AS total_teams
FROM matches;



/* 14. Matches Won Batting vs Fielding First */

SELECT 
    toss_decision,
    COUNT(*) AS wins
FROM matches
WHERE toss_winner = winner
GROUP BY toss_decision;



/* 15. Total Deliveries Bowled */

SELECT 
    COUNT(*) AS total_deliveries
FROM deliveries;



/* ============================================================
   END OF ANALYSIS QUERIES
   ============================================================ */
