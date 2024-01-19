-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER //
DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
	INSERT INTO projects (name) VALUES (project_name)
	ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);

	INSERT INTO corrections (`user_id`, `project_id`, score)
	VALUES (user_id, LAST_INSERT_ID(),score);
END
//

DELIMITER ;
