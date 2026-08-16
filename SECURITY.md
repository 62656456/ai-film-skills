# Security policy

## Report privately

Do not open a public issue for an exposed credential, identity-bearing private path, unpublished project material, or third-party private data. Email [haldissita@gmail.com](mailto:haldissita@gmail.com) with the repository name, affected path, and the minimum reproduction details. Do not include a live secret when a redacted example is enough.

## Public repository boundary

This repository must never contain:

- API keys, tokens, cookies, login state, or account identifiers;
- `.env` files other than redacted examples;
- private project scripts, company information, or unpublished client assets;
- personal contact information or biometric data, except the maintainer's deliberately published contact address `haldissita@gmail.com`;
- copied third-party courses or packages without redistribution permission.

The validator catches several common token formats, but automated scanning is not a substitute for review. Installing a third-party Skill also grants an Agent access to its instructions and possibly its scripts; review the package and the host's permission prompts before enabling it.
