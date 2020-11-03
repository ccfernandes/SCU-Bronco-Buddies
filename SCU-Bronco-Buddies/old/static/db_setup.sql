CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` tinytext NOT NULL,
  `password` tinytext NOT NULL,
  `cookie` tinytext NOT NULL,
  `ip` tinytext NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` tinytext NOT NULL,
  `posts` int(11) NOT NULL
);

CREATE TABLE `forums` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `threads` int(11) NOT NULL
);

CREATE TABLE `threads` (
  `id` int(11) NOT NULL,
  `forum_id` int(11) NOT NULL,
  `poster` text NOT NULL,
  `poster_id` int(11) NOT NULL,
  `title` text NOT NULL,
  `body` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `replies` (
  `id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  `poster` text NOT NULL,
  `poster_id` int(11) NOT NULL,
  `body` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);