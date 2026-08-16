# Security policy

## Report privately

Do not open a public issue for an exposed credential, private path containing personal identity, unpublished project material, or third-party private data. Contact the repository owner through the private security-reporting channel available on GitHub.

## Public repository boundary

This repository must never contain:

- API keys, tokens, cookies, login state, or account identifiers;
- `.env` files other than redacted examples;
- private project scripts, company information, or unpublished client assets;
- personal contact information or biometric data;
- copied third-party courses or packages without redistribution permission.

The validator catches several common token formats, but automated scanning is not a substitute for review.
