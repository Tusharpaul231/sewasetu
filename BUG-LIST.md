# Bug list: Sewa Setu portal (original code as received)
  
 
## Home page `/`
 
| # | Bug | Status |
|---|---|---|
| 1 | The "closes in N hours" countdown used server time (UTC in the container), so it was off by 5.5 hours. | Open |
| 2 | The text says "above 60", but the rule is 60 or older. | Open |

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