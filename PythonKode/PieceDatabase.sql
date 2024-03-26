
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

CREATE TABLE pieces (
    `pieceId` int,
    `pieceName` varchar(20),
    `north` int,
    `east` int,
    `south` int,
    `west` int,
    `artPath` varchar(30),
    `effektId` int,

)

COMMIT;

