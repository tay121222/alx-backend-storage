-- stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE avg_score DECIMAL(10, 2);

	SELECT AVG(score) INTO avg_score
	from corrections WHERE corrections.user_id = user_id;

	UPDATE users SET average_score = avg_score WHERE id = user_id;

END //
DELIMITER ;
