# Printed guides (PDF) — the DZ Charlie house layout

Every guide's PDF follows the Spanish Civil War layout (build/make_pdf.py):
cover (photo + title block + "N SITES" stamp + sureness note) · contents · the story in brief
(+ accuracy rule with HIGH/MEDIUM/LOW legend) · one chapter per area or tour day (map/photo, caption,
italic lede, then numbered sites: name, sureness pill, kind · time, text, "What you can see", "Plan",
GPS, "Read more" links) · timeline · wider context · museums · People · Words to know · Credits.
A4, Georgia body, the guide's display font for headings, footer "Guide · DZ Charlie field guide · page".

Easy Company: `node extract.js` (app served on :8812) dumps each guide's content and day maps,
then `python3 make_pdf.py` writes the three PDFs. Keep each PDF under ~5 MB (maps as JPEG).
