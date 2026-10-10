# Bug list: Sewa Setu portal (original code as received)
  
 
## Home page `/`
 
| # | Bug | Status |
|---|---|---|
| 1 | The "closes in N hours" countdown used server time (UTC in the container), so it was off by 5.5 hours. | Fixed |
| 2 | The text says "above 60", but the rule is 60 or older. | Fixed |

## `/apply` (mobile and OTP request)
 
| # | Bug | Status |
|---|---|---|
| 3 | The security check is never validated, so a wrong answer (5+3 ≠ 11) or a blank still passes. | Open  |
| 4 | The mobile check is `len == 10 and isdigit()`. It accepts non-English digits and doesn't require an Indian mobile to start with 6–9, so `0000000000` passes. | Open |
| 5 | The mobile field has no numeric restriction in the browser (`type="text"`), so letters can be typed and are only rejected on submit. | Open |
| 6 | Every validation error is "Something went wrong. Please try again." | Open |
| 7 | OTP requests are unlimited per number, which allows SMS-bombing anyone. | Open |
| 8 | The OTP comes from `random.randint`, which is not cryptographically secure. | Open |
| 9 | The window-closed check uses server-local time, not IST. | Open |
 
## `/verify` (OTP entry)
 
| # | Bug | Status |
|---|---|---|
| 10 | OTP guesses are unlimited, so a 6-digit code can be brute-forced. | Open |
| 11 | The OTP field accepts any characters (no numeric input or pattern). | Open |
| 12 | There is no "resend OTP" option. After a wrong code the user has to start over. | Open |
| 13 | A used OTP is never invalidated and can be reused until it expires. | Open |
| 14 | "Invalid OTP." gives no guidance. | Open |

## `/form/1` (personal details)
 
| # | Bug | Status |
|---|---|---|
| 15 | Dates are parsed `MM/DD/YYYY` first, so 01/02/1955 is stored as 2 January. This gives a wrong DOB, a wrong age check and a wrong DOB-password. | Open |
| 16 | Common date formats (25-02-1955, 25.02.1955) are rejected. | Open |
| 17 | Validation runs only at final submit, and any error sends the user back to step 1 with "Something went wrong". | Open |
| 18 | Widowed applicants must give their husband's *current* employer. The husband fields show to everyone. | Open |
| 19 | The age error says "must be above 60", which is wrong and gives no date. | Open |
| 20 | The name is cut to 20 bytes. Indic letters are 3 bytes each, so names are cut mid-name or mid-character. | Open |
| 21 | The session lasts 5 minutes, so slow first-time users are logged out mid-form. | Open |
| 22 | Gender is optional and can be saved blank. | Open |
 
## `/form/2` and `/form/3` (address and bank)
 
| # | Bug | Status |
|---|---|---|
| 23 | There is no validation of the bank account or IFSC. Anything is accepted. | Open |
| 24 | Over-long village or block text crashes the DB insert with a 500. | Open |
| 25 | The block value isn't checked against the allowed list on the server. | Open |
 
## `/upload`
 
| # | Bug | Status |
|---|---|---|
| 26 | The page promises "JPG or PDF, 5 MB", but the code accepts only PDF under 100 KB. | Open |
| 27 | All upload failures show `ERR_VAL_47` with no explanation. | Open |
| 28 | The file type is judged by name only, and the client's filename is part of the saved path (path traversal). | Open |
 
## `/declaration` and submission
 
| # | Bug | Status |
|---|---|---|
| 29 | There is no review step, so mistakes can't be Open before submitting. This is why the help desk gets cancel requests. | Open |
| 30 | The acknowledgment PDF is built inside the submit request (including a 4,000-line decorative loop), holding a worker and a DB connection at peak. | Open |
| 31 | "One application per person" is a check-then-insert, so simultaneous submissions both pass. | Open |
| 32 | The SMS is sent inside the request with a 5-second timeout. | Open |
| 33 | `application_no` is a random 6-digit number with no unique constraint, so collisions are possible at scale. | Open |
| 34 | There is no way to edit or withdraw an application after submitting. | Open |
| 35 | The declaration checkbox is enforced only in the browser, not on the server. | Open |
| 36 | All timestamps use `datetime.now()`, which depends on the server's timezone. | Open |