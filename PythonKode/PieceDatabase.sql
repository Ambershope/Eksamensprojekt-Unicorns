
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

CREATE TABLE `pieces` (
    `pieceId` int,
    `pieceName` varchar(20),
    `north` int,
    `east` int,
    `south` int,
    `west` int,
    `artPath` varchar(30),
    `effektId` int,
)

INSERT INTO `pieces` 
(`pieceId`, `pieceName`, `north`, `east`, `south`, `west`, `artPath`, `effektId`) VALUES
(1, 'Fluttershy', 3, 1, 0, 1, 'Fluttershy_Main_Box', 0)

ALTER TABLE `pieces`
  ADD PRIMARY KEY (`pieceId`)

COMMIT;

