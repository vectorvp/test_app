-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 25 2019 г., 23:07
-- Версия сервера: 10.4.10-MariaDB
-- Версия PHP: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `carsharing`
--

-- --------------------------------------------------------

--
-- Структура таблицы `cars`
--

CREATE TABLE `cars` (
  `id` int(30) NOT NULL,
  `model_ru` varchar(50) DEFAULT NULL,
  `model_eng` varchar(50) DEFAULT NULL,
  `c_year` varchar(4) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `cars`
--

INSERT INTO `cars` (`id`, `model_ru`, `model_eng`, `c_year`, `create_date`) VALUES
(3, 'опель', 'opel', '2014', '2019-12-25 19:20:49'),
(4, 'ниссан', 'nissan', '2010', '2019-12-25 19:21:01'),
(5, 'мазда', 'mazda', '2016', '2019-12-25 21:19:57'),
(6, 'лада', 'lada', '2018', '2019-12-25 21:24:53');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `lang` varchar(20) DEFAULT NULL,
  `pass` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `email`, `name`, `lang`, `pass`, `register_date`) VALUES
(1, 'ivan@mail.ru', 'Иван Иванов', 'ru', '$5$rounds=535000$QlQWkTuNa31mnMF2$5URhDz8d.BIS.B5nQiH0dEE5uRPyhOnoS0rJmGc8Or2', '2019-12-25 06:33:36'),
(2, 'ivan@mail.ru', 'Иван Иванов', 'ru', '$5$rounds=535000$QC1XZqNTZozqlXRZ$BECxP8CtdhlfmKFuworImJ9cNhAN7jADI/JftNpaxi3', '2019-12-25 06:38:25'),
(3, 'terh@mail.ru', 'jfk', 'eng', '$5$rounds=535000$HsH9o99hQo0hMk8Y$KHH2sl2g1Eflh.mWo69E6UxqJHOxxf4WtmL787F6iG7', '2019-12-25 06:40:06'),
(4, 'olga@mail.ru', 'Ольга', 'ru', '$5$rounds=535000$Jgz2TcNircARoU51$PFg6Du6sG4fYMpfy6GRKOoOV5Fcat6CPYiJtGX/T8m.', '2019-12-25 08:11:51'),
(5, 'sergey@mail.ru', 'Сергей Иванов', 'rus', '$5$rounds=535000$P3I.2FsE0lpk56Ji$EVKXF2MZivt624eJ5PAmPnshZQWB5oJl7RWjMKIHT.6', '2019-12-25 19:19:29');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
