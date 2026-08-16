# Google Play App Content Checklist

| Console section | Prepared answer | Final owner action |
|---|---|---|
| Privacy Policy | Bilingual `/privacy` page implemented | Verify public URL and submit |
| Ads | No ads and no ads SDK | Confirm declaration |
| App access | No login required | Confirm and provide testing instructions |
| Target audience | Adult/general productivity audience; not designed for children | Select exact age groups |
| Content rating | Utility/productivity; no known restricted content | Complete official questionnaire truthfully |
| Data Safety | Draft in `GOOGLE_PLAY_DATA_SAFETY_DRAFT.md` | Re-audit built AAB and submit |
| Health apps | “My app doesn't provide any health features” | Required declaration even for non-health apps |
| News app | Not a news app | Confirm |
| Government app | Not a government app | Confirm if form appears |
| Financial features | No payments, wallet, trading, lending, or financial services | Confirm if form appears |
| Sensitive permissions | None planned; only normal `INTERNET` permission | Check merged manifest |
| Data deletion | No user account; local language preference removable via site data | Confirm current form requirements |
| Families / children | Not child-directed | Do not select child audience without full policy review |

Health declaration official reference: https://support.google.com/googleplay/android-developer/answer/14738291

No checkbox, policy acceptance, legal declaration, or final submission has been completed by Codex.
