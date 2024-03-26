
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

CREATE TABLE pieces (
    `pieceId` varchar(2),
    `pieceName` varchar(20),
    `north` varchar,
    `east` varchar,
    `south` varchar,
    `west` varchar,
    `artPath` varchar(30),
    `effektId` varchar(2),

)

COMMIT;

