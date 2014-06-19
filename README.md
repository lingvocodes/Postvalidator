Post-validator: program that unifies the appearance of the dictionary articles

This program receives and html-file with an article for the Active Dictionary of Russian Language and returns an html-file with highlighted mistakes of the article.

User has to run "main.py", type the name of the file (which is supposed to be in the folder "articles") and its encoding (if different from cp-1251). The resulting file is stored in "results" folder.

Other files are called from "main.py". They work with different parts of the dictionary entry:
- "collect_marks.py" collects dictionary marks from special files in "marks" folder;
- "preparator.py" is an html-cleaner; it deletes all unnecessary tags that MS Word leaves in html files;
- "intro.py" works with the intro zone;
- "synopsis.py" works with synopsis;
- "entries.py" works with lexeme blocks.

Code starter:
Mark Maltsev - 