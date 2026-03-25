-- CreateTable
CREATE TABLE `membership` (
    `email` VARCHAR(255) NOT NULL,
    `activation_code` VARCHAR(100) NOT NULL,
    `start_date` DATE NOT NULL,
    `end_date` DATE NOT NULL,
    `duration_days` INTEGER NOT NULL,

    PRIMARY KEY (`email`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `notebooks` (
    `notebook_name` VARCHAR(255) NOT NULL,
    `notebook_id` VARCHAR(255) NOT NULL,
    `uid` VARCHAR(255) NOT NULL,
    `created_time` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    INDEX `notebooks_uid_fkey`(`uid`),
    PRIMARY KEY (`notebook_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `questions` (
    `question_id` VARCHAR(255) NOT NULL,
    `time_created` TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `question` VARCHAR(191) NOT NULL,
    `answer` VARCHAR(191) NULL,
    `user_id` VARCHAR(255) NOT NULL,
    `sources` JSON NULL,
    `notebook_id` VARCHAR(191) NULL,
    `youtube` VARCHAR(191) NULL,

    INDEX `questions_notebook_id_fkey`(`notebook_id`),
    INDEX `questions_user_id_fkey`(`user_id`),
    PRIMARY KEY (`question_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `users` (
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `phone` VARCHAR(20) NULL,
    `hashed_password` VARCHAR(255) NULL,
    `college` VARCHAR(255) NULL,
    `sem` INTEGER NULL,
    `branch` VARCHAR(255) NULL,
    `passing_year` INTEGER NULL,
    `uid` VARCHAR(255) NOT NULL,
    `paid` BOOLEAN NOT NULL DEFAULT false,
    `usn` VARCHAR(255) NOT NULL,

    UNIQUE INDEX `users_email_key`(`email`),
    UNIQUE INDEX `users_usn_key`(`usn`),
    PRIMARY KEY (`uid`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `notebooks` ADD CONSTRAINT `notebooks_uid_fkey` FOREIGN KEY (`uid`) REFERENCES `users`(`uid`) ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE `questions` ADD CONSTRAINT `questions_notebook_id_fkey` FOREIGN KEY (`notebook_id`) REFERENCES `notebooks`(`notebook_id`) ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE `questions` ADD CONSTRAINT `questions_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users`(`uid`) ON DELETE CASCADE ON UPDATE NO ACTION;
