# /data — Career Documents

Drop your personal career documents here before running `python ingest.py`.

## Supported formats
| Format | Notes |
|--------|-------|
| `.pdf` | CV, certificates, project write-ups |
| `.md`  | Free-form Markdown text |
| `.txt` | Plain text |

## Recommended documents

| File | What to put in it |
|------|-------------------|
| `cv.pdf` | Your full CV / résumé |
| `about_me.md` | 2–3 paragraphs: who you are, what drives you, what kind of work you're looking for |
| `skills.md` | Detailed breakdown of technical and soft skills, proficiency levels, tools |
| `projects.md` | One section per notable project: problem, your role, tech used, outcome |
| `qa.md` | Pre-written Q&A pairs for common interview questions (see example below) |
| `experience.md` | Timeline of positions, responsibilities, and achievements (if not in CV) |

## qa.md template

```markdown
## Why are you looking for a new role?
[Your honest, polished answer here]

## What are your salary expectations?
[Your answer, or a note that you prefer to discuss this personally]

## What does your ideal team look like?
[Your answer]

## Can you describe a challenge you overcame?
[STAR-format story]
```

## Tips for best retrieval quality
- Be specific — dates, company names, tech stack versions, metrics ("reduced load time by 40%")
- Avoid dense walls of text; use headings and bullet points
- Keep each document focused on one topic so chunks stay semantically tight
- After adding or changing any file, re-run `python ingest.py` to rebuild the vector store
