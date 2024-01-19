DELIMITER //

DROP TRIGGER IF EXISTS update_item_qty;
CREATE TRIGGER update_item_qty AFTER INSERT ON orders
FOR EACH ROW
BEGIN
UPDATE items SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
END;
//

DELIMITER ;
