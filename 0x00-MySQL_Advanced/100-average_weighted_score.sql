--  SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_weighted_score FLOAT;

    SELECT AVG(c.score * p.weight)
    INTO avg_weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    UPDATE users
    SET average_score = IFNULL(avg_weighted_score, 0)
    WHERE id = user_id;
END //

DELIMITER ;
