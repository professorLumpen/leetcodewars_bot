Welcome to the repository of Leetcodewars bot.

In the prework_with_tags folder, preliminary work is performed, which consists of parsing tags from the Leetcode and Codewars sites.

Then comes the human work, which is to compare tags and difficulty levels with each other, which results in the all_tags file.

The file parse_all_tasks collects all tasks from both sites for each tag. Tasks are written to the task_db file.

In the main file, the bot processes received messages, as a result of which the bot provides up to 3 links to random tasks on the selected topic and difficulty level.
